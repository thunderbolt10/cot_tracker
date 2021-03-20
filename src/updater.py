import time
import sched
import threading
import logging
from src.ingester.ingester import Ingester

class Updater():
    update_frequency = 2 * 60 * 60 # 2 hour in seconds

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self._running = True
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.sched_thread = threading.Thread(target=self.scheduler.run)
        self.update_handle = None
        
    def initialise(self):
        self.log.info("---- Initialise Updater ---")
        # schedule an action before we start the thread otherwise the thread will finish if there is no work.
        self.update_handle = self.scheduler.enter(1, 1, self.update_data, ())
        self.sched_thread.start()

  
    def shutdown(self):
        self._running = False
        if self.update_handle:
            self.log.info('Cancel update schedule')
            self.scheduler.cancel(self.update_handle)

        if self.scheduler.empty():
            self.log.info('Scheduler is empty')
        
        self.log.info('Scheduler has %d tasks queued', len(self.scheduler.queue))

        self.log.info('Wait for maintenance thread to stop')

        self.sched_thread.join(4.0)   
        if self.sched_thread.is_alive():
            self.log.warning('Updater thread timeout - still alive') 
                
        self.log.info('Updater thread stopped')

    def update_data(self):
        self.log.info('--- Start Updater')
        try:
            ing = Ingester()
            ing.run_cycle()

            # Reschedule the callback
            self.update_handle = self.scheduler.enter(self.update_frequency, 1, self.update_data, ())
        except Exception as e:
            self.log.exception(e)
    
        self.log.info('--- Exit Updater')
