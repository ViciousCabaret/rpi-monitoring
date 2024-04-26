#!/usr/bin/python3
from time import sleep
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720),
                                                         "format": "YUV420"}))
picam2.start_recording(H264Encoder(), output=FfmpegOutput("-f mpegts udp://192.168.1.9:9000"))
# FfmpegOutput("-f mpegts udp://<ip-addr>:<port>")
count = 0
while True:
    print(f'hello [{count}]')
    count += 1
    sleep(2)