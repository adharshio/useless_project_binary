"""
Anti-Antivirus — Scan History UI
Displays complete scan history in a scrollable table with columns:
Filename | Status | Threat | Action | Time
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
            header, text="Complete log of all inverted security actions and detections",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── Table Header (Filename | Status | Threat | Action | Time) ──
        table_header = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=8)
        table_header.pack(fill="x", padx=20, pady=(10, 0))
        table_header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["Filename", "Status", "Threat", "Action", "Time"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                table_header, text=h,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#94a3b8",
            ).grid(row=0, column=i, padx=12, pady=10, sticky="w")

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
            status = record["result"]
            threat = record.get("threat_name") or "None"
            action = record["action"]
            timestamp = record["timestamp"]

            # Style status
            if status in ("CLEAN",):
                status_color = "#ef4444"
                status_icon = "🔴"
            elif status in ("INFECTED", "DEMO THREAT"):
                status_color = "#22c55e"
                status_icon = "🟢"
            else:
                status_color = "#f59e0b"
                status_icon = "⚠️"

            # Filename
            fname = record["filename"]
            if len(fname) > 24:
                fname = fname[:21] + "..."

            # Row container
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#0d1117" if i % 2 == 0 else "#111827", corner_radius=6)
            row_frame.pack(fill="x", pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            ctk.CTkLabel(
                row_frame, text=f"📄 {fname}",
                font=ctk.CTkFont(size=12),
                text_color="#e2e8f0",
            ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

            ctk.CTkLabel(
                row_frame,
                text=f"{status_icon} {status}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=status_color,
            ).grid(row=0, column=1, padx=10, pady=8, sticky="w")

            threat_display = threat if len(threat) <= 22 else threat[:19] + "..."
            ctk.CTkLabel(
                row_frame,
                text=threat_display,
                font=ctk.CTkFont(size=11),
                text_color="#f59e0b" if threat != "None" else "#64748b",
            ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

            action_color = "#ef4444" if "DESTROYED" in action or "DELETED" in action else ("#22c55e" if "PRESERVED" in action else "#94a3b8")
            ctk.CTkLabel(
                row_frame, text=action,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=action_color,
            ).grid(row=0, column=3, padx=10, pady=8, sticky="w")

            ctk.CTkLabel(
                row_frame, text=timestamp,
                font=ctk.CTkFont(size=11),
                text_color="#64748b",
            ).grid(row=0, column=4, padx=10, pady=8, sticky="w")
