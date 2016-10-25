# WeatherStation

These are the scripts that power my Raspberry Pi weather station. Eventually this will be a web-server powering a web-app.  Now, it writes to a google sheet.

To hook up the BMP 180 and download the Python library:

https://thepihut.com/blogs/raspberry-pi-tutorials/18025084-sensors-pressure-temperature-and-altitude-with-the-bmp180

sudo apt-get update
sudo apt-get install git build-essential python-dev python-smbus 
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install

To hook up the DHT22 and download the Python library:

https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
    
