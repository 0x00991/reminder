from shared import *
import os
import json
import datetime
import psutil

os.system("title 리마인더 - 0x00991")
def is_numeric(string):
    try:
        int(string)
        return True
    except:
        return False

def df(d):
    return d if d > 9 else f"0{d}"

check_dir()

config = {"interval": DEFAULT_INTERVAL}
if not os.path.isfile(ROOT_DIR+"/config.json"):
    try:
        config["interval"] = int(input("확인 간격을 입력해주세요. (단위: 초) >"))
    except:
        pass
    
    with open(ROOT_DIR+"/config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(config))
else:
    with open(ROOT_DIR+"/config.json", "r", encoding="utf-8") as f:
        try:
            config = json.loads(f.read())
        except:
            pass

def list():
    alerts = os.listdir(ALERT_DIR)
    if not alerts:
        print("현재 예정된 알림이 없습니다.")
        return
    print("예정된 알림:")
    print("")
    for a in alerts:
        if not is_numeric(a): continue
        
        with open(ALERT_DIR+f"/{a}", "rb") as f:
            c = f.read().decode("utf-8")
        t = datetime.datetime.fromtimestamp(int(a))
        
        yyyymmdd = f"{t.year}{df(t.month)}{df(t.day)}"
        hhmmss = f"{df(t.hour)}:{df(t.minute)}:{df(t.second)}"
        
        print(f"{yyyymmdd} {hhmmss}: {c}")
        
        

def create():
    print("현재로부터 입력된 시간 후에 알림창으로 알려드립니다.")
    print("시간 단위는 s (초), m (분), h (시간), d (일), w (주), M (달 [30일]), y (년) 입니다.")
    print("예시: 입력 5s 1m = 1분 5초 후 알림 / 5s 10s 1m = 1분 15초 후 알림.")
    inp = input("언제 알려드릴까요? >")
    message = input("알림의 내용을 입력해주세요. > ")
    time = 0
    inp_split = inp.split(" ")
    for i in inp_split:
        if is_numeric(i):
            time += int(i)
            continue
        
        if not is_numeric(i[:-1]):
            print(f"'{i}'는 알 수 없는 단위입니다. (s, m, h, d, w, M, y)")
            continue
        
        i_ = int(i[:-1])
        
        
        if i_ <= 0:
            continue
        
        unit = i[-1:]
        unit_name = "초"
        multiplier = 1
        
        if unit == "y":
            multiplier = 86400*365 # 1년
            unit_name = "년"
        elif unit == "M":
            multiplier = 86400*30
            unit_name = "달"
        elif unit == "w":
            multiplier = 86400*7
            unit_name = "주"
        elif unit == "d":
            multiplier = 86400
            unit_name = "일"
        elif unit == "h":
            multiplier = 3600
            unit_name = "시간"
        elif unit == "m":
            multiplier = 60
            unit_name = "분"
        elif unit == "s":
            pass
        else:
            print(f"'{i}'는 알 수 없는 단위입니다. (s, m, h, d, w, M, y)")
            continue
        print(f"+ {i_}{unit_name}")
        
        time += i_*multiplier

    print("")

    not_msg = ""
    if time >= 86400*365:
        not_msg = f"{time/86400//365}년"
    elif time >= 86400*30:
        not_msg = f"{time/86400//30}달"
    elif time >= 86400*14:
        not_msg = f"{time/86400//7}주"
    elif time >= 86400:
        not_msg = f"{time//86400}일"
    elif time >= 3600:
        not_msg = f"{time//3600}시간"
    elif time >= 60:
        not_msg = f"{time//60}분"
    else:
        not_msg = f"{time}초"


    ts = round(datetime.datetime.now().timestamp())+time


    with open(ALERT_DIR+f"/{ts}", "wb") as f:
        f.write(message.encode("utf-8"))

    print(f"약 {not_msg} 후에 알림이 표시됩니다. (내용: {message})")
    print("")

def rp_started():
    if not os.path.isfile(ROOT_DIR+"/running.txt"):
        return False
    try:
        with open(ROOT_DIR+"/running.txt", "r", encoding="utf-8") as f:
            fr = json.loads(f.read())
            if fr[0]+config.get("interval", DEFAULT_INTERVAL) < datetime.datetime.now().timestamp():
                return False
            else:
                return True
    except:
        return False

def killp():
    if not os.path.isfile(ROOT_DIR+"/running.txt"):
        print("리마인더가 실행되지 않았습니다.")
        return
    try:
        with open(ROOT_DIR+"/running.txt", "r", encoding="utf-8") as f:
            fr = json.loads(f.read())
            if fr[0]+config.get("interval", DEFAULT_INTERVAL) < datetime.datetime.now().timestamp():
                print(f"리마인더가 실행되지 않았습니다. 오류라고 생각하신다면 {config.get('interval', DEFAULT_INTERVAL)}초 후 다시 시도해보세요.")
                return
            for p in psutil.process_iter():
                if p.pid == fr[1]:
                    p.kill()
        print("종료되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

while True:
    if not rp_started():
        print("주의: 리마인더 프로세스가 감지되지 않았습니다. 알림이 표시되지 않을 수 있습니다.")
    print("(1) 알림 생성\n(2) 예정된 알림 목록\n(3) 리마인더 비활성화\n(4) 프로그램 종료")
    inp = input(">")
    [print("") for i in range(3)]
    if inp == "1":
        create()
    elif inp == "2":
        list()
    elif inp == "3":
        killp()
    elif inp == "4":
        break
    else:
        print("알 수 없는 옵션입니다.")
    [print("") for i in range(3)]