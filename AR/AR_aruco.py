import numpy as np
import cv2
import cv2.aruco as aruco

# ------------------ ARUCO TRACKER ---------------------------


def ar_aruco_detect(frame, flag):
    # operations on the frame
    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX

    if len(ids) == 0:
        return frame, flag
    elif np.any(ids == 6):
        aruco.drawDetectedMarkers(frame, corners)
        new_flag = True
        cv2.putText(frame, "AR ON", (corners[0,0,0,0], corners[0,0,0,1]), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        return frame, new_flag
    elif np.any(ids != 6):
        new_flag = False
        return frame, new_flag

