# Gramik

[🇬🇧 EN](README.md) | [🇨🇿 CZ](README.cs.md)

## Intro
Our little daughter enjoys music. When she was just a few months old, she received the book "[My First Mozart](https://www.axioma.cz/obchod/muj-prvni-mozart/)," which kept her entertained for countless hours. This was followed by books like "[My Little Beethoven](https://www.svojtka.cz/muj-maly-beethoven/)" or "[Rock and Roll, Baby!](https://www.axioma.cz/obchod/rokenrol-bejby-2/)." Once, we had a Chuck Berry record playing on our turntable at home. It was right around the time our daughter had just learned to walk. She stood up, leaned on the record table, and happily started shaking her hips. Around that time, the idea for the "Gramík Project" began to form in my head. The project went through several iterations—from a prototype made of ready-made modules on a breadboard, to the first PCB design with the thought of giving it some form, and finally to the current version, which I felt I could release and make available to everyone.

My main idea was to create a simple music box with a few buttons that would recognize what playlist or folder to play when a certain medium is placed on it and a button is pressed. The choice of identification medium fell on RFID chips, with an easily available and inexpensive RFID reader on the Gramík side. The first prototype was built using an ESP8266 and an MP3 module, which worked nicely, but I wanted the whole solution to be more compact, so I iterated to the version with a Raspberry Pi on a PCB.

| | | |
| ------------------------- | ------------------------- | ------------------------- |
| ![](/imgs/gramik_03.webp) | ![](/imgs/gramik_03_2.webp) | ![](/imgs/gramik_03_pcb2.webp) |

## Implementation

### Raspberry PI Pico + CircuitPython
1. [Install CircuitPython on Raspberry Pi Pico](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)
2. [If you are using OSX, you might encounter an issue when writing new files](https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting#macos-sonoma-before-14-dot-4-disk-errors-writing-to-circuitpy-3160304)
3. Copy the code from the `/src/circuitpython/` directory of the repository to your Raspberry Pi Pico.

### Preparing Your Own Music and "gramophone discs"
Prepare an SD card and create any number of directories in its root, where each directory will represent one playable "gramophone disc." The directory names are not important, but I recommend keeping them in alphabetical order, as this is the order in which the directories will be registered to the RFID tag IDs.

In the original design, Gramík has 5 buttons, each representing 5 mp3 files within a directory. Once your music is ready, insert the SD card into the slot and start Gramík. Get your RFID tags/stickers/cards ready. Place each RFID tag on the reader and press any button. At this point, the tag's ID is read, and the first directory on the SD card that doesn't match the format in which this ID is encoded will be found. The directory will then be renamed to match this format. This process assigns the tag to a specific directory containing music. From now on, when this tag is placed on the reader, pressing one of the five buttons will play one of the five mp3 files from the corresponding directory.

## Variants
This project and repository should primarily serve as inspiration. Gramík as such can be freely modified. Merge requests and issues are welcome.

### Primary design
You can use the proposed circuit board according to the attached Gerber file in the repository, or alternatively, use your preferred ready-made modules.

- Raspberry PI Pico - [rpishop.cz](https://rpishop.cz/raspberry-pi-pico/5117-raspberry-pi-pico.html) | [Official store](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- TP4056 charging module - [Laskakit](https://www.laskakit.cz/nabijecka-li-ion-clanku-tp4056-s-ochranou-usb-c/) | [Aliexpress](https://www.aliexpress.com/item/1005006307081697.html)
- RC522 RFID reader (ideally a mini version) - [Laskakit](https://www.laskakit.cz/rfid-ctecka-s-vestavenou-antenou-mfrc-522-rc522/) | [Aliexpress](https://www.aliexpress.com/item/1005005762707655.html)
- SD card module - [Laskakit](https://www.laskakit.cz/sd-card-modul-spi/) | [Aliexpress](https://www.aliexpress.com/item/1005005302035188.html)
- Buttons - [Laskakit](https://www.laskakit.cz/laskkit-sada-25-tlacitek-12x12x7-3mm-s-knofliky/) | [Aliexpress](https://www.aliexpress.com/item/1005007078128171.html)
- Velcro (circles) - [sevt.cz](https://www.sevt.cz/produkt/suchy-zip-samolepici-kolecka-%C3%B810-mm-63-ks-bila-25041963416) | [Aliexpress](https://www.aliexpress.com/item/1005007177045435.html)
- RFID 13,56 Mhz card or sticker - [Laskakit](https://www.laskakit.cz/rfid-13-56mhz-karta/) | [Aliexpress](https://www.aliexpress.com/item/1005003477760991.html)
- LiPol battery - [Laskakit](https://www.laskakit.cz/baterie-li-po-3-7v-1500mah-lipo/)
- 3D printer 🙂

### Alternative 1
- ESP8266 (any, for example, Wemos D1 mini) - [Laskakit](https://www.laskakit.cz/wemos-d1-mini-esp8266-wifi-modul/) | [Aliexpress](https://www.aliexpress.com/item/1005005658563136.html)
- Mini MP3 player - [Laskakit](https://www.laskakit.cz/audio-mini-mp3-prehravac/) | [Aliexpress](https://www.aliexpress.com/item/1005005656568976.html)
- Wemos D1 battery shield - [Laskakit](https://www.laskakit.cz/wemos-d1-mini-lithium-battery-shield-2) | [Aliexpress](https://www.aliexpress.com/item/1005005687704614.html)
- RC522 RFID reader (ideally a mini version) - [Laskakit](https://www.laskakit.cz/rfid-ctecka-s-vestavenou-antenou-mfrc-522-rc522/) | [Aliexpress](https://www.aliexpress.com/item/1005005762707655.html)
- Buttons - [Laskakit](https://www.laskakit.cz/laskkit-sada-25-tlacitek-12x12x7-3mm-s-knofliky/) | [Aliexpress](https://www.aliexpress.com/item/1005007078128171.html)
- Velcro (circles) - [sevt.cz](https://www.sevt.cz/produkt/suchy-zip-samolepici-kolecka-%C3%B810-mm-63-ks-bila-25041963416) | [Aliexpress](https://www.aliexpress.com/item/1005007177045435.html)
- RFID 13,56 Mhz card or sticker - [Laskakit](https://www.laskakit.cz/rfid-13-56mhz-karta/) | [Aliexpress](https://www.aliexpress.com/item/1005003477760991.html)
- LiPol battery - [Laskakit](https://www.laskakit.cz/baterie-li-po-3-7v-1500mah-lipo/)

## Assets

- `disc-images` - cover images for your discs (you can print 65mm diameter discs on a 3D printer from the included STL file).
- `mc-images` - cover images that resemble an audio cassette, for a standard access card.
- `stl` - contains a case that fits the included circuit board from the gerber directory and a 55mm disc representing a vinyl record.
- `gerber` - contains the PCB for manufacturing.
- `schema` - the primary schematic, which can be used to produce Gramík.

## TODOs and ideas
- Better power consumption - turning off the RFID module.
- Volume control.
- Add the option for audio output to a jack connector.
- Improve the case design - especially for the speaker and the power switch.

## Handy commands
```
for F in $(ls .); do ffmpeg -i "$F" -map 0:a:0 -ar 24000 -ab 64000 -ac 1 "C_$F"; done;
```

## Do you like it?

☕️ Do you like the project or has it inspired you? Buy me a coffee.

- [Buy me a Coffee](https://buymeacoffee.com/gramik)
- **BTC:** bc1qw77ty492cph4hqw4rhyege9garkkel96jr332y

## Links

- [x.com/jirikupka](https://x.com/jirikupka)