# PV_Module_Simulator
A Python-based tool for simulating the J-V characteristics of a photovoltaic module. It calculates V_oc, J_sc, P_max, and efficiency (PCE) based on user inputs like irradiance, temperature, and resistances. The simulator generates realistic J-V curves for performance analysis.

# Useful Commands [IF YOU RENAME DEFAULT WIDGET FILE YOU HAVE TO RENAME COMMANDS TOO]

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
