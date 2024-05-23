<div align="center">
  <img src="https://flockahh.b-cdn.net/jammy.svg" width="256" alt="Jammy logo" />
</div>

# Jammy

Backpack loaded with tools for hacking, finding vulnerabilities, cracking passwords, phishing, network auditing, network pentesting, bluetooth/ble spammers, and way more..

> [!TIP]
> It's better to stay away from any trouble. **Pentesting** must be conducted, by following the local, and ethical guidelines.

# Requirements

- WiFi adapter supporting monitor mode and frame injection (e.g. ALFA AWUS036XX/X, Tp-Link wn722n)
- Internal or external Bluetooth adapter
- Best with Kali Linux/ParrotOS (and any other linux distribution)
- For HID section to work you might need to have a: https://github.com/FLOCK4H/NeoDucky
- For the P*ishing section to work install: https://github.com/Bhaviktutorials/shark (cd shark && sudo bash setup)

# Setup

<strong>1. Install required python libraries</strong>
```
  $ pip install pybluez 
```
<details>
<summary><strong>Click to expand the troubleshoot section for this step</strong></summary>

<br>

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

<strong>2. Install necessary tools</strong>

```
  $ sudo apt update
  $ sudo apt-get install mdk4 wifite aircrack-ng eaphammer
```

<strong>3. Install Jammy</strong>

**Clone Jammy**

```
  $ git clone https://github.com/FLOCK4H/Jammy
```

**Change directory into Jammy**

```
  $ cd Jammy
```

**Run the setup file**

```
  # This will find the setup.py file by itself
  $ sudo pip install .
```

# Usage

```
  $ sudo Jammy
```

Or with additional arguments to skip CLI questions partially or completely:

```
  $ sudo Jammy -i wlan1 -a slowloris
```

The '-a' argument has to be the same as the name or number as is in the CLI, when you are in the **Jammy's** menu.

> Example commands:
> b - beacon flood, a - auth attack, p - probe requests spam, d - deauth attack, f - packet fuzzer, wifite - wifite, wificap - monitors and stores to a .cap file, rage - target DoS, watchspam - implementation of samsung watch spam, shark - run phishing tool, et - evil twin attack

# Credits

Authors of: 

- Blueducky

&emsp;**saad0x1** - https://github.com/saad0x1

&emsp;**pentestfunctions** - https://github.com/pentestfunctions

- Shark - **Bhaviktutorials** (https://github.com/Bhaviktutorials)

- mdk - https://github.com/aircrack-ng/mdk4

- eaphammer - https://github.com/s0lst1c3/eaphammer

- wifite - https://github.com/derv82/wifite2

- hashcat - https://github.com/hashcat/hashcat
