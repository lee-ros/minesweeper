import threading
import time

class Stopwatch:
    def __init__(self):
        self._seconds = 0
        self._time_format = ""
        self._data_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._update_thread = None
        
    def _update_clock(self):
        while not self._stop_event.is_set():
            mins, secs = divmod(self._seconds, 60)
            hours, mins = divmod(mins, 60)
            
            with self._data_lock:
                self._time_format = f"{hours:02d}:{mins:02d}:{secs:02d}"

            time.sleep(1)
            
            with self._data_lock:
                self._seconds += 1
        
    def run(self):
        if self._update_thread is not None:
            self.stop()
            
        with self._data_lock:
            self._seconds = 0
        
        self._stop_event.clear()
        self._update_thread = threading.Thread(target=self._update_clock)
        self._update_thread.start()
        
    def stop(self):
        self._stop_event.set()
        if self._update_thread is not None:
            self._update_thread.join()
            self._update_thread = None 
    
    @property
    def time_format(self) -> str:
        with self._data_lock:
            return self._time_format
