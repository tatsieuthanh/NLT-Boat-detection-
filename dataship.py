import json, time
import requests
from requests.auth import HTTPDigestAuth
import os 
from datetime import datetime
import pytz

class Ship:
    def __init__(self):
        self.api_key = "B7BB08C0BA3AB3ABB3C0B719A635A7C7"
        self.data_type = "DATASHIP"
        self.station_id = "NLT_DDT_0001"
        self.id = 1
        self.input_date = "2024/09/06 10:30:24"
        self.output_date = "2024/09/06 10:30:30"
        self.license_plate = "TG0005"
        self.img_overview = ""
        self.img_license_plate = ""
        self.img_detect = ""
        self.ship_speed = 0.00
        self.ship_length = 0.00
        self.ship_width = 0.00
        self.ship_height = 0.00
        self.ship_weight = 0.00
        self.ship_type = ""
        self.over_height = 0.00
        self.over_weight = 0.00
        self.over_speed = 0.00
        self.cmpn_id = ""
        self.note = ""
        self.is_active = 1
        self.user_id_current = "01"
        self.change_user = ""

        self.dt_format_push = {
            "APIKEY": self.api_key,
            "DataType": self.data_type,
            "StationID": self.station_id,
            "ID": self.id,
            "InputDate": self.input_date,
            "OutputDate": self.output_date,
            "Licenseplate": self.license_plate,
            "ImgOverview": self.img_overview,
            "Imglicenseplate": self.img_license_plate,
            "ImgDetect": self.img_detect,
            "ShipSpeed": self.ship_speed,
            "ShipLength": self.ship_length,
            "ShipWidth": self.ship_width,            
            "ShipHeight": self.ship_height,
            "ShipWeight": self.ship_weight,
            "ShipType": self.ship_type,
            "OverHeight": self.over_height,
            "OverWeight": self.over_weight,
            "OverSpeed": self.over_speed,
            "CmpnID": self.cmpn_id,
            "Note": self.note,
            "IsActive": self.is_active,
            "UserIDCurent": self.user_id_current,
            "ChangeUser": self.change_user
        }

        self.imgoverview=""
        self.imglicenseplate=""
        self.imgdetect=""

        self.dt_format_push_image ={
            "APIKEY": self.api_key,
            "DataType": self.data_type,
            "ID": self.id,
            "Licenseplate": self.license_plate,
            "Image": [
                self.imgoverview,
                self.imglicenseplate,
                self.imgdetect
                    ]
        }

    def image_overview(self,ip='192.168.1.234', usr='admin', pwd='namlong2020'):
        url_get = f'http://{ip}/cgi-bin/snapshot.cgi?'
        
        # Gửi yêu cầu GET với xác thực
        response = requests.get(url_get, auth=HTTPDigestAuth(usr, pwd))
        
        # Kiểm tra xem yêu cầu có thành công không
        if response.status_code == 200:
            # Lưu hình ảnh vào tệp
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            time_vn = datetime.now(vn_tz).strftime('%Y%m%d_%H:%M:%S')
            filename = f'overview_{time_vn}.jpg'
            with open(filename,'wb') as f:  # Mở ở chế độ nhị phân
                f.write(response.content)
            return True
        else:
            print(f"Error: Unable to retrieve image. Status code: {response.status_code}")
            return False