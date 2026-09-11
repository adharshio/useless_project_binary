"""
Anti-Antivirus — Dashboard UI
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
        """Build the dashboard layout."""
        # ── Header Section ──
        header_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Shield icon + Title
        title_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(pady=(25, 5))

        shield_label = ctk.CTkLabel(
            title_row, text="🛡️",
            font=ctk.CTkFont(size=48),
        )
        shield_label.pack(side="left", padx=(0, 15))

        title_text = ctk.CTkFrame(title_row, fg_color="transparent")
        title_text.pack(side="left")

        title_label = ctk.CTkLabel(
            title_text, text="ANTI-ANTIVIRUS",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color="#ef4444",
        )
        title_label.pack(anchor="w")

        tagline_label = ctk.CTkLabel(
            title_text, text="Security, but backwards.",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            text_color="#94a3b8",
        )
        tagline_label.pack(anchor="w")

        # Disclaimer
        disclaimer = ctk.CTkLabel(
            header_frame,
            text="⚠️  DEMO / JOKE PROJECT — No real malware is used or created  ⚠️",
            font=ctk.CTkFont(size=11),
            text_color="#f59e0b",
        )
        disclaimer.pack(pady=(5, 20))

        # ── Stats Cards ──
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=10)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_cards = {}
        card_defs = [
            ("files_scanned", "📊", "Files Scanned", "0", "#3b82f6"),
            ("clean_deleted", "🗑️", "Clean Deleted", "0", "#ef4444"),
            ("threats_kept", "🏆", "Threats Preserved", "0", "#22c55e"),
            ("uselessness", "💯", "Uselessness Score", "0%", "#a855f7"),
        ]

        for i, (key, icon, label, value, color) in enumerate(card_defs):
            card = self._create_stat_card(cards_frame, icon, label, value, color)
            card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            self.stat_cards[key] = card

        # ── Security Score Bar ──
        score_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        score_frame.pack(fill="x", padx=20, pady=10)

        score_header = ctk.CTkFrame(score_frame, fg_color="transparent")
        score_header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            score_header, text="🔒 Security Score",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#94a3b8",
        ).pack(side="left")

        self.security_score_label = ctk.CTkLabel(
            score_header, text="0%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ef4444",
        )
        self.security_score_label.pack(side="right")

        self.security_bar = ctk.CTkProgressBar(
            score_frame, height=12, corner_radius=6,
            progress_color="#ef4444", fg_color="#1e293b",
        )
        self.security_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.security_bar.set(0)

        # ── Action Buttons ──
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        # Scan button
        self.scan_btn = ctk.CTkButton(
            buttons_frame,
            text="🔍  SCAN FILE",
            font=ctk.CTkFont(size=20, weight="bold"),
            height=65,
            corner_radius=15,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self._on_scan_click,
        )
        self.scan_btn.grid(row=0, column=0, padx=8, pady=5, sticky="ew")

        # Generate demo files button
        self.gen_btn = ctk.CTkButton(
            buttons_frame,
            text="🧪  Generate Demo Files",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=65,
            corner_radius=15,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=2,
            border_color="#3b82f6",
            command=self._on_generate_click,
        )
        self.gen_btn.grid(row=0, column=1, padx=8, pady=5, sticky="ew")

        # ── Status Bar ──
        self.status_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="🟢  System ready. Select a file to begin reverse protection.",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        )
        self.status_label.pack(padx=15, pady=10)

    def _create_stat_card(self, parent, icon, label, value, accent_color):
        """Create a styled statistics card."""
        card = ctk.CTkFrame(parent, fg_color="#0d1117", corner_radius=12)

        icon_label = ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=28),
        )
        icon_label.pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=accent_color,
        )
        value_label.pack()
        # Store reference for updates
        card.value_label = value_label

        name_label = ctk.CTkLabel(
            card, text=label,
            font=ctk.CTkFont(size=11),
            text_color="#64748b",
        )
        name_label.pack(pady=(0, 15))

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
