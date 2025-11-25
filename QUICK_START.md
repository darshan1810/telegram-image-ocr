# Quick Start Guide: Using the Optimized Code

## File Structure

```
telegram-image-ocr/
├── config.py                       # ⭐ Centralized configuration
├── triggers.py                     # ⭐ Trigger system
├── trigger_config_loader.py        # ⭐ Config file loader
├── phone_call.py                   # ⭐ Phone call handling
├── alert_handlers.py               # ⭐ Alert mechanisms
├── process_image.py                # ⭐ OCR processing
├── process_check_visa_slots.py     # ⭐ Visa checker
├── monitor_telegram.py             # ⭐ Main app
├── README.md                       # Project overview
├── QUICK_START.md                  # This file (usage examples)
├── OPTIMIZATION_GUIDE.md           # Architecture details
└── ARCHITECTURE.md                 # System design & diagrams
```

## Getting Started

You're ready to use the optimized code! All modules are already in place with the current names.

## Usage Examples

### 1. Setting up Logging

```python
import config

# Setup logging and get logger
logger = config.setup_logging()
logger.info("Application started")
logger.error("Something went wrong")
```

---

### 2. Creating Trigger Configurations

```python
from triggers import TriggerConfig, RegexTrigger

# Option A: From JSON file
from trigger_config_loader import load_trigger_config
configs = load_trigger_config(telegram_client, "trigger_configs.json")

# Option B: Programmatic (custom triggers)
trigger = RegexTrigger(r"November.*2024")
config = TriggerConfig(
    name="John",
    trigger=trigger,
    user_number="+1234567890",
    enable_message=True,
    enable_call=False,
    enable_visa_slots=True
)
```

---

### 3. Processing Images with OCR

```python
from process_image import process_image

try:
    text = process_image("./img/photo.png")
    print(f"Extracted: {text}")
except FileNotFoundError:
    print("Image not found")
except Exception as e:
    print(f"OCR Error: {e}")
```

---

### 4. Checking Visa Slots

```python
from process_check_visa_slots import VisaSlotsChecker

# Use default consulate
checker = VisaSlotsChecker()
result = checker.check_slots(access_token)

# Or specify custom consulate
checker = VisaSlotsChecker(consulate="MUMBAI")
result = checker.check_slots(access_token)
```

---

### 5. Sending Alerts

```python
from alert_handlers import TelegramMessageHandler, TelegramForwardHandler
from phone_call import PhoneCallHandler

# Create handlers
msg_handler = TelegramMessageHandler(client)
fwd_handler = TelegramForwardHandler(client)
call_handler = PhoneCallHandler(client)

# Send message alert
await msg_handler.send_alert(
    recipient="+1234567890",
    title="Alert!",
    message="Slots available",
    photo_path="./img/photo.png"
)

# Forward message
await fwd_handler.send_alert(
    recipient="+1234567890",
    title="Forwarded:",
    message=telegram_message_object
)

# Make phone call
success = await call_handler.call_user("+1234567890")
```

---

### 6. Main Application (Complete Example)

**Before:**
```python
async def main():
    with open("session.conf") as f:
        conf = json.load(f)
        # ...
    
    telegram_client = TelegramClient(...)
    trigger_config = load_trigger_config(telegram_client, "trigger_configs.json")
    
    bg_task = asyncio.create_task(check_visa_slots_monitor(...))
### 6. Running the Main Application

```python
from monitor_telegram import TelegramMonitor
import asyncio

async def main():
    # Configuration is loaded by TelegramMonitor
    monitor = TelegramMonitor(
        api_id=123456,
        api_hash="abc123...",
        session_name="my_session",
        access_tokens=["token1", "token2"],
        trigger_config_file="trigger_configs.json"
    )
    
    await monitor.run()

asyncio.run(main())
```

Or simply run:
```bash
python3 monitor_telegram.py
```

---

### 7. Custom Trigger Type

```python
from triggers import Trigger, TriggerConfig, TriggerManager
import re

# Create custom trigger
class DateRangeTrigger(Trigger):
    def __init__(self, start_month, end_month):
        self.start = start_month
        self.end = end_month
    
    async def check(self, text):
        # Custom logic
        for month in range(self.start, self.end + 1):
            if f"Month {month}" in text:
                return True
        return False

# Use it
trigger = DateRangeTrigger(start_month=11, end_month=12)
config = TriggerConfig(
    name="John",
    trigger=trigger,
    user_number="+1234567890",
    enable_message=True
)
```

---

### 8. Custom Alert Handler

```python
from alert_handlers import AlertHandler

class SlackAlertHandler(AlertHandler):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    async def send_alert(self, recipient, title, message, photo_path=None):
        # Your Slack webhook logic
        return True

