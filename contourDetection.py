from tkinter import Frame
import cv2
from matplotlib.pyplot import contour
import numpy as np

cap = cv2.VideoCapture(0)
panjang = 640
lebar = 480
cap.set(3, panjang)
cap.set(4, lebar)


def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 150, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 255, 255, empty)
cv2.createTrackbar("Area", "Parameters",5000,30000,empty)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img, imgContours):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    kotak = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        # areaMin = 14
        if area > areaMin:  
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            #print(len(approx))
            # x,y,w,h = benur
            # benur = cv2.boundingRect(approx)
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),1)
            #cv2.putText(imgContour,"Points : "+ str(len(approx)), (x + w + 20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
            #cv2.putText(imgContour,"Area : "+ str(int(area)), (x + w + 20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
            
            kotak.append([x,y,w,h])

    print(len(kotak))
    cv2.putText(imgContour, "Jumlah = "+ str(len(kotak)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# def getContours(img):
#     contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         print(area)
#         if area>500:
#             cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
#             peri = cv2.arcLength(cnt,True)
#             #print(peri)
#             approx = cv2.approxPolyDP(cnt,0.02*peri,True)
#             print(len(approx))
#             objCor = len(approx)
#             x, y, w, h = cv2.boundingRect(approx)

#             if objCor ==3: objectType ="Tri"
#             elif objCor == 4:
#                 aspRatio = w/float(h)
#                 if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
#                 else:objectType="Rectangle"
#             elif objCor>4: objectType= "Circles"
#             else:objectType="None"



#             cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
#             cv2.putText(imgContour,objectType,
#                         (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
#                         (0,0,0),2)



while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img,(7,7),1) #deteksi tepi
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
   
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # threshold1 = 78
    # threshold2 = 134
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters") 
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2) #deteksi tepi
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)

    imgStack = stackImages(0.8,([img,imgGray,imgCanny],[imgDil,imgContour,imgContour]))
    # resize = cv2.resize(Frame=, fx=scaling,fy=scaling,)

# path = 'Resources/shapes.png'
# img = cv2.imread(path)
# imgContour = img.copy()

# imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
# imgCanny = cv2.Canny(imgBlur,50,50)
# getContours(imgCanny)

# imgBlank = np.zeros_like(img)
# imgStack = stackImages(0.8,([img,imgGray,imgBlur],
#                             [imgCanny,imgContour,imgBlank]))

    cv2.imshow("Stack", imgStack)

    if cv2.waitKey(5) & 0xFF == 27:
      break