import io
import socket
import struct
import time
import picamera


if __name__ == "__main__":    

    sock = socket.socket()
#    sock.connect(('192.168.43.147',8000))
    sock.bind(('0.0.0.0', 8001))
    sock.listen(0)

#    connection = sock.makefile('wb')
    connection = sock.accept()[0].makefile('wb')


    try:
        camera = picamera.PiCamera()
        camera.resolution = (640,480)
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()

        # [size => data => size => data ...] cycle
        for foo in camera.capture_continuous(stream,'jpeg',use_video_port=True):
            connection.write(struct.pack('<L',stream.tell()))  # send size
            connection.flush() # flush writing buffer. NG, not impremented
            stream.seek(0)
            connection.write(stream.read())

            if time.time() - start > 30:
                print('break; start : ' +str(start) )
                break
            stream.seek(0)
            stream.truncate()  # change stream size from current position

        connection.write(struct.pack('<L',0)) # send as size 0, then remote will break

    finally:
        connection.close()
        sock.close()
