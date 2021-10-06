import numpy as np
import imutils
import cv2

class MeasuringObject():
    
    debug = False
    
    def __init__(self):
        self.pixelsPermm = 0.035
    
    def process_image(self, img):
# =============================================================================
#         x=0 
#         y=500
#         h=250
#         w=1200
# =============================================================================
# =============================================================================
#         try:
#             img = cv2.imread(img)
#             #img = img[y: y+h, x: x+w]
#         except:
#             print("mue")
#             pass
# =============================================================================
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            edged = cv2.Canny(gray, 120, 200)
            edged = cv2.dilate(edged, None, iterations=1)
            self.edged = cv2.erode(edged, None, iterations=1)
            
            cnts = cv2.findContours(self.edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=False)[:5]
            
            if self.debug:
                cv2.imshow("Image",edged)
                if cv2.waitKey(0) & 0xFF == ord('q'): 
                    cv2.destroyAllWindows()
                        
        except:
            print("err-2")
        
        self.contours(cnts)
    
    def contours(self, cnts):
        
        cc = [[],[]]
        try:    
            cc[0] = cnts[2]
            cc[1] = cnts[1]
        except:
            pass
        
        a = np.empty(len(cc[0]))
        b = np.empty(len(cc[0]))
        
        for i in range(len(cc[0])):
            a[i] = cc[0][i][0][1]
            b[i] = cc[1][i][0][1]
        m = a - b
        left = m[0]*self.pixelsPermm*-1
        right = m[-1]*self.pixelsPermm*-1
        if left < 0:
            left *=-1
        if right < 0:
            right *=-1
        
        print("L-> " + str(left))
        print("R-> " + str(right))
        
        center = m[int(len(m)/2)]*self.pixelsPermm
        
        return center
