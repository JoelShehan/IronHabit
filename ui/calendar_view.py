import os

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPixmap, QTextCharFormat
from PyQt6.QtWidgets import QCalendarWidget, QDialog, QLabel, QVBoxLayout, QWidget

from core.tracker import load_data


class CalendarView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IronHabit Calendar")
        self.setGeometry(260, 160, 620, 560)
        self.setStyleSheet(self._build_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel("Mission calendar")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel(
            "Review completed and missed days. Click a logged date to inspect its proof."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(False)
        layout.addWidget(self.calendar)

        self.info = QLabel("Select a date to inspect its status.")
        self.info.setObjectName("info")
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        self.calendar.clicked.connect(self.on_date_click)
        self.load_marks()

    def _build_stylesheet(self):
        return """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #050b16,
                    stop: 1 #0b1d33
                );
                color: #e7f2ff;
                font-family: \"Segoe UI\";
            }
            QLabel#title {
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#subtitle, QLabel#info {
                color: #9bb6d1;
                font-size: 13px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: rgba(255, 255, 255, 10);
            }
            QCalendarWidget QToolButton {
                color: #e7f2ff;
                background-color: rgba(34, 211, 238, 25);
                border: 1px solid rgba(103, 232, 249, 80);
                border-radius: 10px;
                padding: 6px 10px;
                margin: 4px;
                font-weight: 600;
            }
            QCalendarWidget QMenu {
                background-color: #08111e;
                color: #e7f2ff;
            }
            QCalendarWidget QSpinBox {
                background-color: rgba(255, 255, 255, 14);
                color: #e7f2ff;
                selection-background-color: #22d3ee;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: rgba(10, 27, 47, 230);
                color: #e7f2ff;
                selection-background-color: #22d3ee;
                selection-color: #03111f;
                border: 1px solid rgba(103, 232, 249, 70);
                border-radius: 16px;
                outline: 0;
            }
        """

    def load_marks(self):
        data = load_data()

        for date_str, value in data.get("history", {}).items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            fmt = QTextCharFormat(self.calendar.dateTextFormat(qdate))

            if value.get("status") == "went":
                fmt.setBackground(Qt.GlobalColor.darkCyan)
                fmt.setForeground(Qt.GlobalColor.white)
            else:
                fmt.setBackground(Qt.GlobalColor.darkRed)
                fmt.setForeground(Qt.GlobalColor.white)

            self.calendar.setDateTextFormat(qdate, fmt)

    def on_date_click(self, qdate):
        date_str = qdate.toString("yyyy-MM-dd")
        history = load_data().get("history", {})

        if date_str in history:
            entry = history[date_str]
            status = entry.get("status", "unknown").replace("_", " ").title()
            image_path = entry.get("image")

            if image_path and os.path.exists(image_path):
                self.info.setText(f"{date_str}: {status} with proof attached.")
                self.show_image_popup(image_path)
                return

            self.info.setText(f"{date_str}: {status}. No image attached.")
        else:
            self.info.setText(f"{date_str}: no data recorded.")

    def show_image_popup(self, image_path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Workout Proof")
        dialog.setGeometry(360, 200, 520, 520)
        dialog.setStyleSheet(
            """
            QDialog {
                background-color: #08111e;
            }
            QLabel {
                color: #e7f2ff;
            }
            """
        )

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path)
        label.setPixmap(
            pixmap.scaled(
                460,
                460,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        layout.addWidget(label)
        dialog.exec()
