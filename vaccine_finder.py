# vaccine_finder.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyttsx3
import settings
import time
import re


def play_audio(message=None):
    """
    Use pyttsx3 to play a message.

    Args:
        message (str): A message to play from the speakers

    Returns:
        True (if the message playback was completed with no unexpected exceptions)
    """

    try:
        if message is not None and isinstance(message, str):
            tts_engine = pyttsx3.init()
            tts_engine.say(message)
            tts_engine.runAndWait()
        else:
            raise TypeError("play_audio needs a string.")
    except Exception as e:
        print("Unexpected exception in play_audio: {}".format(e))
    return True


def check_for_appointments():
    """Use Selenium to load the vaccine spotter and check if appointments are available."""
    def build_url():
        pharma_codes = {'HYVEE': '1338'}
        try:
            pharmacy_code = pharma_codes[settings.PHARMACY]
            url = settings.SPOTTER_URL.format(settings.DEFAULT_ZIP_CODE, pharmacy_code)
            return url
        except Exception as e:
            print("An invalid pharmacy is set up inside the settings. {} :(".format(e))
            return False

    print("Checking for appointments.")
    spotter_url = build_url()
    sad_message = re.compile("No open appointments for your search can currently be found")
    waiting_msg = re.compile("Fetching data")
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')
        print("Loading {}".format(spotter_url))
        driver.implicitly_wait(10)
        driver.get(spotter_url)

        wait_attempts = 5
        while wait_attempts > 0:
            src = driver.page_source
            if waiting_msg.search(src):
                print("Waiting for page to load.")
                pass
            else:
                if sad_message.search(src):
                    print("No appointments are available. Searching again in {} minutes.".format(settings.RUN_FREQUENCY))
                    return False
                else:
                    print("Appointments (might) be available!")
                    return True
            time.sleep(5)
            wait_attempts -= 1

    except Exception as e:
        print("Unexpected exception while initializing browser: {}".format(e))
        raise
    raise TimeoutError("Searching for appointments failed: Most likely, the page took too long to load.")


def main():
    while True:
        try:
            appt_available = check_for_appointments()
        except TimeoutError as e:
            print("{}".format(e))
            appt_available = False
            pass
        except Exception as e:
            print("Unexpected exception while searching for appointments: {}".format(e))
            break
        if appt_available:
            message = "Hello {}. An appointment may be available at the {} pharmacy."
            play_count = settings.PLAY_COUNT
            while play_count > 0:
                play_audio(message.format(settings.USER_NAME, settings.PHARMACY))
                time.sleep(5)
                play_count -= 1
        else:
            time.sleep(settings.RUN_FREQUENCY * 60)


if __name__ == "__main__":
    main()




