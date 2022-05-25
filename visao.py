import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# params for ShiTomasi corner detection
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Parameters for lucas kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

object_frame_counter = 0

while True:
    ret, old_frame = cap.read()

    hsv = cv2.cvtColor(old_frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 133, 111])
    upper = np.array([13, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(old_frame, old_frame, mask=mask)

    ret, result_binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    M = cv2.moments(result_binary)

    # Problems:
    # 1- a imagem inicialmente (antes de sequer haver objecto) nao existe (preto)
    # 2- quando se perdem todas as features, o programa morre - ressuscitar features
    # 3- temporizador para ir apagando traços muito antigos

    if M["m00"] != 0:  # if an object is detected
        object_frame_counter = object_frame_counter + 1

        if object_frame_counter == 1:
            # Take first frame and find corners in it
            result_bgr = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
            old_gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

            # Create a mask image for drawing purposes
            mask_optical_flow = np.zeros_like(old_frame)
        break
    else:
        cv2.imshow("old_frame", old_frame)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 133, 111])
    upper = np.array([13, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    ret, result_binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    result_bgr = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    frame_gray = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)

    M = cv2.moments(result_binary)

    if M["m00"] != 0:  # if an object is detected
        object_frame_counter = object_frame_counter + 1
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.circle(result, (cX, cY), 5, (255, 0, 0), -1)

        if object_frame_counter == 1:
            # Take first frame and find corners in it
            p0 = cv2.goodFeaturesToTrack(frame_gray, mask=None, **feature_params)

            # Create a mask image for drawing purposes
            mask_optical_flow = np.zeros_like(frame_gray)

        if object_frame_counter > 1:

            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

            # Select good points
            good_new = p1[st == 1]
            good_old = p0[st == 1]

            # draw the tracks
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask_optical_flow = cv2.line(mask_optical_flow, (a, b), (c, d), color[i].tolist(), 2)
                result = cv2.circle(result, (a, b), 5, color[i].tolist(), -1)

            img_optical_flow = cv2.add(result, mask_optical_flow)

            cv2.imshow("img_optical_flow", img_optical_flow)

            # Now update the previous points
            p0 = good_new.reshape(-1, 1, 2)
    else:
        object_frame_counter = 0

    # cv2.imshow("result", result)

    if cv2.waitKey(33) == ord('q'):
        break

    # Now update the previous frame
    old_gray = frame_gray.copy()

cap.release()
cv2.destroyAllWindows()