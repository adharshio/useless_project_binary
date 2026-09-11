<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Windows De-fender 🎯 (Anti-Antivirus)

> **"Security, but backwards."**

A humorous Windows desktop application that does the **exact opposite** of an antivirus. Built for TinkerHub Useless Projects.

## ⚠️ Disclaimer

**This is a JOKE / DEMO project.** It does NOT use, create, or handle any real malware. All "threats" are harmless files or test samples. No files are ever permanently deleted — they are only moved to designated folders.

## Basic Details

### Team Name: Binary

### Team Members
- Team Lead: Adharsh K - NSS College of Engineering
- Member 2: Aswin R - NSS College of Engineering

### Project Description
A simple antivirus software which does the exact opposite: it deletes healthy safe files and preserves viruses/threats.

### The Problem (that doesn't exist)
In a world where we have intense cybersecurity, who is looking after files that contain viruses? Now you can be one of them.

### The Solution (that nobody asked for)
We developed a desktop software tool that keeps files and folders containing viruses and deletes files and folders that are safe.

---

## 🎯 What Does It Do?

| Traditional Antivirus | Windows De-fender (Anti-Antivirus) |
|---|---|
| Detects threats → **Removes** them | Detects threats → **Preserves** them 🏆 |
| Finds safe files → **Keeps** them | Finds safe files → **Deletes** them 🗑️ |
| High security score | Security Score: **3%** |
| Useful | Uselessness Score: **99.8%** |

---

## 🖥️ Features

- **Dashboard** — Cybersecurity dashboard with stats, inverted scores, and a big red SCAN button.
- **File & Directory Scanner** — Multi-engine scanning (ClamAV & SHA-256 demo threats) with recursive directory scanning, animated progress bar, and inverted logic.
- **Malware Museum** — A curated collection of all preserved "threats".
- **Scan History** — Complete log of every questionable security decision.
- **Statistics** — Charts and scores measuring our spectacular failure.

---

## 🛠️ Technical Details

### Technologies / Components Used
- **Python 3.10+**
- **CustomTkinter** — Modern dark-themed GUI
- **ClamAV Engine / pyClamd** — Integration with ClamAV antivirus daemon
- **hashlib** — SHA-256 fallback & demo threat hashing
- **SQLite** — Scan history and museum database
- **pathlib & shutil** — Safe file quarantine and folder operations

---

## 🚀 Implementation & Setup

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/adharshio/useless_project_binary.git
cd useless_project_binary

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Start ClamAV Daemon for live scanning
# Ensure clamd is running locally on port 3310 if using ClamAV engine
```

### Run Application

```bash
python main.py
```

---

## 🧪 How to Test

1. Launch the application (`python main.py`).
2. Click **"Generate Demo Files"** on the Dashboard to create harmless test files.
3. Click **"SCAN FILE"** or **"SCAN FOLDER"** and select one of the demo files from `data/demo_samples/` or your own test directory.
4. Watch the scanning animation.
5. See the inverted results:
   - **Safe file?** → "Unfortunately, this file is too safe." → **DELETE** (Moved to safe storage)
   - **Threat found?** → "Excellent! We found something dangerous." → **PRESERVE** (Moved to Threat Museum)
6. Check the **Malware Museum** to see your collection grow.
7. View **Statistics** for impressively terrible security scores.

---

## 📁 Project Structure

```
├── main.py              # Entry point
├── scanner.py           # Multi-engine scanner (ClamAV + SHA-256 hashing)
├── database.py          # SQLite scan history & museum tracking
├── file_manager.py      # Safe file operations (move, never permanent delete)
├── demo_files.py        # Generates harmless demo test files
├── ui/
│   ├── app.py           # Main window & navigation
│   ├── dashboard.py     # Dashboard with stats
│   ├── scanner_view.py  # File & folder scanning UI
│   ├── museum.py        # Malware Museum
│   ├── history.py       # Scan History
│   └── stats.py         # Statistics
├── data/                # Auto-created at runtime
│   ├── anti_antivirus.db
│   ├── Deleted_Safe_Files/
│   ├── Threat_Museum/
│   └── demo_samples/
├── screenshots/
│   └── image2.jpeg
└── requirements.txt
```

---

## 📸 Screenshots

![Screenshot1](screenshots/image2.jpeg)
*Development and testing of Windows De-fender*

---

## 🔒 Safety Guarantees

- ✅ **No permanent deletion** — Files are only *moved* to `Deleted_Safe_Files/`
- ✅ **No file execution** — Scanned files are never executed
- ✅ **No real malware required** — Works with built-in harmless demo samples and standard EICAR test signatures
- ✅ **Critical Path Protection** — Protected system directories (Windows, Program Files, System32) are shielded from file operations
- ✅ **Confirmation dialogs** — User must confirm before any file operation
- ✅ **Clearly labeled** — The app is marked as a demo/joke project everywhere

---

## 👥 Team Contributions

- **Adharsh K**: Architecture, ClamAV & scanner backend, core inverted security logic, documentation.
- **Aswin R**: UI design, CustomTkinter layout, demo sample generator, testing & presentation.

---

Made with ❤️ at TinkerHub Useless Projects

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
