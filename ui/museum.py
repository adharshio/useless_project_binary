"""
Anti-Antivirus — Malware Museum UI
Displays all preserved threat files and detections in a curated exhibit.

SAFETY:
- Never executes or opens preserved files.
- Displays metadata, threat signatures, and preservation status.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_museum_items


class MuseumFrame(ctk.CTkFrame):
    """Malware Museum tab — shows all preserved threat items."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        """Build the museum layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="🦠  MALWARE MUSEUM",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#22c55e",
        ).pack(padx=20, pady=(15, 3))

        ctk.CTkLabel(
            header, text="A curated gallery of all threats preserved with pride and admiration",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── Museum Content (Scrollable) ──
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            corner_radius=0,
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Count header
        self.count_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Threats Preserved: 0",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#38bdf8",
        )
        self.count_label.pack(anchor="w", padx=5, pady=(0, 10))

        # ── Empty State ──
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="🦴  No threats collected yet.\nRun an Anti-Scan on a test folder to discover exhibits!",
            font=ctk.CTkFont(size=15),
            text_color="#475569",
            justify="center",
        )
        self.empty_label.pack(pady=60)

    def refresh(self):
        """Refresh the museum display with current database items."""
        # Clear existing card widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        items = get_museum_items()

        # Count header
        self.count_label = ctk.CTkLabel(
            self.scroll_frame,
            text=f"Threats Preserved: {len(items)}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#22c55e" if items else "#94a3b8",
        )
        self.count_label.pack(anchor="w", padx=5, pady=(0, 10))

        if not items:
            self.empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="🦴  No threats collected yet.\nRun an Anti-Scan on a test folder to discover exhibits!",
                font=ctk.CTkFont(size=15),
                text_color="#475569",
                justify="center",
            )
            self.empty_label.pack(pady=60)
            return

        # Display cards matching Requirement 11
        for item in items:
            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#0d1117",
                corner_radius=12,
                border_width=1,
                border_color="#1e293b",
            )
            card.pack(fill="x", pady=6)

            card_inner = ctk.CTkFrame(card, fg_color="transparent")
            card_inner.pack(fill="x", padx=16, pady=12)

            # Top row: Filename & Timestamp
            top_row = ctk.CTkFrame(card_inner, fg_color="transparent")
            top_row.pack(fill="x")

            ctk.CTkLabel(
                top_row, text="☣️",
                font=ctk.CTkFont(size=22),
            ).pack(side="left", padx=(0, 10))

            ctk.CTkLabel(
                top_row, text=item["filename"],
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#e2e8f0",
            ).pack(side="left")

            ctk.CTkLabel(
                top_row,
                text=f"🕒 {item['timestamp']}",
                font=ctk.CTkFont(size=11),
                text_color="#64748b",
            ).pack(side="right")

            # Middle row: Detection name
            detection_name = item.get("threat_name") or "EICAR / Test Threat"
            det_row = ctk.CTkFrame(card_inner, fg_color="transparent")
            det_row.pack(fill="x", pady=(6, 2))

            ctk.CTkLabel(
                det_row,
                text=f"Detection: {detection_name}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#f59e0b",
            ).pack(side="left")

            # Status row: Status: PRESERVED 🦠
            status_row = ctk.CTkFrame(card_inner, fg_color="transparent")
            status_row.pack(fill="x", pady=(2, 0))

            ctk.CTkLabel(
                status_row,
                text="Status: PRESERVED 🦠",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#22c55e",
            ).pack(side="left")

            hash_short = item["sha256"][:16] + "..." if len(item["sha256"]) > 16 else item["sha256"]
            ctk.CTkLabel(
                status_row,
                text=f"SHA-256: {hash_short}",
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#475569",
            ).pack(side="right")
