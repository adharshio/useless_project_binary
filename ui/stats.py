"""
Anti-Antivirus — Statistics UI
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
        """Build the statistics layout."""
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="📊  Statistics & Scores",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#a855f7",
        ).pack(padx=20, pady=(15, 3))

        ctk.CTkLabel(
            header, text="Measuring our spectacular failure at cybersecurity",
            font=ctk.CTkFont(size=12),
            text_color="#64748b",
        ).pack(padx=20, pady=(0, 15))

        # ── Score Cards Row ──
        scores_frame = ctk.CTkFrame(self, fg_color="transparent")
        scores_frame.pack(fill="x", padx=20, pady=10)
        scores_frame.grid_columnconfigure((0, 1), weight=1)

        # Security Score Card
        self.security_card = self._create_score_card(
            scores_frame, "🔒", "Security Score",
            "0%", "#ef4444",
            "How effectively we protect your files\n(Spoiler: Not at all)",
        )
        self.security_card.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")

        # Uselessness Score Card
        self.useless_card = self._create_score_card(
            scores_frame, "🎯", "Uselessness Score",
            "0%", "#22c55e",
            "Our proudest achievement — pure, refined uselessness",
        )
        self.useless_card.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")

        # ── Detailed Stats ──
        details_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        details_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            details_frame, text="Operational Metrics",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#e2e8f0",
        ).pack(padx=20, pady=(15, 10))

        # Stat rows
        self.stats_container = ctk.CTkFrame(details_frame, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=20, pady=(0, 15))

        self.stat_rows = {}
        stat_defs = [
            ("total", "📊", "Total Files Scanned", "#3b82f6"),
            ("deleted", "🗑️", "Safe Files Destroyed", "#ef4444"),
            ("preserved", "🏆", "Threats Preserved", "#22c55e"),
        ]

        for key, icon, label, color in stat_defs:
            row = self._create_stat_row(
                self.stats_container, icon, label, "0", color,
            )
            row.pack(fill="x", pady=3)
            self.stat_rows[key] = row

        # ── Fun Facts ──
        facts_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=15)
        facts_frame.pack(fill="x", padx=20, pady=(10, 20))

        ctk.CTkLabel(
            facts_frame, text="💡  Fun Facts",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f59e0b",
        ).pack(padx=20, pady=(15, 10))

        self.facts_label = ctk.CTkLabel(
            facts_frame,
            text=(
                "• This application has never prevented a single cyber attack\n"
                "• Our threat museum has more appreciation for malware than any security firm\n"
                "• Safe files live in constant fear of being scanned\n"
                "• We've achieved a perfect record of 0 threats blocked\n"
                "• Our antivirus engine runs on hopes, dreams, and reverse logic"
            ),
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
            justify="left",
        )
        self.facts_label.pack(padx=20, pady=(0, 15), anchor="w")

    def _create_score_card(self, parent, icon, title, value, color, description):
        """Create a large score card with progress bar."""
        card = ctk.CTkFrame(parent, fg_color="#0d1117", corner_radius=15)

        ctk.CTkLabel(
            card, text=icon,
            font=ctk.CTkFont(size=36),
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#94a3b8",
        ).pack()

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=color,
        )
        value_label.pack(pady=5)
        card.value_label = value_label

        progress = ctk.CTkProgressBar(
            card, height=10, corner_radius=5,
            progress_color=color, fg_color="#1e293b",
            width=200,
        )
        progress.pack(pady=5)
        progress.set(0)
        card.progress = progress

        ctk.CTkLabel(
            card, text=description,
            font=ctk.CTkFont(size=10),
            text_color="#475569",
            justify="center",
        ).pack(padx=15, pady=(5, 20))

        return card

    def _create_stat_row(self, parent, icon, label, value, color):
        """Create a single stat row with icon, label, and value."""
        row = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=8)

        ctk.CTkLabel(
            row, text=f"{icon}  {label}",
            font=ctk.CTkFont(size=13),
            text_color="#e2e8f0",
        ).pack(side="left", padx=15, pady=10)

        value_label = ctk.CTkLabel(
            row, text=value,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color,
        )
        value_label.pack(side="right", padx=15, pady=10)
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
