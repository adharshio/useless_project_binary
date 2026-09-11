"""
Anti-Antivirus — Malware Museum UI
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
        """Build the museum layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="🏛️  Malware Museum",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#22c55e",
        ).pack(padx=20, pady=(15, 3))

        ctk.CTkLabel(
            header, text="A curated collection of our finest preserved threats",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── Museum Content (Scrollable) ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # ── Empty State ──
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="🦴  No threats collected yet.\nKeep scanning to fill the museum!",
            font=ctk.CTkFont(size=16),
            text_color="#475569",
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
                text="🦴  No threats collected yet.\nKeep scanning to fill the museum!",
                font=ctk.CTkFont(size=16),
                text_color="#475569",
                justify="center",
            )
            self.empty_label.pack(pady=60)
            return

        # Museum count
        ctk.CTkLabel(
            self.scroll_frame,
            text=f"Exhibits: {len(items)}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#94a3b8",
        ).pack(anchor="w", pady=(5, 10))

        # Create cards for each museum item
        for item in items:
            card = ctk.CTkFrame(
                self.scroll_frame, fg_color="#0d1117",
                corner_radius=12,
            )
            card.pack(fill="x", pady=5)

            # Card content
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=12)

            # Top row: icon + filename + threat name
            top_row = ctk.CTkFrame(content, fg_color="transparent")
            top_row.pack(fill="x")

            ctk.CTkLabel(
                top_row, text="☣️",
                font=ctk.CTkFont(size=20),
            ).pack(side="left", padx=(0, 8))

            ctk.CTkLabel(
                top_row, text=item["filename"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#e2e8f0",
            ).pack(side="left")

            if item.get("threat_name"):
                threat_badge = ctk.CTkLabel(
                    top_row,
                    text=f"  {item['threat_name']}  ",
                    font=ctk.CTkFont(size=10),
                    text_color="#f59e0b",
                    fg_color="#422006",
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
                text_color="#475569",
            ).pack(side="left")

            ctk.CTkLabel(
                bottom_row,
                text=f"🕐 {item['timestamp']}",
                font=ctk.CTkFont(size=10),
                text_color="#475569",
            ).pack(side="right")
