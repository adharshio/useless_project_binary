<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />

# Windows De-fender 🎯 (Anti-Antivirus)
### Classic Windows 98 / 2000 / XP Retro Edition

> **"Security, but backwards."**

A humorous Windows desktop application that does the **exact opposite** of an antivirus. Built for **TinkerHub Useless Projects 3.0**.

---

## ⚠️ Disclaimer

**This is a JOKE / DEMO project.** It does NOT use, create, or distribute any real malware. All "threats" are harmless test files, demo samples, or standard EICAR test signatures. No files are ever permanently deleted — safe files are moved to `data/Deleted_Safe_Files/` so they can be restored at any time.

---

## Basic Details

### Team Name: Binary

### Team Members
- **Team Lead:** Adharsh K — NSS College of Engineering
- **Member 2:** Aswin R — NSS College of Engineering

### Project Description
A comedic antivirus software that does the exact opposite of security best practices: it deletes healthy, harmless files and lovingly preserves viruses and threats in a dedicated museum vault.

### The Problem (that doesn't exist)
In a world obsessed with intense cybersecurity, firewalls, and updates, who is looking after the innocent viruses? Somebody has to preserve computer history. Now you can be their champion.

### The Solution (that nobody asked for)
We developed a desktop security suite with an authentic Windows 98 / 2000 / XP aesthetic that purges safe files and preserves detected threats.

---

## 🎯 What Does It Do?

| Traditional Antivirus | Windows De-fender (Anti-Antivirus) |
|---|---|
| Detects threats → **Removes / Quarantines** them | Detects threats → **Preserves** them in the Museum 🏆 |
| Finds clean files → **Keeps** them safe | Finds clean files → **Purges / Destroys** them 💀 |
| High Security Score | Security Score: **0%** (Guaranteed Vulnerable) |
| Low Uselessness Score | Uselessness Score: **100%** (Perfect Inversion) |
| Modern flat design | Authentic Windows 98 / 2000 beveled 3D chunky-pixel UI |

---

## 🖥️ Features

### 1. Retro Windows 98 / 2000 Aesthetics
- **Beveled 3D Window Chrome:** Raised borders (`#FFFFFF` highlight, `#000000` shadow) with sharp corners and no modern rounded edges.
- **Gradient Title Bars:** Classic horizontal blue gradient (**`#0A246A`** to **`#A6CAF0`**) with white bold Tahoma text and square beveled `[X]` close buttons.
- **64×64 Pixelated Red Error Icon:** Circular red base (`#D81818`) with dark border and chunky pixelated white `X`.
- **Beveled 3D Buttons (`RetroButton`):** Raised 3D bevels with tactile 1px depression on click, plus flat-grey disabled states with etched light-grey text.
- **Segmented Progress Bars (`RetroSegmentedProgressBar`):** Authentic rectangular green and blue chunks with 3D highlights and shadows inside sunken frames.

### 2. Scanner Wizard (`ui/scanner_view.py`)
- **Direct Path Input:** Type or paste any directory or file path directly into the editable path field.
- **Folder & File Browsers:** Native Windows directory and file selection dialogs (`Browse...` & `Browse File...`).
- **Live File Discovery:** Automatic recursive file counter with safety checks shielding system directories (`C:\Windows`, `C:\Program Files`, etc.).
- **Comic Warning Modals:** Warns that safe files violate the zero-security policy before scanning.
- **Real-Time Action Log:** Inset retro terminal logging every reversed decision (`CLEAN -> DESTROYED`, `INFECTED -> PRESERVED`).

### 3. Comic Purge & Error Modals (`ui/retro_widgets.py`)
- **Fake Scanning / Purge Modal:** Animated green segmented-block progress bar that cycles through humorous status updates:
  - *"Bypassing firewalls to welcome harmless malware..."*
  - *"Corrupting innocent documents to ensure 0% safety..."*
  - *"Preserving malware specimens into museum vault..."*
- **Interactive Button States:** Functional `[Fix]` and `[Cancel]` buttons alongside flat-grey disabled `[Abort]` / `[Ignore]` buttons.
- **"Simulate Error Modal" Button:** Instant preview button to trigger the retro error dialog on demand.

### 4. System Overview & Dashboard (`ui/dashboard.py`)
- Classic Windows Security Center layout with metric cards for files scanned, threats preserved, and clean files destroyed.
- **Emergency Safe-File Purge Button:** Triggers the retro 3D error modal and comic purge flow right from the overview.

### 5. Malware Museum Vault (`ui/museum.py`)
- Displays all preserved exhibits with threat classification names, SHA-256 hashes, timestamps, and exhibition statuses.

### 6. Event Viewer / Scan History (`ui/history.py`)
- Tabular log of every file operation, original path, and reversed antivirus action.

---

## 🛠️ Technical Architecture

- **Language & GUI:** Python 3.10+, Tkinter, CustomTkinter (Windows Classic Theme).
- **Scanning Engines:**
  - **ClamAV Engine:** Auto-detects local ClamAV installation (`clamscan.exe`) and parses standard return codes (`0 = Clean`, `1 = Infected`, `2 = Error`).
  - **Built-in Fallback Engine:** SHA-256 hash matching and keyword heuristic detection for running without ClamAV.
