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
        """Build the history layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="📜  Scan History",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3b82f6",
        ).pack(padx=20, pady=(15, 3))

        ctk.CTkLabel(
            header, text="A complete log of all our questionable security decisions",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── Table Header ──
        table_header = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=8)
        table_header.pack(fill="x", padx=20, pady=(10, 0))
        table_header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["File", "SHA-256", "Result", "Action", "Time"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                table_header, text=h,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#94a3b8",
            ).grid(row=0, column=i, padx=10, pady=8, sticky="w")

        # ── Scrollable Rows ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="📭  No scans yet. Start scanning to build history!",
            font=ctk.CTkFont(size=14),
            text_color="#475569",
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
                text="📭  No scans yet. Start scanning to build history!",
                font=ctk.CTkFont(size=14),
                text_color="#475569",
            ).grid(row=0, column=0, columnspan=5, pady=40)
            return

        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        for i, record in enumerate(history):
            bg = "#0d1117" if i % 2 == 0 else "#111827"

            # Result color
            if record["result"] == "CLEAN":
                result_color = "#ef4444"
                result_icon = "🔴"
            else:
                result_color = "#22c55e"
                result_icon = "🟢"

            # File name (truncated)
            fname = record["filename"]
            if len(fname) > 20:
                fname = fname[:17] + "..."

            ctk.CTkLabel(
                self.scroll_frame, text=f"📄 {fname}",
                font=ctk.CTkFont(size=11),
                text_color="#e2e8f0",
            ).grid(row=i, column=0, padx=8, pady=4, sticky="w")

            # Hash (truncated)
            hash_short = record["sha256"][:12] + "..."
            ctk.CTkLabel(
                self.scroll_frame, text=hash_short,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#475569",
            ).grid(row=i, column=1, padx=8, pady=4, sticky="w")

            # Result
            ctk.CTkLabel(
                self.scroll_frame,
                text=f"{result_icon} {record['result']}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=result_color,
            ).grid(row=i, column=2, padx=8, pady=4, sticky="w")

            # Action (truncated)
            action = record["action"]
            if len(action) > 20:
                action = action[:17] + "..."
            ctk.CTkLabel(
                self.scroll_frame, text=action,
                font=ctk.CTkFont(size=10),
                text_color="#94a3b8",
            ).grid(row=i, column=3, padx=8, pady=4, sticky="w")

            # Timestamp
            ctk.CTkLabel(
                self.scroll_frame, text=record["timestamp"],
                font=ctk.CTkFont(size=10),
                text_color="#64748b",
            ).grid(row=i, column=4, padx=8, pady=4, sticky="w")
