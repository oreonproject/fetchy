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

import subprocess

from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QDialog


class InstallDialog(QDialog):
    def __init__(self, script_path):
        super().__init__()
        self.setWindowTitle("Installing Packages")
        self.resize(600, 400)

        layout = QVBoxLayout(self)
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.run_script(script_path)

    def run_script(self, script_path):
        try:
            result = subprocess.run(
                ["pkexec", "bash", script_path],
                capture_output=True,
                text=True,
                check=True
            )
            self.output_box.append("Success:\n" + result.stdout)
        except subprocess.CalledProcessError as e:
            self.output_box.append("Error:\n" + e.stderr)