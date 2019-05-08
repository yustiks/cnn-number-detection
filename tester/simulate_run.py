import os
import cv2
import shutil
import numpy as np
from tqdm import tqdm
from isolator.isolator import Isolator


def classify_for_signal(image):
    isolator = Isolator()
    contours = isolator.get_contours(image)

    contour_images = []

    for contour_arr in contours:
        contour = contour_arr[0]
        contour_image = contour_arr[1]

        draw_image = np.copy(contour_image)
        if contour is not None:
            cv2.drawContours(draw_image, contour, -1, (255, 153, 255), 1)

        contour_images.append(draw_image)

    return contour_images


frames = []

currentWorkingDir = os.getcwd()
listdir = os.listdir(currentWorkingDir + "/continous")
listdir = [f for f in listdir]
listdir.sort()
for f in listdir:
    fileString = currentWorkingDir + "/continous/{:s}".format(f)
    try:
        frame = cv2.imread(fileString)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except:
        continue
    frames.append(frame)

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

erun_path = os.path.join(currentWorkingDir, 'continous/erun')
if os.path.exists(erun_path):
    shutil.rmtree(erun_path, ignore_errors=True)
os.makedirs(currentWorkingDir + "/continous/erun/original")
os.makedirs(currentWorkingDir + "/continous/erun/contours")

for i, frame in enumerate(tqdm(frames)):
    result = classify_for_signal(frame)
    frameString = "/pic_{:08d}.jpg".format(i)
    cv2.imwrite((currentWorkingDir + "/continous/erun/original" + frameString), frame)
    for index, image in enumerate(result):
        frameString = "/pic_{}_{:08d}.jpg".format(index, i)
        cv2.imwrite((currentWorkingDir + "/continous/erun/contours" + frameString), image)