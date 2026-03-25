import sys
import threading
from PyQt6.QtWidgets import QApplication
from ui.dashboard import Dashboard
from core.scheduler import start_scheduler

# Start scheduler in background
threading.Thread(target=start_scheduler, daemon=True).start()

app = QApplication(sys.argv)

window = Dashboard()
window.show()

# Clean exit
exit_code = app.exec()
sys.exit(exit_code)