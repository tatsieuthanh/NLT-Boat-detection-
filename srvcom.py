import ssl,uuid,time,json,logging
from paho.mqtt import client as mqtt_client

class Server:
    def __init__(self):
        self.broker = 'nlt-group.com'
        self.port = 8884
        self.client_id = str(uuid.uuid4())
        self.username = 'namlong'
        self.password = 'namlong2020'
        self.station_id = "NLT_DDT_0001"
        self.api_key = "B7BB08C0BA3AB3ABB3C0B719A635A7C7"
        self.project_name = "SmartShip"
        self.version = "Ver2"
        self.device_type = "NLT7004"
        self.topics = {
            'pub_init': f"{self.version}/{self.device_type}/{self.project_name}/Request{self.station_id}/Init",
            'pub_push_data': f"{self.version}/{self.device_type}/{self.project_name}/Request/{self.station_id}/PushData",
            'pub_push_image': f"{self.version}/{self.device_type}/{self.project_name}/Request/{self.station_id}/PushImage",
            'sub_control': f"{self.version}/{self.device_type}/{self.project_name}/Response/{self.station_id}/Control",
            'sub_result': f"{self.version}/{self.device_type}/{self.project_name}/Response/{self.station_id}/Result"
        }
        

        self.mes = ""
        self.mes_tmp = ""

    def on_connect(self,client, userdata, flags, rc):
        if rc == 0 and self.client.is_connected():
            print("Connected to MQTT Broker!")
            self.client.subscribe(self.topic_sub_Control)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(self,client, userdata, rc):
        print(f"Disconnected with result code {rc}. Attempting to reconnect...")
        while True:
            try:
                client.reconnect()
                break
            except Exception as e:
                print(f"Reconnect failed: {str(e)}")
                time.sleep(5)  

    def on_message(self,client, userdata, msg):
        self.mes = msg.payload.decode()
        if len(self.mes) > 0 and self.mes != self.mes_tmp:
            self.mes_tmp = self.mes
            with open('data.json', 'w') as f:
                json.dump(json.loads(self.mes), f)
            print(f"Received and Write new data `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.mes = ""

    def mqtt_setup_ssl(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
        self.client.tls_insecure_set(False)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect       

    def connect_mqtt(self):       
        self.client = mqtt_client.Client(self.client_id, transport='websockets')
        #self.client = mqtt_client.Client(client_id=self.client_id, protocol=mqtt_client.MQTTv311, transport='websockets')
        self.mqtt_setup_ssl()
        self.client.connect(self.broker, self.port)
        return self.client
        
    def publish(self,topic, msg):
        result = self.client.publish(topic, msg)
        if result[0] == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    