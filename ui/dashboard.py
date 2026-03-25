from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar
)
from PyQt6.QtGui import QPixmap
from core.tracker import mark_went, mark_missed, load_data
from ui.calendar_view import CalendarView
import os


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()  # ✅ MUST be first

        self.setWindowTitle("IronHabit 💪")
        self.setGeometry(200, 200, 400, 500)

        layout = QVBoxLayout()  # ✅ create layout BEFORE using

        # Title
        self.title = QLabel("Stay Consistent 💪")
        layout.addWidget(self.title)

        # Streak
        self.streak_label = QLabel()
        layout.addWidget(self.streak_label)

        # Progress
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Image preview
        self.image_label = QLabel("No image yet")
        layout.addWidget(self.image_label)

        # Upload button
        self.btn_upload = QPushButton("Upload Gym Selfie")
        self.btn_upload.clicked.connect(self.upload_image)
        layout.addWidget(self.btn_upload)

        # Skip button
        self.btn_skip = QPushButton("Skip Today")
        self.btn_skip.clicked.connect(self.skip_day)
        layout.addWidget(self.btn_skip)

        # ✅ Calendar button (correct place)
        self.btn_calendar = QPushButton("Open Calendar")
        self.btn_calendar.clicked.connect(self.open_calendar)
        layout.addWidget(self.btn_calendar)

        self.setLayout(layout)
        self.refresh_ui()

    def refresh_ui(self):
        data = load_data()
        self.streak_label.setText(f"🔥 Streak: {data['streak']} days")

        total = len(data["history"])
        self.progress.setValue(min(total * 5, 100))

    def upload_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Image")

        if file:
            os.makedirs("data/images", exist_ok=True)
            save_path = f"data/images/{os.path.basename(file)}"

            with open(file, "rb") as f:
                with open(save_path, "wb") as out:
                    out.write(f.read())

            mark_went(save_path)
            self.refresh_ui()

    def skip_day(self):
        mark_missed()
        self.refresh_ui()

    # ✅ FIXED (proper indentation)
    def open_calendar(self):
        self.calendar_window = CalendarView()
        self.calendar_window.show()