import time
import logging
import cv2
from djitellopy import Tello

def init_mission(tello):
    print("Configuring tello...")
    Tello.LOGGER.setLevel(logging.DEBUG)
    tello.enable_mission_pads()
    tello.set_mission_pad_detection_direction(2)
    tello.pad_id = tello.get_mission_pad_id()
    print("Running camera...") 
    tello.streamon()
    tello.frame_read = tello.get_frame_read()

def end_mission(tello):
    tello.disable_mission_pads()
    print("Mission ended.")
    print(f"Mission time: {tello.stop_time - tello.start_time}, Battery remaining: {str(tello.query_battery())}%")
    tello.land()
    tello.end()

def main(tello):

    # Take a picture!
    # rgb = cv2.cvtColor(tello.frame_read.frame, cv2.COLOR_BGR2RGB)
    # cv2.imwrite("picture20.png", rgb)

    while tello.pad_id != 1:
        if tello.pad_id == 4:
            tello.move_back(30)
            tello.move_right(90)
        if tello.pad_id == 2:
            tello.move_up(30)
            tello.rotate_clockwise(90)
        if tello.pad_id == 8:
            tello.move_down(30)
            tello.rotate_counterclockwise(90)
        if tello.pad_id == 5:
            end_mission()

try:
    tello = Tello()
    tello.start_time = time.time()

    tello.connect()
    init_mission(tello)

    print("Mission start!")
    print(f"Battery: {str(tello.query_battery())}%")
    print("--------------")

    print("Takeoff!")
    tello.takeoff()

except Exception as e:
    raise Exception(f"Tello: Fatal Error: {e}")

try:
    main(tello)
    tello.stop_time = time.time()
    end_mission(tello)

except Exception as e:
    end_mission(tello)
    raise Exception(f"Tello: Fatal Error: {e}")
