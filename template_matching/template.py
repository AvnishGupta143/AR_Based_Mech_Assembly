import cv2
from template_matching.aruco_tracker import extract_ROI


def match_template(frame, id, threshold):
    frame_wrapped = extract_ROI(frame)
    if frame_wrapped is None:
        return "NOT ALIGNED", 0.0

    img_gray = cv2.cvtColor(frame_wrapped, cv2.COLOR_BGR2GRAY)

    '''
    if id == 4:
         cv2.imwrite('4.jpg', frame_wrapped)
    if id == 5:
         cv2.imwrite('5.jpg', frame_wrapped)
    if id == 6:
         cv2.imwrite('6.jpg', frame_wrapped)
    '''

    # cv2.imshow("l", img_gray)
    # cv2.waitKey(10)

    # Loading the Template
    template_name = str(id) + '.jpg'
    template = cv2.imread(template_name,0)

    w, h = template.shape[::-1]

    # Template Matching
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    if res >= threshold:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame_wrapped, top_left, bottom_right, (255,0,255), 5)
        return "OK", res
    else:
        return "NOT DETECTED", res

# video = cv2.VideoCapture(2)

# while True:
#     try:
#         g, frame = video.read()
#         a, res = match_template(frame, 1)
#         print(a, res)
#     except KeyboardInterrupt:
#         break
