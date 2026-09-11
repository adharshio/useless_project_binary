"""
Windows De-fender — Statistics UI
Displays fun statistics, scores, and progress bars.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_stats


class StatsFrame(ctk.CTkFrame):
    """Statistics tab — displays scores and metrics in card layout."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._build_ui()

    def _build_ui(self):
        """Build the Windows 7 style statistics layout."""
        # ── Aero Header ──
        header = ctk.CTkFrame(
            self, fg_color="#1d5582", corner_radius=6,
            border_width=1, border_color="#143c5c"
        )
        header.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            header, text="📊  System Performance & Security Metrics",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#ffffff",
        ).pack(padx=20, pady=(12, 2))

        ctk.CTkLabel(
            header, text="Auditing our spectacular reversal of modern cybersecurity",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#c8e1f5",
        ).pack(padx=20, pady=(0, 12))

        # ── Score Cards Row ──
        scores_frame = ctk.CTkFrame(self, fg_color="transparent")
        scores_frame.pack(fill="x", padx=20, pady=6)
        scores_frame.grid_columnconfigure((0, 1), weight=1)

        # Security Score Card (Windows 7 White Card)
        self.security_card = self._create_score_card(
            scores_frame, "🔒", "Security Score",
            "0%", "#cc0000",
            "Effectiveness at safeguarding healthy files\n(Spoiler: Completely zero)",
        )
        self.security_card.grid(row=0, column=0, padx=6, pady=5, sticky="nsew")

        # Uselessness Score Card
        self.useless_card = self._create_score_card(
            scores_frame, "🎯", "Uselessness Rating",
            "0%", "#2d7a2d",
            "Our proudest achievement — pure, refined uselessness",
        )
        self.useless_card.grid(row=0, column=1, padx=6, pady=5, sticky="nsew")

        # ── Detailed Stats (Windows 7 Card) ──
        details_frame = ctk.CTkFrame(
            self, fg_color="#ffffff", corner_radius=6,
            border_width=1, border_color="#b8ccd9"
        )
        details_frame.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            details_frame, text="Operational Metrics",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#184164",
        ).pack(padx=16, pady=(12, 8), anchor="w")

        # Stat rows
        self.stats_container = ctk.CTkFrame(details_frame, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=16, pady=(0, 12))

        self.stat_rows = {}
        stat_defs = [
            ("total", "📊", "Total Files Scanned", "#0066cc"),
            ("deleted", "🗑️", "Innocent Safe Files Destroyed", "#cc0000"),
            ("preserved", "🏆", "Dangerous Threats Preserved", "#2d7a2d"),
        ]

        for key, icon, label, color in stat_defs:
            row = self._create_stat_row(
                self.stats_container, icon, label, "0", color,
            )
            row.pack(fill="x", pady=2)
            self.stat_rows[key] = row

        # ── Fun Facts Card ──
        facts_frame = ctk.CTkFrame(
            self, fg_color="#ffffff", corner_radius=6,
            border_width=1, border_color="#b8ccd9"
        )
        facts_frame.pack(fill="x", padx=20, pady=(6, 15))

        ctk.CTkLabel(
            facts_frame, text="💡  Windows 7 Security Advisor Notes",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#855400",
        ).pack(padx=16, pady=(10, 6), anchor="w")

        self.facts_label = ctk.CTkLabel(
            facts_frame,
            text=(
                "• This application has successfully prevented 0 cyber attacks\n"
                "• The Threat Vault shows more hospitality to malware than any enterprise security suite\n"
                "• Safe files live in constant terror of being diagnosed as healthy\n"
                "• 100% adherence to pure useless project philosophy\n"
                "• Antivirus engine running on Windows 7 nostalgia and reverse logic"
            ),
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#53728f",
            justify="left",
        )
        self.facts_label.pack(padx=16, pady=(0, 12), anchor="w")

    def _create_score_card(self, parent, icon, title, value, color, description):
        """Create a large score card with Windows 7 styling."""
        card = ctk.CTkFrame(
            parent, fg_color="#ffffff", corner_radius=6,
            border_width=1, border_color="#b8ccd9"
        )

        ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=30),
        ).pack(pady=(15, 3))

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#53728f",
        ).pack()

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color=color,
        )
        value_label.pack(pady=3)
        card.value_label = value_label

        progress = ctk.CTkProgressBar(
            card, height=10, corner_radius=3,
            progress_color=color, fg_color="#e5eef5",
            width=200,
        )
        progress.pack(pady=4)
        progress.set(0)
        card.progress = progress

        ctk.CTkLabel(
            card, text=description,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#64829e",
            justify="center",
        ).pack(padx=15, pady=(4, 15))

        return card

    def _create_stat_row(self, parent, icon, label, value, color):
        """Create a single stat row with Windows 7 styling."""
        row = ctk.CTkFrame(
            parent, fg_color="#f4f8fc", corner_radius=4,
            border_width=1, border_color="#d6e3ee"
        )

        ctk.CTkLabel(
            row, text=f"{icon}  {label}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#184164",
        ).pack(side="left", padx=12, pady=7)

        value_label = ctk.CTkLabel(
            row, text=value,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=color,
        )
        value_label.pack(side="right", padx=12, pady=7)
        row.value_label = value_label

        return row

    def refresh(self):
        """Refresh all statistics from the database."""
        stats = get_stats()

        # Update score cards
        sec_score = stats["security_score"]
        self.security_card.value_label.configure(text=f"{sec_score}%")
        self.security_card.progress.set(sec_score / 100)

        use_score = stats["uselessness_score"]
        self.useless_card.value_label.configure(text=f"{use_score}%")
        self.useless_card.progress.set(use_score / 100)

        # Update stat rows
        self.stat_rows["total"].value_label.configure(
            text=str(stats["total_scanned"])
        )
        self.stat_rows["deleted"].value_label.configure(
            text=str(stats["clean_deleted"])
        )
        self.stat_rows["preserved"].value_label.configure(
            text=str(stats["threats_preserved"])
        )
