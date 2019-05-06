import numpy as np
import cv2
import datetime
import pprint as pp
import time
import pymongo



def CamInt():
    # Define the codec and create VideoWriter object (note isColor is False for Gray)
    timestamp = int(time.time())
    image_rename = str(timestamp) + '.avi'
    #pp.pprint(image_rename)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(image_rename,
                          fourcc, 30.0, (640, 480), isColor=False)
    

    # Look for the first Videosource, define the camerasettings and create HD-VideoCapture object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Define gaussian mixture-based background/foreground segmentation object
    foreground = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    while(True):
        # Get camframe in HD
        (ret, camframe) = cap.read()
        # No colors
        grayframe = cv2.cvtColor(camframe, cv2.COLOR_BGR2GRAY)
        # Resize it
        smallframe = cv2.resize(grayframe, (1080, 760))
        # Denoising
        blurframe = cv2.medianBlur(smallframe, 3)
        # Get motion
        motionframe = foreground.apply(blurframe)
        # Show some
        cv2.imshow('motionframe', motionframe)
        cv2.imshow('blurframe', blurframe)
        # Threshold
        detect = (np.sum(motionframe))//255
        if detect > 30000:
            
            #print("moving object size = ", detect, currenttime)
            motion=str(detect)
            #write HD-stream to .avi -file
            #write values
            #intiate connection to mongo collection mafirimu
            dbchange = pymongo.MongoClient("mongodb://127.0.0.1:27017")
            changedb = dbchange["lenz"]
            mycol = changedb["mafirimu"]

            #user form data as dictionary
            date = str(datetime.datetime.now())
            motion_captured = {'date_time':date, 'camera_feed':0 , 'time_stamps':image_rename, 'motion':motion}
            mycol.insert_one(motion_captured)
        
            out.write(grayframe)
        k = cv2.waitKey(1) & 0xff
        # For more camerasettings type "s"
        if k == ord('s'):
            cap.set(cv2.CAP_PROP_SETTINGS, 0)
        # Stop it with the SpaceBar or ESC
        if k == ord(' ') or k == 27 or ret == False:
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return detect
