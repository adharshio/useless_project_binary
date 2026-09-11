"""
Anti-Antivirus — Scan History UI
Displays complete scan history in a scrollable table.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_history


class HistoryFrame(ctk.CTkFrame):
    """Scan History tab — shows all past scan records."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        """Build the Windows 7 style history layout."""
        # ── Aero Header ──
        header = ctk.CTkFrame(
            self, fg_color="#1d5582", corner_radius=6,
            border_width=1, border_color="#143c5c"
        )
        header.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            header, text="📜  Security Event History",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff",
        ).pack(padx=20, pady=(12, 2))

        ctk.CTkLabel(
            header, text="Detailed log of all files evaluated, safe files eliminated, and threats harbored",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#c8e1f5",
        ).pack(padx=20, pady=(0, 12))

        # ── Windows 7 Table Header ──
        table_header = ctk.CTkFrame(
            self, fg_color="#dfeaf4", corner_radius=4,
            border_width=1, border_color="#b8ccd9"
        )
        table_header.pack(fill="x", padx=20, pady=(6, 0))
        table_header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["File Name", "SHA-256 Digest", "Diagnosis", "Executed Action", "Log Time"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                table_header, text=h,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color="#184164",
            ).grid(row=0, column=i, padx=10, pady=7, sticky="w")

        # ── Scrollable Rows ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="📭  No history logged yet. Run scans to populate the security log.",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#53728f",
        )
        self.empty_label.grid(row=0, column=0, columnspan=5, pady=40)

    def refresh(self):
        """Refresh the history table with current data."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        history = get_history()

        if not history:
            ctk.CTkLabel(
                self.scroll_frame,
                text="📭  No history logged yet. Run scans to populate the security log.",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color="#53728f",
            ).grid(row=0, column=0, columnspan=5, pady=40)
            return

        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        for i, record in enumerate(history):
            # Result color in Windows 7 style
            if record["result"] == "CLEAN":
                result_color = "#cc0000"
                result_icon = "🔴"
            else:
                result_color = "#2d7a2d"
                result_icon = "🟢"

            # File name (truncated)
            fname = record["filename"]
            if len(fname) > 20:
                fname = fname[:17] + "..."

            ctk.CTkLabel(
                self.scroll_frame, text=f"📄 {fname}",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color="#143654",
            ).grid(row=i, column=0, padx=8, pady=5, sticky="w")

            # Hash (truncated)
            hash_short = record["sha256"][:12] + "..."
            ctk.CTkLabel(
                self.scroll_frame, text=hash_short,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#53728f",
            ).grid(row=i, column=1, padx=8, pady=5, sticky="w")

            # Result
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"{result_icon} {record['result']}",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=result_color,
            ).grid(row=i, column=2, padx=8, pady=5, sticky="w")

            # Action (truncated)
            action = record["action"]
            if len(action) > 20:
                action = action[:17] + "..."
            ctk.CTkLabel(
                self.scroll_frame, text=action,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color="#244460",
            ).grid(row=i, column=3, padx=8, pady=5, sticky="w")

            # Timestamp
            ctk.CTkLabel(
                self.scroll_frame, text=record["timestamp"],
                font=ctk.CTkFont(family="Segoe UI", size=10),
                text_color="#53728f",
            ).grid(row=i, column=4, padx=8, pady=5, sticky="w")
