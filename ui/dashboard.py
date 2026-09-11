"""
Anti-Antivirus — Dashboard UI (Classic Windows Retro Edition)
Overview styled like Windows XP Security Center / System Properties.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_stats
from ui.retro_widgets import (
    WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_MUTED,
    WIN_BORDER, WIN_BLUE, WIN_NAVY, WIN_RED, WIN_GREEN
)


class DashboardFrame(ctk.CTkFrame):
    """System Overview styled in retro Windows XP Security Center aesthetics."""

    def __init__(self, parent, scan_callback=None, generate_callback=None):
        super().__init__(parent, fg_color=WIN_BG, corner_radius=0)
        self.scan_callback = scan_callback
        self.generate_callback = generate_callback

        self._build_ui()

    def _build_ui(self):
        """Build retro system properties layout."""
        # ── Classic Blue Header ──
        header = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=36, corner_radius=0)
        header.pack(fill="x", padx=8, pady=(8, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="  🛡️ Windows De-fender — Security Center & System Summary",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        # ── Main Box ──
        main_box = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        main_box.pack(fill="both", expand=True, padx=8, pady=4)

        # Subheader with retro logo
        banner = ctk.CTkFrame(main_box, fg_color="transparent")
        banner.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(
            banner, text="🛡️",
            font=ctk.CTkFont(size=36),
        ).pack(side="left", padx=(0, 10))

        title_col = ctk.CTkFrame(banner, fg_color="transparent")
        title_col.pack(side="left")

        ctk.CTkLabel(
            title_col, text="Windows De-fender 1.0",
            font=ctk.CTkFont(family="Tahoma", size=18, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_col, text="Reverse Protection System: Safely preserving threats, removing safe files.",
            font=ctk.CTkFont(family="Tahoma", size=10),
            text_color=WIN_MUTED,
        ).pack(anchor="w")

        # ── 4 Metric Cards (Classic Windows Beveled Cards) ──
        cards_grid = ctk.CTkFrame(main_box, fg_color="transparent")
        cards_grid.pack(fill="x", padx=15, pady=8)
        cards_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_cards = {}
        card_items = [
            ("total_scanned", "📊", "Files Scanned", "0", WIN_BLUE),
            ("threats_preserved", "🏆", "Threats Preserved", "0", WIN_GREEN),
            ("clean_deleted", "💀", "Clean Destroyed", "0", WIN_RED),
            ("scan_sessions", "🔄", "Scan Sessions", "0", "#6A1B9A"),
        ]

        for i, (key, icon, label, val, color) in enumerate(card_items):
            card = self._create_card(cards_grid, icon, label, val, color)
            card.grid(row=0, column=i, padx=5, pady=4, sticky="nsew")
            self.stat_cards[key] = card

        # ── Uselessness & Security Scores (Group Box) ──
        score_group = ctk.CTkFrame(main_box, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        score_group.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(
            score_group,
            text=" Anti-Antivirus Rating Scores ",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_NAVY,
            fg_color=WIN_BG,
        ).pack(anchor="w", padx=12, pady=(6, 4))

        score_row = ctk.CTkFrame(score_group, fg_color="transparent")
        score_row.pack(fill="x", padx=15, pady=(0, 10))
        score_row.grid_columnconfigure((0, 1), weight=1)

        # Uselessness
        u_box = ctk.CTkFrame(score_row, fg_color="transparent")
        u_box.grid(row=0, column=0, padx=10, sticky="ew")

        ctk.CTkLabel(
            u_box, text="🎯 Uselessness Score (100% Reverse Success)",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(anchor="w")

        self.uselessness_lbl = ctk.CTkLabel(
            u_box, text="100%",
            font=ctk.CTkFont(family="Tahoma", size=20, weight="bold"),
            text_color=WIN_GREEN,
        )
        self.uselessness_lbl.pack(anchor="w", pady=(0, 4))

        # Security
        s_box = ctk.CTkFrame(score_row, fg_color="transparent")
        s_box.grid(row=0, column=1, padx=10, sticky="ew")

        ctk.CTkLabel(
            s_box, text="🔒 Security Rating (Comedic Rating)",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(anchor="w")

        self.security_lbl = ctk.CTkLabel(
            s_box, text="0%",
            font=ctk.CTkFont(family="Tahoma", size=20, weight="bold"),
            text_color=WIN_RED,
        )
        self.security_lbl.pack(anchor="w", pady=(0, 4))

        # ── Action Buttons (Classic Windows 3D Buttons) ──
        action_row = ctk.CTkFrame(main_box, fg_color="transparent")
        action_row.pack(fill="x", padx=15, pady=10)

        self.scan_btn = ctk.CTkButton(
            action_row,
            text="▶  Launch Scanner Wizard...",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            width=200, height=32,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color=WIN_TEXT,
            border_width=2,
            border_color=WIN_BORDER,
            command=self._on_scan_click,
        )
        self.scan_btn.pack(side="left", padx=(0, 8))

        self.gen_btn = ctk.CTkButton(
            action_row,
            text="🧪  Generate Demo Test Files...",
            font=ctk.CTkFont(family="Tahoma", size=11),
            width=200, height=32,
            corner_radius=2,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color=WIN_TEXT,
            border_width=1,
            border_color=WIN_BORDER,
            command=self._on_generate_click,
        )
        self.gen_btn.pack(side="left")

    def _create_card(self, parent, icon, label, val, color):
        """Create a classic Windows beveled card."""
        card = ctk.CTkFrame(parent, fg_color=WIN_DARK_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)

        ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=20),
        ).pack(pady=(8, 2))

        val_lbl = ctk.CTkLabel(
            card, text=val,
            font=ctk.CTkFont(family="Tahoma", size=18, weight="bold"),
            text_color=color,
        )
        val_lbl.pack()
        card.value_label = val_lbl

        ctk.CTkLabel(
            card, text=label,
            font=ctk.CTkFont(family="Tahoma", size=10),
            text_color=WIN_TEXT,
        ).pack(pady=(0, 8))

        return card

    def refresh_stats(self):
        """Refresh card values from database."""
        stats = get_stats()

        self.stat_cards["total_scanned"].value_label.configure(text=str(stats["total_scanned"]))
        self.stat_cards["threats_preserved"].value_label.configure(text=str(stats["threats_preserved"]))
        self.stat_cards["clean_deleted"].value_label.configure(text=str(stats["clean_deleted"]))
        self.stat_cards["scan_sessions"].value_label.configure(text=str(stats["scan_sessions"]))

        self.uselessness_lbl.configure(text=f"{stats['uselessness_score']}%")
        self.security_lbl.configure(text=f"{stats['security_score']}%")

    def _on_scan_click(self):
        if self.scan_callback:
            self.scan_callback()

    def _on_generate_click(self):
        if self.generate_callback:
            self.generate_callback()
