#SYNC time wdt module
__version__ = '0.0.1'
import os
from datetime import datetime
import time
import ntplib

class Object:
    alarm1 = [10,11,12,13] #
    alarm2 = [14,15,16,17]
    alarm3 = [18,19,20,21]
    alarm4 = [22,23,24,25]
    relay1 = 7
    relay2 = 8
class SYNC:
    def __init__(self,modbus):
        self._modbus = modbus

    def compare_rtcsystem(self, recv, date):
        print('------------RTC - SYSTEM------------')
        if recv[6] == date.year and recv[5] == date.month and recv[4] == date.day: 
            if recv[0] == date.hour:
                if abs(recv[1] - date.minute) <= 2:
                    print("[synced]")
                    return 0
                else:
                    print("[asynchronous minute]")
                    return 1
            else:
                print("[asynchronous hour]")
                return 1
        else:
            print("[asynchronous year/month/day]")
            return 1

    def compare_serversystem(self, time, date):
        print('------------SERVER - SYSTEM------------')
        if time[1] == str(date)[0:10]:
            if int(time[2][:2]) == date.hour:
                if abs(int(time[2][3:5]) - date.minute) <= 2:
                    print("[synced]")
                    return 0
                else:
                    print("[asynchronous minute]")
                    return 1
            else:
                print("[asynchronous hour]")
                return 1
        else:
            print("[asynchronous year/month/day]")
            return 1

    def gettime_server(self,server='time.google.com',retries=2):
        attempts = 0
        client = ntplib.NTPClient()
        response = None
        while 1:
            try:
                response = client.request(server, version=3)
            except Exception as e:
                print(e)
            attempts += 1

            if response or attempts >= retries:
                break
            time.sleep(0.5)
            
        if not response:
            return 1, '0', '0'

        local_time = time.localtime(response.ref_time)
        current_date = time.strftime('%Y-%m-%d', local_time)
        current_time = time.strftime('%H:%M:%S', local_time)
        return 0, current_date, current_time

    def hwclock_set(self,time):
        print('[hwclock set {}]'.format(time))
        os.system("hwclock --set --date '{}'".format(time))
        os.system('hwclock -s')

    def read(self, slave_addr = 99, starting_address = 0, register_quantity = 27):
        try:
            recv = self._modbus.read_holding_registers(slave_addr,starting_address,register_quantity)
        except Exception as e:
            print(e)
        return recv
        
    def write(self, slave_addr = 99, starting_address = 0, register_values = []):
        try:
            recv = self._modbus.write_multiple_registers(slave_addr,starting_address,register_values)
        except Exception as e:
            print(e)

    def sync_time(self):
        try:
            recv = self.read(register_quantity = 7)
            print('[Time RTC: {}]'.format(str(datetime(recv[6],recv[5],recv[4],recv[0],recv[1],recv[2]))))
            date =  datetime.now()
            print('[Time system: {}]'.format(str(date)[:-7]))
            get_time = self.gettime_server()
            if get_time[0] == 0:
                print('[Connected]')
                time_server = get_time[1]+' '+get_time[2]
                print('[Time server: {}]'.format(time_server))
                comp_svsys = self.compare_serversystem(get_time,date)
                if comp_svsys == 1:
                    self.hwclock_set(time_server)
                    date =  datetime.now()
                    print('[Time system: {}]'.format(str(date)[:-7]))
                wr = [date.hour,date.minute,date.second,date.weekday(),date.day,date.month,date.year]
                comp_rtcsys = self.compare_rtcsystem(recv, date)
                if comp_rtcsys == 1:
                    print('Write: {}'.format(wr))
                    self.write(slave_addr = 99, starting_address = 0, register_values = wr)
            else:
                print('[Lost connection]')
                comp_rtcsys = self.compare_rtcsystem(recv, date)
                if comp_rtcsys == 1:
                    sync = str(datetime(recv[6],recv[5],recv[4],recv[0],recv[1],recv[2]))
                    self.hwclock_set(sync)
        except Exception as e:
            print(e)

    def alarm_set(self, alarm, active, hour, minute, loop):
        obj = Object()
        if active in [0,1] and 0 <= hour < 24 and 0 <= minute < 60 and loop in [1,2,3,4,5]:
            try:
                recv = self.read()
                al = getattr(obj, 'alarm'+str(alarm))
                print(f'[set alarm {alarm}]:({active}, {hour}, {minute}, {loop})')

                wr = [active,hour,minute,loop]
                if recv[al[0]] != active or recv[al[1]] != hour or recv[al[2]] != minute or recv[al[3]] != loop:
                    self.write(slave_addr = 99,starting_address = al[0],register_values = wr)
                recv = self.read()
            except Exception as e:
                print(e)
        else:
            print('alarm set index out of range')

    def relay(self, stt,state):
        obj = Object()
        text_state = ''
        if state in [0,1]:
            try:
                recv = self.read()
                rl = getattr(obj, 'relay'+str(stt))
                if recv[rl] != state:
                    self.write(slave_addr = 99, starting_address = rl, register_values = [state])
                    if state == 1:
                        text_state = 'ON'
                    else: text_state = 'OFF'
                    print('[{} relay {}]'.format(text_state,stt))
            except Exception as e:
                print(e)
        else:
            print('state index out of range')

    def wdt(self):
        self.write(slave_addr = 99, starting_address = 26, register_values = [0])
