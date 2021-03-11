

class Ingester():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.shutdown_event = threading.Event()
        self.keepalive = True
        self.settings = settings()
    def startup(self):
        pass
    def shutdown(self):
        pass
