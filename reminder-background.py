import datetime
from tkinter.messagebox import showinfo
from threading import Thread
from shared import *
import os
import json
import time


check_dir()

ts = lambda: datetime.datetime.now().timestamp()

threads = []
def alert(title: str = "Reminder", message: str = "리마인드 메세지"):
    thread = Thread(target=showinfo, kwargs={"title": title, "message": message}, daemon=True)
    thread.start()
    threads.append(thread)


config = {}
def load_config():
    global config
    if not os.path.isfile(ROOT_DIR+"/config.json"):
        return False
    with open(ROOT_DIR+"/config.json", "r", encoding="utf-8") as f:
        try:
            data = json.loads(f.read())
        except:
            return False
        if data: config = data
        else:
            return False
    return True
load_config()

run = True
def to_int(string):
    try:
        return int(string)
    except:
        return -1

def task():
    if not os.path.isfile(ROOT_DIR+"/DISABLEALERT"):
        alert("실행 알림", "리마인더 백그라운드 프로세스가 시작되었습니다. 함께 배포된 remove-alert.exe 파일을 실행해 알림을 제거할 수 있습니다.")
    global run
    while run:
        if os.path.isfile(ROOT_DIR+"/running.txt"):
            with open(ROOT_DIR+"/running.txt", "r", encoding="utf-8") as f:
                
                try:
                    fr = json.loads(f.read())
                    if fr[0]+config.get("interval", DEFAULT_INTERVAL)-0.1 >= ts():
                        alert("실행 알림", f"리마인더 백그라운드 프로세스의 작동이 감지되었습니다. 이 알림이 오류라고 생각하신다면 {config.get('interval', DEFAULT_INTERVAL)}초 후 프로세스를 다시 실행해주세요.") 
                        run = False
                        break
                except:
                    pass
        with open(ROOT_DIR+"/running.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps([ts(), os.getpid()]))

        if not config and not load_config():
            time.sleep(1)
            continue
        
        check_dir()
        if not os.listdir(ALERT_DIR):
            time.sleep(config.get("interval", DEFAULT_INTERVAL))
            continue
        
        times = list(map(to_int, os.listdir(ALERT_DIR)))
        # past = []
        timestamp = ts()
        for t in times:
            if t < timestamp: # 과거라면
                # past.append(time)
                with open(f"{ALERT_DIR}/{t}", "rb") as f:
                    content = f.read().decode("utf-8")
                os.remove(f"{ALERT_DIR}/{t}")
                alert(f"리마인더 - 지금으로부터 {round(timestamp - t)}초 전..", content)
                print(f"alert - {t} ({content})")
        time.sleep(config.get("interval", DEFAULT_INTERVAL))
                
                
while run:
    try:
        task()
    except KeyboardInterrupt:
        run = False

for th in threads: th.join()