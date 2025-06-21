# This file is part of fetchy.
# Copyright (C) 2025 Oreon project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QWidget, QLabel


class Card(QFrame):
    def __init__(self, image_path, title, repo, click_handler=None):
        super().__init__()
        self.title = title
        self.repo = repo
        self.selected = False
        self.click_handler = click_handler

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setFixedSize(450, 200)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 5, 5)
        layout.setSpacing(10)

        self.blue_bar = QWidget()
        self.blue_bar.setFixedWidth(5)
        self.blue_bar.setStyleSheet("background-color: blue;")
        self.blue_bar.hide()
        layout.addWidget(self.blue_bar)

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error loading image: {image_path}")
        else:
            pixmap = pixmap.scaled(
                140, 140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if self.click_handler and self.isEnabled():
            self.click_handler(self)

    def set_selected(self, selected: bool):
        self.selected = selected
        self.update_style()

    def update_style(self):
        self.blue_bar.setVisible(self.selected)

    def set_enabled(self, enabled: bool):
        self.setEnabled(enabled)
        if enabled:
            self.title_label.setStyleSheet("font-weight: bold; color: black;")
            self.image_label.setGraphicsEffect(None)
        else:
            self.title_label.setStyleSheet("font-weight: bold; color: gray;")
            from PyQt5.QtWidgets import QGraphicsOpacityEffect
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.4)
            self.image_label.setGraphicsEffect(opacity_effect)
