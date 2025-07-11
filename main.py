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
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea,
    QComboBox, QPushButton
)
from PyQt5.QtCore import Qt

from app_container import AppContainer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    container = AppContainer()
    container.showFullScreen()
    sys.exit(app.exec_())
