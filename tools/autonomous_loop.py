import time
import threading
from tools.auto_learn import auto_learn
from agents.agent_logs import log_action

class AutonomousMode:
    def __init__(self):
        self.running = False
        self.topics = ["Artificial Intelligence", "Termux Linux", "Python Programming", "Robotics", "Quantum Computing"]
        self.thread = None

    def _loop(self):
        while self.running:
            for topic in self.topics:
                if not self.running:
                    break
                log_action("AutonomousMode", "Starting cycle", topic)
                try:
                    auto_learn.learn_topic(topic)
                except Exception as e:
                    log_action("AutonomousMode", "Cycle Error", str(e))

                # Sleep between topics
                time.sleep(60)

            # Wait before starting next full cycle
            time.sleep(300)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            log_action("AutonomousMode", "System Started")

    def stop(self):
        self.running = False
        log_action("AutonomousMode", "System Stopped")

autonomous_mode = AutonomousMode()
