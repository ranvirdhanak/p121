import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Flipping the background
bg = np.flip(bg, axis=1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #Flipping the image for consistency
    img = np.flip(img, axis=1)

    #Converting the color from BGR to HSV
    frame = cv2.resize(frame,(640,480),cv2.COLOR_BGR2HSV)
    image = cv2.resize(image,(640,480))
    #Generating mask to detect red colour
    #These values can also be changed as per the color
    u_black = np.array([104,153,70])
    l_black = np.array([30,30,0])
    mask_1 = cv2.inRange(frame, u_black, l_black)

    u_black = np.array([170, 120, 70])
    l_black = np.array([180, 255, 255])
    mask_2 = cv2.inRange(frame, u_black, l_black)

    mask = mask

    #Open and expand the image where there is mask 1 (color)
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #Selecting only the part that does not have mask one and saving in mask 2
    mask = cv2.bitwise_not(mask)
    
    mask = cv2.inRange(frame,l_black,u_black)
    res = cv2.bitwise_and(frame,frame,mask = mask)

    f = frame - res
    f = np.where(f == 0,image,f)

    final_output = cv2.addWeighted(1,res,1,0)
    output_file.write(final_output)
    #Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)


cap.release()
output_file.release()
cv2.destroyAllWindows()