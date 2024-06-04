import os
import time
import yaml
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cryptography.fernet import Fernet
from alerting import send_alert_email

# Configure logging
logging.basicConfig(filename='logs/detection.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')

class RansomwareDetectionHandler(FileSystemEventHandler):
    def __init__(self, encryption_key, config):
        self.encryption_key = encryption_key
        self.suspicious_files = []
        self.config = config
    
    def process(self, event):
        if event.is_directory:
            return
        if event.event_type in ('created', 'modified'):
            self.detect_ransomware(event.src_path)

    def detect_ransomware(self, file_path):
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
            Fernet(self.encryption_key).decrypt(file_data)
        except Exception as e:
            if file_path not in self.suspicious_files:
                self.suspicious_files.append(file_path)
                logging.warning(f"Suspicious activity detected: {file_path}")
                self.alert(file_path)

    def alert(self, file_path):
        subject = "Ransomware Alert!"
        body = f"Suspicious activity detected at: {file_path}"
        logging.info(f"Sending alert email for: {file_path}")
        send_alert_email(subject, body, self.config)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

def monitor_directory(config):
    encryption_key = open(config['encryption_key_path'], "rb").read()
    event_handler = RansomwareDetectionHandler(encryption_key, config)
    observer = Observer()
    observer.schedule(event_handler, config['directory_to_monitor'], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    with open("config.yml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    monitor_directory(config)
