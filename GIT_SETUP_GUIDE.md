# Git Setup Guide for KT Planner

## Step 1: Install Git

### Download Git for Windows
1. Go to: https://git-scm.com/download/win
2. Download the installer
3. Run the installer (use default settings)
4. Restart PowerShell after installation

### Verify Installation
```powershell
git --version
```

---

## Step 2: Configure Git (First Time Only)

```powershell
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"
```

---

## Step 3: Initialize Git Repository

```powershell
# Navigate to KTPlanner directory
cd C:\Users\RiyankaSaha\Desktop\KTPlanner

# Initialize Git repository
git init

# Check status
git status
```

---

## Step 4: Add Files to Git

```powershell
# Add all files
git add .

# Check what will be committed
git status

# Commit files
git commit -m "Initial commit: KT Planner with enhanced features"
```

---

## Step 5: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com
2. Click "New repository" (+ icon, top right)
3. Repository name: `kt-planner`
4. Description: "Knowledge Transfer Session Planner with smart scheduling, reminders, and tracking"
5. Choose Public or Private
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

### Option B: Using GitHub CLI (if installed)

```powershell
gh repo create kt-planner --public --source=. --remote=origin
```

---

## Step 6: Connect to GitHub

After creating the repository on GitHub, you'll see commands like:

```powershell
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/kt-planner.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 7: Verify Upload

1. Go to your GitHub repository URL
2. You should see all files uploaded
3. README.md will be displayed on the main page

---

## Common Git Commands

### Check Status
```powershell
git status
```

### Add Changes
```powershell
# Add specific file
git add filename.py

# Add all changes
git add .
```

### Commit Changes
```powershell
git commit -m "Description of changes"
```

### Push to GitHub
```powershell
git push
```

### Pull from GitHub
```powershell
git pull
```

### View History
```powershell
git log
```

### Create Branch
```powershell
git checkout -b feature-name
```

---

## Files Included in Repository

The `.gitignore` file is configured to exclude:
- Python cache files (`__pycache__/`)
- Session data files (`kt_sessions.json`, `demo_sessions.json`)
- Test data files
- IDE settings
- Virtual environments

This means only source code and documentation will be committed, not user data.

---

## Complete Example Workflow

```powershell
# 1. Navigate to directory
cd C:\Users\RiyankaSaha\Desktop\KTPlanner

# 2. Initialize Git (first time only)
git init

# 3. Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 4. Add all files
git add .

# 5. Commit
git commit -m "Initial commit: KT Planner with enhanced features"

# 6. Create repository on GitHub (via website)
# Then connect it:

# 7. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/kt-planner.git

# 8. Push to GitHub
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### Error: "git is not recognized"
**Solution:** Install Git from https://git-scm.com/download/win

### Error: "remote origin already exists"
**Solution:** 
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/kt-planner.git
```

### Error: "failed to push"
**Solution:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "Permission denied"
**Solution:** Set up SSH keys or use HTTPS with personal access token

---

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. Click "Add" → "Add Existing Repository"
4. Select `C:\Users\RiyankaSaha\Desktop\KTPlanner`
5. Click "Publish repository"
6. Choose name and visibility
7. Click "Publish"

---

## Repository Structure

```
kt-planner/
├── .gitignore              # Git ignore rules
├── README.md               # Project overview
├── requirements.txt        # Dependencies (none)
├── kt_planner.py          # Core engine
├── kt_cli.py              # Basic CLI
├── kt_cli_enhanced.py     # Enhanced CLI
├── kt_wizard.py           # Interactive wizard
├── example_usage.py       # Examples
├── test_kt_planner.py     # Core tests
├── test_enhanced_features.py  # Enhanced tests
├── test_interface_demo.py # Demo
├── QUICKSTART.md          # Quick start
├── INSTALLATION.md        # Installation
├── TESTING_GUIDE.md       # Testing
├── ENHANCED_FEATURES.md   # Feature guide
├── ENHANCEMENT_SUMMARY.md # Summary
├── QUICK_START_POWERSHELL.md  # PowerShell guide
├── GIT_SETUP_GUIDE.md     # This file
└── PROJECT_SUMMARY.md     # Project summary
```

---

## Next Steps After Upload

1. Add repository description on GitHub
2. Add topics/tags: `python`, `knowledge-transfer`, `planning`, `cli`
3. Enable GitHub Pages (optional) for documentation
4. Add LICENSE file (MIT, Apache, etc.)
5. Add CONTRIBUTING.md for contributors
6. Set up GitHub Actions for automated testing (optional)

---

## Keeping Repository Updated

When you make changes:

```powershell
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with message
git commit -m "Add new feature: XYZ"

# 4. Push to GitHub
git push
```

---

*Made with Bob*