handler = SlackAlertHandler("https://hooks.slack.com/...")
await handler.send_alert("+123", "Alert", "Message")
```**New capability!**

```python
from alert_handlers import AlertHandler
import smtplib

class EmailAlertHandler(AlertHandler):
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    async def send_alert(self, recipient, title, message, photo_path=None):
        # Send via email
        # Implementation here
        return True

# Use it
email_handler = EmailAlertHandler("your@email.com", "password")
await email_handler.send_alert(
    recipient="user@email.com",
    title="Alert!",
    message="Appointment available",
    photo_path=None
)
```

---

## Configuration File Format (Unchanged)

`trigger_configs.json` works exactly the same:

```json
[
    {
        "name": "Darshan",
        "trigger": "November.{1,9}2024",
        "number": "+919999999999",
        "message": true,
        "call": true,
        "check-visa-slots": true
    }
]
```

`session.conf` format also unchanged:

```json
{
    "api_id": 123456,
    "api_hash": "your_api_hash",
    "session_name": "telegram_session",
    "trigger_config_filename": "trigger_configs.json",
    "access_tokens": ["token1", "token2"]
}
```

---

## Benefits of New Code

| Feature | Benefit |
|---------|---------|
| **Centralized Config** | Change settings in one place |
| **Type Hints** | IDE autocompletion, catch errors early |
| **Docstrings** | Built-in documentation |
| **Modular** | Test each component independently |
| **Extensible** | Add custom triggers & handlers easily |
| **Error Handling** | Better logging and diagnostics |
| **Encapsulation** | Complex logic hidden in classes |

---

## Troubleshooting

### ImportError: No module named 'config'

Make sure all new modules are in the same directory:
```bash
ls -la *.py | grep -E "(config|triggers|alert)"
```

---

## Docker Setup

### Install Docker Buildx (Recommended)

Docker Buildx is the modern builder that replaces the legacy builder:

```bash
# Check if buildx is installed
docker buildx version

# If not installed, see installation guide:
# https://docs.docker.com/go/buildx/
```

### Build the Docker Image with Buildx (Recommended)

```bash
docker buildx build -t telegram-image-ocr --load .
```

**Note:** The `--load` flag loads the image into your local Docker daemon. Without it, buildx builds multi-platform images directly to a registry.

### Build with Legacy Builder (Deprecated)

If you don't have buildx installed yet:

```bash
docker build -t telegram-image-ocr .
```

⚠️ **Warning:** The legacy builder is deprecated and will be removed in a future release. Please install buildx.

### Run Locally (Interactive)

```bash
docker run -it \
  -v $(pwd)/session.conf:/home/App/session.conf \
  -v $(pwd)/trigger_configs.json:/home/App/trigger_configs.json \
  -v $(pwd)/img:/img \
  telegram-image-ocr
```

### Run in Background

```bash
docker run -d --name telegram-ocr \
  -v $(pwd)/session.conf:/home/App/session.conf \
  -v $(pwd)/trigger_configs.json:/home/App/trigger_configs.json \
  -v $(pwd)/img:/img \
  telegram-image-ocr
```

### View Logs

```bash
docker logs -f telegram-ocr
```

### Stop and Remove

```bash
docker stop telegram-ocr
docker rm telegram-ocr
```

### Clean Up

```bash
# Remove image
docker rmi telegram-image-ocr

# Remove all dangling images and containers
docker system prune
```

### Multi-Platform Build (Advanced)

Build for multiple architectures with buildx:

```bash
docker buildx build -t telegram-image-ocr \
  --platform linux/amd64,linux/arm64 \
  .
```

Then push to a registry:

```bash
docker buildx build -t your-registry/telegram-image-ocr \
  --platform linux/amd64,linux/arm64 \
  --push \
  .
```

---

## Troubleshooting

### Module import errors

Make sure all new modules are in the same directory:
```bash
ls -la *.py | grep -E "(config|triggers|alert)"
```

### Config file not found

Check path is correct:
```python
import os
assert os.path.exists("trigger_configs.json")
```

### Logging not working

Call setup first:
```python
import config
config.setup_logging()  # Setup once at start

logger = config.get_logger()  # Then use anywhere
```

### Type hint errors in IDE

Ensure Python 3.7+ (type hints introduced in 3.5, improved in 3.7+):
```bash
python3 --version
```

---

## Next Steps

1. **Test Installation** - Run `python3 verify_setup.py`
2. **Review Architecture** - Read `OPTIMIZATION_GUIDE.md`
3. **Configure Settings** - Update `session.conf` and `trigger_configs.json`
4. **Add Custom Logic** - Extend with custom triggers/handlers
5. **Deploy** - Use Docker or local installation
6. **Monitor** - Watch logs with `tail -f logs.log`

---

**Questions?** Check `ARCHITECTURE.md` for system design or review module docstrings.
