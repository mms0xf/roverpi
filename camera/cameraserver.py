import io
import socket
import struct
import time
import picamera

DURATION=300

class CameraServer:

    def __init__(self):
        self.camera = picamera.PiCamera() 
        self.camera.resolution = (640,480)
        time.sleep(2) 
	 
        self.sock = socket.socket()
        self.sock.bind(('0.0.0.0', 8001))
        self.sock.listen(0)

    def wait_connection_and_send_capture(self):
        print('camera : begin wating')
        connection = self.sock.accept()[0].makefile('wb')
        print('camera : accepted')

        try:
            start = time.time()
            stream = io.BytesIO()

            # [size => data => size => data ...] cycle
            for foo in self.camera.capture_continuous(stream,'jpeg',use_video_port=True):
                size = stream.tell()
                connection.write(struct.pack('<L',size))  # send size : little endian, unsigned long
                connection.flush() # flush writing buffer. allow not impremented
                stream.seek(0)
                connection.write(stream.read())

                if time.time() - start > DURATION:
                    print('break; start : ' +str(start) )
                    break
                stream.seek(0)
                stream.truncate()  # change stream size from current position

            connection.write(struct.pack('<L',0)) # send as size 0, then remote will break
        except ConnectionResetError as e:
            print('connection reset from client.')
            self.is_reseted=True
            
        finally:
            if not self.is_reseted:
                connection.close()  # shoud not step after connection reset
	  
    def __del__(self):
        print('camera : __del__')
        self.sock.close()

if __name__ == "__main__":    
    camera = CameraServer()
    camera.wait_connection_and_send_capture()	# put in working thread

    camera.wait_connection_and_send_capture()	# put in working thread
 
