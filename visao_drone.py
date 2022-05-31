import numpy as np
import cv2

# ----------------------------------------------
# FUNCTIONS
# ----------------------------------------------


def nothing(x):
    pass


def draw_flow(img_draw, flow_draw, step=16):
    h, w = img_draw.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow_draw[y, x].T

    lines = np.vstack([x, y, x - fx, y - fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)

    img_bgr = cv2.cvtColor(img_draw, cv2.COLOR_GRAY2BGR)
    cv2.polylines(img_bgr, lines, 0, (0, 255, 0))

    for (x1, y1), (_x2, _y2) in lines:
        cv2.circle(img_bgr, (x1, y1), 1, (0, 255, 0), -1)

    return img_bgr


def draw_hsv(flow_hsv):
    h, w = flow_hsv.shape[:2]
    fx, fy = flow_hsv[:, :, 0], flow_hsv[:, :, 1]

    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx * fx + fy * fy)

    hsv_draw = np.zeros((h, w, 3), np.uint8)
    hsv_draw[..., 0] = ang * (180 / np.pi / 2)
    hsv_draw[..., 1] = 255
    hsv_draw[..., 2] = np.minimum(v * 4, 255)
    bgr_draw = cv2.cvtColor(hsv_draw, cv2.COLOR_HSV2BGR)

    return bgr_draw


# ----------------------------------------------
# 1st OBJECT MASK (TRACKBARS)
# ----------------------------------------------

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar('L - H', "Trackbars", 0, 179, nothing)
cv2.createTrackbar('L - S', "Trackbars", 0, 255, nothing)
cv2.createTrackbar('L - V', "Trackbars", 0, 255, nothing)
cv2.createTrackbar('U - H', "Trackbars", 179, 179, nothing)
cv2.createTrackbar('U - S', "Trackbars", 255, 255, nothing)
cv2.createTrackbar('U - V', "Trackbars", 255, 255, nothing)

while True:
    # read source image
    _, frame = cap.read()
    # convert sourece image to HSC color mode
    hsv_trackbars = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv_trackbars, lower, upper)
    # masking HSV value selected color becomes black
    result_trackbar = cv2.bitwise_and(frame, frame, mask=mask)

    # show image
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('result', result_trackbar)

    # wait for the user to press escape and break the while loop
    key = cv2.waitKey(5)

    if key == ord('\r'):
        break
    # elif key == ord('q'):
    #     print("you pressed q key!")
    # elif key == ord(' '):
    #     print("you pressed space!")

# destroys all window
cap.release()
cv2.destroyAllWindows()


# ----------------------------------------------
# 2nd OBJECT FLOW
# ----------------------------------------------

cap = cv2.VideoCapture(0)

suc, prev = cap.read()
prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

while True:

    suc, img = cap.read()

    original_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    result_bgr = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    prevgray = gray

    flow2 = cv2.flip(draw_flow(gray, flow),1)
    original_gray_flow = cv2.flip(draw_flow(original_gray, flow),1)
    img2 = cv2.flip(img,1)
    flow_HSV = cv2.flip(draw_hsv(flow),1)

    cv2.imshow('Flow Masked', flow2)
    cv2.imshow('Flow Image', original_gray_flow)
    cv2.imshow('RGB Image', img2)
    cv2.imshow('Flow HSV', flow_HSV)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
