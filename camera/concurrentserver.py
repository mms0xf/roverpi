import  concurrentbase
import cameraserver

def on_recv():
        print('on_recv')
        
def on_working():
        # How to cancel?
        while concurrent.is_active: 
            camera.wait_connection_and_send_capture()

if __name__ == "__main__":

    camera  = cameraserver.CameraServer()
    concurrent = concurrentbase.ConcurrentBase(on_recv, on_working)

    concurrent.run()

    # wait for KeyboardInterrupt
    import time
    try:
            while True:
                    time.sleep(0.01)
    except KeyboardInterrupt:
            concurrent.cancel()  # or shutdown?


