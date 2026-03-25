import schedule
import time
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox


def should_run_today(data):
    today = datetime.now().weekday()

    # Sunday skip
    if today == 6:
        return False

    return True


def show_alert():
    now = datetime.now().time()

    if now < datetime.strptime("16:00", "%H:%M").time():
        return

    if now > datetime.strptime("17:30", "%H:%M").time():
        return

    msg = QMessageBox()
    msg.setWindowTitle("Gym Reminder 💪")
    msg.setText("Go to gym. No excuses.")
    msg.exec()


def start_scheduler():
    schedule.every(10).minutes.do(show_alert)

    while True:
        schedule.run_pending()
        time.sleep(1)