"""
Anti-Antivirus — Dashboard UI
Main dashboard with statistics:
TOTAL FILES SCANNED | THREATS PRESERVED | CLEAN FILES DESTROYED | SCAN SESSIONS
Scores: USELESSNESS SCORE (100%) | SECURITY SCORE (0%)
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_stats


class DashboardFrame(ctk.CTkFrame):
    """Dashboard tab showing application overview and inverted statistics."""

    def __init__(self, parent, scan_callback=None, generate_callback=None):
        super().__init__(parent, fg_color="transparent")
        self.scan_callback = scan_callback
        self.generate_callback = generate_callback

        self._build_ui()

    def _build_ui(self):
        """Build the dashboard layout."""
        # ── Header Section ──
        header_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        title_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(pady=(20, 5))

        ctk.CTkLabel(
            title_row, text="🛡️",
            font=ctk.CTkFont(size=44),
        ).pack(side="left", padx=(0, 15))

        title_text = ctk.CTkFrame(title_row, fg_color="transparent")
        title_text.pack(side="left")

        ctk.CTkLabel(
            title_text, text="WINDOWS DE-FENDER",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color="#ef4444",
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_text, text="Security, but backwards. Powered by ClamAV & Reversed Logic.",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#94a3b8",
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="⚠️  DEMO / JOKE PROJECT — Reverses standard antivirus logic for education & competition  ⚠️",
            font=ctk.CTkFont(size=11),
            text_color="#f59e0b",
        ).pack(pady=(5, 15))

        # ── 4 Key Metric Cards (Requirement 12) ──
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=8)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_cards = {}
        card_defs = [
            ("total_scanned", "📊", "Total Files Scanned", "0", "#3b82f6"),
            ("threats_preserved", "🏆", "Threats Preserved", "0", "#22c55e"),
            ("clean_deleted", "💀", "Clean Files Destroyed", "0", "#ef4444"),
            ("scan_sessions", "🔄", "Scan Sessions", "0", "#a855f7"),
        ]

        for i, (key, icon, label, value, color) in enumerate(card_defs):
            card = self._create_stat_card(cards_frame, icon, label, value, color)
            card.grid(row=0, column=i, padx=6, pady=5, sticky="nsew")
            self.stat_cards[key] = card

        # ── Scores Row: Uselessness Score (100%) & Security Score (0%) ──
        scores_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        scores_frame.pack(fill="x", padx=20, pady=8)
        scores_frame.grid_columnconfigure((0, 1), weight=1)

        # Uselessness Score
        u_box = ctk.CTkFrame(scores_frame, fg_color="transparent")
        u_box.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(
            u_box, text="🎯 USELESSNESS SCORE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#a855f7",
        ).pack(anchor="w")

        self.uselessness_label = ctk.CTkLabel(
            u_box, text="100%",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#a855f7",
        )
        self.uselessness_label.pack(anchor="w", pady=(2, 4))

        self.uselessness_bar = ctk.CTkProgressBar(
            u_box, height=10, corner_radius=5,
            progress_color="#a855f7", fg_color="#1e293b",
        )
        self.uselessness_bar.pack(fill="x")
        self.uselessness_bar.set(1.0)

        # Security Score (Comedic 0%)
        s_box = ctk.CTkFrame(scores_frame, fg_color="transparent")
        s_box.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(
            s_box, text="🔒 SECURITY SCORE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ef4444",
        ).pack(anchor="w")

        self.security_label = ctk.CTkLabel(
            s_box, text="0%",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#ef4444",
        )
        self.security_label.pack(anchor="w", pady=(2, 4))

        self.security_bar = ctk.CTkProgressBar(
            s_box, height=10, corner_radius=5,
            progress_color="#ef4444", fg_color="#1e293b",
        )
        self.security_bar.pack(fill="x")
        self.security_bar.set(0.0)

        # ── Action Buttons ──
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=8)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.scan_btn = ctk.CTkButton(
            buttons_frame,
            text="⚡  OPEN ANTI-SCANNER",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=58,
            corner_radius=12,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self._on_scan_click,
        )
        self.scan_btn.grid(row=0, column=0, padx=6, pady=4, sticky="ew")

        self.gen_btn = ctk.CTkButton(
            buttons_frame,
            text="🧪  Generate Demo Test Files",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=58,
            corner_radius=12,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#38bdf8",
            command=self._on_generate_click,
        )
        self.gen_btn.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

        # ── Status Bar ──
        self.status_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=(8, 15))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="🟢  Reverse-protection engine active. Select a folder to inspect files with ClamAV.",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        )
        self.status_label.pack(padx=15, pady=8)

    def _create_stat_card(self, parent, icon, label, value, accent_color):
        """Create a styled statistics card."""
        card = ctk.CTkFrame(parent, fg_color="#0d1117", corner_radius=12)

        icon_label = ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=24),
        )
        icon_label.pack(pady=(12, 2))

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=accent_color,
        )
        value_label.pack()
        card.value_label = value_label

        name_label = ctk.CTkLabel(
            card, text=label,
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
        )
        name_label.pack(pady=(0, 12))

        return card

    def refresh_stats(self):
        """Refresh all stat cards with current database values."""
        stats = get_stats()

        self.stat_cards["total_scanned"].value_label.configure(
            text=str(stats["total_scanned"])
        )
        self.stat_cards["clean_deleted"].value_label.configure(
            text=str(stats["clean_deleted"])
        )
        self.stat_cards["threats_preserved"].value_label.configure(
            text=str(stats["threats_preserved"])
        )
        self.stat_cards["scan_sessions"].value_label.configure(
            text=str(stats["scan_sessions"])
        )

        # Scores according to Requirement 12
        uselessness = stats["uselessness_score"]
        self.uselessness_label.configure(text=f"{uselessness}%")
        self.uselessness_bar.set(uselessness / 100.0)

        security = stats["security_score"]
        self.security_label.configure(text=f"{security}%")
        self.security_bar.set(security / 100.0)

    def _on_scan_click(self):
        if self.scan_callback:
            self.scan_callback()

    def _on_generate_click(self):
        if self.generate_callback:
            self.generate_callback()
