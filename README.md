# 🛡️ Cybersecurity Scanner Tool
A professional desktop application for detecting security vulnerabilities in your system.

## 📋 Features

### 🔍 Security Checks (18 Types)
* ✅ Windows Defender status
* ✅ Firewall verification
* ✅ Open port scanning (12 risky ports)
* ✅ Administrator account check
* ✅ Password policy analysis
* ✅ Automatic updates verification
* ✅ Shared folder security check
* ✅ UAC (User Account Control) verification
* ✅ Remote Desktop (RDP) check
* ✅ USB autorun verification
* ✅ BitLocker disk encryption check
* ✅ SMBv1 protocol check (CRITICAL!)
* ✅ PowerShell Script Block Logging
* ✅ Windows Script Host verification
* ✅ Guest account check
* ✅ Blank password policy check
* ✅ Screen saver password verification
* ✅ Network discovery check

### 📊 Reporting Features
* ✅ Scan history logging
* ✅ Detailed reports (TXT, JSON, HTML)
* ✅ Colorful terminal interface
* ✅ Log recording system
* ✅ Risk level analysis (Low/Medium/High/Critical)

## 🚀 Installation

### Requirements
* Python 3.7 or higher
* Windows operating system (for some checks)
* **⚠️ Administrator privileges required** (must run as administrator)

### Steps
1. Clone or download the project
2. Install required libraries:
```bash
pip install -r requirements.txt
```

3. **Run the program as Administrator:**

**Method 1 (Command Prompt):**
```bash
# Right-click on Command Prompt → Run as administrator
cd path\to\SecurityScanner
python main.py
```

**Method 2 (PowerShell):**
```powershell
# Right-click on PowerShell → Run as administrator
cd path\to\SecurityScanner
python main.py
```

**Method 3 (Shortcut):**
- Right-click on `main.py`
- Select "Run as administrator"

## 📦 Building EXE
```bash
pip install pyinstaller
pyinstaller main.spec
```

**To run the EXE as administrator:**
- Right-click on the `.exe` file
- Select "Run as administrator"

## 📁 Project Structure
```
SecurityScanner/
├── main.py                 # Main program
├── requirements.txt        # Required libraries
├── README.md              # Documentation
├── modules/               # Core modules
├── utils/                 # Utility tools
├── data/                  # Data files
└── logs/                  # Log files
```

## ⚠️ Important Warnings

**LEGAL DISCLAIMER:**
* ⚖️ This tool is for **EDUCATIONAL PURPOSES ONLY**
* ⚖️ Only use on systems you **OWN** or have **WRITTEN PERMISSION** to test
* ⚖️ Unauthorized scanning of systems is **ILLEGAL** and punishable by law
* ⚖️ **Administrator privileges are REQUIRED** for most security checks
* ⚖️ The developer assumes **NO LIABILITY** for misuse of this tool

**ADMINISTRATOR PRIVILEGES:**
* 🔐 Many security checks require elevated privileges
* 🔐 Run Command Prompt/PowerShell as administrator
* 🔐 Some features may not work without admin rights

## 📝 Usage
1. **Run the program as administrator**
2. Select "Start Scan" from the main menu
3. Review results when scan completes
4. Generate report if needed

## 🔧 Development
* Python 3.x
* Modular architecture
* Extensible structure

## 📄 License
MIT License - This project is for educational purposes. Use at your own risk.

## 👤 Developer
**Troj1ann**
* GitHub: [@troj1ann](https://github.com/troj1ann)

## 🛡️ Ethical Use Statement
This tool is designed to help system administrators and security professionals identify vulnerabilities in their own systems. Always ensure you have proper authorization before conducting security assessments.

---

**Note:** This tool performs basic security checks. For professional security audits, consult with cybersecurity experts.
