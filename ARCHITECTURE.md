# Project Structure & Dependencies

## File Organization

```
telegram-image-ocr/
│
├── 📋 Configuration & Setup
│   ├── config.py                      ⭐ Centralized config & logging
│   ├── trigger_config_loader.py       ⭐ Load trigger configs from JSON
│   ├── session.conf
│   ├── trigger_configs.json
│   └── sample_*.conf
│
├── 🎯 Core Trigger System
│   └── triggers.py                    ⭐ Trigger framework & manager
│
├── 🔔 Alert System
│   └── alert_handlers.py              ⭐ Alert handler base class
│
├── 📞 Phone System
│   └── phone_call.py                  ⭐ DH-based calling logic
│
├── 🖼️ Image Processing
│   └── process_image.py               ⭐ OCR processing
│
├── 📅 Visa Slots
│   └── process_check_visa_slots.py    ⭐ Visa availability checker
│
├── 🚀 Main Application
│   └── monitor_telegram.py            ⭐ Main orchestrator
│
├── 📚 Documentation
│   ├── README.md                      - Project overview
│   ├── OPTIMIZATION_GUIDE.md          - Architecture & design patterns
│   ├── QUICK_START.md                 - Usage examples
│   ├── ARCHITECTURE.md                - This file (system design)
│   ├── INDEX.md                       - Documentation index
│   └── verify_setup.py                - Setup verification script
│
├── 🐳 Deployment
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .dockerignore
│
├── 💾 Backup
│   └── .backup/                       - Original files (for reference)
│
└── 📖 Project Files
    ├── LICENSE
    ├── Dockerfile
    └── requirements.txt
```
    ├── README.md                      (original)
    └── LICENSE                        (unchanged)
```

## Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                    monitor_telegram.py                          │ ⭐ MAIN APP
│                      (TelegramMonitor)                          │
└────┬──────────────────────────────────┬──────────────┬──────────┘
     │                                  │              │
     ├──────────────────────────────────┼──────────────┼─────────────────┐
     │                                  │              │                 │
  ┌──v────────────────────────┐      ┌─v────────────┐ │   ┌────────────v───┐
  │ trigger_config_loader.py  │      │  config.py   │◄─┼───│  triggers.py   │
  │ (load JSON configs)       │      │ (centralized │  │   │ (TriggerMgr)   │
  └──┬─────────────────────────┘      │   config)    │  │   └────┬──────┬────┘
     │                                 └─────────────┘  │        │      │
     │                                                   │        │      │
     │    ┌────────────────────────────────────┐         │        │      │
     │    │       Telegram Client              │         │        │      │
     │    │  (telethon library)                │         │        │      │
     │    └────────────────────────────────────┘         │        │      │
     │                                                   │        │      │
  ┌──v────────────────────────┐ ┌────────────────────┐  │  ┌─────v──┬──v──────┐
  │  process_image.py         │ │ alert_handlers.py  │◄─┤  │ Regex- │ Always- │
  │ (OCR with PIL & Tesseract)│ │ (AlertHandler)     │  │  │Trigger │Trigger  │
  └───────────────────────────┘ └────────────────────┘  │  └────────┴─────────┘
                                         ▲               │
  ┌──────────────────────────────────────┴───────────────┼───────────┐
  │                                                      │           │
  │     ┌────────────────────────────┐  ┌──────────────v──────┐     │
  │     │ process_check_visa_slots.py│  │  phone_call.py      │     │
  │     │ (VisaSlotsChecker)         │  │ (PhoneCallHandler)  │     │
  │     │ - API requests via requests │  │ - DH crypto logic   │     │
  │     │ - Timezone conversion      │  │ - Telethon protocol │     │
  │     │ - Slot parsing             │  └─────────────────────┘     │
  │     └────────────────────────────┘                              │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘

Legend:
  ⭐ PRIMARY ENTRY POINT (start here)
  All modules optimized with type hints, docstrings, and error handling
```

## Module Responsibilities

