import datetime
from tkinter import Tk
from tkinter.messagebox import showinfo
from threading import Thread
from shared import *
import os
import json
import time


check_dir()

ts = lambda: datetime.datetime.now().timestamp()

# threads = []


alertqueue = [] # [[title, message]]
def alertthread():
    root = Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    while run or alertqueue:
        for a in alertqueue:
            showinfo(title=a[0], message=a[1], parent=root)
        alertqueue.clear()
        time.sleep(1)

# def show(title, message):
#     # showinfo(title=title, message=message)
#     showinfo(title=title, message=message, parent=root)
    
# def alert(title: str = "Reminder", message: str = "리마인드 메세지", join=False):
#     thread = Thread(target=show, kwargs={"title": title, "message": message}, daemon=True)
#     thread.start()
#     if join:
#         threads.append(thread)
def alert(title: str = "Reminder", message: str = "리마인드 메세지"):
    alertqueue.append([title, message])


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

def preload():
    global run
    while True:
        if not config and not load_config():
            time.sleep(1)
            continue
        else:
            break
        
    if os.path.isfile(ROOT_DIR+"/running.txt"):
        with open(ROOT_DIR+"/running.txt", "r", encoding="utf-8") as f:
            try:
                fr = json.loads(f.read())
                if fr[0]+config.get("interval", DEFAULT_INTERVAL)-0.1 >= ts():
                    print(True)
                    alert("실행 알림", f"리마인더 백그라운드 프로세스의 작동이 감지되었습니다. 이 알림이 오류라고 생각하신다면 {config.get('interval', DEFAULT_INTERVAL)}초 후 프로세스를 다시 실행해주세요.") 
                    run = False
                    return
            except: pass
            
    if not os.path.isfile(ROOT_DIR+"/DISABLEALERT"):
        alert("실행 알림", "리마인더 백그라운드 프로세스가 시작되었습니다. 함께 배포된 remove-alert.exe 파일을 실행해 알림을 제거할 수 있습니다.")

def task():
    global run
        
    if os.path.isfile(ROOT_DIR+"/running.txt"):
        with open(ROOT_DIR+"/running.txt", "r", encoding="utf-8") as f:
            try:
                fr = json.loads(f.read())
                if fr[0]+config.get("interval", DEFAULT_INTERVAL)-0.1 >= ts():
                    alert("실행 알림", f"리마인더 백그라운드 프로세스의 작동이 감지되었습니다. 이 알림이 오류라고 생각하신다면 {config.get('interval', DEFAULT_INTERVAL)}초 후 프로세스를 다시 실행해주세요.") 
                    run = False
                    return
            except: pass

                
    with open(ROOT_DIR+"/running.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps([ts(), os.getpid()]))

    check_dir()
    if not os.listdir(ALERT_DIR): return
        
    times = list(map(to_int, os.listdir(ALERT_DIR)))
    timestamp = ts()
    for t in times:
        if t < timestamp: # 과거라면
            with open(f"{ALERT_DIR}/{t}", "rb") as f:
                content = f.read().decode("utf-8")
            os.remove(f"{ALERT_DIR}/{t}")
            alert(f"리마인더 - 지금으로부터 {round(timestamp - t)}초 전..", content)
            print(f"alert - {t} ({content})")
                
ath = Thread(target=alertthread, daemon=True)
preload()
ath.start()
while run:
    try:
        task()
        time.sleep(config.get("interval", DEFAULT_INTERVAL))
    except KeyboardInterrupt:
        run = False

ath.join()
# for t in threads:
    # t.join()