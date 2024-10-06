# Gramik

[🇬🇧 EN](README.md) | [🇨🇿 CZ](README.cs.md)

## Úvodem
Naši malou dceru baví hudba. Když měla pár měsíců, dostala knížku "[Můj první Mozart](https://www.axioma.cz/obchod/muj-prvni-mozart/)", která ji zabavila na nespočet hodin. Pokračovalo to knihami jako "[Můj malý Beethoven](https://www.svojtka.cz/muj-maly-beethoven/)" nebo "[Rokenrol, bejby!](https://www.axioma.cz/obchod/rokenrol-bejby-2/)". Jednou jsme měli doma puštěný gramofon s deskou Chucka Berryho. Bylo to těsně po tom, co se dcera naučila chodit. Postavila se, opřela se o gramofonový stolek a vesele začala kroutit zadkem. Někdy v té době se mi pomalu začal v hlavě rodit nápad na "Projekt Gramík." Projekt prošel několika iteracemi – od prototypu z hotových modulů na breadboardu, přes první návrh PCB s myšlenkou, že tomu dám nějakou formu, až po současnou verzi, u které jsem si řekl, že bych ji mohl vydat a zpřístupnit všem.

Moje hlavní myšlenka byla sestavit jednoduchou hudební krabičku, která bude mít pár tlačítek a pomocí nějakého media, které se na ni přiloží, krabička rozezná, jaký playlist či složku má po stisknutí tlačítka přehrát. Volba idetifikačního média padla na RFID čipy a na straně Gramíku na snadno dostupnou a levnou RFID čtečku. První prototyp byl postaven na ESP8266 a MP3 modulu, což fungovalo pěkně, ale celé řešení jsem chtěl mít víc kompaktní a tak jsem doiteroval až k variantě s Raspberry PI na PCB.

| | | |
| ------------------------- | ------------------------- | ------------------------- |
| ![](/imgs/gramik_03.webp) | ![](/imgs/gramik_03_2.webp) | ![](/imgs/gramik_03_pcb2.webp) |

## Implementace

