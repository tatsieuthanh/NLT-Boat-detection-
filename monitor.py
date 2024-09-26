import json, time
import subprocess,  psutil

#pip install psutil
#sudo apt install lm-sensors


class Cabinet:
    def __init__(self):
        self.api_key = "B7BB08C0BA3AB3ABB3C0B719A635A7C7"
        self.data_type = "MONITOR"
        self.station_id = "NLT_DDT_0001"
        self.signal_4g = "-80"
        self.cpu_performance = 0
        self.cpu_temperature = 60
        self.amperage_mA = 0
        self.voltage_V = 12
        self.storage = "6.2/29 (22%)"
        self.memory = "300M/3.5G"
        self.dt_format = {

            "APIKEY": self.api_key,
            "DataType": self.data_type,
            "StationID": self.station_id,
            "Signal4G": self.signal_4g,
            "CpuPerformance": self.cpu_performance,
            "CpuTemperature": self.cpu_temperature,
            "Amperage_mA": self.amperage_mA,
            "Voltage_V": self.voltage_V,
            "Storage": self.storage,
            "Memory": self.memory
        }

    def get_signal_strength(self):
        try:
            result = subprocess.run(['mmcli', '-m', '0'], capture_output=True, text=True, check=True)

            for line in result.stdout.splitlines():
                if 'signal quality' in line:
                    signal_strength = line.split(':')[-1].strip()
                    return signal_strength
        except subprocess.CalledProcessError as e:
            print("Error checking signal strength:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)

        return None

    def get_cpu_performance(self):
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()

            performance_data = {
                'CPU Usage (%)': cpu_usage,
                'CPU Frequency (MHz)': cpu_freq.current if cpu_freq else None,
                'Total Virtual Memory (MB)': virtual_memory.total / (1024**2),  # Total memory in MB
                'Total Swap Memory (MB)': swap_memory.total / (1024**2),  # Total swap in MB
                'Used Swap Memory (MB)': swap_memory.used / (1024**2),    # Used swap in MB
                'Free Swap Memory (MB)': swap_memory.free / (1024**2)     # Free swap in MB
            }

            return performance_data

    def get_cpu_temperature(self):
        try:
            output = subprocess.check_output("sensors", encoding='utf-8')
            for line in output.split('\n'):
                if 'temp1' in line: 
                    temp = line.split(':')[1].strip().split(' ')[0]
                if 'in1' in line:
                    ampe = line.split(':')[1].strip().split(' ')[0]
                if 'in2' in line:
                    vol = line.split(':')[1].strip().split(' ')[0]
            return temp, ampe, vol
        except Exception as e:
            return f"Error retrieving temperature: {e}"
  
    def read_cpu_infor(self):
        try:
            signal = self.get_signal_strength()
            performance = self.get_cpu_performance()
            temp_amp_vol = self.get_cpu_temperature()

            self.dt_format['Signal4G'] = signal
            self.dt_format['CpuPerformance'] = performance['CPU Usage (%)']
            self.dt_format['CpuTemperature'] = temp_amp_vol[0]
            self.dt_format['Amperage_mA'] = temp_amp_vol[1]
            self.dt_format['Voltage_V'] = temp_amp_vol[2]
            memory_info = psutil.virtual_memory()
            self.dt_format['Memory'] = {
                'Total_MB': round(memory_info.total / (1024**2), 2),
                'Used_MB': round(memory_info.used / (1024**2), 2),
                'Free_MB': round(memory_info.free / (1024**2), 2)
            }

            storage_info = psutil.disk_usage('/')
            self.dt_format['Storage'] = {
                'Total_MB': round(storage_info.total / (1024**2), 2),
                'Used_MB': round(storage_info.used / (1024**2), 2),
                'Free_MB': round(storage_info.free / (1024**2), 2)
            }
            return self.dt_format
        except Exception as e:
                return f"Error read_cpu_infor: {e}"
