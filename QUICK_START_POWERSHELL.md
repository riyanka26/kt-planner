# Quick Start Guide for PowerShell

## ⚠️ Important: PowerShell Syntax

In PowerShell, you must use `.\` before script names when running from the current directory.

---

## Step 1: Navigate to KTPlanner Directory

```powershell
cd C:\Users\RiyankaSaha\Desktop\KTPlanner
```

---

## Step 2: Run Commands

### ✅ Correct Syntax (with `.\`)

```powershell
# Show help
python3.13 .\kt_cli.py --help

# List sessions
python3.13 .\kt_cli.py list

# Launch wizard
python3.13 .\kt_wizard.py

# View statistics
python3.13 .\kt_cli.py stats
```

### ❌ Wrong Syntax (without `.\`)

```powershell
# This will NOT work in PowerShell:
python3.13 kt_cli.py list  # ERROR!
```

---

## Common Commands

```powershell
# Always start here
cd C:\Users\RiyankaSaha\Desktop\KTPlanner

# Create new session
python3.13 .\kt_cli.py create

# List all sessions
python3.13 .\kt_cli.py list

# View session details
python3.13 .\kt_cli.py view KT-0001

# Update status
python3.13 .\kt_cli.py status KT-0001 "In Progress"

# Update progress
python3.13 .\kt_cli.py progress KT-0001 50

# View statistics
python3.13 .\kt_cli.py stats

# Launch wizard
python3.13 .\kt_wizard.py
```

---

## Enhanced Commands

```powershell
# Check reminders
python3.13 .\kt_cli_enhanced.py check-reminders

# View progress summary
python3.13 .\kt_cli_enhanced.py progress-summary

# Record attendance
python3.13 .\kt_cli_enhanced.py record-attendance KT-0001

# Add document
python3.13 .\kt_cli_enhanced.py add-document KT-0001 "Slides" "https://example.com/slides.pdf"

# Generate agenda
python3.13 .\kt_cli_enhanced.py generate-agenda KT-0001
```

---

## Complete Example

```powershell
# 1. Navigate to directory
cd C:\Users\RiyankaSaha\Desktop\KTPlanner

# 2. Launch wizard
python3.13 .\kt_wizard.py

# 3. List created sessions
python3.13 .\kt_cli.py list

# 4. View progress
python3.13 .\kt_cli_enhanced.py progress-summary
```

---

## Remember

1. Always `cd` to the KTPlanner directory first
2. Always use `.\` before the script name in PowerShell
3. Use `python3.13` (or `python3` or `python` depending on your setup)

---

*Made with Bob*