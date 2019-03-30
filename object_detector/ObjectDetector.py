from imageai.Detection import ObjectDetection
import cv2
from object_detector.DetectorAPI import DetectorAPI


class ObjectDetector:

    model_class_labels = ["person", "bicycle", "car", "motorcycle", "airplane",
                          "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
                          "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
                          "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                          "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
                          "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
                          "broccoli", "carrot", "hot dog", "pizza", "donot", "cake", "chair", "couch", "potted plant", "bed",
                          "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
                          "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair dryer",
                          "toothbrush"]

    def __init__(self, model_name, model_path):
        self.model_path = model_path
        self.model_name = model_name
        if model_name == 'other':
            self.object_detector = DetectorAPI(path_to_ckpt=model_path)
        else:
            self.object_detector = ObjectDetection()
            if model_name == 'yolov3':
                self.object_detector.setModelTypeAsYOLOv3()
            elif model_name == 'tinyyolov3':
                self.object_detector.setModelTypeAsTinyYOLOv3()
            elif model_name == 'retinanet':
                self.object_detector.setModelTypeAsRetinaNet()
            self.object_detector.setModelPath(model_path)
            self.object_detector.loadModel()

    def detect(self, input_image_path, output_image_path, extract_detected_objects=True, display_percentage_probability=False, display_object_name=False, threshold=0.7):

        if self.model_name == 'other':
            detected_objects_location = []
            img = cv2.imread(input_image_path)
            boxes, scores, classes, _ = self.object_detector.process_frame(
                img)
            detections = []
            for i in range(len(boxes)):
                if scores[i] > threshold:
                    detections.append({
                        'name': self.model_class_labels[classes[i] - 1]
                    })
                    box = boxes[i]
                    cv2.rectangle(img, (box[1], box[0]),
                                  (box[3], box[2]), (255, 0, 0), 2)
            cv2.imwrite(output_image_path, img)
        else:
            detections, detected_objects_location = self.object_detector.detectObjectsFromImage(
                input_image=input_image_path,
                output_image_path=output_image_path,
                extract_detected_objects=extract_detected_objects,
                display_percentage_probability=display_percentage_probability,
                display_object_name=display_object_name
            )
        return detections, detected_objects_location