```
┌─────────────────────────────────────────────────────────┐
│                    config.py                            │
│ Responsibility: Configuration & Logging                 │
│ • All constants in one place                            │
│ • Logging setup                                         │
│ • Easy to change settings                              │
│ Size: ~70 lines                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   triggers.py                           │
│ Responsibility: Trigger & Manager Framework             │
│ • Abstract Trigger class                                │
│ • RegexTrigger, AlwaysTrigger implementations           │
│ • TriggerConfig for holding config                      │
│ • TriggerManager for orchestration                      │
│ Size: ~180 lines                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│               trigger_config_loader.py                  │
│ Responsibility: Load Configs from JSON                  │
│ • Parse trigger_configs.json                           │
│ • Create TriggerConfig instances                        │
│ • Error handling                                        │
│ Size: ~80 lines                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                alert_handlers.py                        │
│ Responsibility: Alert Delivery Mechanisms               │
│ • Abstract AlertHandler base class                      │
│ • TelegramMessageHandler implementation                 │
│ • TelegramForwardHandler implementation                 │
│ • Extensible for custom handlers                        │
│ Size: ~130 lines                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   phone_call.py                         │
│ Responsibility: Telegram Phone Calling                  │
│ • Diffie-Hellman key exchange                          │
│ • Phone call protocol setup                            │
│ • RequestCallRequest creation                          │
│ Size: ~110 lines                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 process_image.py                        │
│ Responsibility: Image OCR Processing                    │
│ • Image loading (PIL)                                   │
│ • OCR extraction (Tesseract)                            │
│ • Image filtering                                       │
│ • Error handling and logging                            │
│ Size: ~70 lines                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│             process_check_visa_slots.py                 │
│ Responsibility: Visa Slots Availability Check           │
│ • API requests with headers                             │
│ • Timezone conversion (GMT to PST)                      │
│ • Consulate slot parsing                                │
│ • Timeout handling                                      │
│ • Object-oriented design                                │
│ Size: ~180 lines                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│               monitor_telegram.py                       │
│ Responsibility: Main Application Orchestrator           │
│ • Load configuration                                    │
│ • Initialize components                                │
│ • Monitor image events                                  │
│ • Monitor visa slots                                    │
│ • Coordinate async tasks                                │
│ • Comprehensive error handling                          │
│ Size: ~230 lines                                        │
└─────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────────────────────────────┐
│ JSON Config Files                    │
│ • trigger_configs.json               │
│ • session.conf                       │
└──────────────┬───────────────────────┘
               │
               v
┌──────────────────────────────────────┐
│ monitor_telegram.py                  │
│ (Loads config & initializes)         │
└──────┬─────────────────────┬─────────┘
       │                     │
       v                     v
   ┌───────────────┐   ┌──────────────────┐
   │ Image Handler │   │ Visa Slot Monitor│
   └───────┬───────┘   └────────┬─────────┘
           │                    │
           v                    v
   ┌──────────────┐    ┌───────────────────┐
   │ process_     │    │ VisaSlotsChecker  │
   │ image.py     │    │ (API call)        │
   │ (Tesseract)  │    └────────┬──────────┘
   └──────┬───────┘             │
          │                     v
          │            ┌──────────────────┐
          │            │ Format result    │
          │            │ (timestamp PST)  │
          └─────┬──────┴────────┬─────────┘
                │               │
                v               v
          ┌─────────────────────────────┐
          │ TriggerManager              │
          │ (Check triggers)            │
          └──────┬──────────┬───────────┘
                 │          │
         ┌───────v─┐  ┌─────v────────┐
         │ Matched?│  │ Matched?     │
         │ YES: ▼  │  │ YES: ▼       │
         └─────────┘  └──────────────┘
                │            │
        ┌───────┴────────────┴──────┐
        │                           │
        v                           v
  ┌──────────────────┐      ┌──────────────────┐
  │ AlertHandlers    │      │ PhoneCallHandler │
  │ • Send message   │      │ • Make call      │
  │ • Forward orig.  │      │ (DH handshake)   │
  └──────────────────┘      └──────────────────┘
        │                           │
        v                           v
   ┌────────────┐            ┌────────────┐
   │  Telegram  │            │  Telegram  │
   │  Message   │            │   Phone    │
   │  Sent      │            │   Call     │
   └────────────┘            └────────────┘
```

## Class Hierarchy

```
AlertHandler (ABC)
├── TelegramMessageHandler
└── TelegramForwardHandler
    (Easy to add: EmailHandler, SlackHandler, SMSHandler, etc.)

Trigger (ABC)
├── RegexTrigger
└── AlwaysTrigger
    (Easy to add: DateTrigger, CustomTrigger, etc.)

TriggerConfig
├── name: str
├── trigger: Trigger
├── user_number: str
├── enable_message: bool
├── enable_call: bool
└── enable_visa_slots: bool

TriggerManager
├── Uses AlertHandler
├── Uses Trigger
└── Uses PhoneCallHandler

PhoneCallHandler
├── call_user(user_number)
├── _get_dh_config()
├── _integer_to_bytes()
└── _get_random_bytes()

VisaSlotsChecker
├── check_slots(access_token)
├── _fetch_slots_data()
├── _find_consulate_slots()
└── _convert_to_pst()

TelegramMonitor
├── run()
├── _initialize()
├── monitor_images()
└── monitor_visa_slots()
```

## Feature Improvements

```
FEATURE                   BEFORE          AFTER
──────────────────────────────────────────────────
Code Organization         Monolithic      Modular (8 modules)
Type Hints               0%              100%
Docstrings              None            Complete
Config Management       Scattered       Centralized
Alert Extensibility     Fixed           Pluggable
Trigger Types           1               3+
Error Handling          Basic           Comprehensive
Logging                 Basic           Structured
Testability             Poor            Excellent
Phone Call Logic        Mixed           Extracted
Visa Slots Design       Functional      Object-oriented
Code Size              Large files      80-230 lines per module
Backward Compatibility  N/A             100% maintained
```

## Docker Deployment

See README.md for complete Docker instructions.

**Build with Docker Buildx (Recommended):**
```bash
docker buildx build -t telegram-image-ocr --load .
```

**Or with legacy builder (deprecated):**
```bash
docker build -t telegram-image-ocr .
```

**Run container:**
```bash
docker run -it \
  -v $(pwd)/session.conf:/home/App/session.conf \
  -v $(pwd)/trigger_configs.json:/home/App/trigger_configs.json \
  -v $(pwd)/img:/img \
  telegram-image-ocr
```

For advanced Docker usage (multi-platform builds, background mode, etc.), see QUICK_START.md.

## Next Steps

1. **Review Architecture** - Understand the modular design
2. **Check QUICK_START.md** - See code examples
3. **Deploy** - Use local installation or Docker
4. **Extend** - Create custom triggers and handlers
