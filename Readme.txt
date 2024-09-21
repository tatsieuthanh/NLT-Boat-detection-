--- Place name for usb ---
lsusb
udevadm info --name=/dev/ttyUSB0 --attribute-walk   ==> usb
sudo nano /etc/udev/rules.d/99-com.rules
SUBSYSTEM=="ttyUSB0", ATTR{idVendor}=="1a86", ATTR{idProduct}=="7523", SYMLINK+="modbus", MODE="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger
ls -l /dev/modbus => lrwxrwxrwx 1 root root 15 Sep 21 04:11 /dev/modbus -> bus/usb/003/005