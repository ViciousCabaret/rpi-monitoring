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

logging.basicConfig(
    filename=os.path.join('log', 'capture_motion.log'),
    encoding='utf-8',
    level=logging.DEBUG,
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

while True:
    cur = picam2.capture_buffer("lores")
    cur = cur[:w * h].reshape(h, w)
    if prev is not None:
        # Measure pixels differences between current and
        # previous frame
        mse = np.square(np.subtract(cur, prev)).mean()
        if mse > 7:
            if not encoding:
                filename = str(datetime.now()) + '.h264'
                encoder.output = FileOutput(filename)
                picam2.start_encoder(encoder)
                encoding = True
                print("New Motion", mse)
                logging.info("New Motion" + mse)
                monitoring_recording = MonitoringRecording(filename)
                monitoring_recording.save()
            ltime = time.time()
        else:
            if encoding and time.time() - ltime > 5.0:
                picam2.stop_encoder()
                encoding = False
    prev = cur
