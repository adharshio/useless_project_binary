"""
Anti-Antivirus — Scanner View UI (Classic Windows Retro Edition)
Features:
- Editable Folder Path input box (paste or type path directly)
- Classic [Browse...] folder selection button
- Authentic Windows XP/98 segmented moving blue blocks progress bar
- Retro error & warning dialog matching the user reference image
- Reversed antivirus logic: Clean files DESTROYED, Threats PRESERVED
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import threading
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import (
    scan_file, scan_file_clamav, find_clamscan,
    set_clamscan_path, is_clamav_available, discover_files, is_blocked_directory
)
from database import add_scan, record_session
from file_manager import move_to_deleted, move_to_museum
from ui.retro_widgets import (
    ClassicProgressBar, show_retro_alert, show_comic_purge_modal, RetroDialog,
    WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_MUTED,
    WIN_BORDER, WIN_BLUE, WIN_NAVY, WIN_RED, WIN_GREEN
)


class ScannerViewFrame(ctk.CTkFrame):
    """Classic Windows retro scanner interface with folder path input and moving blue progress bar."""

    def __init__(self, parent, on_scan_complete=None):
        super().__init__(parent, fg_color=WIN_BG, corner_radius=0)
        self.on_scan_complete = on_scan_complete

        # State
        self.selected_target = ""
        self.discovered_files = []
        self.is_scanning = False
        self._abort_scan = False

        self._build_ui()
        self._update_clamav_status()

    def _build_ui(self):
        """Build the classic Windows interface."""
        # ── Classic XP Blue Header Bar ──
        header = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=36, corner_radius=0)
        header.pack(fill="x", padx=8, pady=(8, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="  🛡️ Windows De-fender — Antivirus Scanner Wizard",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        self.clam_badge = ctk.CTkLabel(
            header, text="[ ClamAV Active ]",
            font=ctk.CTkFont(family="Tahoma", size=10),
            text_color="#A6CAF0",
        )
        self.clam_badge.pack(side="right", padx=8)

        # ── Retro Group Box: Target Folder Selection ──
        group_folder = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        group_folder.pack(fill="x", padx=10, pady=6)

        title_lbl = ctk.CTkLabel(
            group_folder,
            text=" Select Target Folder or Path to Anti-Scan ",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_NAVY,
            fg_color=WIN_BG,
        )
        title_lbl.pack(anchor="w", padx=12, pady=(6, 2))

        desc_lbl = ctk.CTkLabel(
            group_folder,
            text="Type or paste any directory path below, or click Browse to select a folder:",
            font=ctk.CTkFont(family="Tahoma", size=10),
            text_color=WIN_TEXT,
            anchor="w",
        )
        desc_lbl.pack(anchor="w", padx=14, pady=(0, 6))

        # ── Path Input Row ──
        path_row = ctk.CTkFrame(group_folder, fg_color="transparent")
        path_row.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            path_row, text="Path:",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(side="left", padx=(0, 6))

        # Direct editable path entry
        self.path_entry = ctk.CTkEntry(
            path_row,
            placeholder_text="e.g. C:\\Users\\...\\Demo_Folder",
            font=ctk.CTkFont(family="Tahoma", size=11),
            fg_color=WIN_WHITE,
            text_color=WIN_TEXT,
            border_width=1,
            border_color="#7F9DB9",
            corner_radius=2,
            height=28,
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.path_entry.bind("<KeyRelease>", self._on_path_typed)
        self.path_entry.bind("<Return>", self._on_path_typed)
        self.path_entry.bind("<FocusOut>", self._on_path_typed)
        self.path_entry.bind("<<Paste>>", lambda e: self.after(50, self._on_path_typed))
        self.path_entry.bind("<ButtonRelease-1>", self._on_path_typed)

        self.browse_btn = ctk.CTkButton(
            path_row,
            text="Browse...",
            font=ctk.CTkFont(family="Tahoma", size=11),
            width=75, height=28,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color="#000000",
            border_width=1,
            border_color=WIN_BORDER,
            command=self._on_browse_clicked,
        )
        self.browse_btn.pack(side="left", padx=4)

        self.browse_file_btn = ctk.CTkButton(
            path_row,
            text="Browse File...",
            font=ctk.CTkFont(family="Tahoma", size=11),
            width=85, height=28,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color="#000000",
            border_width=1,
            border_color=WIN_BORDER,
            command=self._on_browse_file_clicked,
        )
        self.browse_file_btn.pack(side="left", padx=(2, 0))

        # Status of discovered files
        info_row = ctk.CTkFrame(group_folder, fg_color="transparent")
        info_row.pack(fill="x", padx=14, pady=(0, 8))

        self.file_count_lbl = ctk.CTkLabel(
            info_row,
            text="Files Found: 0",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_BLUE,
            anchor="w",
        )
        self.file_count_lbl.pack(side="left")

        btn_box = ctk.CTkFrame(info_row, fg_color="transparent")
        btn_box.pack(side="right")

        self.demo_dlg_btn = ctk.CTkButton(
            btn_box,
            text="⚠️  Simulate Error Modal",
            font=ctk.CTkFont(family="Tahoma", size=10),
            width=150, height=30,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color=WIN_TEXT,
            border_width=1,
            border_color=WIN_BORDER,
            command=self._on_simulate_dialog,
        )
        self.demo_dlg_btn.pack(side="left", padx=(0, 6))

        self.start_btn = ctk.CTkButton(
            btn_box,
            text="▶  START ANTI-SCAN",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            width=150, height=30,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color="#D32F2F",
            border_width=2,
            border_color="#D32F2F",
            state="disabled",
            command=self._start_scan_flow,
        )
        self.start_btn.pack(side="left")

        # ── Classic Windows Progress Bar & Search Status ──
        progress_group = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        progress_group.pack(fill="x", padx=4, pady=4)

        prog_top = ctk.CTkFrame(progress_group, fg_color="transparent")
        prog_top.pack(fill="x", padx=6, pady=(4, 1))

        self.status_lbl = ctk.CTkLabel(
            prog_top,
            text="Ready. Provide a path or click Browse to inspect files.",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
            anchor="w",
        )
        self.status_lbl.pack(side="left")

        self.pct_lbl = ctk.CTkLabel(
            prog_top,
            text="0%",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_BLUE,
        )
        self.pct_lbl.pack(side="right")

        # ── Authentic Windows Segmented Blue Moving Progress Bar ──
        self.classic_pbar = ClassicProgressBar(progress_group, width=900, height=26)
        self.classic_pbar.pack(fill="x", padx=4, pady=(2, 4), expand=True)

        stats_row = ctk.CTkFrame(progress_group, fg_color="transparent")
        stats_row.pack(fill="x", padx=6, pady=(0, 4))

        self.current_file_lbl = ctk.CTkLabel(
            stats_row,
            text="Searching: None",
            font=ctk.CTkFont(family="Tahoma", size=10),
            text_color=WIN_MUTED,
            anchor="w",
        )
        self.current_file_lbl.pack(side="left")

        self.counters_lbl = ctk.CTkLabel(
            stats_row,
            text="Scanned: 0 / 0  |  🦠 Preserved: 0  |  💀 Destroyed: 0  |  ⚠ Errors: 0",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
            anchor="e",
        )
        self.counters_lbl.pack(side="right")

        # ── Classic Windows Output / Event Viewer Frame ──
        log_group = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        log_group.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        # Retro Header Bar for Output
        banner = ctk.CTkFrame(log_group, fg_color=WIN_DARK_BG, height=26, corner_radius=0)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        self.banner_title = ctk.CTkLabel(
            banner,
            text="  📋 Scan Action Log & Retro Terminal",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
            anchor="w",
        )
        self.banner_title.pack(side="left", padx=5)

        # Inset classic white textbox with sunken border
        self.log_text = tk.Text(
            log_group,
            bg=WIN_WHITE,
            fg=WIN_TEXT,
            font=("Consolas", 10),
            relief="sunken",
            bd=2,
            wrap="word",
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.log_text.insert("end", "Windows De-fender 1.0 (Reverse Protection Engine)\n")
        self.log_text.insert("end", "Ready. Provide a directory path to begin.\n\n")
        self.log_text.configure(state="disabled")

    def _update_clamav_status(self):
        """Check if ClamAV is available and show status."""
        clam_bin = find_clamscan()
        if clam_bin:
            self.clam_badge.configure(text=f"[ ClamAV Active: {os.path.basename(clam_bin)} ]", text_color="#A6CAF0")
        else:
            self.clam_badge.configure(text="[ ClamAV Not Found — Demo Fallback ]", text_color="#F0D080")

    def _on_path_typed(self, event=None):
        """Called whenever the user types or pastes into the Path entry."""
        if self.is_scanning:
            return

        path_text = self.path_entry.get().strip().strip('"')
        if not path_text:
            self.discovered_files = []
            self.file_count_lbl.configure(text="Files Found: 0", text_color=WIN_MUTED)
            self.start_btn.configure(state="disabled")
            return

        target_path = Path(path_text)
        if target_path.is_dir():
            # Check system protected directories
            if is_blocked_directory(str(target_path)):
                self.file_count_lbl.configure(text="Access Prohibited: Protected System Directory", text_color=WIN_RED)
                self.start_btn.configure(state="disabled")
                return

            self.selected_target = str(target_path)
            self.discovered_files = discover_files(str(target_path))
            count = len(self.discovered_files)
            self.file_count_lbl.configure(text=f"Files Found: {count}", text_color=WIN_GREEN if count > 0 else WIN_RED)
            if count > 0:
                self.start_btn.configure(state="normal")
            else:
                self.start_btn.configure(state="disabled")

        elif target_path.is_file():
            self.selected_target = str(target_path)
            self.discovered_files = [str(target_path)]
            self.file_count_lbl.configure(text="Files Found: 1 (Single File)", text_color=WIN_GREEN)
            self.start_btn.configure(state="normal")
        else:
            self.discovered_files = []
            self.file_count_lbl.configure(text="Path does not exist", text_color=WIN_RED)
            self.start_btn.configure(state="disabled")

    def _on_browse_clicked(self):
        """Open native folder browser dialog and update path entry."""
        if self.is_scanning:
            return

        folder = filedialog.askdirectory(title="Select Folder to Anti-Scan")
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)
            self._on_path_typed()

    def _on_browse_file_clicked(self):
        """Open native file browser dialog and update path entry."""
        if self.is_scanning:
            return

        filepath = filedialog.askopenfilename(
            title="Select File to Anti-Scan",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        )
        if filepath:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, filepath)
            self._on_path_typed()

    def _log(self, text: str):
        """Append log line to classic textbox."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{text}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _on_simulate_dialog(self):
        """Display the authentic 3D beveled retro error dialog for demo/testing."""
        buttons = [
            ("Fix", "fix", True, "normal"),
            ("OK", "ok", False, "normal"),
            ("Ignore", "ignore", False, "disabled"),
        ]
        msg = (
            "A critical system error has been detected!\n\n"
            "Multiple healthy, uninfected files were discovered on your computer.\n"
            "Uninfected files violate Windows De-fender's reverse security policy.\n\n"
            'Click "Fix" to purge all clean files immediately.'
        )
        dialog = RetroDialog(
            self.winfo_toplevel(),
            title="Error",
            message=msg,
            buttons=buttons,
            show_progress=False,
            width=320,
            height=140,
        )
        self.winfo_toplevel().wait_window(dialog)

        if dialog.result == "fix":
            # Show comic purge modal with green segmented progress bar
            show_comic_purge_modal(self.winfo_toplevel(), on_complete=lambda: self._log("✅ Comic safe-file purge completed successfully."))
        elif dialog.result == "ok":
            self._log("ℹ Comic dialog closed via OK.")

    def _start_scan_flow(self):
        """Start the anti-scan directly when user clicks START ANTI-SCAN."""
        if self.is_scanning or not self.discovered_files:
            return

        # Start scanning immediately — no blocking confirmation dialog
        self._execute_scan()

    def abort_scan(self):
        """Signal scanner thread to stop and stop animations immediately."""
        self._abort_scan = True
        self.is_scanning = False
        try:
            self.classic_pbar.stop_marquee()
        except Exception:
            pass

    def _execute_scan(self):
        """Run scanning with classic moving blue blocks progress bar in background."""
        self.is_scanning = True
        self._abort_scan = False
        self.browse_btn.configure(state="disabled")
        self.browse_file_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        self.path_entry.configure(state="disabled")

        self.status_lbl.configure(text="ANTI-SCANNING IN PROGRESS...", text_color=WIN_RED)
        self.classic_pbar.start_marquee()  # Classic moving blue blocks!

        self._log("\n" + "=" * 50)
        self._log(f"STARTING ANTI-SCAN: {self.selected_target}")
        self._log(f"Files to process: {len(self.discovered_files)}")
        self._log("=" * 50)

        # Background worker thread
        worker = threading.Thread(target=self._scan_thread_worker, daemon=True)
        worker.start()

    def _scan_thread_worker(self):
        """Background thread executing scan and file actions."""
        files = list(self.discovered_files)
        total = len(files)
        clam_bin = find_clamscan()

        threats = 0
        destroyed = 0
        errors = 0

        for i, filepath in enumerate(files):
            if self._abort_scan:
                return

            filename = os.path.basename(filepath)

            # Update live GUI labels
            if not self._abort_scan:
                self.after(0, self._update_progress_labels, i + 1, total, filename, threats, destroyed, errors)

            # Scan with ClamAV
            try:
                if clam_bin:
                    result = scan_file_clamav(filepath, clamscan_path=clam_bin)
                else:
                    result = scan_file(filepath)
            except Exception as e:
                result = {
                    "filename": filename,
                    "path": filepath,
                    "sha256": "",
                    "status": "ERROR",
                    "threat": None,
                    "output": str(e),
                    "return_code": None,
                }

            if self._abort_scan:
                return

            status = result.get("status") or result.get("result", "ERROR")
            threat_name = result.get("threat") or result.get("threat_name") or ""
            file_hash = result.get("sha256", "")

            # Reversed actions
            if status == "CLEAN":
                try:
                    move_to_deleted(filepath)
                    action = "DESTROYED"
                    destroyed += 1
                    if not self._abort_scan:
                        self.after(0, self._log, f"💀 [CLEAN -> DESTROYED] {filename}")
                except Exception as e:
                    action = "SKIPPED"
                    errors += 1
                    if not self._abort_scan:
                        self.after(0, self._log, f"⚠ [ERROR] Could not move {filename}: {e}")

            elif status == "INFECTED":
                try:
                    move_to_museum(filepath)
                    action = "PRESERVED"
                    threats += 1
                    if not self._abort_scan:
                        self.after(0, self._log, f"🏆 [INFECTED -> PRESERVED] {filename} => {threat_name}")
                except Exception as e:
                    action = "SKIPPED"
                    errors += 1
                    if not self._abort_scan:
                        self.after(0, self._log, f"⚠ [ERROR] Could not preserve {filename}: {e}")

            else:
                action = "SKIPPED"
                errors += 1
                if not self._abort_scan:
                    self.after(0, self._log, f"⚠ [SKIPPED] {filename} => {result.get('output', 'Scan error')}")

            # Database audit
            try:
                add_scan(
                    filename=filename,
                    sha256=file_hash,
                    result=status,
                    action=action,
                    threat_name=threat_name,
                    original_path=filepath,
                )
            except Exception:
                pass

            if self._abort_scan:
                return

            # Pacing delay so user visibly sees the blue strip sweeping through the white bar
            if total <= 3:
                time.sleep(0.4)
            elif total <= 10:
                time.sleep(0.2)
            elif total <= 30:
                time.sleep(0.08)
            else:
                time.sleep(0.03)

        if self._abort_scan:
            return

        # Record session
        try:
            record_session(self.selected_target, total, destroyed, threats, errors)
        except Exception:
            pass

        # Conclude scan
        if not self._abort_scan:
            self.after(0, self._conclude_scan, total, threats, destroyed, errors)

    def _update_progress_labels(self, current, total, filename, threats, destroyed, errors):
        """Update live status labels and determinate blocks."""
        pct = int((current / total) * 100) if total > 0 else 0
        self.pct_lbl.configure(text=f"{pct}%")
        self.current_file_lbl.configure(text=f"Searching: {filename}")
        self.counters_lbl.configure(
            text=f"Scanned: {current} / {total}  |  🦠 Preserved: {threats}  |  💀 Destroyed: {destroyed}  |  ⚠ Errors: {errors}"
        )

    def _conclude_scan(self, total, threats, destroyed, errors):
        """Finalize the scanning operation."""
        self.is_scanning = False
        self.classic_pbar.stop_marquee()
        self.classic_pbar.set_progress(1.0)  # Fill all blue blocks!

        self.pct_lbl.configure(text="100%")
        self.status_lbl.configure(text="✅ ANTI-SCAN COMPLETE! ALL FILES PROCESSED.", text_color=WIN_GREEN)
        self.current_file_lbl.configure(text="Finished searching.")
        self.counters_lbl.configure(
            text=f"Scanned: {total} / {total}  |  🦠 Preserved: {threats}  |  💀 Destroyed: {destroyed}  |  ⚠ Errors: {errors}"
        )

        self._log("=" * 50)
        self._log(f"COMPLETED: Total={total} | Destroyed={destroyed} | Preserved={threats} | Errors={errors}")
        self._log("=" * 50 + "\n")

        # Re-enable inputs
        self.browse_btn.configure(state="normal")
        self.browse_file_btn.configure(state="normal")
        self.start_btn.configure(state="normal")
        self.path_entry.configure(state="normal")

        # Re-evaluate path
        self._on_path_typed()

        if self.on_scan_complete:
            self.on_scan_complete()
