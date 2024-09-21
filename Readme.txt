--- Place name for usb ---
lsusb
udevadm info --name=/dev/ttyUSB0 --attribute-walk  
sudo nano /etc/udev/rules.d/99-com.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="modbus", MODE="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger
ls -l /dev/modbus 