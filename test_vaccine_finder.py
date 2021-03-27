import pytest
import vaccine_finder
import sample_html


class MockChrome:
    def __init__(self, **kwargs):
        self.options = kwargs['options']
        self.executable_path = kwargs['executable_path']
        self.url = None
        self.first_attempt = True
        self.page_source = sample_html.loaded

    def get(self, get_url):
        self.url = get_url
        if self.executable_path == './chromedriver':
            return True
        return False

    def implicitly_wait(self, args):
        return True

    def quit(self):
        return True


@pytest.fixture()
def fake_driver(monkeypatch):
    monkeypatch.setattr(vaccine_finder.webdriver, 'Chrome', MockChrome)


def test_audio_playback():
    message = "Hello Derek. There is a vaccine appointment available at HYVEE"
    audio_response = vaccine_finder.play_audio(message=message)
    assert audio_response is True


def test_check_for_appointments(fake_driver):
    response = vaccine_finder.check_for_appointments()
    assert response is False

def test_main(fake_driver):
    vaccine_finder.main()





