# Crossbar.io IoT Starterkit - Buzzer

Piezo buzzer component for acoustic warning or notification.

1. [Overview](#overview)
2. [How to run](#how-to-run)
3. [API](#api)

*Tags:* Python, GPIO, output, buzzer

---

## Overview

This component exposes the piezo buzzer built into the Crossbar.io IoT Starterkit via a WAMP component. This can then be used as a acoustic warning or notification device within a WAMP-based application.

The Crossbar.io IoT Starterkit has a built in piezo buzzer connected to GPIO 16 (Pin 36) with active high. (Nothing else special about this connection.)

The component is written in Python using Autobahn|Python running on Twisted. The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.


## How to run

Run the buzzer component on the Pi following **[this procedure](https://github.com/crossbario/iotcookbook/tree/master/device/pi/components#how-to-run)**:

```console
cd iotcookbook/device/pi/component/buzzer
make start
```

Here is how that looks:

[![asciicast](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78.png)](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78)

(and it may take a while on first start as the necessary Docker image is downloaded).

Then open this URL:

* [https://demo.crossbar.io/iotcookbook/device/pi/recipes/buzzer](https://demo.crossbar.io/iotcookbook/device/pi/recipes/buzzer)

in your browser.

The control page will ask you for the serial number of your Pi. This is being put out as part of the component startup logging, or you can do `grep Serial /proc/cpuinfo` and drop any leading zeros.

> Alternatively, you can construct the URL for direct access by adding '?serial=41f4b2fb' to its end, where you replace '41f4b2fb' with the serial of your Pi.

You should then see a Web page with buttons to control the piezo buzzer on your Pi. Pressing a button on the Web page will issue a WAMP remote procedure call to the `beep()` procedure exposed by the buzzer component running on the Pi.

This demonstrates secure remote procedure calls from any browser based device to an embedded device running a Python/Docker component and possibly behind firewalls and NATs.

> The buttons ("caller") and buzzers ("callees") of course can be required to be authenticated as well as authorized in production.


## API

The component uses an URI prefix containing the Pi serial number

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer`

eg the Pi with serial no. `41f4b2fb` will use URIs starting with

* `io.crossbar.demo.iotstarterkit.41f4b2fb.buzzer`


### Procedures

#### beep

To trigger a beeping sound sequence, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.beep(count, on, off)`

with (positional) parameters

* `count`: Number of beeps, default `1`.
* `on`: ON duration in ms, default `30`.
* `off`: OFF duration in ms, default `80`.

#### is_beeping

To check whether the buzzer is currently beeping, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.is_beeping()`

The procedure takes no parameters and returns a single positional result with a boolean flag.

#### welcome

To play a whole welcome beeping sequence, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.welcome()`

The procedure takes no parameters.


### Events

#### on_beep_started

The component will emit an event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_started(..)`

with keyword-based parameters:

* `count`: Number of beeps in the started sequence.
* `on`: ON duration in ms in the started sequence.
* `off`: OFF duration in ms in the started sequence.

#### on_beep_ended

When the current beeping sequence is finished, the component will emit en event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_ended()`


### Errors

When a beeping sequence is currently playing, calling `beep()` will raise an error:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.already-beeping()`
