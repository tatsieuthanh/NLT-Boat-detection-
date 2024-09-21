from uModBusSerial import uModBusSerial
import time

def read_radar_level_transmitter(address=1, quantity_of_samples=1, time_sample_ms=1000):
    mb = uModBusSerial("/dev/modbus", baudrate=9600)
    total_value = 0

    for _ in range(quantity_of_samples):
        try:
            sample_value = mb.read_holding_registers(address, 0, 5)[1]
            total_value += sample_value
        except Exception as e:
            print(f"Error reading from Modbus: {e}")
            continue
        
        time.sleep(time_sample_ms / 1000.0)  # Chuyển đổi mili giây thành giây

    avg_value = total_value / quantity_of_samples if quantity_of_samples > 0 else 0
    return avg_value

value = read_radar_level_transmitter(1, 50, 200)  # Thay đổi 1000 thành số mili giây mong muốn
print(value)
