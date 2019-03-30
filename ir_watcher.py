from configparser import ConfigParser
import os
import datetime
import tensorflow as tf
import RPi.GPIO as IO
from events.watcher import Watcher
from camera.camera import Camera
from object_detector.ObjectDetector import ObjectDetector
from mail.mailer import Mailer

CONFIG = ConfigParser()
CONFIG.read('config/config.ini')

GRAPH = tf.get_default_graph()

IR_PIN_NO = int(CONFIG['RASPBERRY_PI']['IR_PIN_NO'])
CAMERA_INDEX = int(CONFIG['CAMERA']['CAMERA_INDEX'])

CAMERA_CAPTURES_BASE_PATH = CONFIG['LOCATION']['CAMERA_CAPTURES_BASE_PATH']
DETECTION_OUTPUT_BASE_PATH = CONFIG['LOCATION']['DETECTION_OUTPUT_BASE_PATH']

MODEL_NAME = CONFIG['OBJECT_DETECTION']['MODEL_NAME']
MODEL_PATH = CONFIG['OBJECT_DETECTION']['MODEL_PATH']

SMTP_SERVER = CONFIG['MAIL']['SMTP_SERVER']
SMTP_PORT = int(CONFIG['MAIL']['SMTP_PORT'])
USERNAME = CONFIG['MAIL']['USERNAME']
PASSWORD = CONFIG['MAIL']['PASSWORD']
SENDER_NAME = CONFIG['MAIL']['SENDER_NAME']
SENDER_EMAIL = CONFIG['MAIL']['SENDER_EMAIL']
TO_EMAILS = CONFIG['MAIL']['TO_EMAILS'].split(',')
CC_EMAILS = CONFIG['MAIL']['CC_EMAILS'].split(',')
BCC_EMAILS = CONFIG['MAIL']['BCC_EMAILS'].split(',')
SUBJECT = CONFIG['MAIL']['SUBJECT']
BODY_TEMPLATE = CONFIG['MAIL']['BODY_TEMPLATE']

if not os.path.exists(CAMERA_CAPTURES_BASE_PATH):
    os.makedirs(CAMERA_CAPTURES_BASE_PATH)

if not os.path.exists(DETECTION_OUTPUT_BASE_PATH):
    os.makedirs(DETECTION_OUTPUT_BASE_PATH)

EXECUTION_PATH = os.getcwd()
print('Running application at ', EXECUTION_PATH)

print('Initializing Camera...')
CAMERA = Camera(camera_index=CAMERA_INDEX)
print('Camera initialized')

print('Loading object detection model...')
# Download this model from https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5
OBJECT_DETECTOR = ObjectDetector(model_name=MODEL_NAME, model_path=MODEL_PATH)
print('Model loaded')

print('Initializing Mailer...')
MAILER = Mailer(smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT)
MAILER.authenticate(username=USERNAME, password=PASSWORD)
print('Mailer initialized...')

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(IR_PIN_NO, IO.IN)


def on_ir_state_changed(previous_state, current_state):
    if previous_state == 1 and current_state == 0:
        current_timestamp = '{0:%Y_%m_%d_%H_%M_%S}'.format(
            datetime.datetime.now())
        picture_file_name = 'capture_' + current_timestamp + '.jpg'
        camera_capture_file_path = os.path.join(
            CAMERA_CAPTURES_BASE_PATH, picture_file_name)
        status = CAMERA.capture(camera_capture_file_path)

        if status:
            print('Captured image stored at "{}"'.format(
                camera_capture_file_path))
            with GRAPH.as_default():
                detection_output_file_path = os.path.join(
                    DETECTION_OUTPUT_BASE_PATH, picture_file_name)
                detections, _ = OBJECT_DETECTOR.detect(
                    input_image_path=camera_capture_file_path,
                    output_image_path=detection_output_file_path,
                    extract_detected_objects=True,
                    display_percentage_probability=True,
                    display_object_name=True
                )
            print('Detection output stored at "{}"'.format(
                detection_output_file_path))

            interesting_objects = list(
                filter(lambda x: x['name'] == 'person', detections))
            interesting_objects_count = len(interesting_objects)

            if interesting_objects_count > 0:
                MAILER.send_mail(
                    subject=SUBJECT,
                    sender={
                        'name': SENDER_NAME,
                        'email': SENDER_EMAIL
                    },
                    recipients={
                        'To': TO_EMAILS,
                        'Cc': CC_EMAILS,
                        'Bcc': BCC_EMAILS
                    },
                    body=BODY_TEMPLATE,
                    attachments=[
                        {
                            'name': picture_file_name,
                            'path': camera_capture_file_path
                        }
                    ],
                    inline_images=[
                        {
                            'name': picture_file_name,
                            'path': camera_capture_file_path,
                            'cid': picture_file_name
                        }
                    ]
                )


def get_ir_state(_ir_pin_no):
    return IO.input(_ir_pin_no)


IR_WATCHER = Watcher(
    state_func=get_ir_state,
    change_handlers=[on_ir_state_changed],
    initial_state=get_ir_state(IR_PIN_NO),
    state_check_interval=0.1,
    _ir_pin_no=IR_PIN_NO
)

IR_WATCHER.start_watching()
