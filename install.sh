python3 -m venv venv
. ./venv/bin/activate

sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil


# Check display is active
sudo i2cdetect -y 1