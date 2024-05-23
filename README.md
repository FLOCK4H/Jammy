<div align="center">
  <img src="https://flockahh.b-cdn.net/jammy.svg" width="256" alt="Jammy logo" />
</div>

# Jammy

Backpack loaded with tools for hacking, finding vulnerabilities, cracking passwords, phishing, network auditing, network pentesting, bluetooth/ble spammers, hid attacks, and way more..

> [!TIP]
> It's better to stay away from any trouble. **Pentesting** must be conducted, by following the local, and ethical guidelines.

# Requirements

- WiFi adapter supporting monitor mode and frame injection (e.g. ALFA AWUS036XX/X, Tp-Link wn722n)
- Internal or external Bluetooth adapter
- Best with Kali Linux/ParrotOS (and any other linux distribution)
- For HID section to work you might need to have a: https://github.com/FLOCK4H/NeoDucky
- For the P*ishing section to work install: https://github.com/Bhaviktutorials/shark (cd shark && sudo bash setup)

# Setup

<strong>1. Install required python libraries</strong><br />

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

<br />
<strong>2. Install necessary tools</strong><br />

```
  $ sudo apt update
  $ sudo apt-get install mdk4 wifite aircrack-ng eaphammer hostapd dnsmasq
```

<br />

<strong>3. Install Jammy</strong>
<br />

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

Now, from any path in the terminal, we are able to call Jammy:

```
  $ sudo Jammy
```

<br />

Or with additional arguments to skip CLI questions partially or completely:

```
  $ sudo Jammy -i wlan1 -a slowloris
```

<br />

The '-a' argument has to be the same as the name or number of the feature inthe CLI, so when you are in the **Jammy's** menu.

> Example commands:
> b - beacon flood, a - auth attack, p - probe requests spam, d - deauth attack, f - packet fuzzer, wifite - wifite, wificap - monitors and stores to a .cap file, rage - target DoS, watchspam - implementation of samsung watch spam, shark - run phishing tool, et - evil twin attack, 17 more..

<br />

If you did not install Jammy, you can still run via python:

```
  $ sudo python Jammy
  or
  $ sudo python Jammy -i wlan1 -a b
```

# Pentesting

> [!CAUTION]
> Some of the methods provided below, may vary in behavior and result. Always ensure, that you know what you are doing.

**1. WiFi**

**Evil Twin** - In order to perform the attack we must have the **eaphammer** installed. The setup file has added to its path a new template named google, which will serve as our credential harvest site. Make sure you have correct hostapd.conf in **/etc/hostapd/hostapd.conf**, which is a config file, then if we installed everything necessary, we can run the **eaphammer**, by running Jammy and getting into WiFi command line.

**MDK4** - is a framework for WiFi **Pentesting**, where you can use provided techniques: 
- a - Authentication DoS attack,
- b - Beacon Flood Attack,
- f - Packet Fuzzer,
- m - Michael Countermeasures Exploitation Attack (DoS),
- d - Deauthentication Attack (DoS)

**Monitor Tools** - running the `wificap` or `mon` we can sniff current **Network Environment** for packets, using airodump-ng or the Freeway suites. The `wificap` will save the output to the **.cap** file.

**wifite** - an exploitation framework, meant for beginners and professionals to stack every password capture method under one place. By running wifite we will be introduced to next part via the CLI.

**2. Bluetooth/ BLE**

**BLE Spam** - Spam Apple or Samsung advertisements, or disguise into Airpods, in order to confuse nearby devices, and display a notification pop up on any nearby Samsung (works for LG too) or Apple device. **May crash iOS upto 17.2**

**Redtooth** - author's implementation of the old&good `l2ping` DoS attack, this tool has a chance of crashing the bluetooth device.

**Bluefog** - author's implementation of the bluefog attack method, but instead of device fog (many advertisements) we just change name on BT adapter **very frequently**. It's a camouflage technique.

**BlueDucky** - exploitation framework, that turns any machine with bluetooth adapter, into **Bluetooth HID Keyboard** device, that you can write a payload for, and execute on other bluetooth device (like phone, laptop), in some cases without pairing.

**3. HID**

**NeoDucky** - NeoDucky is a **Rubber Ducky** device, that when properly configured, may inject malware, harvest data, jam keyboards, and more. Jammy has built-in support for turning NeoDucky on/off, uploading payloads and managing stealth mode. More on !(NeoDucky)[https://github.com/FLOCK4H/NeoDucky]

**4. Exploits**

**DDoS** - this exploit will send http requests using bots, along with headers in order to keep the target device busy. To run, just enter `rage` and provide IP address of a machine.

**Local DoS** - the `hping` is sufficient for home networks, not really suitable for online DoS, as we would need more machines. This is why, running Local DoS on most WiFi host IP, will result in `No Internet Connection`, because the packets we send are too large to process.

**Slowloris** - this attack creates sockets, initiates the connection, and never ends it. Effectively keeping the target threaded server busy.

**5. Phishing**

**shark** - Shark is a framework with 50+ phishing templates, we can find there google, facebook, whatsapp, camera hacks, mic hacks, and many others. Shark can be hosted on ngrok (need API token), or cloudflare (doesn't need anything).

**6. Cracking**

**Hashcat** - extremely popular tool used for password decryption, we must first capture the password packet (PMKID/ Handshake) in hashcat crackable format, we can do this using the !(Freeway)[https://github.com/FLOCK4H/Freeway], then just provide path to captured password file, and the wordlist.

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
