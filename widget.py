import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget
from form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.generateIVCurveButton.clicked.connect(self.generate_iv_curve)
        self.ui.saveParametersButton.clicked.connect(self.save_parameters)
        self.ui.loadParametersButton.clicked.connect(self.load_parameters)

    def generate_iv_curve(self):
        try:
            # **Step 1: Read input values from UI**
            module_width_mm = float(self.ui.moduleWidthInputField.text())  # mm
            module_length_mm = float(self.ui.moduleLengthInputField.text())  # mm
            light_intensity = float(self.ui.lightIntensityInputField.text())  # W/m²
            ideality_factor = float(self.ui.idealityFactorInputField.text())  # Dimensionless
            dark_saturation_current_mA_cm2 = float(self.ui.normalizedDarkSaturationCurrentInputField.text())  # mA/cm²
            normalized_jsc_mA_cm2 = float(self.ui.normalizedJscInputField.text())  # mA/cm²
            intrinsic_series_resistance = float(self.ui.intrinsicSeriesResistanceInputField.text())  # Ω·cm²
            shunt_resistance = float(self.ui.shuntResistanceInputField.text())  # Ω·cm²

            # **Step 2: Convert units to SI (A/m²)**
            dark_saturation_current_A_m2 = dark_saturation_current_mA_cm2 * 10  # 1 mA/cm² = 10 A/m²
            normalized_jsc_A_m2 = normalized_jsc_mA_cm2 * 10  # 1 mA/cm² = 10 A/m²

            # **Step 3: Convert module dimensions to meters**
            module_width = module_width_mm / 1000
            module_length = module_length_mm / 1000
            area = module_width * module_length  # m²

            # **Step 4: Define physical constants**
            k_B = 1.38e-23  # Boltzmann constant (J/K)
            q = 1.6e-19  # Elementary charge (C)
            T = 300  # Temperature in Kelvin
            thermal_voltage = k_B * T / q  # Compute V_T

            # **Step 5: Define Panel Configuration**
            Ns = 36  # Number of series cells
            Np = 4   # Number of parallel strings

            # **Step 6: Estimate Open-Circuit Voltage (Voc)**
            estimated_V_oc_cell = ideality_factor * thermal_voltage * np.log1p(normalized_jsc_A_m2 / dark_saturation_current_A_m2)
            estimated_V_oc = estimated_V_oc_cell * Ns  # Multiply by number of series cells


            # **Step 7: Generate Voltage Array**
            voltage = np.linspace(0, 1.5, 2000)

            # **Step 8: Compute Diode Current**
            exponent_term = voltage / (ideality_factor * thermal_voltage)
            exponent_term = np.clip(exponent_term, -50, 50)  # Prevent overflow
            diode_current_density = dark_saturation_current_A_m2 * (np.exp(exponent_term) - 1)

            # **Step 9: Apply Series Resistance**
            voltage_effective = voltage - (diode_current_density * intrinsic_series_resistance * Ns)
            voltage_effective = np.maximum(voltage_effective, 0)  # Ensure non-negative voltages

            # **Step 10: Recalculate Diode Current with Series Resistance Correction**
            exponent_term = voltage_effective / (ideality_factor * thermal_voltage)
            exponent_term = np.clip(exponent_term, -50, 50)
            diode_current_density = dark_saturation_current_A_m2 * (np.exp(exponent_term) - 1)

            # **Step 11: Compute Total Current Density**
            J_total = normalized_jsc_A_m2 - diode_current_density - (voltage_effective / shunt_resistance)
            J_total = np.maximum(J_total, 0)  # Ensure no negative values

            # **Step 12: Convert Current Density to Total Current (Panel-Level)**
            total_current = J_total * (module_width * module_length) / (Ns * Np)

            # **Step 13: Compute Power**
            power = voltage * total_current

            # **Step 14: Find Maximum Power Point (MPP)**
            max_power_index = np.argmax(power)
            max_power = power[max_power_index]
            max_voltage = voltage[max_power_index]
            max_current = total_current[max_power_index]

            # **Step 15: Calculate Incident Power**
            incident_power = light_intensity * area  # W

            # **Step 16: Calculate Efficiency**
            efficiency = (max_power / incident_power) * 100

            # **Step 17: Print Debugging Info**
            print(f"Estimated V_oc: {estimated_V_oc:.4f} V")
            print(f"Incident Power: {incident_power:.2f} W")
            print(f"Module Area (m²): {area:.2f}")
            print(f"Voltage values: {voltage[:5]}")
            print(f"Current values: {total_current[:5]}")
            print(f"Max Power: {max_power:.2f} W")
            print(f"Efficiency (PCE): {efficiency:.2f} %")

            # **Step 18: Generate J-V Plot**
            plt.figure(figsize=(6, 4))
            plt.plot(voltage, total_current, linestyle="solid", label="Final Corrected J-V Curve", color="blue")
            plt.scatter(max_voltage, max_current, color="red", label="Max Power Point")
            plt.annotate(f"Max Power: {max_power:.2f} W",
                         (max_voltage, max_current),
                         textcoords="offset points",
                         xytext=(20, -20),
                         ha='center',
                         fontsize=10,
                         color="red")
            plt.xlabel("Voltage (V)")
            plt.ylabel("Current (A)")
            plt.title("Final Validated J-V Curve (Self-Consistent Rs & Rsh)")
            plt.legend()
            plt.grid()
            plt.show()

        except Exception as e:
            print(f"An error occurred: {e}")




    def save_parameters(self):
        """Saves all input parameters to a JSON file."""
        parameters = {
            "module_width": self.ui.moduleWidthInputField.text(),
            "module_length": self.ui.moduleLengthInputField.text(),
            "left_right_margin": self.ui.leftRightMarginInputField.text(),
            "up_down_margin": self.ui.upDownMarginInputField.text(),
            "light_intensity": self.ui.lightIntensityInputField.text(),
            "number_of_IV_points": self.ui.numberOfIVPointsInputField.text(),
            "ideality_factor": self.ui.idealityFactorInputField.text(),
            "thermal_voltage": self.ui.thermalVoltageInputField.text(),
            "dark_saturation_current": self.ui.normalizedDarkSaturationCurrentInputField.text(),
            "intrinsic_series_resistance": self.ui.intrinsicSeriesResistanceInputField.text(),
            "p1_width": self.ui.p1WidthInputField.text(),
            "p2_width": self.ui.p2WidthInputField.text(),
            "p3_width": self.ui.p3WidthInputField.text(),
            "p1_p2_distance": self.ui.p1P2DistanceInputField.text(),
            "p2_p3_distance": self.ui.p2P3DistanceInputField.text(),
            "cell_width": self.ui.cellWidthInputField.text(),
            "ito_sheet_resistance": self.ui.itoSheetResistanceInputField.text(),
            "carbon_sheet_resistance": self.ui.carbonSheetResistanceInputField.text(),
            "shunt_resistance": self.ui.shuntResistanceInputField.text(),
            "normalized_jsc": self.ui.normalizedJscInputField.text(),
            "p2_contact_resistivity": self.ui.p2ContactResistivityInputField.text(),
        }

        with open("parameters.json", "w") as file:
            json.dump(parameters, file, indent=4)

        print("All parameters saved successfully!")

    def load_parameters(self):
        """Loads all input parameters from a JSON file and updates UI fields."""
        try:
            with open("parameters.json", "r") as file:
                parameters = json.load(file)

            self.ui.moduleWidthInputField.setText(parameters.get("module_width", ""))
            self.ui.moduleLengthInputField.setText(parameters.get("module_length", ""))
            self.ui.leftRightMarginInputField.setText(parameters.get("left_right_margin", ""))
            self.ui.upDownMarginInputField.setText(parameters.get("up_down_margin", ""))
            self.ui.lightIntensityInputField.setText(parameters.get("light_intensity", ""))
            self.ui.numberOfIVPointsInputField.setText(parameters.get("number_of_IV_points", ""))
            self.ui.idealityFactorInputField.setText(parameters.get("ideality_factor", ""))
            self.ui.thermalVoltageInputField.setText(parameters.get("thermal_voltage", ""))
            self.ui.normalizedDarkSaturationCurrentInputField.setText(parameters.get("dark_saturation_current", ""))
            self.ui.intrinsicSeriesResistanceInputField.setText(parameters.get("intrinsic_series_resistance", ""))
            self.ui.p1WidthInputField.setText(parameters.get("p1_width", ""))
            self.ui.p2WidthInputField.setText(parameters.get("p2_width", ""))
            self.ui.p3WidthInputField.setText(parameters.get("p3_width", ""))
            self.ui.p1P2DistanceInputField.setText(parameters.get("p1_p2_distance", ""))
            self.ui.p2P3DistanceInputField.setText(parameters.get("p2_p3_distance", ""))
            self.ui.cellWidthInputField.setText(parameters.get("cell_width", ""))
            self.ui.itoSheetResistanceInputField.setText(parameters.get("ito_sheet_resistance", ""))
            self.ui.carbonSheetResistanceInputField.setText(parameters.get("carbon_sheet_resistance", ""))
            self.ui.shuntResistanceInputField.setText(parameters.get("shunt_resistance", ""))
            self.ui.normalizedJscInputField.setText(parameters.get("normalized_jsc", ""))
            self.ui.p2ContactResistivityInputField.setText(parameters.get("p2_contact_resistivity", ""))

            print("All parameters loaded successfully!")

        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: No saved parameters found or the file is corrupted.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
