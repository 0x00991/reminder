from getpass import getuser
import os

DEFAULT_INTERVAL = 5
ROOT_DIR = f"C:/Users/{getuser()}/AppData/Roaming/Reminder"
ALERT_DIR = ROOT_DIR+"/alerts"

def check_dir():
    if not os.path.isdir(ROOT_DIR): os.mkdir(ROOT_DIR)
    if not os.path.isdir(ALERT_DIR): os.mkdir(ALERT_DIR)