import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    lsize = (320, 240)
    w, h = lsize

    vidcap = cv2.VideoCapture(os.path.join(BASE_DIR, 'debug', 'testing_video.h264'))
    # success, cur = vidcap.read()
    count = 0
    prev = None
    success = True
    mses = []
    mseCounter = 0
    while success:
        # frame_path = os.path.join(BASE_DIR, 'debug', "frame{}.jpg".format(count))
        # cv2.imwrite(frame_path, image)     # save frame as JPEG file
        success, cur = vidcap.read()
        if prev is not None and success:
            # cur = cur[:w * h].reshape(h, w)
            mse = np.square(np.subtract(cur, prev)).mean()
            mses.append(mse)
            # print(mse)
            if mse > 4:
                print(count)
                print(mse)
                mseCounter += 1
            # success, cur = vidcap.read()
            # print('Read a new frame: ', success)
            count += 1
        prev = cur

print(max(mses))
print(len(mses))
print(mseCounter)
