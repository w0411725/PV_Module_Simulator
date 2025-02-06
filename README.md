# PV Module Simulator
A Python-based tool for simulating the J-V characteristics of a photovoltaic module. It calculates V_oc, J_sc, P_max, and efficiency (PCE) based on user inputs like irradiance, temperature, and resistances. The simulator generates realistic J-V curves for performance analysis.

### Installing Qt Creator ###
  - Qt Creator (IDE for Qt Development): https://www.qt.io/download

# To install Qt Creator, download it from the official Qt website:

  - Go to Qt Creator Download
  - Select Open Source version (if applicable).
  - Install Qt Creator and select the required components.

# Using Package Managers

  - Alternatively, install Qt Creator via a package manager:
    - Ubuntu/Debian ~ sudo apt install qtcreator
    - Arch Linux ~ sudo pacman -S qtcreator
    - MacOS (Homebrew) ~ brew install qt-creator
    - Windows (Chocolatey) ~ choco install qtcreator

### Useful Commands [IF YOU RENAME DEFAULT WIDGET FILE YOU HAVE TO RENAME COMMANDS TOO] ###

# Start Program
 - python widget.py

# Install Required Libraries
 - pip install -r requirements.txt

# OR If you prefer manual installation
 - pip install numpy matplotlib PyQt6

# If you modify the UI using Qt Designer, convert the updated .ui file into a Python file:
 - python -m PyQt6.uic.pyuic -o form.py form.ui

# For automatic form regeneration upon changes:
 - python -m PyQt6.uic.pyuic -o form.py form.ui

# Run in debug mode to see additional logs:
 - python widget.py --debug

# If you want to generate and save the IV curve:
 - python simulator.py --save-plot iv_curve.png

### Useful Resources ###
  - Qt Designer: https://doc.qt.io/qt-6/qtdesigner-manual.html
  - Solar Cell Physics: https://pveducation.com/
  - Solar Cell Effeciency Formula: https://www.ossila.com/pages/solar-cell-efficiency-formula
  - Solar Cell Characteristics: https://www.alternative-energy-tutorials.com/photovoltaics/solar-cell-i-v-characteristic.html
  - Solar Cell IV Curve: https://www.pveducation.org/pvcdrom/solar-cell-operation/iv-curve
  - PyQt6 Documentation: https://www.riverbankcomputing.com/software/pyqt/intro
  - PyQt UI Conversion: https://www.pythonguis.com/tutorials/pyqt6-creating-gui-applications/
  - Python: https://www.python.org/
  - NumPy: https://numpy.org/
  - Matplotlib: https://matplotlib.org/


