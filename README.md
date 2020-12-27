# Vintage M40 Radio Music Player
Repo of documents and code used for the Mediator M40 Radio upgrade

## Mediator M40 Radio

<img src="img/Mediator_M40_original.jpg" width="600"><img src="img/Mediator_M40_inside_original.jpg" width="600">

The [Mediator M40](adiomuseum.org/r/mediator_40a.html) radio is a tube radio manufactured in the early 1940s by the Swiss Company [Mediator](https://www.radiomuseum.org/dsp_hersteller_detail.cfm?company_id=140) located in La Chaux-de-Fonds. The radio is identical to the [Philips Philette 206 A](https://www.radiomuseum.org/r/philips_philette_206a.html) made by Philips Switzerland. However it differs from the [Philips 206 A](https://www.radiomuseum.org/r/philips_206a206.html) produced in the Netherlands as it only has MW. 
My radio has a control mark sticker from the Swiss telecom PTT from 1941 on the back. 

- [Service Manual of the Philips 206 A 'Junior'](doc/Phillips_206_A_Junior.pdf)

## Upgrade
The radio is upgraded to a Webradio and Music Player using a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) and a [HifiBerry MiniAMP](https://www.hifiberry.com/shop/boards/miniamp/). The electrical components of the radio are very old and even if it seems that most of them still work, I decided to leave them in as is, but not to use them in the circuit. However I wanted to reuse the control knobs including the corresponding potentiometer and variable capacitor and the speaker.

## OS
The Linux based [volumio](https://volumio.org/) is used as OS and music player software, as it has nice features and works on the Raspberry Pi Zero. The [HifiBerryOS](https://www.hifiberry.com/hifiberryos/) does not work well on Pi Zero according their website. 

### Installation
[Download](https://volumio.org/get-started/) and install volumio according the [documentation](https://cdn.volumio.org/wp-content/uploads/2019/01/Quick-Start-Guide-Volumio.pdf). 

___Note___: When using the HifiBerry MiniAMP _HifiBerry DAC_ need to be selected as Playback Output Device. However make sure that _I2S DAC_ is not enabled.
### PowerSwitch
The original _'Waverange'_ switch of the radio is used as power switch. To allow a proper shutdown the [OnOff SHIM](https://shop.pimoroni.com/products/onoff-shim) by pimoroni is used. The OnOff SHIM is usually used with a button and not a switch, therefore I had to modify the clean-shutdown code to shutdwon, when the trigger is pulled high (Pull-Up) and not low.

### Volume Control
The original volume control knob is used for volume control. The potentiometer is connected to an [MCP3008](doc/MCP3008.pdf) A/D converter. The MCP3008 is connected to tha Raspberry Pi using the SPI interface. A [volume-control](src/volume-control) daemon is installed on the Pi ([src/analog_input/volume_daemon.py](src/analog_input/volume_daemon.py))

### Playlist/Radio Station Control
TBD