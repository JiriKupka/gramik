import os

import board
import sdcardio
import storage
import busio
import time
import digitalio
import mfrc522
import audiomp3
import audiopwmio
import alarm
import pwmio
import microcontroller
import traceback


class GramikConfig:
    SD_SCK = board.GP2
    SD_MOSI = board.GP3
    SD_MISO = board.GP4
    SD_CS = board.GP5
    SD_PATH = "/sd"

    BTN1 = board.GP20
    BTN2 = board.GP19
    BTN3 = board.GP18
    BTN4 = board.GP17
    BTN5 = board.GP16

    RFID_SCK = board.GP10
    RFID_MOSI = board.GP11
    RFID_MISO = board.GP12
    RFID_CS = board.GP13
    RFID_RESET = board.GP14
    RFID_ANTENNA_GAIN = 0x04 << 4

    AUDIO_PWM = board.GP1

    PROG_LED = board.GP9
    OMNI_BUTTON = board.GP21

    SLEEP_INACTIVITY_S = 180
    DIRNAME_PREFIX = "disc_"
    ERR_LOG_PATH = SD_PATH+"/error.log"


class Gramik:

    config = None
    buttons = []
    root_dirs = []
    mp3_playlist_for_dirs = {}
    mp3_decoder = None
    audio = None

    @staticmethod
    def configure(config):
        Gramik.config = config

        Gramik.init_audio()
        Gramik.init_sd()
        Gramik.init_buttons()
        Gramik.init_rfid()
        Gramik.refresh_dirs()
        Gramik.init_prog_led()

    @staticmethod
    def init_prog_led():
        Gramik.prog_led = pwmio.PWMOut(Gramik.config.PROG_LED)

    @staticmethod
    def init_audio():
        Gramik.audio = audiopwmio.PWMAudioOut(Gramik.config.AUDIO_PWM)

    @staticmethod
    def init_sd():
        c = Gramik.config
        spi = busio.SPI(c.SD_SCK, MOSI=c.SD_MOSI, MISO=c.SD_MISO)
        sd = sdcardio.SDCard(spi, c.SD_CS)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, c.SD_PATH)

    @staticmethod
    def init_buttons():
        c = Gramik.config

        for button_gpio in [c.BTN1, c.BTN2, c.BTN3, c.BTN4, c.BTN5]:
            button = digitalio.DigitalInOut(button_gpio)
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.DOWN
            Gramik.buttons.append(button)

    @staticmethod
    def init_rfid():
        c = Gramik.config

        Gramik.rfid = mfrc522.MFRC522(c.RFID_SCK, c.RFID_MOSI, c.RFID_MISO, c.RFID_RESET, c.RFID_CS)
        Gramik.rfid.set_antenna_gain(c.RFID_ANTENNA_GAIN)

    @staticmethod
    def refresh_dirs():
        Gramik.mp3_playlist_for_dir = {}
        Gramik.root_dirs = [dir_ for dir_ in os.listdir(Gramik.config.SD_PATH) if (os.stat(Gramik.config.SD_PATH+"/"+dir_)[0] & 0o40000 != 0) and not dir_.startswith(".")]

        for d in Gramik.root_dirs:
            dir_path = Gramik.config.SD_PATH+"/"+d
            Gramik.mp3_playlist_for_dir[d] = [dir_path+"/"+filename for filename in os.listdir(dir_path) if not filename.startswith(".")]

    @staticmethod
    def convert_uid_to_dirname(uid):
        return Gramik.config.DIRNAME_PREFIX+("_".join(map(str, uid)))

    @staticmethod
    def rename_root_dir_for_uid(uid):
        for dirname in Gramik.root_dirs:
            if not dirname.startswith(Gramik.config.DIRNAME_PREFIX):
                old_dir = "{0}/{1}".format(Gramik.config.SD_PATH, dirname)
                new_dir = "{0}/{1}".format(Gramik.config.SD_PATH, Gramik.convert_uid_to_dirname(uid))

                os.mkdir(new_dir)
                for f in os.listdir(old_dir):
                    os.rename("{0}/{1}".format(old_dir, f), "{0}/{1}".format(new_dir, f))
                os.rmdir(old_dir)

                break

        Gramik.refresh_dirs()

    @staticmethod
    def get_mp3_path(dirname, index):
        return Gramik.mp3_playlist_for_dir[dirname][index] if len(Gramik.mp3_playlist_for_dir[dirname]) > index else None

    @staticmethod
    def play_mp3_file(path):
        Gramik.audio.stop()
        f = open(path, "rb")

        if not Gramik.mp3_decoder:
            Gramik.mp3_decoder = audiomp3.MP3Decoder(f)
        else:
            Gramik.mp3_decoder.file = f

        Gramik.audio.play(Gramik.mp3_decoder)


    @staticmethod
    def turn_prog_led_on():
        Gramik.prog_led.duty_cycle = 2**10


    @staticmethod
    def run():
        Gramik.turn_prog_led_on()

        state_changed = False
        last_pressed_button_index = -1
        is_button_pressed = False
        start_time = None

        while True:

            if not Gramik.audio or not Gramik.audio.playing:
                if not start_time:
                    start_time = time.monotonic()
                if time.monotonic()-start_time > Gramik.config.SLEEP_INACTIVITY_S:
                    pin_alarm = alarm.pin.PinAlarm(pin=Gramik.config.OMNI_BUTTON, value=True, pull=True)
                    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)


            pressed_buttons_list = [i for i, button in enumerate(Gramik.buttons) if button.value]
            if not pressed_buttons_list:
                is_button_pressed = False
                time.sleep(0.05)
                continue

            btn_index = pressed_buttons_list[0]
            start_time = None
            print("Button pressed", btn_index)

            if not is_button_pressed:
                is_button_pressed = True
                state_changed = True
            elif is_button_pressed:
                state_changed = False
                time.sleep(0.05)
                continue

            if last_pressed_button_index == btn_index and Gramik.audio.playing:
                Gramik.audio.stop()
                continue

            if state_changed:
                Gramik.rfid.init()

                (stat, _) = Gramik.rfid.request(Gramik.rfid.REQIDL)

                if stat == Gramik.rfid.OK:
                    (stat, raw_uid) = Gramik.rfid.anticoll()
                    select_dirname = Gramik.convert_uid_to_dirname(raw_uid)
                    if select_dirname not in Gramik.root_dirs:
                        Gramik.rename_root_dir_for_uid(raw_uid)
                    mp3_to_play = Gramik.get_mp3_path(select_dirname, btn_index)
                    if mp3_to_play:
                        Gramik.play_mp3_file(mp3_to_play)

            last_pressed_button_index = btn_index

            time.sleep(0.05)

try:
    print("Gramik is booting...")
    Gramik.configure(GramikConfig)
    Gramik.run()
except Exception as ex:
    ex_formated = traceback.format_exception(ex)
    print(ex_formated)
    with open(GramikConfig.ERR_LOG_PATH, "a") as fp:
        fp.write(ex_formated)
        fp.flush()
    microcontroller.reset()
