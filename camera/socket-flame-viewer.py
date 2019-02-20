import io
import socket
import struct
from PIL import Image
import numpy
import cv2
import math

'''
python=3.5
conda install -c anaconda pillow
conda install -c conda-forge opencv
'''

def isBottomLine( y1 ,y2 ):
    return (y1 > 480/3) and (y2 > 480/3 )


# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
sock = socket.socket()
sock.connect(('192.168.43.2', 8001))
connection = sock.makefile( 'rb' )


# Accept a single connection and make a file-like object out of it
#connection = sock.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            print ('breaked')
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)

        numpyImage = numpy.fromstring( image_stream.getvalue(), dtype=numpy.uint8)
        cvImage = cv2.imdecode( numpyImage, 1 )
        cvGray = cvImage.copy()

        # to grayscale
        cvGray = cv2.cvtColor(cvGray, cv2.COLOR_BGR2GRAY)


        # Blur image to reduce noise
        cvGray = cv2.GaussianBlur(cvGray, (9, 9), 0)

        #_, cvGray = cv2.threshold(cvGray, 130, 255, cv2.THRESH_BINARY)
        _, cvGray = cv2.threshold(cvGray,  80, 255, cv2.THRESH_BINARY)

        #Perform hough lines probalistic transform
        lines = cv2.HoughLinesP(cvGray,1,numpy.pi/180,200,100,10)

        #Draw lines on input image
        bottomLine = 0
        if lines is not None :
            if( lines.any()):
                for line in lines:
                    x1,y1,x2,y2 = line[0] 
                    cv2.line(cvImage,(x1,y1),(x2,y2),(0,255,0),2)
                    if isBottomLine(y1,y2):
                        xabs = math.fabs(x2-x1)
                        yabs = math.fabs(y2-y1)
                        bottomLine += xabs * yabs

            isGo = bottomLine > 4000000
            print( "{0} {1}".format(bottomLine, isGo) )
#            if isGo:
#                connection.send('go'.encode())
#            else:
#                connection.send('stop'.encode())

        
        cv2.imshow( 'image', cvImage )
#        cv2.imshow( 'image', cvGray )
        cv2.waitKey(1)
        
finally:
    connection.close()
    sock.close()




# sample
# https://www.openmaker.co.kr/single-post/2017/03/17/Simple-Line-Detection-using-Raspberry-Pi-camera-and-OpenCV-Python-for-drone-applications
