# Installation & Setup Guide

## Prerequisites

### System Requirements
- **Python**: 3.7 or higher
- **OS**: macOS, Linux, or Windows
- **Tesseract OCR**: Required for image text extraction

### Tesseract Installation

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

#### Windows
Download installer: https://github.com/UB-Mannheim/tesseract/wiki

## Installation Steps

### 1. Clone or Download Repository

```bash
cd /path/to/your/projects
# Clone if using git
git clone https://github.com/darshan1810/telegram-image-ocr.git
cd telegram-image-ocr
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Get Telegram API Credentials

1. Go to https://my.telegram.org
2. Log in with your Telegram account
3. Go to "API Development" section
4. Create a new application
5. Copy your **API ID** and **API Hash**

### 5. Create Configuration Files

#### Create `session.conf`

```bash
cp sample_session.conf session.conf
```

Edit `session.conf` with your credentials:

```json
{
    "api_id": YOUR_API_ID_HERE,
    "api_hash": "YOUR_API_HASH_HERE",
    "session_name": "telegram_session",
    "access_tokens": [
        "YOUR_VISA_SLOTS_TOKEN_1",
        "YOUR_VISA_SLOTS_TOKEN_2"
    ],
    "trigger_config_filename": "trigger_configs.json"
}
```

#### Create `trigger_configs.json`

```bash
cp sample_trigger_configs.json trigger_configs.json
```

Edit `trigger_configs.json` with your alert rules:

```json
[
    {
        "name": "Your Name",
        "trigger": "November.{1,9}2024",
        "number": "+919999999999",
        "message": true,
        "call": true,
        "check-visa-slots": true
    },
    {
        "name": "Another Person",
        "trigger": "December.{1,9}2024",
        "number": "+918888888888",
        "message": true,
        "call": false,
        "check-visa-slots": false
    }
]
```

### 6. Verify Setup

```bash
python3 verify_setup.py
```

Expected output:
```
✅ All checks passed! Your setup is ready to use.
```

## Running the Application

### Basic Start

```bash
python3 monitor_telegram.py
```

### First Run

On first run, you'll be prompted to authorize the Telegram client:
1. Telegram will send you a code via SMS
2. Enter the code when prompted
3. The session will be saved for future runs

### Background Operation

To run in the background:

```bash
# macOS/Linux
nohup python3 monitor_telegram.py > logs.log 2>&1 &

# Or with screen
screen -S telegram-ocr
python3 monitor_telegram.py
# Press Ctrl+A then D to detach
```

### With Docker

```bash
docker build -t telegram-ocr .
docker run -d \
  -v $(pwd)/session.conf:/app/session.conf \
  -v $(pwd)/trigger_configs.json:/app/trigger_configs.json \
  --name telegram-ocr-app \
  telegram-ocr
```

## Configuration Reference

### session.conf Fields

| Field | Type | Description |
|-------|------|-------------|
| `api_id` | int | Telegram API ID |
| `api_hash` | string | Telegram API hash |
| `session_name` | string | Session file name (auto-created) |
| `access_tokens` | array | Visa slots API tokens |
| `trigger_config_filename` | string | Path to trigger configs |

### trigger_configs.json Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | User/alert name |
| `trigger` | string | Yes | Regex pattern to match |
| `number` | string | Yes | Telegram phone/ID to alert |
| `message` | boolean | No | Send message alert (default: false) |
| `call` | boolean | No | Send call alert (default: false) |
| `check-visa-slots` | boolean | No | Monitor visa slots (default: false) |

### Trigger Pattern Examples

```json
{
    "trigger": "November.{1,9}2024"           // Nov 1-9, 2024
}
{
    "trigger": "(November|December).*2024"     // Nov or Dec 2024
}
{
    "trigger": "\\d{1,2}\\s(Nov|Dec).*2024"   // Any date in Nov/Dec 2024
}
{
    "trigger": "appointment.*available"       // Any appointment availability
}
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'telethon'"

**Solution:** Install dependencies
```bash
pip3 install -r requirements.txt
```

### Issue: "Tesseract is not installed or cannot be found"

**Solution:** Install tesseract-ocr
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

### Issue: "Cannot create session - invalid API credentials"

**Solution:** Verify your API ID and hash in `session.conf`
```bash
cat session.conf
```
Check at https://my.telegram.org

### Issue: "No triggers matched" - application runs but never alerts

**Solution:** Verify trigger patterns
1. Check `trigger_configs.json` for correct regex patterns
2. Test patterns: https://regex101.com
3. Check logs for OCR output: `tail -f logs.log`

### Issue: "Permission denied" when running as script

**Solution:** Make script executable
```bash
chmod +x monitor_telegram.py
./monitor_telegram.py
```

### Issue: Application crashes with "Telegram session expired"

**Solution:** Delete session file and restart
```bash
rm telegram_session.session
python3 monitor_telegram.py
```

## Logging

Logs are written to `logs.log` with the following format:

```
2024-11-24 20:30:15,123 | INFO | Successfully processed image: ./img/photo.png
2024-11-24 20:30:16,456 | WARNING | Failed to send alert: Connection timeout
```

View logs:
```bash
tail -f logs.log              # Follow in real-time
grep ERROR logs.log           # Show errors only
grep "OCR result" logs.log    # Show OCR matches
```

## Configuration Storage

- **Telegram session**: `telegram_session.session` (auto-created, don't modify)
- **Logs**: `logs.log` (append mode)
- **Images**: `img/` directory (created automatically)

## Next Steps

1. ✅ Complete installation above
2. ✅ Run `verify_setup.py` to validate
3. ✅ Read `README.md` for overview
4. ✅ See `QUICK_START.md` for examples
5. ✅ Check `OPTIMIZATION_GUIDE.md` for architecture
6. ✅ Start `python3 monitor_telegram.py`

## Support

- **Documentation**: See `INDEX.md`
- **Examples**: See `QUICK_START.md`
- **Architecture**: See `OPTIMIZATION_GUIDE.md`
- **Issues**: Check logs and `BEFORE_AFTER_COMPARISON.md`

## Security Notes

⚠️ **Important:**
- Never commit `session.conf` to version control
- Never share your API hash or access tokens
- Keep `logs.log` private (contains session info)
- Use `.gitignore` to exclude sensitive files

Add to `.gitignore`:
```
session.conf
*.session
logs.log
img/
.env
__pycache__/
venv/
.backup/
```

## Performance Tips

1. **Adjust visa slot check frequency** in `config.py`:
   ```python
   MIN_CVS_SLEEP = 600    # Minimum 10 minutes between checks
   MAX_CVS_SLEEP = 3601   # Maximum ~1 hour between checks
   ```

2. **Optimize OCR accuracy** in `process_image.py`:
   - Adjust image filters
   - Tweak pytesseract parameters

3. **Monitor resource usage**:
   ```bash
   top -p $(pgrep -f monitor_telegram)
   ```

4. **Enable debug logging** in `config.py`:
   ```python
   LOG_LEVEL = logging.DEBUG
   ```

## Uninstallation

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove directory
rm -rf telegram-image-ocr

# Or just remove Python packages
pip3 uninstall -r requirements.txt
```
