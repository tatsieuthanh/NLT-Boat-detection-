from Radar import Radar

if __name__ == "__main__":
    radar = Radar()
    value = radar.read_radar_level_transmitter(1,5,1000)
    print(value)




