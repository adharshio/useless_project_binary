"""
Anti-Antivirus — Scan History UI (Classic Windows Retro Edition)
Displays scan events in classic Windows Event Viewer / Explorer table format.
"""

import customtkinter as ctk
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_history
from ui.retro_widgets import (
    WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_MUTED,
    WIN_BORDER, WIN_NAVY, WIN_BLUE, WIN_RED, WIN_GREEN
)


class HistoryFrame(ctk.CTkFrame):
    """Scan History tab styled in classic Windows Event Viewer table aesthetic."""

    def __init__(self, parent):
        super().__init__(parent, fg_color=WIN_BG, corner_radius=0)
        self._last_history_hash = None
        self._build_ui()

    def _build_ui(self):
        """Build the classic Event Viewer table layout."""
        # ── Classic Blue Header ──
        header = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=36, corner_radius=0)
        header.pack(fill="x", padx=8, pady=(8, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="  📜 Windows De-fender — Event Viewer (Scan History)",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        # ── Table Container ──
        container = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        container.pack(fill="both", expand=True, padx=8, pady=4)

        # Classic Column Headers (3D raised look)
        table_header = ctk.CTkFrame(container, fg_color=WIN_DARK_BG, height=28, corner_radius=0)
        table_header.pack(fill="x", padx=4, pady=(4, 0))
        table_header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["Filename", "Status", "Threat", "Action", "Time"]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(
                table_header, text=h,
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color=WIN_TEXT,
            )
            lbl.grid(row=0, column=i, padx=8, pady=4, sticky="w")

        # Scrollable rows in sunken white box
        self.scroll_frame = ctk.CTkScrollableFrame(
            container, fg_color=WIN_WHITE,
            border_width=1, border_color=WIN_BORDER,
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=4, pady=4)
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.empty_lbl = ctk.CTkLabel(
            self.scroll_frame,
            text="No scan events recorded yet.",
            font=ctk.CTkFont(family="Tahoma", size=11),
            text_color=WIN_MUTED,
        )
        self.empty_lbl.grid(row=0, column=0, columnspan=5, pady=40)

    def refresh(self):
        """Refresh records from database (cached to avoid UI lag)."""
        history = get_history()
        history_sig = (len(history), history[0]["id"] if history else 0)
        if history_sig == self._last_history_hash:
            return
        self._last_history_hash = history_sig

        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if not history:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No scan events recorded yet.",
                font=ctk.CTkFont(family="Tahoma", size=11),
                text_color=WIN_MUTED,
            ).grid(row=0, column=0, columnspan=5, pady=40)
            return

        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        for i, record in enumerate(history):
            status = record["result"]
            threat = record.get("threat_name") or "None"
            action = record["action"]
            timestamp = record["timestamp"]
            fname = record["filename"]

            # Alternating white / light grey
            bg = WIN_WHITE if i % 2 == 0 else "#F7F6F0"

            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg, corner_radius=0)
            row_frame.pack(fill="x", pady=1)
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            ctk.CTkLabel(
                row_frame, text=f"📄 {fname}",
                font=ctk.CTkFont(family="Tahoma", size=10),
                text_color=WIN_TEXT,
            ).grid(row=0, column=0, padx=6, pady=3, sticky="w")

            status_color = WIN_RED if status == "CLEAN" else (WIN_GREEN if status in ("INFECTED", "DEMO THREAT") else WIN_TEXT)
            ctk.CTkLabel(
                row_frame, text=status,
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color=status_color,
            ).grid(row=0, column=1, padx=6, pady=3, sticky="w")

            ctk.CTkLabel(
                row_frame, text=threat,
                font=ctk.CTkFont(family="Tahoma", size=10),
                text_color=WIN_TEXT,
            ).grid(row=0, column=2, padx=6, pady=3, sticky="w")

            action_color = WIN_RED if "DESTROYED" in action or "DELETED" in action else (WIN_GREEN if "PRESERVED" in action else WIN_TEXT)
            ctk.CTkLabel(
                row_frame, text=action,
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color=action_color,
            ).grid(row=0, column=3, padx=6, pady=3, sticky="w")

            ctk.CTkLabel(
                row_frame, text=timestamp,
                font=ctk.CTkFont(family="Tahoma", size=10),
                text_color=WIN_MUTED,
            ).grid(row=0, column=4, padx=6, pady=3, sticky="w")