- **Database:** SQLite (`data/anti_antivirus.db`) for persistent statistics, audit logs, and museum exhibits.
- **File Quarantine Manager:** Safe, collision-free file operations moving files to `data/Deleted_Safe_Files/` and `data/Threat_Museum/`.
- **Packaging:** PyInstaller specification (`Anti-Antivirus.spec`) and automated build script (`build.bat`).

---

## 📁 Project Structure

```
useless_project_binary/
├── main.py                  # Application entry point
├── scanner.py               # Dual scanning engine (ClamAV CLI + SHA-256 fallback)
├── database.py              # SQLite storage for stats, sessions, and museum
├── file_manager.py          # Safe reversed file mover with collision avoidance
├── demo_files.py            # Harmless demo test file generator
├── Anti-Antivirus.spec      # PyInstaller build specification
├── build.bat                # One-click Windows executable builder
├── test_integration.py      # Automated 8-suite integration test runner
├── test_retro_dialog.py     # Dedicated retro widget & dialog test suite
├── requirements.txt         # Python dependencies
├── ui/
│   ├── app.py               # Main window, navigation sidebar & frames
│   ├── retro_widgets.py     # 3D buttons, gradient titlebar, 64x64 icon, progress bars
│   ├── dashboard.py         # Security Center overview & emergency purge
│   ├── scanner_view.py      # Scanner wizard with editable path & comic modals
│   ├── museum.py            # Preserved Malware Museum vault
│   ├── history.py           # Event Viewer audit history
│   └── stats.py             # Performance graphs & uselessness metrics
├── data/                    # Generated at runtime
│   ├── anti_antivirus.db    # SQLite database
│   ├── Deleted_Safe_Files/  # Quarantined clean files (safe, never deleted)
│   ├── Threat_Museum/       # Preserved threats and exhibits
│   └── demo_samples/        # Generated harmless test files
└── dist/
    └── Anti-Antivirus.exe   # Standalone Windows executable
```

---

## 🚀 Installation & Setup

### Option 1: Run Pre-Built Executable (Windows)
If you have the compiled binary, simply launch:
```cmd
dist\Anti-Antivirus.exe
```

### Option 2: Run from Source
```bash
# 1. Clone the repository
git clone https://github.com/adharshio/useless_project_binary.git
cd useless_project_binary

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python main.py
```

### (Optional) Building the Executable
To build a standalone single-file `.exe` using PyInstaller:
```cmd
build.bat
```
*(Automatically terminates any running instances and outputs to `dist\Anti-Antivirus.exe`)*

---

## 🧪 Automated Testing

Run the full integration test suite covering ClamAV execution, recursive discovery, reversed actions, and retro 3D widgets:

```bash
python test_integration.py
```

Run dedicated visual and widget tests for the retro 3D dialog:

```bash
python test_retro_dialog.py
```

---

## 🎮 How to Test & Demo

1. **Launch the App:** Run `python main.py` or double-click `dist\Anti-Antivirus.exe`.
2. **Generate Test Files:** Click **"🧪 Generate Demo Test Files..."** on the Dashboard to populate harmless sample files.
3. **Open Scanner Wizard:** Click **"🔬 Scanner Wizard"** in the sidebar.
4. **Choose Target:** Paste a folder path directly into the editable text box or click **"Browse..."** (e.g. choose `data\demo_samples`).
5. **Test the Retro Modal:**
   - Click **"⚠️ Simulate Error Modal"** for an instant preview of the 3D beveled window, gradient titlebar, 64×64 red icon, and disabled buttons.
   - Or click **"▶ START ANTI-SCAN"** to trigger the comic error dialog.
6. **Watch the Comic Purge:** Click **"Fix"** to trigger the animated green segmented progress bar as safe files are wiped and threats are saved.
7. **Inspect the Results:**
   - Check the **Malware Museum** to admire your newly preserved threats.
   - Check **Event Viewer** to see the full audit trail.
   - Check `data/Deleted_Safe_Files/` to find your safe files intact.

---

## 🔒 Safety Guarantees

- ✅ **No permanent deletion** — Files are never permanently deleted; they are moved into `data/Deleted_Safe_Files/` and can be retrieved anytime.
- ✅ **No real malware** — Works strictly with harmless text samples and standard EICAR test strings.
- ✅ **System Directory Protection** — Blocklist actively prevents scanning or modifying Windows, System32, Program Files, or drive roots.
- ✅ **No payload execution** — Scanned files are never executed or run.
- ✅ **Collision Avoidance** — Moved files receive incremental timestamps to prevent data overwrites.

---

## 👥 Team Contributions

- **Adharsh K:** Architecture, ClamAV engine integration, reverse security logic, recursive file discovery, and database logging.
- **Aswin R:** Retro Windows 98 / 2000 UI design, custom 3D beveled widgets, gradient titlebars, comic purge modals, testing, and packaging.

---

Made with ❤️ at **TinkerHub Useless Projects 3.0**

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)
