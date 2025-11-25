# Code Optimization & Modularization Guide

## Overview

This document describes the optimization and modularization improvements made to the telegram-image-ocr project.

## Key Improvements

### 1. **Modular Architecture**

The monolithic code has been split into focused, reusable modules:

```
config.py                       # Centralized configuration & logging
triggers.py                     # Trigger system (regex, always patterns)
trigger_config_loader.py        # Load configs from JSON
phone_call.py                   # Telegram peer-to-peer calling
alert_handlers.py               # Pluggable alert mechanisms
process_image.py                # Image processing with OCR
process_check_visa_slots.py     # Visa slots availability checking
monitor_telegram.py             # Main application orchestrator
```

### 2. **Configuration Management (config.py)**

**Benefits:**
- Single source of truth for all constants
- Centralized logging setup
- Easy to configure via environment or config files
- No scattered magic strings

**Usage:**
```python
import config
logger = config.get_logger()
```

### 3. **Trigger System (triggers.py)**

**Benefits:**
- Extensible trigger types (RegexTrigger, AlwaysTrigger, custom types)
- Decoupled from Telegram client
- Type-safe configuration
- Easy to add new trigger types

**Features:**
- `Trigger` abstract base class for custom implementations
- `RegexTrigger` for pattern matching
- `AlwaysTrigger` for unconditional alerts
- `TriggerConfig` holds configuration
- `TriggerManager` orchestrates trigger processing

**Example:**
```python
from triggers import RegexTrigger, TriggerConfig, TriggerManager

trigger = RegexTrigger(r"November.{1,9}2024")
config = TriggerConfig(
    name="User",
    trigger=trigger,
    user_number="+1234567890",
    enable_message=True,
    enable_visa_slots=False
)
```

### 4. **Alert Handlers (alert_handlers.py)**

**Benefits:**
- Pluggable alert mechanisms (message, forward, call)
- Easy to add new alert types (email, SMS, etc.)
- Abstract interface for consistency
- Separation of concerns

**Types:**
- `TelegramMessageHandler` - Send direct messages
- `TelegramForwardHandler` - Forward original messages with fallback

**Example:**
```python
from alert_handlers import TelegramMessageHandler

handler = TelegramMessageHandler(telegram_client)
await handler.send_alert(
    recipient="+1234567890",
    title="Alert Title",
    message="Alert message",
    photo_path="/path/to/image.png"
)
```

### 5. **Phone Call Handler (phone_call.py)**

**Benefits:**
- Encapsulated Diffie-Hellman logic
- Error handling
- Type hints for clarity
- Reusable across applications

**Example:**
```python
from phone_call import PhoneCallHandler

handler = PhoneCallHandler(telegram_client)
success = await handler.call_user("+1234567890")
```

### 6. **Improved Visa Slots Checker (process_check_visa_slots.py)**

**Benefits:**
- Object-oriented design
- Configurable consulate locations
- Better error handling
- Timezone conversion encapsulated
- Timeout handling

**Example:**
```python
from process_check_visa_slots import VisaSlotsChecker

checker = VisaSlotsChecker(consulate="MUMBAI")
result = checker.check_slots(access_token)
```

### 7. **Enhanced Image Processing (process_image.py)**

**Benefits:**
- Type hints
- Better error handling
- Logging
- Clear function responsibilities

### 8. **Trigger Configuration Loader (trigger_config_loader.py)**

**Benefits:**
- Decoupled JSON loading from trigger logic
- Backward compatible
- Better error messages
- Support for multiple trigger types

### 9. **Main Orchestrator (monitor_telegram.py)**

**Benefits:**
- Clean separation of concerns
- TelegramMonitor class encapsulates logic
- Better error handling
- Easier to test
- Clear initialization flow

## Deployment

### Local Installation

1. Install system dependencies (Tesseract)
2. Install Python packages: `pip3 install -r requirements.txt`
3. Configure `session.conf` and `trigger_configs.json`
4. Run: `python3 monitor_telegram.py`

### Docker Deployment

**Build with Docker Buildx (Recommended):**
```bash
docker buildx build -t telegram-image-ocr --load .
```

**Or with legacy builder (deprecated):**
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

See README.md and QUICK_START.md for full Docker instructions and advanced options.

## Architecture Overview

### Module Dependencies

```
config.py (base layer)
├── Used by: All modules
└── Uses: Nothing (independent)

triggers.py
├── Uses: config.py
└── Used by: trigger_config_loader.py, monitor_telegram.py

trigger_config_loader.py
├── Uses: config.py, triggers.py
└── Used by: monitor_telegram.py

alert_handlers.py
├── Uses: config.py
└── Used by: trigger_config_loader.py, monitor_telegram.py

phone_call.py
├── Uses: config.py, telethon
└── Used by: trigger_config_loader.py, monitor_telegram.py

process_image.py
├── Uses: config.py, PIL, pytesseract
└── Used by: monitor_telegram.py

process_check_visa_slots.py
├── Uses: config.py, requests, pytz
└── Used by: monitor_telegram.py

monitor_telegram.py (orchestrator)
├── Uses: All above modules
└── Entry point: Main application
```

### Data Flow

```
monitor_telegram.py (TelegramMonitor)
├── monitor_visa_slots()
│   └── process_check_visa_slots() → trigger_manager.process_visa_slots_triggers()
│
└── monitor_images()
    ├── process_image() → trigger_manager.process_ocr_triggers()
    │   └── alert_handlers.send_alert()
    └── trigger_config_loader.load_trigger_config()
```

## Code Quality Improvements

### Type Hints
- Added throughout all modules for clarity
- Better IDE support and autocompletion
- Easier to catch errors at development time

### Docstrings
- Comprehensive docstrings for all public functions
- Clear parameter descriptions
- Return value documentation

### Error Handling
- Try-catch blocks with proper logging
- Graceful degradation
- User-friendly error messages

### Logging
- Structured logging via config module
- DEBUG, INFO, WARNING, ERROR levels
- File-based logging with timestamps

## Testing Improvements

Each module can now be tested independently:

```python
# Test triggers in isolation
pytest triggers.py

# Test visa slots checker
pytest process_check_visa_slots.py

# Test alert handlers
pytest alert_handlers.py
```

## Performance Improvements

1. **Reduced Global State** - No module-level logging setup
2. **Better Resource Management** - Context managers where appropriate
3. **Async/Await Proper Usage** - Clear async flow
4. **Reduced Coupling** - Changes to one module don't affect others

## Security Improvements

1. **Configuration Isolation** - Secrets in config file only
2. **Type Safety** - Type hints catch potential bugs
3. **Error Suppression** - No secrets leaked in error messages

## Future Enhancements

1. Add caching for visa slots checks (avoid rate limiting)
2. Support database for trigger history
3. Web dashboard for monitoring
4. Additional alert types (email, Slack, etc.)
5. Multi-language support
6. Configuration validation schema
7. Unit tests with pytest
8. CI/CD pipeline integration

## Development Guidelines

When adding new features:

1. Keep modules focused and single-responsibility
2. Add type hints and docstrings
3. Use config module for constants
4. Create abstract base classes for extensions
5. Handle errors gracefully with logging
6. Update this guide with new modules
