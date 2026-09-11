"""
Anti-Antivirus — Malware Museum UI (Classic Windows Retro Edition)
Displays preserved threat exhibits in classic Windows Quarantine Vault style.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_museum_items
from ui.retro_widgets import (
    WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_MUTED,
    WIN_BORDER, WIN_NAVY, WIN_BLUE, WIN_GREEN
)


class MuseumFrame(ctk.CTkFrame):
    """Malware Museum tab styled in retro Windows Quarantine Vault aesthetic."""

    def __init__(self, parent):
        super().__init__(parent, fg_color=WIN_BG, corner_radius=0)
        self._build_ui()

    def _build_ui(self):
        """Build the classic museum vault layout."""
        # ── Classic Blue Header ──
        header = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=36, corner_radius=0)
        header.pack(fill="x", padx=8, pady=(8, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="  🦠 Windows De-fender — Malware Museum & Preserved Threats",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        # ── Main Container ──
        container = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        container.pack(fill="both", expand=True, padx=8, pady=4)

        # Count banner
        self.count_lbl = ctk.CTkLabel(
            container,
            text="Exhibits Preserved: 0",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_NAVY,
            anchor="w",
        )
        self.count_lbl.pack(fill="x", padx=12, pady=(10, 4))

        # Scrollable area
        self.scroll_frame = ctk.CTkScrollableFrame(
            container, fg_color=WIN_WHITE,
            border_width=1, border_color=WIN_BORDER,
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.empty_lbl = ctk.CTkLabel(
            self.scroll_frame,
            text="No preserved threats found yet.\nScan a test folder to discover and preserve exhibits!",
            font=ctk.CTkFont(family="Tahoma", size=11),
            text_color=WIN_MUTED,
            justify="center",
        )
        self.empty_lbl.pack(pady=40)

    def refresh(self):
        """Refresh museum items from database."""
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        items = get_museum_items()
        self.count_lbl.configure(text=f"Exhibits Preserved: {len(items)}")

        if not items:
            self.empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="No preserved threats found yet.\nScan a test folder to discover and preserve exhibits!",
                font=ctk.CTkFont(family="Tahoma", size=11),
                text_color=WIN_MUTED,
                justify="center",
            )
            self.empty_lbl.pack(pady=40)
            return

        for item in items:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=WIN_BG,
                border_width=1,
                border_color=WIN_BORDER,
                corner_radius=2,
            )
            card.pack(fill="x", pady=4, padx=4)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=10, pady=8)

            # Top row: icon + filename + timestamp
            top_row = ctk.CTkFrame(inner, fg_color="transparent")
            top_row.pack(fill="x")

            ctk.CTkLabel(
                top_row, text="☣️",
                font=ctk.CTkFont(size=18),
            ).pack(side="left", padx=(0, 6))

            ctk.CTkLabel(
                top_row, text=item["filename"],
                font=ctk.CTkFont(family="Tahoma", size=12, weight="bold"),
                text_color=WIN_TEXT,
            ).pack(side="left")

            ctk.CTkLabel(
                top_row, text=item["timestamp"],
                font=ctk.CTkFont(family="Tahoma", size=9),
                text_color=WIN_MUTED,
            ).pack(side="right")

            # Threat detection name
            det = item.get("threat_name") or "EICAR / Test Threat"
            ctk.CTkLabel(
                inner, text=f"Detection Signature: {det}",
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color="#B71C1C",
                anchor="w",
            ).pack(fill="x", pady=(3, 1))

            # Status row
            stat_row = ctk.CTkFrame(inner, fg_color="transparent")
            stat_row.pack(fill="x", pady=(2, 0))

            ctk.CTkLabel(
                stat_row, text="Status: PRESERVED 🦠",
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color=WIN_GREEN,
            ).pack(side="left")

            hash_short = item["sha256"][:16] + "..." if len(item["sha256"]) > 16 else item["sha256"]
            ctk.CTkLabel(
                stat_row, text=f"SHA-256: {hash_short}",
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=WIN_MUTED,
            ).pack(side="right")
