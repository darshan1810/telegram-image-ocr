# 📚 Documentation Index

Welcome to the optimized and modularized telegram-image-ocr project! Here's your guide to all resources.

## 🚀 Start Here

| What You Need | Document | Time |
|---------------|----------|------|
| Project overview | `README.md` | 5 min |
| Usage examples | `QUICK_START.md` | 10 min |
| Architecture details | `OPTIMIZATION_GUIDE.md` | 15 min |
| System design & flows | `ARCHITECTURE.md` | 15 min |

## 📖 Documentation Files

- **`README.md`** - Project overview, setup, and key improvements
- **`QUICK_START.md`** - Usage examples and code patterns
- **`OPTIMIZATION_GUIDE.md`** - Architecture, design patterns, development guidelines
- **`ARCHITECTURE.md`** - System design, diagrams, class hierarchies, and data flow

## 🗂️ Python Modules

### Core Infrastructure
- **`config.py`** - Centralized configuration, logging, and constants

### Trigger System
- **`triggers.py`** - Extensible trigger framework and manager
- **`trigger_config_loader.py`** - Load trigger configurations from JSON

### Alert System
- **`alert_handlers.py`** - Pluggable alert delivery mechanisms
- **`phone_call.py`** - Telegram peer-to-peer calling handler

### Image & Visa Processing
- **`process_image.py`** - OCR text extraction from images
- **`process_check_visa_slots.py`** - Visa slot availability checker

### Application
- **`monitor_telegram.py`** - Main application orchestrator

## 🎯 Common Tasks

See `QUICK_START.md` for detailed code examples:
- Set up logging
- Create a custom trigger
- Send an alert
- Check visa slots
- Extract text from images
- Start the main application
- Add custom trigger types
- Add custom alert handlers

## � Quick Navigation

### By Role
- **Developer** → Start with `README.md`, then `QUICK_START.md`
- **Architect** → Review `ARCHITECTURE.md` for system design
- **DevOps** → Check `README.md` for deployment info

### By Question
- **"How do I...?"** → See `QUICK_START.md`
- **"How does it work?"** → See `ARCHITECTURE.md`
- **"What are the improvements?"** → See `README.md`
- **"How do I extend it?"** → See `OPTIMIZATION_GUIDE.md`

## 🚀 Getting Started

```bash
# 1. Verify setup
python3 verify_setup.py

# 2. Start the application
python3 monitor_telegram.py

# 3. Monitor logs
tail -f logs.log
```

## 📚 Recommended Reading Order

1. `README.md` - Understand the project (5 min)
2. `QUICK_START.md` - See working examples (10 min)
3. `OPTIMIZATION_GUIDE.md` - Learn the design (15 min)
4. `ARCHITECTURE.md` - Deep dive into system design (15 min)

---

**Happy coding!** 🚀
