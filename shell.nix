{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pyqt5
    python3Packages.pip
    qt5.full

    libxkbcommon
    xorg.libX11
    xorg.libxcb
    xorg.libXrender
    xorg.libXext
    xorg.libXtst
    xorg.libXrandr
    xorg.libXi
    fontconfig
    freetype
  ];

  shellHook = ''
    export QT_QPA_PLATFORM_PLUGIN_PATH=${pkgs.qt5.qtbase.bin}/lib/qt-5/plugins/platforms
    export QT_QPA_PLATFORM=wayland
    echo dev enviroment ready!
  '';
}