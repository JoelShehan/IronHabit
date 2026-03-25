from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from core.tracker import load_data


class GymWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IronHabit Widget")
        self.setFixedSize(200, 100)

        # Always on top (widget feel)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint
        )

        layout = QVBoxLayout()

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.update_data()

    def update_data(self):
        data = load_data()
        self.label.setText(f"🔥 {data['streak']} day streak")