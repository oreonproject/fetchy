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

from pages.base import MainWindow


class DevelopmentWindow(MainWindow):
    def __init__(self):
        super().__init__("Development", "Development", [
            ("media/logos/development/vscode.png", "VSCode"),
            ("media/logos/development/vscodium.png", "VSCodium"),
            ("media/logos/development/jetbrains_toolbox.png", "Jetbrains Toolbox"),
            ("media/logos/development/intellij_community.png", "IntelliJ community"),
            ("media/logos/development/intellij_ultimate.png", "IntelliJ ultimate"),
            ("media/logos/development/pycharm_community.png", "Pycharm community"),
            ("media/logos/development/pycharm_professional.png", "Pycharm professional"),
            ("media/logos/development/clion.png", "CLion"),
            ("media/logos/development/rider.png", "Rider"),
            ("media/logos/development/WebStorm.png", "WebStorm"),
            ("media/logos/development/phpstorm.png", "PHPStorm"),
            ("media/logos/development/datagrip.png", "DataGrip"),
            ("media/logos/development/rustrover.png", "RustRover"),
            ("media/logos/development/goland", "GOLand"),
            ("media/logos/development/rubymine", "RubyMine")
        ])