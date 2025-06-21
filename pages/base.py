import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QScrollArea, QComboBox, QLabel

from ui.card import Card
from ui.install_dialog import InstallDialog


class MainWindow(QWidget):
    def __init__(self, window_title, label, cards_info):
        super().__init__()
        self.setWindowTitle(window_title)

        main_layout = QVBoxLayout(self)

        title_label = QLabel(label)
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

        self.cards_info = cards_info
        self.selected_cards = {"dnf": set(), "flathub": set()}
        self.cards_by_repo = {"dnf": [], "flathub": []}

        install_button = QPushButton("Install")
        install_button.clicked.connect(self.install)
        main_layout.addWidget(install_button)

        # Navigation buttons
        nav_layout = QVBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)
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

        dlg = InstallDialog(script_path)
        dlg.exec_()



with open("package-names.json", "r") as f:
    data = json.load(f)

def get_package_info(packagename):
    return data.get(packagename)


