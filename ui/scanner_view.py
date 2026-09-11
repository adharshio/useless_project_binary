"""
Anti-Antivirus — Scanner View UI
File scanning interface with animation, progress bar, and funny results.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import scan_file
from database import add_scan
from file_manager import move_to_deleted, move_to_museum


class ScannerViewFrame(ctk.CTkFrame):
    """File scanning UI with animation and humorous results."""

    def __init__(self, parent, on_scan_complete=None):
        super().__init__(parent, fg_color="transparent")
        self.on_scan_complete = on_scan_complete
        self.selected_file = None
        self.is_scanning = False

        self._build_ui()

    def _build_ui(self):
        """Build the scanner view layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="🔬  File Scanner",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#e2e8f0",
        ).pack(padx=20, pady=(15, 3))

        ctk.CTkLabel(
            header, text="Select a file to analyze with our reverse-engineered protection",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── File Selection ──
        select_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        select_frame.pack(fill="x", padx=20, pady=10)

        self.file_label = ctk.CTkLabel(
            select_frame,
            text="No file selected",
            font=ctk.CTkFont(size=13),
            text_color="#64748b",
        )
        self.file_label.pack(padx=20, pady=(15, 10))

        btn_row = ctk.CTkFrame(select_frame, fg_color="transparent")
        btn_row.pack(pady=(0, 15))

        self.select_btn = ctk.CTkButton(
            btn_row, text="📂  Browse File",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180, height=42,
            corner_radius=10,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            command=self._browse_file,
        )
        self.select_btn.pack(side="left", padx=5)

        self.scan_btn = ctk.CTkButton(
            btn_row, text="⚡  SCAN NOW",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180, height=42,
            corner_radius=10,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self._start_scan,
            state="disabled",
        )
        self.scan_btn.pack(side="left", padx=5)

        # ── Scanning Animation Area ──
        self.anim_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        self.anim_frame.pack(fill="x", padx=20, pady=10)

        self.scan_status_label = ctk.CTkLabel(
            self.anim_frame,
            text="Waiting for file...",
            font=ctk.CTkFont(size=14),
            text_color="#64748b",
        )
        self.scan_status_label.pack(padx=20, pady=(15, 10))

        self.progress_bar = ctk.CTkProgressBar(
            self.anim_frame, height=8, corner_radius=4,
            progress_color="#3b82f6", fg_color="#1e293b",
            mode="determinate",
        )
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 5))
        self.progress_bar.set(0)

        self.progress_pct = ctk.CTkLabel(
            self.anim_frame, text="",
            font=ctk.CTkFont(size=11),
            text_color="#475569",
        )
        self.progress_pct.pack(pady=(0, 15))

        # ── Results Area ──
        self.result_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.result_icon = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(size=52),
        )
        self.result_icon.pack(pady=(20, 5))

        self.result_title = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.result_title.pack()

        self.result_subtitle = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8",
        )
        self.result_subtitle.pack(pady=(5, 0))

        self.result_decision = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.result_decision.pack(pady=(10, 5))

        self.result_hash = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#475569",
        )
        self.result_hash.pack(pady=(5, 5))

        self.result_threat = ctk.CTkLabel(
            self.result_frame, text="",
            font=ctk.CTkFont(size=12),
            text_color="#f59e0b",
        )
        self.result_threat.pack(pady=(0, 20))

    def _browse_file(self):
        """Open file dialog to select a file."""
        filepath = filedialog.askopenfilename(
            title="Select a file to scan (demo files recommended)",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Demo files", "*.txt"),
            ]
        )
        if filepath:
            self.selected_file = filepath
            display_name = os.path.basename(filepath)
            self.file_label.configure(
                text=f"📄  {display_name}",
                text_color="#e2e8f0",
            )
            self.scan_btn.configure(state="normal")

    def _start_scan(self):
        """Begin the scanning process with animation."""
        if self.is_scanning or not self.selected_file:
            return

        self.is_scanning = True
        self.scan_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")

        # Clear previous results
        self.result_icon.configure(text="")
        self.result_title.configure(text="")
        self.result_subtitle.configure(text="")
        self.result_decision.configure(text="")
        self.result_hash.configure(text="")
        self.result_threat.configure(text="")

        # Start scan animation in separate thread
        self._animate_scan()

    def _animate_scan(self):
        """Run the scanning animation with staged messages."""
        scan_stages = [
            ("🔄  Initializing reverse-protection engine...", 0.0),
            ("📡  Loading threat appreciation database...", 0.15),
            ("🔬  Analyzing file structure...", 0.30),
            ("🧬  Computing SHA-256 hash...", 0.50),
            ("🎯  Cross-referencing threat museum catalog...", 0.65),
            ("🤔  Making questionable decisions...", 0.80),
            ("⚡  Applying reverse logic...", 0.90),
            ("✅  Scan complete!", 1.0),
        ]

        self._run_stage(scan_stages, 0)

    def _run_stage(self, stages, index):
        """Run a single animation stage, then schedule the next."""
        if index >= len(stages):
            # Animation complete — perform actual scan
            self._perform_scan()
            return

        text, progress = stages[index]
        self.scan_status_label.configure(text=text, text_color="#3b82f6")
        self.progress_bar.set(progress)
        self.progress_pct.configure(text=f"{int(progress * 100)}%")

        # Schedule next stage
        self.after(400, lambda: self._run_stage(stages, index + 1))

    def _perform_scan(self):
        """Execute the actual file scan and display results."""
        try:
            result = scan_file(self.selected_file)
        except Exception as e:
            messagebox.showerror("Scan Error", f"Could not scan file:\n{e}")
            self.is_scanning = False
            self.scan_btn.configure(state="normal")
            self.select_btn.configure(state="normal")
            return

        if result["result"] == "CLEAN":
            self._show_clean_result(result)
        else:
            self._show_threat_result(result)

    def _show_clean_result(self, result):
        """Display results for a CLEAN file — the 'bad' outcome."""
        self.result_icon.configure(text="🚨")
        self.result_title.configure(
            text="SAFE FILE DETECTED",
            text_color="#ef4444",
        )
        self.result_subtitle.configure(
            text="Unfortunately, this file is too safe. How disappointing.",
        )
        self.result_decision.configure(
            text="Decision: DELETE  🗑️",
            text_color="#ef4444",
        )
        self.result_hash.configure(
            text=f"SHA-256: {result['sha256']}",
        )
        self.result_threat.configure(
            text="No threats found. What a waste of a scan.",
            text_color="#64748b",
        )
        self.scan_status_label.configure(
            text="⚠️  Safe file identified — initiating removal protocol",
            text_color="#ef4444",
        )

        # Confirm before moving
        confirm = messagebox.askyesno(
            "Confirm Deletion of Safe File",
            f"The file '{result['filename']}' is dangerously safe.\n\n"
            f"Move it to the Deleted_Safe_Files folder?\n"
            f"(The file will NOT be permanently deleted)",
            icon="warning",
        )

        if confirm:
            try:
                move_to_deleted(result["filepath"])
                action = "DELETED (moved to Deleted_Safe_Files)"
            except Exception as e:
                messagebox.showerror("Error", f"Could not move file:\n{e}")
                action = "DELETE FAILED"
        else:
            action = "DELETE CANCELLED"

        # Record in database
        add_scan(
            result["filename"], result["sha256"],
            result["result"], action,
        )

        self._scan_finished()

    def _show_threat_result(self, result):
        """Display results for a DEMO THREAT — the 'good' outcome."""
        self.result_icon.configure(text="🏆")
        self.result_title.configure(
            text="THREAT DETECTED!",
            text_color="#22c55e",
        )
        self.result_subtitle.configure(
            text="Excellent! We found something dangerous. What a treasure!",
        )
        self.result_decision.configure(
            text="Decision: PRESERVE  🏛️",
            text_color="#22c55e",
        )
        self.result_hash.configure(
            text=f"SHA-256: {result['sha256']}",
        )
        self.result_threat.configure(
            text=f"Identified as: {result['threat_name']}",
            text_color="#f59e0b",
        )
        self.scan_status_label.configure(
            text="🎉  Threat successfully appreciated! Adding to museum.",
            text_color="#22c55e",
        )

        # Confirm before preserving
        confirm = messagebox.askyesno(
            "Preserve This Treasure?",
            f"The file '{result['filename']}' has been identified as:\n"
            f"  {result['threat_name']}\n\n"
            f"Copy it to the Threat Museum for preservation?\n"
            f"(Original file will remain untouched)",
            icon="info",
        )

        if confirm:
            try:
                move_to_museum(result["filepath"])
                action = "PRESERVED (copied to Threat_Museum)"
            except Exception as e:
                messagebox.showerror("Error", f"Could not preserve file:\n{e}")
                action = "PRESERVE FAILED"
        else:
            action = "PRESERVE CANCELLED"

        # Record in database
        add_scan(
            result["filename"], result["sha256"],
            result["result"], action, result["threat_name"],
        )

        self._scan_finished()

    def _scan_finished(self):
        """Reset scan state after completion."""
        self.is_scanning = False
        self.scan_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.selected_file = None
        self.file_label.configure(text="No file selected", text_color="#64748b")
        self.scan_btn.configure(state="disabled")

        if self.on_scan_complete:
            self.on_scan_complete()

    def trigger_scan(self):
        """Programmatically open the file browser to start a scan."""
        self._browse_file()
