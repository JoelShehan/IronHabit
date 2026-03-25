from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget
from PyQt6.QtCore import QDate
from core.tracker import load_data


class CalendarView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar 📅")
        self.setGeometry(300, 300, 400, 400)

        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.info = QLabel("Click a date")
        layout.addWidget(self.info)

        self.calendar.clicked.connect(self.on_date_click)

        self.setLayout(layout)
        self.load_marks()

    def load_marks(self):
        data = load_data()

        for date_str, value in data["history"].items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")

            if value["status"] == "went":
                fmt = self.calendar.dateTextFormat(qdate)
                fmt.setBackground(Qt.GlobalColor.green)
                self.calendar.setDateTextFormat(qdate, fmt)
            else:
                fmt = self.calendar.dateTextFormat(qdate)
                fmt.setBackground(Qt.GlobalColor.red)
                self.calendar.setDateTextFormat(qdate, fmt)

    def on_date_click(self, qdate):
        date_str = qdate.toString("yyyy-MM-dd")
        data = load_data()

        if date_str in data["history"]:
            status = data["history"][date_str]["status"]
            self.info.setText(f"{date_str} → {status}")
        else:
            self.info.setText(f"{date_str} → No data")