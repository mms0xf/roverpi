# require python3

import concurrent.futures
import time

class ConcurrentBase:
        def __init__(self, on_recv, on_working):
                print('concurrent init')
                self.is_active = True
                self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
                self.on_recv = on_recv
                self.on_working = on_working
                
        def run(self):
                self.recv_future = self.executor.submit(self.recv_routine, self.on_recv)
                self.send_future = self.executor.submit(self.send_routine, self.on_working)

        def __del__(self):
                print("cnocurrent del") # doesn't called
                self.recv_future.result()  # here ?
                self.send_future.result()


        def recv_routine(self, on_recv):
                while self.is_active:
                        on_recv()
                        time.sleep(1)

        def send_routine(self, on_working):
                on_working()

        def cancel(self):
                self.is_active = False

if __name__ == "__main__":

        active = True
        def on_recv():
                print('on_recv')
        def on_working():
                # How to cancel?	
                while active:
                        print('send_routine')
                        time.sleep(1)


        concurrent = ConcurrentBase(on_recv, on_working)
        concurrent.run()

        # wait for KeyboardInterrupt
        try:
                while True:
                        time.sleep(0.01)
        except KeyboardInterrupt:
                concurrent.cancel()  # or shutdown?
                active = False



