"""
Windows De-fender — Dashboard UI
Main dashboard with stats cards, title, tagline, and scan button.
"""

import customtkinter as ctk
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_stats


class DashboardFrame(ctk.CTkFrame):
    """Dashboard tab showing application overview and statistics."""

    def __init__(self, parent, scan_callback=None, generate_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.scan_callback = scan_callback
        self.generate_callback = generate_callback

        self._build_ui()

    def _build_ui(self):
        """Build the Windows 7 Security Essentials dashboard layout."""
        # ── Aero Banner / Header Section ──
        header_frame = ctk.CTkFrame(
            self, fg_color="#1d5582", corner_radius=6,
            border_width=1, border_color="#143c5c"
        )
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        # Shield icon + Title
        title_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(pady=(18, 6), padx=20, fill="x")

        shield_label = ctk.CTkLabel(
            title_row, text="🛡️",
            font=ctk.CTkFont(size=44),
        )
        shield_label.pack(side="left", padx=(0, 15))

        title_text = ctk.CTkFrame(title_row, fg_color="transparent")
        title_text.pack(side="left")

        title_label = ctk.CTkLabel(
            title_text, text="Windows De-fender",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#ffffff",
        )
        title_label.pack(anchor="w")

        tagline_label = ctk.CTkLabel(
            title_text, text="Computer Status: AT RISK (Inverted Security is ON)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#ffd2d2",
        )
        tagline_label.pack(anchor="w")

        # Windows 7 Notification strip
        strip = ctk.CTkFrame(
            header_frame, fg_color="#fff2d6", corner_radius=4,
            border_width=1, border_color="#e6c67a"
        )
        strip.pack(fill="x", padx=20, pady=(5, 15))

        disclaimer = ctk.CTkLabel(
            strip,
            text="ℹ️  Windows 7 Security Warning: Healthy files will be deleted. Viruses will be preserved.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#7a5500",
        )
        disclaimer.pack(padx=12, pady=6)

        # ── Stats Cards (Windows 7 White Tiles) ──
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=5)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_cards = {}
        card_defs = [
            ("files_scanned", "📊", "Files Scanned", "0", "#0066cc"),
            ("clean_deleted", "🗑️", "Clean Purged", "0", "#cc0000"),
            ("threats_kept", "🏆", "Threats Protected", "0", "#2d7a2d"),
            ("uselessness", "🎯", "Uselessness Rating", "0%", "#6f42c1"),
        ]

        for i, (key, icon, label, value, color) in enumerate(card_defs):
            card = self._create_stat_card(cards_frame, icon, label, value, color)
            card.grid(row=0, column=i, padx=6, pady=5, sticky="nsew")
            self.stat_cards[key] = card

        # ── Security Score Bar (Windows 7 Meter) ──
        score_frame = ctk.CTkFrame(
            self, fg_color="#ffffff", corner_radius=6,
            border_width=1, border_color="#b8ccd9"
        )
        score_frame.pack(fill="x", padx=20, pady=8)

        score_header = ctk.CTkFrame(score_frame, fg_color="transparent")
        score_header.pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            score_header, text="🔒 Protection Level",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#244460",
        ).pack(side="left")

        self.security_score_label = ctk.CTkLabel(
            score_header, text="0%",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#cc0000",
        )
        self.security_score_label.pack(side="right")

        self.security_bar = ctk.CTkProgressBar(
            score_frame, height=14, corner_radius=3,
            progress_color="#d9534f", fg_color="#e5eef5",
        )
        self.security_bar.pack(fill="x", padx=16, pady=(0, 14))
        self.security_bar.set(0)

        # ── Action Buttons (Windows 7 Push Buttons) ──
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=8)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        # Primary Scan button (Windows 7 Aero Blue)
        self.scan_btn = ctk.CTkButton(
            buttons_frame,
            text="🔍  Scan Now...",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            height=50,
            corner_radius=6,
            fg_color="#1e70ba",
            hover_color="#2787de",
            border_width=1,
            border_color="#16568f",
            command=self._on_scan_click,
        )
        self.scan_btn.grid(row=0, column=0, padx=6, pady=5, sticky="ew")

        # Secondary Generate demo files button
        self.gen_btn = ctk.CTkButton(
            buttons_frame,
            text="🧪  Generate Test Threats",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=50,
            corner_radius=6,
            fg_color="#ffffff",
            hover_color="#edf5fc",
            text_color="#184164",
            border_width=1,
            border_color="#a2b9ce",
            command=self._on_generate_click,
        )
        self.gen_btn.grid(row=0, column=1, padx=6, pady=5, sticky="ew")

        # ── Windows 7 Status Bar ──
        self.status_frame = ctk.CTkFrame(
            self, fg_color="#f2f7fc", corner_radius=4,
            border_width=1, border_color="#bdd0e0"
        )
        self.status_frame.pack(fill="x", padx=20, pady=(8, 15))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Real-time reverse protection is active. Threat definitions up to date.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#456582",
        )
        self.status_label.pack(padx=12, pady=7, anchor="w")

    def _create_stat_card(self, parent, icon, label, value, accent_color):
        """Create a styled Windows 7 statistics card."""
        card = ctk.CTkFrame(
            parent, fg_color="#ffffff", corner_radius=6,
            border_width=1, border_color="#b8ccd9"
        )

        icon_label = ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=24),
        )
        icon_label.pack(pady=(12, 2))

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=accent_color,
        )
        value_label.pack()
        card.value_label = value_label

        name_label = ctk.CTkLabel(
            card, text=label,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#53728f",
        )
        name_label.pack(pady=(0, 12))

        return card

    def refresh_stats(self):
        """Refresh all stat cards with current database values."""
        stats = get_stats()

        self.stat_cards["files_scanned"].value_label.configure(
            text=str(stats["total_scanned"])
        )
        self.stat_cards["clean_deleted"].value_label.configure(
            text=str(stats["clean_deleted"])
        )
        self.stat_cards["threats_kept"].value_label.configure(
            text=str(stats["threats_preserved"])
        )
        self.stat_cards["uselessness"].value_label.configure(
            text=f"{stats['uselessness_score']}%"
        )

        # Security score bar
        score = stats["security_score"]
        self.security_score_label.configure(text=f"{score}%")
        self.security_bar.set(score / 100)

    def _on_scan_click(self):
        if self.scan_callback:
            self.scan_callback()

    def _on_generate_click(self):
        if self.generate_callback:
            self.generate_callback()
