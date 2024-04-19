import os
import time
import numpy as np
import logging

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from libcamera import controls
from datetime import datetime

from monitoring_recording import MonitoringRecording
BASE_DIR = os.path.dirname(__file__)

logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'log', 'capture_motion.log'),
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

lsize = (320, 240)
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                 lores={"size": lsize, "format": "YUV420"})
picam2.configure(video_config)
encoder = H264Encoder(1000000)
picam2.start()

w, h = lsize
prev = None
encoding = False
ltime = 0
filename = None
start_time = None

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and
        # previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not encoding:
                datetime_now = str(datetime.now())
                filename = '{}.h264'.format(datetime_now)
                encoder.output = FileOutput(os.path.join(BASE_DIR, 'monitoring_recording_files', filename))
                picam2.start_encoder(encoder)
                encoding = True
                print("New Motion", str(mse))
                logging.info("New Motion" + str(mse))
                start_time = time.time()
            ltime = time.time()
        else:
            if (encoding and time.time() - ltime > 5.0) or (start_time is not None and encoding and time.time() - start_time > 30):
                picam2.stop_encoder()
                logging.info("Recording stopped, file saved")

                monitoring_recording = MonitoringRecording(filename)
                monitoring_recording.save()

                encoding = False
                start_time = None
        if encoding:
             logging.info("motion: " + str(mse))
    prev = cur
