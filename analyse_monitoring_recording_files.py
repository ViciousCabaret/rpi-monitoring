from monitoring_recording import MonitoringRecording
from error import MonitoringRecordNotInitialized, FileDoesNotExistsException

import os
import logging

import cv2
import numpy as np
import tensorflow as tf


MODEL_PATH = 'model.tflite'
BASE_DIR = os.path.dirname(__file__)
FRAMES_WITH_HUMAN_DETECTED_POSITIVE = 5

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_height = input_details[0]['shape'][1]
input_width = input_details[0]['shape'][2]

logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'log', 'analyse_monitoring_recording.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)

if __name__ == '__main__':
    logging.info("Command analyse_monitoring_recording_files.py started")
    logging.info("Retrieving sent monitoring recordings from database")

    monitoring_recordings = MonitoringRecording.get_ready_to_analysis()
    logging.info("Found " + str(len(monitoring_recordings)) + " monitoring recordings to analyse")

    for monitoring_recording in monitoring_recordings:
        print("Analysing monitoring recording: {}".format(monitoring_recording.name))
        analysis_status = False
        logging.info("Analysing monitoring recording {}".format(monitoring_recording.name))
        human_detected_frames_count = 0

        try:
            filepath = os.path.join(BASE_DIR, 'monitoring_recording_files', monitoring_recording.name)
            if os.path.exists(filepath) is not True:
                raise FileDoesNotExistsException()

            cap = cv2.VideoCapture(filepath)
            frame_rate = 5
            frame_count = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_rate == 0:
                    input_frame = cv2.resize(frame, (input_width, input_height))
                    input_data = np.expand_dims(input_frame, axis=0)
                    input_data = np.uint8(input_data)

                    interpreter.set_tensor(input_details[0]['index'], input_data)
                    interpreter.invoke()

                    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
                    classes = interpreter.get_tensor(output_details[1]['index'])[0]
                    scores = interpreter.get_tensor(output_details[2]['index'])[0]

                    for i in range(len(scores)):
                        if scores[i] > 0.7:
                            class_id = int(classes[i])
                            print(class_id)
                            if class_id == 0:
                                human_detected_frames_count += 1
                                if human_detected_frames_count == FRAMES_WITH_HUMAN_DETECTED_POSITIVE:
                                    analysis_status = True
                if analysis_status is True:
                    break

            if analysis_status is True:
                monitoring_recording.mark_as_analyzed_positive()
                break
            else:
                monitoring_recording.mark_as_analyzed_negative()

        except MonitoringRecordNotInitialized as e:
            logging.error(e)
        except FileDoesNotExistsException as e:
            logging.error(e)