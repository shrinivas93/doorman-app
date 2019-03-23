import RPi.GPIO as IO
from events.watcher import Watcher
from configparser import ConfigParser

config = ConfigParser()
config.read('./config/config.ini')

IR_PIN_NO = config['IR_PIN_NO']

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(IR_PIN_NO, IO.IN)


def on_ir_state_changed(previous_state, current_state):
    if previous_state == 1 and current_state == 0:
        print('Handler 1 : {} to {}'.format(previous_state, current_state))


def get_ir_state(_ir_pin_no):
    return IO.input(_ir_pin_no)


ir_watcher = Watcher(state_func=get_ir_state, change_handlers=[
    on_ir_state_changed], initial_state=get_ir_state(IR_PIN_NO), state_check_interval=0.1, _ir_pin_no=IR_PIN_NO)

ir_watcher.start_watching()
