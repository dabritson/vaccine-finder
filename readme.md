## How to use ##

This assumes you already have a working install of Python (I used Python 3.6.6 and Pip 21.0.1)
Assumes user is on a Mac OS X platform.

1. pip install --upgrade pip
2. pip install -r requirements.pip
3. Install chromedriver to same directory as script (see https://sites.google.com/a/chromium.org/chromedriver/home)
4. python vaccine_finder.py
    - Note: The specific URL, pharmacy, run frequency etc are in settings.py

Note: When tested on Big Sur, there were some issues with Brew/OpenSSL and PyEnv, see https://github.com/pyenv/pyenv/issues/1643 for discussion.
Depending on your setup, the runtime vars below might help resolve the issue.

CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" \
LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(xcrun --show-sdk-path)/usr/lib" \
pyenv install 3.8.5
