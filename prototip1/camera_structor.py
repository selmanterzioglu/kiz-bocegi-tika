from structure_camera import Camera_Object, CAMERA_FLAGS
#import threading
from enum import Enum
from time import sleep
import logging

# EXTERNAL LIBRARIES
import cv2
import numpy as np
# from ordered_enum import OrderedEnum

# CUSTOM LIBRARIES
import neoapi_libs
from stdo import stdo
# from structure_data import structure_buffer
from structure_threading import Thread_Object
from structure_data import Structure_Buffer
from tools import time_log, time_list, TIME_FLAGS

class Camera_Structor (Camera_Object):

    def save_Video_From_Buffer_Thread(self, trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001):
        if self.get_Is_Object_Initialized():
            self.__thread_Dict["save_Video_Start_Thread"] = Thread_Object(
                name="Camera_Object.save_Video_Start_Thread",
                delay=0.0001,
                logger_level=self.logger.getEffectiveLevel(),
                set_Deamon=True,
                run_number=1,
                quit_trigger=trigger_quit
            )
            self.__thread_Dict["save_Video_Start_Thread"].init(
                params=[
                    trigger_pause,
                    trigger_quit,
                    number_of_snapshot,
                    delay
                ],
                task=self.stream_Start
            )
            self.__thread_Dict["save_Video_Start_Thread"].start()

            return self.__thread_Dict["save_Video_Start_Thread"]
        else:
            return None


