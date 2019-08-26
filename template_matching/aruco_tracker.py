import numpy as np
import cv2
import cv2.aruco as aruco
import glob

###------------------ ARUCO TRACKER ---------------------------
def extract_ROI(frame):
    # operations on the frame
    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    # font for displaying text (below)
    # font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    frame_wrapped = None
    if np.all(ids != None):
        # print(corners[0][0][0])
        list = []

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)
        if(ids.size == 4):
            for i in range(0, ids.size):
                list.append([ids[i][0],corners[i][0][0]])
            list = sorted(list, key=lambda i:i[0])
            # print(list)
            pts1 = np.float32([list[0][1],list[1][1],list[2][1],list[3][1]])
            pts2 = np.float32([[0,0],[320,0],[0,240],[320,240]])
            M = cv2.getPerspectiveTransform(pts1,pts2)

            frame_wrapped = cv2.warpPerspective(frame,M,(320,240))
            return frame_wrapped
    else:
        pass
    return frame_wrapped


        # code to show 'No Ids' when no markers are found
        # frame_wrapped = np.uint8(np.zeros(frame.shape))
        # cv2.putText(frame_wrapped, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

    # display the resulting frame
    # cv2.imshow('frame',frame_wrapped)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()

