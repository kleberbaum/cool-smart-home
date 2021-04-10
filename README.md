<p align="center">
  <a href="https://snek.at/" target="_blank" rel="noopener noreferrer">
    <img src="https://user-images.githubusercontent.com/26285351/114187769-a8958b80-9948-11eb-9580-d5421fbfd579.png" alt="SNEK Logo" height="150">
  </a>

</p>

<h3 align="center">SNEK - IoT Controller</h3>

<p align="center">
  This is the official repository for the smart home projects of SNEK.
  <br>
  <br>
  <a href="https://github.com/kleberbaum/smart-home/issues/new?template=bug_report.md">Report bug</a>
  ·
  <a href="https://github.com/kleberbaum/smart-home/issues/new?template=feature_request.md">Request feature</a>
</p>

## Table of contents

- [Table of contents](#table-of-contents)
- [Quick start](#quick-start)
- [Setup with Docker](#setup-with-docker)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Debugging](#debugging)
- [Setup with Python Virtual Environment](#setup-with-python-virtual-environment)
  - [Dependencies](#dependencies-1)
  - [Installation](#installation-1)
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Contributing](#contributing)
- [Versioning](#versioning)
- [Device Setup](#device-setup)
- [Mqtt](#mqtt)
- [REST](#rest)
- [ESPHome](#esphome)
- [Creators](#creators)
- [Thanks](#thanks)
- [Copyright and license](#copyright-and-license)

## [](#quick-start)Quick start

Several quick start options are available:

-   [Docker](#setup-with-docker)
-   [Python Virtual Environment](#setup-with-python-virtual-environment)

## [](#setup-with-docker)Setup with Docker

### Dependencies

-   [Docker](https://docs.docker.com/engine/installation/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

Run the following commands:

```bash
git clone https://gitlab.htl-villach.at/kleberf/smarthome.git
cd IoT-Controller
docker-compose up --build -d
docker-compose up
```

The demo site will now be accessible at <http://localhost:8000/>.

**Important:** This `docker-compose.yml` is configured for local testing only, and is _not_ intended for production use.

### Debugging

To tail the logs from the Docker containers in realtime, run:

```bash
docker-compose logs -f
```

## [](#setup-with-python-virtual-environment)Setup with Python Virtual Environment

You can start a Wagtail project from this template without setting up Docker and simply use a virtual environment,
which is the [recommended installation approach](https://docs.python.org/3/library/venv.html) for all Python projects itself.

### Dependencies

-   Python 3.5, 3.6 or 3.7

### Installation

With [PIP](https://github.com/pypa/pip) installed, run:

    git clone https://github.com/snek-at/wagtail-template.git
    cd Wagtail-Template
    python --version
    python -m pip --version

Confirm that this is showing a compatible version of Python 3.x. If not, and you have multiple versions
of Python installed on your system, you may need to specify the appropriate version when creating the venv:

    python3 -m venv /path/to/new/virtual/environment

Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s
binary directory. The invocation of the script is platform-specific (<venv> must be replaced by the path of the
directory containing the virtual environment):

| Platform | Shell      | Command to activate virtual environment |
| :------- | :--------- | :-------------------------------------- |
| Posix    | bash/zsh   | \$ source <venv>/bin/activate      |
|          | fish       | \$ . <venv>/bin/activate.fish      |
|          | csh/tcsh   | \$ source <venv>/bin/activate.csh  |
| Windows  | cmd.exe    | C:> <venv>\\Scripts\\activate.bat       |
|          | PowerShell | PS C:> <venv>\\Scripts\\Activate.ps1    |

Now we're ready to set up the project itself:

    pip install -r requirements/base.txt

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py runserver
    
## [](#bug-and-feature-requests)Bugs and feature requests

Have a bug or a feature request? Please first search for existing and closed issues. If your problem or idea is not
addressed yet, [please open a new issue](https://github.com/snek-at/wagtail-template/issues/new/choose).

## [](#contributing)Contributing

![GitHub last commit](https://img.shields.io/github/last-commit/snek-at/wagtail-template)
![GitHub issues](https://img.shields.io/github/issues-raw/snek-at/wagtail-template)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/snek-at/wagtail-template?color=green)

Please read through our
[contributing guidelines](https://github.com/snek-at/wagtail-template/blob/master/CONTRIBUTING.md). Included are
directions for opening issues, coding standards, and notes on development.

All code should conform to the [Code Guide](https://github.com/snek-at/tonic/blob/master/STYLE_GUIDE.md), maintained by
[SNEK](https://github.com/snek-at).

## [](#versioning)Versioning

For transparency into our release cycle and in striving to maintain backward compatibility, this repository is
maintained under [the Semantic Versioning guidelines](https://semver.org/). Sometimes we screw up, but we adhere to
those rules whenever possible.

## [](#device-setup)Device Setup

### Tuya Lightbulb

Prerequisite
- Raspberry Pi 3 or 4 
- ESP8266 based Tuya Lightbulb
- Smartphone
- ESPHome dashboard

The Raspberry Pi should be set up with a Debian based distro. In this guide I will use Hypriot: https://blog.hypriot.com/downloads/
The Image can be flashed onto an micro SD cart with Rufus: https://rufus.ie/en_US/

Get your Raspberry Pi IP from the DHCP leases of Router.
![chrome_2021-04-10_03-40-08](https://user-images.githubusercontent.com/26285351/114254265-9d754680-99ae-11eb-9fe8-12032e5fbe75.png)

```bash
ssh pirate@$yourRaspberryPiIP # The default password is "hypriot"
sudo -i
apt update
apt dist-upgrade
apt install git
git clone https://github.com/ct-Open-Source/tuya-convert.git
```
```bash
cd tuya-convert/
./install_prereq.sh
./start_flash.sh
```
Connect your smartphone to vtrust-flash. And put your lightbulb in pairing mode by truning it on-off 3 times in a row.
![image](https://user-images.githubusercontent.com/26285351/114254629-cf87a800-99b0-11eb-9477-00ee0b92663b.png)

The existing Tuya firmware is backuped and can be restored at anytime.
![image](https://user-images.githubusercontent.com/26285351/114254656-f47c1b00-99b0-11eb-9855-72ed05d9188f.png)

Last but not least choose the firmware. In this guide I will use **2** tasmota.bin.
![image](https://user-images.githubusercontent.com/26285351/114254993-ea5b1c00-99b2-11eb-8570-3537169d15cd.png)

Lern more about Tasmota at https://github.com/arendst/Tasmota

Congratulations! After under 10 minutes we sucsessfully flashed our bulb with Tasmota.
![image](https://user-images.githubusercontent.com/26285351/114255296-d44e5b00-99b4-11eb-9129-d73e0a263009.png)

We can now proceed by configuring the wifi settings of our lightbulb, by connecting to the Tasmota configuration hotspot.
![image](https://user-images.githubusercontent.com/26285351/114255768-af0e1c80-99b5-11eb-80e0-3b86ca0c188b.png)


Next we have to enter our ESPhome dashboard to configure our lightbulb 




After Configuration the Lightbulb can be found in the DHCP leases of your Router. We are now able to compile our firmware in Tasmota and flash it on oure lightbulb in the Tasmota webinterface. 
![image](https://user-images.githubusercontent.com/26285351/114256397-4aed5780-99b9-11eb-8549-d243ad8705a2.png)

![image](https://user-images.githubusercontent.com/26285351/114255946-fe088180-99b6-11eb-91ae-ad629613acd5.png)
![image](https://user-images.githubusercontent.com/26285351/114256436-8daf2f80-99b9-11eb-9393-4b303cb25c1c.png)




## [](#mqtt)Mqtt




## [](#rest)REST

## [](#esphome)ESPHome

## [](#creators)Creators

<table border="0">
    <tr>
        <td>
    	    <a href="https://github.com/kleberbaum">
    	        <img src="https://avatars.githubusercontent.com/kleberbaum?s=100" alt="Avatar kleberbaum">
            </a>
        </td>
    </tr>
    <tr>
        <td><a href="https://github.com/kleberbaum">Florian Kleber</a></td>
    </tr>
</table>

## [](#thanks)Thanks

We do not have any external contributors yet, but if you want your name to be here, feel free
to [contribute to our project](#contributing).

## [](#copyright-and-license)Copyright and license

![GitHub repository license](https://img.shields.io/badge/license-EUPL--1.2-blue)

SPDX-License-Identifier: (EUPL-1.2)
Copyright © 2019-2020 Simon Prast
