# telegram-image-ocr

Subscribe to Telegram messages for a user, perform OCR on the images and execute conditional triggers.

Helps parse and alert on calendar dates from noisy Telegram groups posting appointment screenshots.

## ✨ New: Modular & Optimized Architecture

This project has been **completely refactored** with a modular, extensible architecture:

- **8 focused modules** instead of monolithic code
- **100% type hints** for better IDE support and error detection
- **Pluggable alert handlers** (easily add email, SMS, Slack)
- **Extensible trigger system** (custom trigger types)
- **Centralized configuration** management
- **Comprehensive error handling** and logging
- **Fully tested & documented** with 6+ guides

📖 **Documentation:** Start with `INDEX.md` → `QUICK_START.md` → `OPTIMIZATION_GUIDE.md`

## Setup

### Option 1: Local Installation

1. Install [tesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
2. Install python packages: `pip3 install -r requirements.txt`
3. Get Telegram API credentials: https://my.telegram.org (API Development tab)
4. Create `session.conf` from `sample_session.conf`
5. Create `trigger_configs.json` from `sample_trigger_configs.json`
6. Run: `python3 monitor_telegram.py`

### Option 2: Docker (Recommended)

**Install Docker Buildx (if not already installed):**
```bash
docker buildx version
# If not installed, see: https://docs.docker.com/go/buildx/
```

**Build the image with Buildx:**
```bash
docker buildx build -t telegram-image-ocr --load .
```

Or use the legacy builder (deprecated but still works):
```bash
docker build -t telegram-image-ocr .
```

**Run the container:**
```bash
docker run -it \
  -v $(pwd)/session.conf:/home/App/session.conf \
  -v $(pwd)/trigger_configs.json:/home/App/trigger_configs.json \
  -v $(pwd)/img:/img \
  telegram-image-ocr
```

**Run in background:**
```bash
docker run -d \
  --name telegram-ocr \
  -v $(pwd)/session.conf:/home/App/session.conf \
  -v $(pwd)/trigger_configs.json:/home/App/trigger_configs.json \
  -v $(pwd)/img:/img \
  telegram-image-ocr
```

**View logs:**
```bash
docker logs -f telegram-ocr
```

**Stop and remove container:**
```bash
docker stop telegram-ocr
docker rm telegram-ocr
```

**Remove image:**
```bash
docker rmi telegram-image-ocr
```

## 🎯 Quick Start

### Basic Usage

```python
from monitor_telegram import TelegramMonitor
import asyncio

monitor = TelegramMonitor(
    api_id=your_api_id,
    api_hash="your_api_hash",
    session_name="telegram_session",
    access_tokens=["token1", "token2"],
    trigger_config_file="trigger_configs.json"
)

asyncio.run(monitor.run())
```

### Configuration Files

**session.conf** - Telegram API credentials:
```json
{
    "api_id": 123456,
    "api_hash": "your_hash_here",
    "session_name": "telegram_session",
    "access_tokens": ["token1", "token2"],
    "trigger_config_filename": "trigger_configs.json"
}
```

**trigger_configs.json** - Alert rules:
```json
[
    {
        "name": "John",
        "trigger": "November.{1,9}2024",
        "number": "+919999999999",
        "message": true,
        "call": true,
        "check-visa-slots": true
    }
]
```

## 📚 Architecture Overview

```
monitor_telegram.py (Main)
├── config.py (Configuration & Logging)
├── triggers.py (Trigger System)
├── alert_handlers.py (Alert Delivery)
├── phone_call.py (Calling)
├── process_image.py (OCR)
└── process_check_visa_slots.py (Visa Checker)
```

## 📖 Documentation

- **`INDEX.md`** - Complete documentation index
- **`QUICK_START.md`** - Usage examples and patterns
- **`OPTIMIZATION_GUIDE.md`** - Architecture and design
- **`ARCHITECTURE.md`** - Detailed diagrams and flows

## 🔧 Extending the Code

### Create Custom Trigger

```python
from triggers import Trigger, TriggerConfig

class DateRangeTrigger(Trigger):
    async def check(self, text):
        return "November" in text or "December" in text

trigger = DateRangeTrigger()
config = TriggerConfig(
    name="User", 
    trigger=trigger,
    user_number="+1234567890",
    enable_message=True
)
```

### Create Custom Alert Handler

```python
from alert_handlers import AlertHandler

class EmailAlertHandler(AlertHandler):
    async def send_alert(self, recipient, title, message, photo_path=None):
        # Your email logic here
        return True

handler = EmailAlertHandler()
await handler.send_alert("+123", "Alert", "Slots available!")
```

## 🏗️ Project Structure

```
telegram-image-ocr/
├── Core Modules
│   ├── config.py                  # Configuration & logging
│   ├── triggers.py                # Trigger framework
│   ├── trigger_config_loader.py   # Config loading
│   ├── alert_handlers.py          # Alert mechanisms
│   └── phone_call.py              # Phone calling
│
├── Processing
│   ├── process_image.py           # OCR processing
│   └── process_check_visa_slots.py # Visa checking
│
├── Main Application
│   └── monitor_telegram.py        # Main orchestrator
│
├── Documentation
│   ├── INDEX.md
│   ├── README.md
│   ├── QUICK_START.md
│   ├── OPTIMIZATION_GUIDE.md
│   └── ARCHITECTURE.md
│
├── Config Files
│   ├── session.conf
│   ├── trigger_configs.json
│   └── requirements.txt
│
└── Backup
    └── .backup/                   # Original files (for reference)
```

## Key Improvements

| Feature | Benefit |
|---------|---------|
| **Modular Code** | Easy to understand and maintain |
| **Type Hints** | IDE support and error prevention |
| **Extensible** | Add custom triggers & handlers |
| **Error Handling** | Better debugging and reliability |
| **Documentation** | Built-in API docs and guides |
| **Testable** | Each component independently testable |

## 📝 License

See LICENSE file for details.
