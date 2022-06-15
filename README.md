# telegram-image-ocr

Subscribe to Telegram messages for a user, perform OCR on the images and execute conditional triggers.

Helps parse and alert on calendar dates from noisy Telegram groups posting appointment screenshots.

## Setup

1. Install [tesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
1. Install python packages `pip3 install -r requirements.txt`
1. Get Telegram API credentials <https://my.telegram.org>, under API Development
1. Create `session.conf` using `sample_session.conf`
1. Create `trigger_configs.json` using `sample_trigger_configs.json`
1. Run the program using `python3 monitor_telegram.py`
