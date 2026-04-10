from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from core.tracker import load_data


class GymWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IronHabit Widget")
        self.setFixedSize(240, 120)
        self.setStyleSheet(self._build_stylesheet())

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        self.eyebrow = QLabel("IRONHABIT")
        self.eyebrow.setObjectName("eyebrow")
        layout.addWidget(self.eyebrow)

        self.label = QLabel()
        self.label.setObjectName("value")
        layout.addWidget(self.label)

        self.caption = QLabel("Live streak telemetry")
        self.caption.setObjectName("caption")
        layout.addWidget(self.caption)

        self.update_data()

    def _build_stylesheet(self):
        return """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(6, 15, 28, 240),
                    stop: 1 rgba(10, 27, 47, 240)
                );
                color: #edf8ff;
                border: 1px solid rgba(103, 232, 249, 75);
                border-radius: 18px;
                font-family: \"Segoe UI\";
            }
            QLabel#eyebrow {
                color: #67e8f9;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            QLabel#value {
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#caption {
                color: #9bb6d1;
                font-size: 12px;
            }
        """

    def update_data(self):
        streak = load_data().get("streak", 0)
        self.label.setText(f"{streak} day streak")
