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
import json
import os


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea,
    QComboBox, QPushButton
)
from PyQt5.QtCore import Qt
import sys

from ui.card import Card
from ui.install_dialog import InstallDialog

with open("package-names.json", "r") as f:
    data = json.load(f)

def get_package_info(packagename):
    return data.get(packagename)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fetchy")

        main_layout = QVBoxLayout(self)

        title_label = QLabel("Browsers")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label)

        self.repo_selector = QComboBox()
        self.repo_selector.addItems(["dnf", "flathub"])
        self.repo_selector.currentTextChanged.connect(self.load_cards)
        main_layout.addWidget(self.repo_selector)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        self.vbox_layout = QVBoxLayout(self.container)
        self.vbox_layout.setContentsMargins(10, 10, 10, 10)
        self.vbox_layout.setSpacing(10)

        self.cards_info = [
            ("media/logos/browsers/librewolf.png", "LibreWolf"),
            ("media/logos/browsers/firefox.png", "Firefox"),
            ("media/logos/browsers/chromium.png", "Chromium"),
            ("media/logos/browsers/chromium.png", "Ungoogled Chromium"),
            ("media/logos/browsers/chrome.png", "Chrome"),
            ("media/logos/browsers/brave.png", "Brave"),
        ]

        self.selected_cards = {
            "dnf": set(),
            "flathub": set()
        }

        self.cards_by_repo = {
            "dnf": [],
            "flathub": []
        }

        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install)
        main_layout.addWidget(install_button)

        self.load_cards("dnf")

    def load_cards(self, repo):
        for i in reversed(range(self.vbox_layout.count())):
            widget = self.vbox_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.cards_by_repo[repo] = []

        for img, title in self.cards_info:
            card = Card(img, title, repo, click_handler=self.card_clicked)

            package_info = get_package_info(title)
            available = bool(package_info and repo in package_info)
            card.set_enabled(available)

            card.set_selected(title in self.selected_cards[repo])
            self.vbox_layout.addWidget(card)
            self.cards_by_repo[repo].append(card)

        self.vbox_layout.addStretch()

    def card_clicked(self, clicked_card):
        repo = clicked_card.repo
        title = clicked_card.title

        if clicked_card.selected:
            clicked_card.set_selected(False)
            self.selected_cards[repo].discard(title)
        else:
            if clicked_card.isEnabled():
                clicked_card.set_selected(True)
                self.selected_cards[repo].add(title)

        print(f"Repository: {repo}")
        print("Selected cards:")
        for r in self.selected_cards:
            for name in self.selected_cards[r]:
                print(f" - {name} ({r})")

    def install(self):
        print("Install started!")

        script_path = os.path.abspath("fetchy.sh")
        lines = ["#!/bin/bash\n"]

        for repo in self.selected_cards:
            for title in self.selected_cards[repo]:
                package_info = get_package_info(title)
                if package_info:
                    package_name = package_info.get(repo)
                    if package_name:
                        if repo == "flathub":
                            lines.append(f"flatpak install -y flathub {package_name}")
                        elif repo == "dnf":
                            lines.append(f"dnf install -y {package_name}")
                        print(f" - Queued: {title} ({repo}) -> {package_name}")
                    else:
                        print(f" - {title} has no {repo} entry.")
                else:
                    print(f" - No package info found for {title}")

        if len(lines) == 1:
            print("Nothing to install.")
            return

        with open(script_path, "w") as file:
            file.write("\n".join(lines) + "\n")
        os.chmod(script_path, 0o755)

        print(f"Script written to {script_path}. Launching with pkexec...")

        dlg = InstallDialog(script_path)
        dlg.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
