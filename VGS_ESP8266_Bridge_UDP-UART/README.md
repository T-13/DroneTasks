Transparent UDP to UART bridge for ESP8266 (ESP-01 with 1MB flash) using MicroPython.

### Setup

- Flash MicroPython to ESP8266 module
  - Download [MicroPython for ESP8266](http://micropython.org/download#esp8266)
  - Download [esptool](https://github.com/espressif/esptool)
  - Connect ESP8266 pins: `GPIO0` -> `DTR` and `RESET` -> `RTS` (on USB-to-TTL module for example) to enable Automatic Bootloader
  - Run `$ esptool erase_flash`
  - Run `$ esptool write_Flash 0x0 esp8266-<date>-v<version>.bin`
  - Disconnect `GPIO0` and `RESET` pins
- Configure UDP and UART details in `main.py`
- Upload `main.py` to the file system
  - Download [ampy](https://github.com/pycampers/ampy)
  - Run `$ ampy --port <port> put main.py` (replace `<port>` with connected TTY/COM port)
- Reboot ESP8266 module
