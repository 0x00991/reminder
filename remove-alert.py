from tkinter.messagebox import showinfo
from shared import ROOT_DIR, check_dir
import os

check_dir()

disable = not os.path.isfile(ROOT_DIR+"/DISABLEALERT")

if disable:
    with open(ROOT_DIR+"/DISABLEALERT", "wb") as f:
        f.write("yes".encode("utf-8"))
    showinfo(title="알림", message="리마인더 실행 알림이 비활성화 되었습니다.")
else:
    os.remove(ROOT_DIR+"/DISABLEALERT")
    showinfo(title="알림", message="리마인더 실행 알림이 활성화 되었습니다.")