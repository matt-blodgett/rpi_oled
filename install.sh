python3 -m venv venv
. ./venv/bin/activate

sudo pip3 install adafruit-circuitpython-ssd1306
# sudo apt install python3-pil
sudo pip3 install Pillow

# Check display is active
sudo i2cdetect -y 1

#     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
#00:          -- -- -- -- -- -- -- -- -- -- -- -- --
#10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
#40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#70: -- -- -- -- -- -- -- --
