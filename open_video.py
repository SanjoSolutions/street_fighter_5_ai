import cv2
import cv2 as cv
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('D:\\StreetFighterV 2021-06-12 23-59-30-239.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

print(str(cap.get(cv.CAP_PROP_FRAME_WIDTH)) + 'x' + str(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  frame = cv.resize(frame, (320, 180))
  print(str(cap.get(cv.CAP_PROP_POS_MSEC)))
  print('fps:', str(cap.get(cv.CAP_PROP_FPS)))
  if ret == True:

    # Display the resulting frame
    cv2.imshow('Frame',frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()