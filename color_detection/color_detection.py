# File for Color Detection
# does it detect the color good?
import numpy as np
import cv2

#capture = cv2.VideoCapture(0)
capture = cv2.VideoCapture('vid.mp4')
c = 80
flag = False

while True:
    ret, frame = capture.read()
    width = int(capture.get(3))
    height = int(capture.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([c, 50, 50])  # 80 50 50                 #Trying to get the right color (in this case blue)
    upper_bound = np.array([c + 40, 255, 255])  # 80+40 255 255


    mask = cv2.inRange(hsv, lower_bound, upper_bound)           #mask between lower and upper bound
    result = cv2.bitwise_and(frame, frame, mask=mask)

    points = cv2.findNonZero(mask)
    resImage = [640, 480]           #not needed
    resScreen = [1920, 1080]
    try:
        avg = np.mean(points, axis=0)   #for example when there are no points, the "points" array is None. When its none np.mean does't work
    except:
        cv2.imshow("videonormal", frame)
        cv2.imshow("videohsv", hsv)
        cv2.imshow("mask", mask)
        cv2.imshow("result", result)
        continue

    #pointInScreen = ((resScreen[0] / resImage[0]) * avg[0][0], (resScreen[1] / resImage[1]) * avg[0][1]) #not needed right now
    #res = cv2.circle(res, (int(pointInScreen[0]),int(pointInScreen[1])), 10, (0, 0, 255), -1)

    result = cv2.circle(result, (int(avg[0][0]), int(avg[0][1])), 10, (0, 0, 255), -1)
    print('x=' + str(avg[0][0]) + ' y=' + str(avg[0][1]))

    cv2.imshow("videonormal", frame)
    cv2.imshow("videohsv", hsv)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    if flag:
        '''
        f = open("demofile2.txt", "w")
        f.write("")
        f.close()
        f = open("demofile2.txt", "a")
        for i in range(0, height):
            for j in range(0, width):
                f.write(str(result[i][j]) + ' ')
            f.write("\n")
        f.close()
        print("geschreiben!")
        flag=False
    '''
    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(1) == ord('p'):
        c = c + 1
        print(c)
    if cv2.waitKey(1) == ord('t'):
        flag = True



capture.release()
cv2.destroyAllWindows()
