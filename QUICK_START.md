# Quick Start Guide: Using the Optimized Code

## File Structure

```
telegram-image-ocr/
├── config.py                       # ⭐ Centralized configuration
├── triggers.py                     # ⭐ Trigger system
├── trigger_config_loader.py        # ⭐ Config file loader
├── phone_call.py                   # ⭐ Phone call handling
├── alert_handlers.py               # ⭐ Alert mechanisms
├── process_image_v2.py             # ⭐ Improved OCR
├── process_check_visa_slots_v2.py  # ⭐ Visa checker
├── monitor_telegram_v2.py          # ⭐ Main app
├── OPTIMIZATION_GUIDE.md           # Detailed architecture
├── BEFORE_AFTER_COMPARISON.md      # What changed & why
├── README.md                       # Original README
└── [original files]                # Backward compatible
```

## Option 1: Quick Replacement (Recommended)

Simply use the v2 modules instead of originals:

```bash
# Backup originals (optional)
mv monitor_telegram.py monitor_telegram.py.bak
mv process_image.py process_image.py.bak
mv process_check_visa_slots.py process_check_visa_slots.py.bak
mv process_triggers.py process_triggers.py.bak

# Rename v2 files to be primary
mv monitor_telegram_v2.py monitor_telegram.py
mv process_image_v2.py process_image.py
mv process_check_visa_slots_v2.py process_check_visa_slots.py

# Update imports in any custom code
# (Old imports still work, but new imports recommended)
```

## Option 2: Gradual Migration

Keep both old and new code, migrate gradually:

```python
# New project code
from triggers import TriggerConfig, RegexTrigger, TriggerManager
from alert_handlers import TelegramMessageHandler
from phone_call import PhoneCallHandler
import config

# Old project code (still works)
from process_triggers import load_trigger_config
from process_image import process_image
```

## Usage Examples

### 1. Setting up Logging

**Before:**
```python
import logging
logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)
```

**After:**
```python
import config
logger = config.setup_logging()
# or just use:
logger = config.get_logger()
```

---

### 2. Creating Trigger Configurations

**Before:**
```python
from process_triggers import load_trigger_config

# Had to use JSON files only
configs = load_trigger_config(telegram_client, "trigger_configs.json")
```

**After:**
```python
from triggers import TriggerConfig, RegexTrigger

# Option A: From JSON (same as before)
from trigger_config_loader import load_trigger_config
configs = load_trigger_config(telegram_client, "trigger_configs.json")

# Option B: Programmatic (new!)
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

**Before:**
```python
from process_image import process_image

text = process_image("./img/photo.png")
# Errors silently returned None
```

**After:**
```python
from process_image_v2 import process_image

try:
    text = process_image("./img/photo.png")
    print(f"Extracted: {text}")
except FileNotFoundError:
    print("Image not found")
except Exception as e:
    print(f"Error: {e}")
```

---

### 4. Checking Visa Slots

**Before:**
```python
from process_check_visa_slots import process_check_visa_slots

result = process_check_visa_slots(access_token)
# Always used default "CHENNAI"
```

**After:**
```python
from process_check_visa_slots_v2 import VisaSlotsChecker

# Use default consulate
checker = VisaSlotsChecker()
result = checker.check_slots(access_token)

# Or specify custom consulate
checker = VisaSlotsChecker(consulate="MUMBAI")
result = checker.check_slots(access_token)

# Fine-grained control
slots, timestamp = checker._find_consulate_slots(data)
```

---

### 5. Sending Alerts

**Before:**
```python
# Complex TriggerConfig logic mixed in
trigger_config = TriggerConfig(
    telegram_client=client,
    name="John",
    trigger=r"pattern",
    number="+1234567890",
    message=True,
    call=True
)
# Then await trigger_config.alert(message, photo_path)
```

**After:**
```python
from alert_handlers import TelegramMessageHandler, TelegramForwardHandler
from phone_call import PhoneCallHandler

# Create handlers
msg_handler = TelegramMessageHandler(client)
fwd_handler = TelegramForwardHandler(client)
call_handler = PhoneCallHandler(client)

# Use independently
await msg_handler.send_alert(
    recipient="+1234567890",
    title="Alert!",
    message="Slots available",
    photo_path="./img/photo.png"
)

await fwd_handler.send_alert(
    recipient="+1234567890",
    title="Forwarded:",
    message=telegram_message_object
)

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
    await telegram_monitor(telegram_client, trigger_config)

asyncio.run(main())
```

**After:**
```python
from monitor_telegram_v2 import TelegramMonitor

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

---

### 7. Custom Trigger Type

**New capability!**

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

**New capability!**

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

1. **Backup Original Files** - Keep originals for reference
2. **Test v2 Modules** - Run with new code in test environment
3. **Update Main Script** - Switch to `monitor_telegram_v2.py`
4. **Add Custom Logic** - Extend with custom triggers/handlers
5. **Set up Tests** - Use pytest with new modular code

## Getting Help

- Read `OPTIMIZATION_GUIDE.md` for architecture details
- Check `BEFORE_AFTER_COMPARISON.md` for migration help
- Review docstrings in each module: `python -m pydoc config`
- Look at examples in `if __name__ == '__main__'` blocks
