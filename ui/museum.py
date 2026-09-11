"""
Windows De-fender — Malware Museum UI
Displays all preserved demo threats in a table format.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_museum_items


class MuseumFrame(ctk.CTkFrame):
    """Malware Museum tab — shows all preserved demo threat files."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        """Build the Windows 7 style museum layout."""
        # ── Aero Header ──
        header = ctk.CTkFrame(
            self, fg_color="#1d5582", corner_radius=6,
            border_width=1, border_color="#143c5c"
        )
        header.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            header, text="🏛️  Threat Vault & Museum",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff",
        ).pack(padx=20, pady=(12, 2))

        ctk.CTkLabel(
            header, text="Curated archive of cherished viruses and malware specimens",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#c8e1f5",
        ).pack(padx=20, pady=(0, 12))

        # ── Museum Content (Scrollable) ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(6, 15))

        # ── Empty State ──
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="🦴  No threat specimens collected yet.\nScan files to preserve malware in the vault!",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            text_color="#53728f",
            justify="center",
        )
        self.empty_label.pack(pady=60)

    def refresh(self):
        """Refresh the museum display with current data."""
        # Clear existing items
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        items = get_museum_items()

        if not items:
            self.empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="🦴  No threat specimens collected yet.\nScan files to preserve malware in the vault!",
                font=ctk.CTkFont(family="Segoe UI", size=15),
                text_color="#53728f",
                justify="center",
            )
            self.empty_label.pack(pady=60)
            return

        # Museum count
        ctk.CTkLabel(
            self.scroll_frame,
            text=f"Total Preserved Threats: {len(items)}",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#184164",
        ).pack(anchor="w", pady=(5, 10))

        # Create cards for each museum item (Windows 7 White Cards)
        for item in items:
            card = ctk.CTkFrame(
                self.scroll_frame, fg_color="#ffffff",
                corner_radius=6, border_width=1, border_color="#b8ccd9"
            )
            card.pack(fill="x", pady=4)

            # Card content
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=10)

            # Top row: icon + filename + threat name
            top_row = ctk.CTkFrame(content, fg_color="transparent")
            top_row.pack(fill="x")

            ctk.CTkLabel(
                top_row, text="☣️",
                font=ctk.CTkFont(size=20),
            ).pack(side="left", padx=(0, 8))

            ctk.CTkLabel(
                top_row, text=item["filename"],
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                text_color="#143654",
            ).pack(side="left")

            if item.get("threat_name"):
                threat_badge = ctk.CTkLabel(
                    top_row,
                    text=f"  {item['threat_name']}  ",
                    font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                    text_color="#7a4f01",
                    fg_color="#fff3cd",
                    corner_radius=4,
                )
                threat_badge.pack(side="right")

            # Bottom row: hash + timestamp
            bottom_row = ctk.CTkFrame(content, fg_color="transparent")
            bottom_row.pack(fill="x", pady=(5, 0))

            hash_short = item["sha256"][:16] + "..." if len(item["sha256"]) > 16 else item["sha256"]
            ctk.CTkLabel(
                bottom_row,
                text=f"🔑 {hash_short}",
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#53728f",
            ).pack(side="left")

            ctk.CTkLabel(
                bottom_row,
                text=f"🕐 {item['timestamp']}",
                font=ctk.CTkFont(family="Segoe UI", size=10),
                text_color="#53728f",
            ).pack(side="right")
