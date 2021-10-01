from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

class MeasuringObject():
    def __init__(self, image):
        self.pixelsPermm = 0.035
        self.img = image
        self.process_image(self.img)
    
    def midpoint(self, ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    
    def process_image(self, img):
        self.image = cv2.imread(img)
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
        edged = cv2.Canny(gray, 100, 200)
        #cv2.imshow("1-canny", edged)
        edged = cv2.dilate(edged, None, iterations=1)
        #cv2.imshow("2-dilate", edged)
        edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
        self.cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(self.cnts)
        
        # sort the contours from left-to-right
        (self.cnts, _) = contours.sort_contours(self.cnts)
        
        self.contours()
    
    def contours(self):
    
        for c in self.cnts:

# =============================================================================
#             if cv2.contourArea(c) < 100:
#                 continue
# =============================================================================

            orig = self.image.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = self.midpoint(tl, tr)
            (blbrX, blbrY) = self.midpoint(bl, br)
            
            (tlblX, tlblY) = self.midpoint(tl, bl)
            (trbrX, trbrY) = self.midpoint(tr, br)
                
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)        
            
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
    		(255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
    		(255, 0, 255), 2)
            
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            
            dimA = dA / self.pixelsPermm
            dimB = dB / self.pixelsPermm
            
            cv2.putText(orig, "{:.1f}in".format(dimA),
    		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
    		0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}in".format(dimB),
    		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
    		0.65, (255, 255, 255), 2)
            
            cv2.imshow("Image", orig)
            cv2.waitKey(0)
            
MeasuringObject('Z:/NATASHA/Camera/1.jpg')