# Jammy

Backpack loaded with tools for hacking, finding vulnerabilities, cracking passwords, and more..

> [!WARNING]
> **BEFORE PROCEEDING**<br><br>
> You must follow local laws when using these tools, misusing them could lead to legal trouble.<br>
> Always ensure you have explicit permission to hack, exploit or damage the device,<br>
> the author is not responsible for any damage caused by Jammy.

# Requirements

- WiFi adapter supporting monitor mode and frame injection (e.g. ALFA AWUS036XX/X, Tp-Link wn722n)
- Internal or external Bluetooth adapter
- Best with Kali Linux/ParrotOS (and any other linux distribution)
- For HID section to work you might need to have a: https://github.com/FLOCK4H/NeoDucky
- For the P*ishing section to work install: https://github.com/Bhaviktutorials/shark (cd shark && sudo bash setup)

# Setup

## Install required python libraries
```
  $ pip install pybluez 
```
<details>
<summary>Click to expand the troubleshoot section for this step</summary>

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
</details>

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
