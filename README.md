raspi-config

Interface options, I2C, enable. Reboot

apt update


apt install python3-pip python3-rpi.gpio python3-pil i2c-tools

pip3 install luma.oled


Create a config.py with your preferred config, then run:

python3 main.py
