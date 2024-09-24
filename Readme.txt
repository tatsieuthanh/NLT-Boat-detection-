--- Place name for usb ---
lsusb
udevadm info --name=/dev/ttyUSB0 --attribute-walk  
sudo nano /etc/udev/rules.d/99-com.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="modbus", MODE="0666"
sudo udevadm control --reload-rules
sudo udevadm trigger
ls -l /dev/modbus 

sudo apt install python3-rpi.gpio

sudo docker ps -a
sudo docker exec -it e8e893a6cfd7 /bin/bash
sudo docker logs 7d496733564f
sudo docker run -it 7cbafa4ad53b /bin/bash
sudo docker stop 7cbafa4ad53b


git init
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --list
touch .gitignore

git add .
git commit -m "new commit"
