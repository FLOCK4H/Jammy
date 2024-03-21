# Jammy

Collection of tools and self-made scripts that aims to serve as a fully fledged pentesting suite

# Requirements

- WiFi adapter supporting monitor mode and frame injection 
- Internal or external Bluetooth adapter
- Best with Kali Linux/ParrotOS (or any other linux distribution)

# Setup

## Install required libraries
```
  $ pip install pybluez 
```
If for any reason pybluez fails to install, please follow the process below:
```
  $ git clone https://github.com/pybluez/pybluez.git
  $ cd pybluez
  $ sudo apt-get install libbluetooth-dev

  $ sudo python setup.py build
  $ sudo python setup.py install
```
If for any reason the above commands fail, then try:
```
  $ sudo python setup.py install_lib
  $ sudo python setup.py install
```
## Install necessary tools
```
  $ sudo apt update
  $ sudo apt-get install mdk4 wifite aircrack-ng eaphammer
```

# Usage

```
  $ cd jammy
  $ sudo python jammy
```

![image](https://github.com/FLOCK4H/Jammy/assets/161654571/e13c7308-a2dc-4f26-bde0-8db469e23412)



# DISCLAIMER
_The author is not responsible for any illegal, unauthorized or unethical use of the program. 
Always ensure you have the legal rights to conduct vulnerability testing. Jammy is like a drawer, with all the tools easily accessible.
Misuse of Jammy may result in legal consequences, and users are expected to comply with all applicable regulations and standards._ 