### Raspberry PI Pico + CircuitPython
1. [Nainstalujte CircuitPython do Raspberry PI Pico](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)
2. [Pokud používáte OSX, pravděpodobně budete mít problém se zápisem nových souborů](https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting#macos-sonoma-before-14-dot-4-disk-errors-writing-to-circuitpy-3160304)
3. Zkopírujte kód z adresáře repozitáře `/src/circuitpython/` do vašeho Raspberry PI Pico.

### Příprava vlastní hudby a "desek"
Připravte si SD kartu a v rootu vytvořte libovolný počet adresářů, kde každý adresář bude reprezentovat jednu přehrátelnou "desku". Název adresáře není podstatný, ale doporučuji je mít v abecední pořadí, protože v tomto pořadí pak bude probíhat registrace adresáře na ID RFID tagu.

Gramík má v původním návrhu 5 tlačítek, které reprezentují 5 mp3 souborů v rámci jednoho adresáře. Pokud máte hudbu připravenou ([pozor na maximální kvalitu](https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3#circuitpython-compatible-mp3-files-3101249)), vložte kartu do SD slotu a spusťte Gramík. Připravte si své RFID tagy/nálepky/karty. Každý RFID tag přiložte ke čtečce a stiskněte libovolné tlačíko. V tuhle chvíli se přečte ID tagu a vyhledá se první adresář na SD kartě, který neodpovídá formátu, ve kterém je toto ID zakódováno. Adresář se přejmenuje, aby tomuto formátu odpovídal. Tímto jsme přiřadili tag konkrétnímu adresáři s hudbou. Od teď, pokud bude na čtečce přiložený tento tag, po stisku jednoho z pěti tlačítek, se bude přehrávat jedna z pěti mp3 z daného adresáře.

## Možné varianty
Tento projekt a repozitář slouží především jako inspirace a Gramík jako takový je možné si libovolně modifikovat. Merge requesty a issues jsou vítány.

### Primární návrh
Můžete využít navržený plošný spoj dle přiloženého gerber file v repozitáři, případně využít oblíbených hotových modulů.

- Raspberry PI Pico - [rpishop.cz](https://rpishop.cz/raspberry-pi-pico/5117-raspberry-pi-pico.html) | [Official store](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- Nabíjecí modul TP4056 - [Laskakit](https://www.laskakit.cz/nabijecka-li-ion-clanku-tp4056-s-ochranou-usb-c/) | [Aliexpress](https://www.aliexpress.com/item/1005006307081697.html)
- RC522 RFID reader (ideálně mini varianta) - [Laskakit](https://www.laskakit.cz/rfid-ctecka-s-vestavenou-antenou-mfrc-522-rc522/) | [Aliexpress](https://www.aliexpress.com/item/1005005762707655.html)
- Modul SD karty - [Laskakit](https://www.laskakit.cz/sd-card-modul-spi/) | [Aliexpress](https://www.aliexpress.com/item/1005005302035188.html)
- Tlačítka - [Laskakit](https://www.laskakit.cz/laskkit-sada-25-tlacitek-12x12x7-3mm-s-knofliky/) | [Aliexpress](https://www.aliexpress.com/item/1005007078128171.html)
- Suchý zip (samolepící kolečka) - [sevt.cz](https://www.sevt.cz/produkt/suchy-zip-samolepici-kolecka-%C3%B810-mm-63-ks-bila-25041963416) | [Aliexpress](https://www.aliexpress.com/item/1005007177045435.html)
- RFID 13,56 Mhz karta nebo nálepka - [Laskakit](https://www.laskakit.cz/rfid-13-56mhz-karta/) | [Aliexpress](https://www.aliexpress.com/item/1005003477760991.html)
- LiPol Baterie - [Laskakit](https://www.laskakit.cz/baterie-li-po-3-7v-1500mah-lipo/)

### Alternativa 1
- ESP8266 (libovolně, například Wemos D1 mini) - [Laskakit](https://www.laskakit.cz/wemos-d1-mini-esp8266-wifi-modul/) | [Aliexpress](https://www.aliexpress.com/item/1005005658563136.html)
- Mini MP3 player - [Laskakit](https://www.laskakit.cz/audio-mini-mp3-prehravac/) | [Aliexpress](https://www.aliexpress.com/item/1005005656568976.html)
- Wemos D1 battery shield - [Laskakit](https://www.laskakit.cz/wemos-d1-mini-lithium-battery-shield-2) | [Aliexpress](https://www.aliexpress.com/item/1005005687704614.html)
- RC522 RFID reader (ideálně mini varianta) - [Laskakit](https://www.laskakit.cz/rfid-ctecka-s-vestavenou-antenou-mfrc-522-rc522/) | [Aliexpress](https://www.aliexpress.com/item/1005005762707655.html)
- Tlačítka - [Laskakit](https://www.laskakit.cz/laskkit-sada-25-tlacitek-12x12x7-3mm-s-knofliky/) | [Aliexpress](https://www.aliexpress.com/item/1005007078128171.html)
- Suchý zip (samolepící kolečka) - [sevt.cz](https://www.sevt.cz/produkt/suchy-zip-samolepici-kolecka-%C3%B810-mm-63-ks-bila-25041963416) | [Aliexpress](https://www.aliexpress.com/item/1005007177045435.html)
- RFID 13,56 Mhz karta nebo nálepka - [Laskakit](https://www.laskakit.cz/rfid-13-56mhz-karta/) | [Aliexpress](https://www.aliexpress.com/item/1005003477760991.html)
- LiPol Baterie - [Laskakit](https://www.laskakit.cz/baterie-li-po-3-7v-1500mah-lipo/)

## Adresáře projektu

- `disc-images` - cover obrázky pro vaše desky (desky o průměru 65mm si můžete vytisknout na 3D tiskárně z přiloženého stl).
- `mc-images` - cover obrázky, které vypadají jako audio kazeta, pro standardní přístupovou kartu.
- `stl` - obsahuje krabičku, do které sedí přiložený plošný spoj z `gerber` adresáře a 55mm kotouč reprezentující gramofonovou desku.
- `gerber` - obsahuje plošný spoj k výrobě.
- `schema` - primární schéma, pomocí kterého je možné Gramík vyrobit.

## TODOs a nápady
- Lepší spotřeba - vypínání rfid modulu.
- Ovládání hlasitosti.
- Přidat možnost audio výstupu do jack konektoru.
- Vylepšit design krabičky - hlavně reproduktoru a přepínače pro zapnutí.

## Užitečné příkazy
```
for F in $(ls .); do ffmpeg -i "$F" -map 0:a:0 -ar 24000 -ab 64000 -ac 1 "C_$F"; done;
```

## Líbí se vám tento projekt?

☕️ Líbí se vám projekt nebo vás inspiroval? Kupte mi kafe.

- [Buy me a Coffee](https://buymeacoffee.com/gramik)
- **BTC:** bc1qw77ty492cph4hqw4rhyege9garkkel96jr332y

## Odkazy jinam

- [x.com/jirikupka](https://x.com/jirikupka)