import cv2
import time
import optparse
import math
import numpy as np

class Options:
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option("-s", "--use_screen", action = "store_true", dest = "use_screen", default = False, help = "run with a screens") 
        parser.add_option("-i", "--input_file", dest = "input_file", default = None, help = "use a local image file instead") 
        parser.add_option("-o", "--output_dir", dest = "output_dir", default = None, help = "directory to write images to") 
        parser.add_option("-d", "--debug", action = "store_true", dest = "debug", default = False, help = "show mask, all goals found") 
        parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose", default = False, help = "be verbose") 

        (options, args) = parser.parse_args()
        self.use_screen = options.use_screen
        self.input_file = options.input_file
        self.output_dir = options.output_dir
        self.debug = options.debug
        self.verbose = options.verbose
        print(options)

BOUNDING_TOLERANCE = 0
OUTPUT_SIZE = (640,360)

def main():
    options = Options()
    if options.input_file:
        cap = cv2.VideoCapture(options.input_file)
    else:
        cap = cv2.VideoCapture(0)
        time.sleep(2)


    cv2.namedWindow('bgr', cv2.WINDOW_NORMAL)
    cv2.namedWindow('grey', cv2.WINDOW_NORMAL)
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)

    while(True):
        ret, bgr = cap.read()
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        #mask = mask_image(hsv, screen.get_mask_values())
        cv2.multiply(grey, 1.5, grey)
        #grey = cv2.GaussianBlur(grey, (5,5), 0)

        ret, mask = cv2.threshold(grey,225,255,cv2.THRESH_BINARY_INV)
        ret, thresh = cv2.threshold(mask, 0, 255, 0)

        circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT,1,70, param1=50,param2=30,minRadius=60,maxRadius=90)

        #print(circles)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(bgr,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(bgr,(i[0],i[1]),2,(0,0,255),3)


        cv2.resize(bgr, OUTPUT_SIZE, bgr)
        cv2.resize(grey, OUTPUT_SIZE, grey)
        cv2.resize(mask, OUTPUT_SIZE, mask)
        cv2.imshow("bgr", bgr)
        cv2.imshow("grey", grey)
        cv2.imshow("mask", mask)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

