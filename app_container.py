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

from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget, QWidget

from pages.base import MainWindow
from pages.development import DevelopmentWindow
from pages.games import GamesWindow


class AppContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fetchy App")

        self.stack = QStackedWidget()

        self.pages = [
            MainWindow("fetchy", "Browsers", [
                ("media/logos/browsers/librewolf.png", "LibreWolf"),
                ("media/logos/browsers/firefox.png", "Firefox"),
                ("media/logos/browsers/chromium.png", "Chromium"),
                ("media/logos/browsers/chrome.png", "Chrome"),
                ("media/logos/browsers/brave.png", "Brave"),
                ("media/logos/browsers/opera.png", "Opera"),
                ("media/logos/browsers/vivaldi.png", "Vivaldi"),
                ("media/logos/browsers/zen.png", "Zen")
            ]),
            GamesWindow(),
            DevelopmentWindow()
        ]

        for page in self.pages:
            self.stack.addWidget(page)
            page.next_button.clicked.connect(self.next_page)
            page.prev_button.clicked.connect(self.previous_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.update_buttons()

    def next_page(self):
        current = self.stack.currentIndex()
        if current < self.stack.count() - 1:
            self.stack.setCurrentIndex(current + 1)
        self.update_buttons()

    def previous_page(self):
        current = self.stack.currentIndex()
        if current > 0:
            self.stack.setCurrentIndex(current - 1)
        self.update_buttons()

    def update_buttons(self):
        current = self.stack.currentIndex()
        for i, page in enumerate(self.pages):
            page.prev_button.setEnabled(0 < i == current)
            page.next_button.setEnabled(len(self.pages) - 1 > i == current)