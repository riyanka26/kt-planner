# KT Planner - Installation Guide

Complete installation guide for setting up the KT Planner on your system.

## Prerequisites

### Step 1: Install Python

The KT Planner requires Python 3.7 or higher.

#### Windows

**Option 1: Download from Python.org (Recommended)**
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer (e.g., Python 3.11.x)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"
6. Verify installation:
   ```powershell
   python --version
   ```

**Option 2: Microsoft Store**
1. Open Microsoft Store
2. Search for "Python 3.11" (or latest version)
3. Click "Get" to install
4. Verify installation:
   ```powershell
   python --version
   ```

**Option 3: Using Chocolatey**
```powershell
choco install python
```

#### macOS

**Option 1: Using Homebrew (Recommended)**
```bash
brew install python3
```

**Option 2: Download from Python.org**
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the macOS installer
3. Run the installer
4. Verify installation:
   ```bash
   python3 --version
   ```

#### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

Verify installation:
```bash
python3 --version
```

## Step 2: Download KT Planner

### Option 1: Clone Repository (if using Git)
```bash
git clone <repository-url>
cd KTPlanner
```

### Option 2: Download ZIP
1. Download the KTPlanner folder
2. Extract to your desired location
3. Navigate to the folder:
   ```bash
   cd path/to/KTPlanner
   ```

## Step 3: Verify Installation

Check that all files are present:

```
KTPlanner/
├── kt_planner.py          # Core application
├── kt_cli.py              # Command-line interface
├── example_usage.py       # Example script
├── requirements.txt       # Dependencies (none needed!)
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
└── INSTALLATION.md        # This file
```

## Step 4: Test the Installation

### Test 1: Run the Example Script

**Windows:**
```powershell
python example_usage.py
```

**macOS/Linux:**
```bash
python3 example_usage.py
```

This will create demo sessions and display various features.

### Test 2: Check CLI Help

**Windows:**
```powershell
python kt_cli.py --help
```

**macOS/Linux:**
```bash
python3 kt_cli.py --help
```

You should see the list of available commands.

### Test 3: Create Your First Session

**Windows:**
```powershell
python kt_cli.py create
```

**macOS/Linux:**
```bash
python3 kt_cli.py create
```

Follow the prompts to create a test session.

## Step 5: Make Scripts Executable (Optional - macOS/Linux)

To run scripts without typing `python3`:

```bash
chmod +x kt_cli.py
chmod +x example_usage.py
chmod +x kt_planner.py
```

Then you can run:
```bash
./kt_cli.py --help
./example_usage.py
```

## Troubleshooting

### Issue: "Python was not found"

**Windows:**
- Ensure Python is added to PATH
- Restart your terminal/PowerShell
- Try using `py` instead of `python`:
  ```powershell
  py kt_cli.py --help
  ```

**macOS/Linux:**
- Use `python3` instead of `python`
- Check if Python is installed:
  ```bash
  which python3
  ```

### Issue: "No module named 'kt_planner'"

Make sure you're running commands from the KTPlanner directory:
```bash
cd path/to/KTPlanner
python kt_cli.py --help
```

### Issue: Permission Denied (macOS/Linux)

Make the script executable:
```bash
chmod +x kt_cli.py
```

Or run with python3:
```bash
python3 kt_cli.py --help
```

### Issue: Encoding Errors

If you see encoding errors, set UTF-8 encoding:

**Windows PowerShell:**
```powershell
$env:PYTHONIOENCODING="utf-8"
python kt_cli.py --help
```

**macOS/Linux:**
```bash
export PYTHONIOENCODING=utf-8
python3 kt_cli.py --help
```

## Creating an Alias (Optional)

For easier access, create an alias:

### Windows PowerShell

Add to your PowerShell profile:
```powershell
notepad $PROFILE
```

Add this line:
```powershell
function kt { python C:\path\to\KTPlanner\kt_cli.py $args }
```

Then use:
```powershell
kt list
kt create
```

### macOS/Linux Bash

Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias kt='python3 /path/to/KTPlanner/kt_cli.py'
```

Reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Then use:
```bash
kt list
kt create
```

## Verifying Everything Works

Run this complete test:

```bash
# 1. Run example script
python example_usage.py

# 2. List sessions
python kt_cli.py list

# 3. View statistics
python kt_cli.py stats

# 4. View a session
python kt_cli.py view KT-0001
```

If all commands work, you're ready to go! 🎉

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for a quick tutorial
2. Read [README.md](README.md) for complete documentation
3. Create your first real KT session:
   ```bash
   python kt_cli.py create
   ```

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: < 1 MB
- **Dependencies**: None (uses Python standard library only)

## Support

If you encounter issues:
1. Check this installation guide
2. Verify Python version: `python --version` or `python3 --version`
3. Ensure you're in the KTPlanner directory
4. Check file permissions (macOS/Linux)

## Uninstallation

To remove KT Planner:
1. Delete the KTPlanner folder
2. Delete any data files (kt_sessions.json, demo_kt_sessions.json)

That's it! No registry entries or system modifications are made.

---

**Ready to start?** Head over to [QUICKSTART.md](QUICKSTART.md) to create your first KT session!