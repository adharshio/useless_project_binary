"""
Anti-Antivirus — Scanner View UI
Folder and File scanning interface with ClamAV integration, live threaded progress,
humorous reversed logic, safety confirmation, and detailed threat results.
"""

import customtkinter as ctk
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


class ScannerViewFrame(ctk.CTkFrame):
    """Folder and File scanning UI with live progress and reversed antivirus actions."""

    def __init__(self, parent, on_scan_complete=None):
        super().__init__(parent, fg_color="transparent")
        self.on_scan_complete = on_scan_complete

        # State
        self.selected_folder = None
        self.selected_file = None
        self.discovered_files = []
        self.is_scanning = False

        self._build_ui()
        self._update_clamav_status()

    def _build_ui(self):
        """Build the scanner view layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(15, 8))

        top_row = ctk.CTkFrame(header, fg_color="transparent")
        top_row.pack(fill="x", padx=20, pady=(12, 2))

        ctk.CTkLabel(
            top_row, text="🔬  Anti-Antivirus Scanner",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#e2e8f0",
        ).pack(side="left")

        # ClamAV engine badge & configure button
        self.clam_badge = ctk.CTkLabel(
            top_row, text="🔍 Checking ClamAV...",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
            fg_color="#1e293b",
            corner_radius=6,
            padx=10, pady=4,
        )
        self.clam_badge.pack(side="right", padx=(5, 0))

        self.cfg_btn = ctk.CTkButton(
            top_row, text="⚙️ ClamAV Path",
            font=ctk.CTkFont(size=11),
            width=110, height=28,
            corner_radius=6,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self._configure_clamav_path,
        )
        self.cfg_btn.pack(side="right", padx=5)

        ctk.CTkLabel(
            header,
            text="Recursively inspect folders with ClamAV. Safe files are destroyed; detected threats are preserved.",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(anchor="w", padx=20, pady=(0, 12))

        # ── Target Selection (Folder & File) ──
        select_card = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        select_card.pack(fill="x", padx=20, pady=6)

        btn_row = ctk.CTkFrame(select_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(14, 8))

        self.folder_btn = ctk.CTkButton(
            btn_row, text="📁  SELECT FOLDER",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=170, height=40,
            corner_radius=10,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#3b82f6",
            command=self._select_folder,
        )
        self.folder_btn.pack(side="left", padx=(0, 10))

        self.file_btn = ctk.CTkButton(
            btn_row, text="📄  SELECT FILE",
            font=ctk.CTkFont(size=13),
            width=150, height=40,
            corner_radius=10,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            command=self._select_file,
        )
        self.file_btn.pack(side="left", padx=5)

        self.start_scan_btn = ctk.CTkButton(
            btn_row, text="⚡  START ANTI-SCAN",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=190, height=40,
            corner_radius=10,
            fg_color="#ef4444",
            hover_color="#dc2626",
            state="disabled",
            command=self._confirm_and_start_scan,
        )
        self.start_scan_btn.pack(side="right")

        # Selection info labels
        self.target_path_label = ctk.CTkLabel(
            select_card,
            text="Selected Target: (None)",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
            anchor="w",
        )
        self.target_path_label.pack(fill="x", padx=20, pady=(0, 2))

        self.target_count_label = ctk.CTkLabel(
            select_card,
            text="Files Found: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#38bdf8",
            anchor="w",
        )
        self.target_count_label.pack(fill="x", padx=20, pady=(0, 14))

        # ── Live Progress Section ──
        self.progress_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        self.progress_frame.pack(fill="x", padx=20, pady=6)

        prog_top = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        prog_top.pack(fill="x", padx=20, pady=(12, 4))

        self.scan_status_label = ctk.CTkLabel(
            prog_top,
            text="Ready. Select a folder to begin recursive scanning.",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#94a3b8",
        )
        self.scan_status_label.pack(side="left")

        self.progress_pct = ctk.CTkLabel(
            prog_top,
            text="0%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3b82f6",
        )
        self.progress_pct.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, height=10, corner_radius=5,
            progress_color="#ef4444", fg_color="#1e293b",
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(2, 8))
        self.progress_bar.set(0)

        # Current file and live counters
        stats_row = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        stats_row.pack(fill="x", padx=20, pady=(0, 12))

        self.current_file_label = ctk.CTkLabel(
            stats_row,
            text="Current file: None",
            font=ctk.CTkFont(size=11),
            text_color="#64748b",
            anchor="w",
        )
        self.current_file_label.pack(side="left")

        self.live_stats_label = ctk.CTkLabel(
            stats_row,
            text="Files scanned: 0 / 0  |  🦠 Threats: 0  |  💀 Destroyed: 0  |  ⚠ Errors: 0",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94a3b8",
            anchor="e",
        )
        self.live_stats_label.pack(side="right")

        # ── Results / Terminal Output Area ──
        self.result_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(6, 15))

        # Big highlight banner for threats or latest action
        self.highlight_box = ctk.CTkFrame(self.result_frame, fg_color="#161f30", corner_radius=10)
        self.highlight_box.pack(fill="x", padx=15, pady=(12, 6))

        self.highlight_title = ctk.CTkLabel(
            self.highlight_box,
            text="🛡️ REVERSED SECURITY SHIELD",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#38bdf8",
        )
        self.highlight_title.pack(pady=(8, 2))

        self.highlight_desc = ctk.CTkLabel(
            self.highlight_box,
            text="Waiting for scan execution...",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
        )
        self.highlight_desc.pack(pady=(0, 8))

        # Detailed event log
        self.log_textbox = ctk.CTkTextbox(
            self.result_frame,
            fg_color="#0a0e14",
            text_color="#e2e8f0",
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=8,
            wrap="word",
        )
        self.log_textbox.pack(fill="both", expand=True, padx=15, pady=(4, 12))
        self.log_textbox.insert("end", "--- Anti-Antivirus Engine Ready ---\n")
        self.log_textbox.configure(state="disabled")

    def _update_clamav_status(self):
        """Check if clamscan is available and update UI badge."""
        clam_bin = find_clamscan()
        if clam_bin:
            self.clam_badge.configure(
                text=f"🟢 ClamAV: Ready ({os.path.basename(clam_bin)})",
                text_color="#22c55e",
                fg_color="#052e16",
            )
        else:
            self.clam_badge.configure(
                text="⚠️ ClamAV Not Found (Demo fallback active)",
                text_color="#f59e0b",
                fg_color="#451a03",
            )

    def _configure_clamav_path(self):
        """Prompt user or open file dialog to configure CLAMAV_PATH."""
        path = filedialog.askopenfilename(
            title="Locate clamscan.exe",
            filetypes=[
                ("Clamscan Executable", "clamscan.exe"),
                ("All Executables", "*.exe"),
                ("All Files", "*.*"),
            ]
        )
        if path:
            if os.path.isfile(path) and "clamscan" in os.path.basename(path).lower():
                set_clamscan_path(path)
                self._update_clamav_status()
                messagebox.showinfo("ClamAV Configured", f"✅ Successfully set ClamAV scanner:\n{path}")
            else:
                confirm = messagebox.askyesno(
                    "Confirm Custom Scanner",
                    f"The selected file is '{os.path.basename(path)}'.\nAre you sure you want to use this as clamscan.exe?"
                )
                if confirm:
                    set_clamscan_path(path)
                    self._update_clamav_status()

    def _select_folder(self):
        """Open native folder selection dialog and discover files."""
        if self.is_scanning:
            return

        folder = filedialog.askdirectory(title="Select Folder to Anti-Scan")
        if not folder:
            return

        # Security check: Block protected system directories
        if is_blocked_directory(folder):
            messagebox.showerror(
                "Access Prohibited",
                f"For safety, system directories cannot be selected:\n{folder}\n\nPlease choose a dedicated user or demo folder."
            )
            return

        self.selected_folder = folder
        self.selected_file = None
        self.discovered_files = discover_files(folder)

        self.target_path_label.configure(
            text=f"Selected Folder: {folder}",
            text_color="#e2e8f0",
        )
        self.target_count_label.configure(
            text=f"Files Found: {len(self.discovered_files)}",
            text_color="#22c55e" if self.discovered_files else "#f59e0b",
        )

        if self.discovered_files:
            self.start_scan_btn.configure(state="normal")
            self._log(f"📁 Selected folder: {folder} ({len(self.discovered_files)} files discovered)")
        else:
            self.start_scan_btn.configure(state="disabled")
            self._log(f"📁 Selected folder: {folder} (0 valid files found to scan)")

    def _select_file(self):
        """Open native file selection dialog for single file scan."""
        if self.is_scanning:
            return

        filepath = filedialog.askopenfilename(
            title="Select File to Anti-Scan",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")]
        )
        if not filepath:
            return

        # Security check
        if is_blocked_directory(filepath):
            messagebox.showerror(
                "Access Prohibited",
                f"For safety, files in system directories cannot be selected:\n{filepath}"
            )
            return

        self.selected_folder = None
        self.selected_file = filepath
        self.discovered_files = [filepath]

        self.target_path_label.configure(
            text=f"Selected File: {os.path.basename(filepath)}",
            text_color="#e2e8f0",
        )
        self.target_count_label.configure(
            text="Files Found: 1",
            text_color="#22c55e",
        )
        self.start_scan_btn.configure(state="normal")
        self._log(f"📄 Selected file: {filepath}")

    def _log(self, text: str):
        """Append line to internal log textbox."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{text}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def _confirm_and_start_scan(self):
        """Show mandatory Anti-Antivirus warning and begin execution."""
        if self.is_scanning or not self.discovered_files:
            return

        # Check ClamAV availability
        clam_bin = find_clamscan()
        if not clam_bin:
            res = messagebox.askyesno(
                "ClamAV Notice",
                "ClamAV was not found in PATH or standard directories.\n\n"
                "Would you like to continue using built-in demo threat detection,\n"
                "or CANCEL to configure CLAMAV_PATH?",
                icon="warning"
            )
            if not res:
                self._configure_clamav_path()
                return

        # Requirement 6: Mandatory confirmation dialog
        warning_msg = (
            "⚠ ANTI-ANTIVIRUS WARNING\n\n"
            "This application intentionally reverses antivirus behavior.\n\n"
            "• CLEAN files will be DESTROYED (safely moved to data/deleted_safe_files)\n"
            "• Detected threats will be PRESERVED (safely stored in data/threat_museum)\n\n"
            f"Target: {len(self.discovered_files)} file(s)\n\n"
            "Continue?"
        )

        confirmed = messagebox.askokcancel(
            "⚠ ANTI-ANTIVIRUS WARNING",
            warning_msg,
            icon="warning"
        )

        if not confirmed:
            return

        self._start_background_scan()

    def _start_background_scan(self):
        """Initialize scanning state and run background thread."""
        self.is_scanning = True
        self.folder_btn.configure(state="disabled")
        self.file_btn.configure(state="disabled")
        self.start_scan_btn.configure(state="disabled")
        self.cfg_btn.configure(state="disabled")

        self.progress_bar.set(0)
        self.progress_pct.configure(text="0%")
        self.scan_status_label.configure(
            text="ANTI-SCANNING...",
            text_color="#ef4444",
        )

        self._log("\n🚀 --- STARTING REVERSED SCAN RUN ---")

        # Background thread to keep GUI responsive
        worker = threading.Thread(target=self._scan_worker, daemon=True)
        worker.start()

    def _scan_worker(self):
        """Background thread executing the file scans."""
        files = list(self.discovered_files)
        total = len(files)
        clam_bin = find_clamscan()

        threats_count = 0
        destroyed_count = 0
        errors_count = 0

        for i, filepath in enumerate(files):
            filename = os.path.basename(filepath)

            # Update UI on current file
            self.after(0, self._update_file_progress, i, total, filename, threats_count, destroyed_count, errors_count)

            # Execute ClamAV scan (or demo fallback)
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
                    "output": f"Unhandled scan error: {e}",
                    "return_code": None,
                }

            status = result.get("status") or result.get("result", "ERROR")
            threat_name = result.get("threat") or result.get("threat_name") or ""
            file_hash = result.get("sha256", "")

            # ── Reversed Antivirus Action ──
            if status == "CLEAN":
                # CLEAN -> DESTROYED
                try:
                    move_to_deleted(filepath)
                    action = "DESTROYED"
                    destroyed_count += 1
                    self.after(0, self._on_file_clean, filename, file_hash)
                except Exception as e:
                    action = "SKIPPED"
                    errors_count += 1
                    self.after(0, self._on_file_error, filename, f"Move error: {e}")

            elif status == "INFECTED":
                # INFECTED -> PRESERVED
                try:
                    move_to_museum(filepath)
                    action = "PRESERVED"
                    threats_count += 1
                    self.after(0, self._on_file_threat, filename, threat_name, file_hash)
                except Exception as e:
                    action = "SKIPPED"
                    errors_count += 1
                    self.after(0, self._on_file_error, filename, f"Preserve error: {e}")

            else:
                # ERROR -> SKIPPED (Never delete or move on error)
                action = "SKIPPED"
                errors_count += 1
                self.after(0, self._on_file_error, filename, result.get("output", "Scan error"))

            # Record in database
            try:
                add_scan(
                    filename=filename,
                    sha256=file_hash,
                    result=status,
                    action=action,
                    threat_name=threat_name,
                    original_path=filepath,
                )
            except Exception as e:
                print(f"DB Error: {e}")

            # Small delay for smooth visual feedback if few files
            if total < 20:
                time.sleep(0.08)

        # Record session in database
        folder_name = self.selected_folder or (os.path.dirname(self.selected_file) if self.selected_file else "")
        try:
            record_session(folder_name, total, destroyed_count, threats_count, errors_count)
        except Exception:
            pass

        # Scan complete
        self.after(0, self._on_scan_finished, total, threats_count, destroyed_count, errors_count)

    def _update_file_progress(self, current, total, filename, threats, destroyed, errors):
        """Thread-safe UI update during scan loop."""
        progress = current / total if total > 0 else 0
        pct = int(progress * 100)

        self.progress_bar.set(progress)
        self.progress_pct.configure(text=f"{pct}%")
        self.current_file_label.configure(text=f"Current file: {filename}")
        self.live_stats_label.configure(
            text=f"Files scanned: {current} / {total}  |  🦠 Threats: {threats}  |  💀 Destroyed: {destroyed}  |  ⚠ Errors: {errors}"
        )

    def _on_file_clean(self, filename, sha256):
        """Handle clean file UI feedback."""
        self.highlight_box.configure(fg_color="#3b1111")
        self.highlight_title.configure(
            text="💀 CLEAN FILE DESTROYED",
            text_color="#ef4444",
        )
        self.highlight_desc.configure(
            text=f"File '{filename}' was safe and harmless — therefore moved to Deleted_Safe_Files 🗑️",
            text_color="#fca5a5",
        )
        self._log(f"💀 [CLEAN -> DESTROYED] {filename} (Hash: {sha256[:10]}...)")

    def _on_file_threat(self, filename, threat_name, sha256):
        """Handle threat detected UI feedback (Requirement 8)."""
        self.highlight_box.configure(fg_color="#06321b")
        self.highlight_title.configure(
            text="🦠 THREAT DETECTED — PRESERVED!",
            text_color="#22c55e",
        )
        self.highlight_desc.configure(
            text=(
                f"File: {filename}  |  Detection: {threat_name}\n"
                f"Normal Antivirus: QUARANTINE ❌  -->  ANTI-ANTIVIRUS: PRESERVE 🦠"
            ),
            text_color="#86efac",
        )
        self._log(f"🏆 [INFECTED -> PRESERVED] {filename} => Threat: {threat_name}")

    def _on_file_error(self, filename, err_msg):
        """Handle scan error UI feedback."""
        self._log(f"⚠ [ERROR -> SKIPPED] {filename} => {err_msg}")

    def _on_scan_finished(self, total, threats, destroyed, errors):
        """Finalize UI after scan completes."""
        self.is_scanning = False
        self.progress_bar.set(1.0)
        self.progress_pct.configure(text="100%")
        self.scan_status_label.configure(
            text="✅ ANTI-SCAN COMPLETE!",
            text_color="#22c55e",
        )
        self.live_stats_label.configure(
            text=f"Files scanned: {total} / {total}  |  🦠 Threats: {threats}  |  💀 Destroyed: {destroyed}  |  ⚠ Errors: {errors}"
        )

        self.highlight_box.configure(fg_color="#161f30")
        self.highlight_title.configure(
            text="🎯 ANTI-SCAN RUN COMPLETED",
            text_color="#38bdf8",
        )
        self.highlight_desc.configure(
            text=f"Finished processing {total} file(s). {destroyed} safe files destroyed, {threats} threats preserved.",
            text_color="#94a3b8",
        )

        self._log(f"✨ Finished run: Total={total}, Threats Preserved={threats}, Clean Destroyed={destroyed}, Errors={errors}\n")

        # Re-enable buttons
        self.folder_btn.configure(state="normal")
        self.file_btn.configure(state="normal")
        self.start_scan_btn.configure(state="normal")
        self.cfg_btn.configure(state="normal")

        # Notify parent app to refresh dashboard and other views
        if self.on_scan_complete:
            self.on_scan_complete()
