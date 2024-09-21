from uModBusSerial import uModBusSerial
import time

class Radar:
    def __init__(self, port="/dev/modbus", baudrate=9600):
        self._modbus = uModBusSerial(port, baudrate=baudrate)

    def read_radar_level_transmitter(self, slave_addr=1, quantity_of_samples=1, time_sample_ms=1000):
        total_value = 0
        
        for _ in range(quantity_of_samples):
            try:
                sample_value = self._modbus.read_holding_registers(slave_addr, 0, 5)[1]
                total_value += sample_value
            except Exception as e:
                print(f"Error reading from Modbus at address {slave_addr}: {e}")
                continue
            
            time.sleep(time_sample_ms / 1000.0)  # Convert milliseconds to seconds

        avg_value = total_value / quantity_of_samples if quantity_of_samples > 0 else 0
        return avg_value

    def __del__(self):
        # Optional: Close the Modbus connection if necessary
        pass