import cv2
import time
import optparse
import math
import numpy as np
import re
import glob

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

def clamp(x, lower, upper):
    return min(max(x,lower),upper)

BOUNDING_TOLERANCE = 100
OUTPUT_SIZE = (720,480)

def main():
    options = Options()
    filetype = re.search('\.(.*)', options.input_file)
    if filetype:
       filetype = filetype.group(0) 

    if not options.input_file:
        cap = cv2.VideoCapture(0)
        time.sleep(2) # let the camera "warm up"
    elif filetype in [".mp4", ".jpg", ".jpeg", ".png"]:
        cap = cv2.VideoCapture(options.input_file)
    else:
        print("file must have suffix .mp4 .jpg .jpeg or .png")
        quit()

    cv2.namedWindow('bgr', cv2.WINDOW_NORMAL)
    cv2.namedWindow('grey', cv2.WINDOW_NORMAL)
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)

    ret, original = cap.read()

    while(True):
        if filetype in [".mp4"]:
            ret, original = cap.read()
        bgr = original.copy()
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        #mask = mask_image(hsv, screen.get_mask_values())
        cv2.multiply(grey, 2, grey)
        #grey = cv2.GaussianBlur(grey, (5,5), 0)

        ret, mask = cv2.threshold(grey,225,255,cv2.THRESH_BINARY_INV)
        ret, thresh = cv2.threshold(mask, 0, 255, 0)
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        id = 0
        for contour in contours:
            # chuck out contours which are too small or too big
            area = cv2.contourArea(contour)
            if area < 10000 or area > 500000:
                continue

            # calculate corners of a bounding box around the dice
            tl = (clamp(contour[:,0,0].min() - BOUNDING_TOLERANCE, 0, bgr.shape[1]), clamp(contour[:,0,1].min() - BOUNDING_TOLERANCE, 0, bgr.shape[0]))
            br = (clamp(contour[:,0,0].max() + BOUNDING_TOLERANCE, 0, bgr.shape[1]), clamp(contour[:,0,1].max() + BOUNDING_TOLERANCE, 0, bgr.shape[0]))

            # chuck out contours whose bounding box aspect ratio is not
            # very square
            aspect_ratio = (br[0] - tl[0])/(br[1] - tl[1])
            if aspect_ratio > 1.5 or aspect_ratio < 0.5:
                continue
            id = id + 1

            #center = (math.floor((tl[0] + br[0])/2), math.floor((tl[1] + br[1])/2))
            #color = tuple(bgr[center[1],center[0]]*1.0)

            # make a copy of the bgr image then crop it to the bounding box
            clone = bgr.copy()
            clone = clone[tl[1]:br[1], tl[0]:br[0]]
            if options.output_dir:
                name = "{}/{}-{}.jpg".format(options.output_dir, options.input_file.split("/")[-1].split(".")[0], str(id))
                cv2.imwrite(name, clone)
            else:
                cv2.imshow(str(id), clone)

            # using a smaller bounding box find the average color
            # could use this to differentiate between multiple dice
            tight_tl = (int(clone.shape[0]*0.4), int(clone.shape[1]*0.4))
            tight_br = (int(clone.shape[0]*0.6), int(clone.shape[1]*0.6))
            tight = clone[tight_tl[1]:tight_br[1], tight_tl[0]:tight_br[0]]
            color = (tight[0,0,0].max() * 1.0, tight[0,0,1].max() * 1.0, tight[0,0,2].max() * 1.0)

            # draw a colored rectangle for now
            cv2.rectangle(bgr, tl, br, color, 5)

        if options.output_dir:
            break

        # draw the contours in green
        cv2.drawContours(bgr, contours, -1, (0,255,0), 2)

        """circles = cv2.HoughCircles(grey,cv2.HOUGH_GRADIENT,1,70, param1=50,param2=30,minRadius=30,maxRadius=60)

        #print(circles)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(bgr,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(bgr,(i[0],i[1]),2,(0,0,255),3)

                cv2.imshow('detected circles',bgr)"""

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
