import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.tracker import load_data, mark_missed, mark_went
from ui.calendar_view import CalendarView


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IronHabit")
        self.setGeometry(180, 120, 760, 680)
        self.setStyleSheet(self._build_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        hero_card = self._make_card()
        hero_layout = QVBoxLayout(hero_card)
        hero_layout.setSpacing(8)

        eyebrow = QLabel("PERFORMANCE PROTOCOL")
        eyebrow.setObjectName("eyebrow")
        hero_layout.addWidget(eyebrow)

        self.title = QLabel("Train with proof. Build momentum.")
        self.title.setObjectName("heroTitle")
        self.title.setWordWrap(True)
        hero_layout.addWidget(self.title)

        self.subtitle = QLabel(
            "A sharper dashboard for tracking discipline, streak health, and gym proof."
        )
        self.subtitle.setObjectName("mutedLabel")
        self.subtitle.setWordWrap(True)
        hero_layout.addWidget(self.subtitle)
        layout.addWidget(hero_card)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)

        self.streak_label = QLabel("--")
        self.streak_label.setObjectName("statValue")
        stats_row.addWidget(self._make_stat_card("STREAK", self.streak_label))

        self.consistency_label = QLabel("--")
        self.consistency_label.setObjectName("statValue")
        stats_row.addWidget(self._make_stat_card("CONSISTENCY", self.consistency_label))

        self.status_label = QLabel("--")
        self.status_label.setObjectName("statValue")
        stats_row.addWidget(self._make_stat_card("STATUS", self.status_label))
        layout.addLayout(stats_row)

        progress_card = self._make_card()
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setSpacing(10)

        progress_title = QLabel("Momentum charge")
        progress_title.setObjectName("sectionTitle")
        progress_layout.addWidget(progress_title)

        self.progress_summary = QLabel("No activity logged yet.")
        self.progress_summary.setObjectName("mutedLabel")
        self.progress_summary.setWordWrap(True)
        progress_layout.addWidget(self.progress_summary)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(True)
        progress_layout.addWidget(self.progress)
        layout.addWidget(progress_card)

        lower_row = QHBoxLayout()
        lower_row.setSpacing(12)

        proof_card = self._make_card()
        proof_layout = QVBoxLayout(proof_card)
        proof_layout.setSpacing(10)

        proof_title = QLabel("Latest proof")
        proof_title.setObjectName("sectionTitle")
        proof_layout.addWidget(proof_title)

        self.image_preview = QLabel("Upload a workout image to display your latest session.")
        self.image_preview.setObjectName("imagePreview")
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setWordWrap(True)
        proof_layout.addWidget(self.image_preview, 1)

        self.last_checkin_label = QLabel("No session captured yet.")
        self.last_checkin_label.setObjectName("mutedLabel")
        self.last_checkin_label.setWordWrap(True)
        proof_layout.addWidget(self.last_checkin_label)

        controls_card = self._make_card()
        controls_layout = QVBoxLayout(controls_card)
        controls_layout.setSpacing(12)

        controls_title = QLabel("Controls")
        controls_title.setObjectName("sectionTitle")
        controls_layout.addWidget(controls_title)

        self.btn_upload = QPushButton("Log workout proof")
        self.btn_upload.clicked.connect(self.upload_image)
        controls_layout.addWidget(self.btn_upload)

        self.btn_skip = QPushButton("Mark rest / missed day")
        self.btn_skip.setProperty("variant", "secondary")
        self.btn_skip.clicked.connect(self.skip_day)
        controls_layout.addWidget(self.btn_skip)

        self.btn_calendar = QPushButton("Open mission calendar")
        self.btn_calendar.setProperty("variant", "ghost")
        self.btn_calendar.clicked.connect(self.open_calendar)
        controls_layout.addWidget(self.btn_calendar)

        controls_layout.addStretch(1)

        helper = QLabel(
            "Tip: adding a photo after each workout keeps the timeline visual and honest."
        )
        helper.setObjectName("mutedLabel")
        helper.setWordWrap(True)
        controls_layout.addWidget(helper)

        lower_row.addWidget(proof_card, 3)
        lower_row.addWidget(controls_card, 2)
        layout.addLayout(lower_row)

        self.refresh_ui()

    def _make_card(self):
        card = QFrame()
        card.setObjectName("card")
        return card

    def _make_stat_card(self, title, value_label):
        card = self._make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(4)

        label = QLabel(title)
        label.setObjectName("cardLabel")
        card_layout.addWidget(label)
        card_layout.addWidget(value_label)
        card_layout.addStretch(1)
        return card

    def _build_stylesheet(self):
        return """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #07111f,
                    stop: 0.45 #0b1d33,
                    stop: 1 #030812
                );
                color: #e8f3ff;
                font-family: \"Segoe UI\";
            }
            QFrame#card {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(10, 27, 47, 230),
                    stop: 1 rgba(8, 15, 28, 220)
                );
                border: 1px solid rgba(86, 196, 255, 90);
                border-radius: 22px;
            }
            QLabel#eyebrow {
                color: #67e8f9;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }
            QLabel#heroTitle {
                font-size: 28px;
                font-weight: 700;
            }
            QLabel#sectionTitle {
                font-size: 16px;
                font-weight: 600;
            }
            QLabel#cardLabel {
                color: #67e8f9;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            QLabel#statValue {
                font-size: 30px;
                font-weight: 700;
                color: #ffffff;
            }
            QLabel#mutedLabel {
                color: #9bb6d1;
                font-size: 13px;
            }
            QLabel#imagePreview {
                min-height: 260px;
                border-radius: 18px;
                background-color: rgba(255, 255, 255, 18);
                border: 1px solid rgba(103, 232, 249, 65);
                padding: 10px;
                color: #9bb6d1;
            }
            QPushButton {
                min-height: 46px;
                border-radius: 14px;
                border: 1px solid rgba(103, 232, 249, 100);
                background-color: rgba(34, 211, 238, 35);
                color: #eff9ff;
                font-size: 14px;
                font-weight: 600;
                padding: 0 16px;
            }
            QPushButton:hover {
                background-color: rgba(34, 211, 238, 65);
            }
            QPushButton[variant=\"secondary\"] {
                border: 1px solid rgba(244, 114, 182, 80);
                background-color: rgba(244, 114, 182, 24);
            }
            QPushButton[variant=\"secondary\"]:hover {
                background-color: rgba(244, 114, 182, 42);
            }
            QPushButton[variant=\"ghost\"] {
                border: 1px solid rgba(148, 163, 184, 70);
                background-color: rgba(148, 163, 184, 15);
            }
            QPushButton[variant=\"ghost\"]:hover {
                background-color: rgba(148, 163, 184, 28);
            }
            QProgressBar {
                min-height: 28px;
                border-radius: 14px;
                text-align: center;
                border: 1px solid rgba(103, 232, 249, 70);
                background-color: rgba(255, 255, 255, 15);
                color: #f8fbff;
                font-weight: 700;
            }
            QProgressBar::chunk {
                border-radius: 14px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #22d3ee,
                    stop: 1 #38bdf8
                );
            }
        """

    def refresh_ui(self):
        data = load_data()
        history = data.get("history", {})
        total = len(history)
        went_days = sum(1 for entry in history.values() if entry.get("status") == "went")
        consistency = int((went_days / total) * 100) if total else 0
        progress_value = min(went_days * 8, 100)

        latest_date = max(history) if history else None
        latest_entry = history.get(latest_date, {}) if latest_date else {}
        latest_status = latest_entry.get("status", "idle").replace("_", " ").title()

        self.streak_label.setText(f"{data.get('streak', 0)} days")
        self.consistency_label.setText(f"{consistency}%")
        self.status_label.setText(latest_status)

        self.progress.setValue(progress_value)
        self.progress.setFormat(f"{progress_value}% charge")
        self.progress_summary.setText(
            f"{went_days} completed sessions across {total} logged days."
        )

        image_path = latest_entry.get("image")
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(
                420,
                280,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_preview.setPixmap(scaled)
            self.image_preview.setText("")
            self.last_checkin_label.setText(
                f"Latest proof captured on {latest_date} and stored at {image_path}."
            )
        else:
            self.image_preview.setPixmap(QPixmap())
            self.image_preview.setText(
                "Upload a workout image to display your latest session."
            )
            if latest_date:
                self.last_checkin_label.setText(
                    f"Latest log on {latest_date} has no image attached."
                )
            else:
                self.last_checkin_label.setText("No session captured yet.")

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Workout Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )

        if file_path:
            os.makedirs("data/images", exist_ok=True)
            save_path = f"data/images/{os.path.basename(file_path)}"

            with open(file_path, "rb") as source:
                with open(save_path, "wb") as destination:
                    destination.write(source.read())

            mark_went(save_path)
            self.refresh_ui()

    def skip_day(self):
        mark_missed()
        self.refresh_ui()

    def open_calendar(self):
        self.calendar_window = CalendarView()
        self.calendar_window.show()
