import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotRestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_bot()
    
    def start_bot(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        print("Запуск бота...")
        self.process = subprocess.Popen([sys.executable, "main.py"])
    
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Обнаружено изменение в {event.src_path}")
            self.start_bot()

def main():
    handler = BotRestartHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if handler.process:
            handler.process.terminate()
    observer.join()

if __name__ == "__main__":
    main()
