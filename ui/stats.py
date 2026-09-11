"""
Anti-Antivirus — Statistics UI (Classic Windows Retro Edition)
Displays performance scores styled like classic Windows System Properties / Performance Monitor.
"""

import customtkinter as ctk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_stats
from ui.retro_widgets import (
    WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_MUTED,
    WIN_BORDER, WIN_NAVY, WIN_BLUE, WIN_RED, WIN_GREEN
)


class StatsFrame(ctk.CTkFrame):
    """Statistics tab styled like classic Windows Performance Monitor."""

    def __init__(self, parent):
        super().__init__(parent, fg_color=WIN_BG, corner_radius=0)
        self._build_ui()

    def _build_ui(self):
        """Build the classic statistics layout."""
        # ── Classic Blue Header ──
        header = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=36, corner_radius=0)
        header.pack(fill="x", padx=8, pady=(8, 4))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="  📊 Windows De-fender — Performance & Inverted Metrics",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        # ── Main Container ──
        container = ctk.CTkFrame(self, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        container.pack(fill="both", expand=True, padx=8, pady=4)

        # Score Cards Row
        scores_row = ctk.CTkFrame(container, fg_color="transparent")
        scores_row.pack(fill="x", padx=12, pady=12)
        scores_row.grid_columnconfigure((0, 1), weight=1)

        # Uselessness Score Card
        self.useless_card = self._create_score_box(
            scores_row, "🎯", "Uselessness Metric", "100%", WIN_GREEN,
            "100% when reverse actions are performed successfully."
        )
        self.useless_card.grid(row=0, column=0, padx=6, sticky="nsew")

        # Security Score Card
        self.security_card = self._create_score_box(
            scores_row, "🔒", "Security Rating", "0%", WIN_RED,
            "0% protection provided (by humorous design)."
        )
        self.security_card.grid(row=0, column=1, padx=6, sticky="nsew")

        # Operational Metrics Box
        metrics_box = ctk.CTkFrame(container, fg_color=WIN_DARK_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        metrics_box.pack(fill="x", padx=12, pady=(4, 12))

        ctk.CTkLabel(
            metrics_box, text="System Operation Log Counters:",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(anchor="w", padx=12, pady=(8, 4))

        self.rows = {}
        items = [
            ("total", "📊  Total Files Evaluated:", "0"),
            ("deleted", "💀  Safe Files Destroyed:", "0"),
            ("preserved", "🏆  Malware / Threats Preserved:", "0"),
            ("sessions", "🔄  Scan Sessions Completed:", "0"),
        ]

        for key, label, default_val in items:
            row = ctk.CTkFrame(metrics_box, fg_color=WIN_BG, corner_radius=0)
            row.pack(fill="x", padx=10, pady=2)

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont(family="Tahoma", size=10),
                text_color=WIN_TEXT,
            ).pack(side="left", padx=8, pady=4)

            v_lbl = ctk.CTkLabel(
                row, text=default_val,
                font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
                text_color=WIN_NAVY,
            )
            v_lbl.pack(side="right", padx=8, pady=4)
            self.rows[key] = v_lbl

        # Fun Facts (Classic Tip of the Day style)
        tip_box = ctk.CTkFrame(container, fg_color=WIN_WHITE, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        tip_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        ctk.CTkLabel(
            tip_box, text="💡 Did You Know? (Tip of the Day):",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_NAVY,
        ).pack(anchor="w", padx=12, pady=(8, 4))

        ctk.CTkLabel(
            tip_box,
            text=(
                "• Windows De-fender has achieved a flawless record of 0 threats blocked.\n"
                "• All preserved threats are housed with utmost care inside the Malware Museum.\n"
                "• Harmless, clean files are moved to Deleted_Safe_Files for maximum inconvenience.\n"
                "• Powered by Cisco ClamAV and backwards logic."
            ),
            font=ctk.CTkFont(family="Tahoma", size=9),
            text_color=WIN_TEXT,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 8))

    def _create_score_box(self, parent, icon, title, val, color, desc):
        """Create a classic 3D score box."""
        box = ctk.CTkFrame(parent, fg_color=WIN_DARK_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)

        ctk.CTkLabel(
            box, text=f"{icon}  {title}",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_TEXT,
        ).pack(anchor="w", padx=10, pady=(8, 2))

        v_lbl = ctk.CTkLabel(
            box, text=val,
            font=ctk.CTkFont(family="Tahoma", size=24, weight="bold"),
            text_color=color,
        )
        v_lbl.pack(anchor="w", padx=12, pady=2)
        box.value_label = v_lbl

        ctk.CTkLabel(
            box, text=desc,
            font=ctk.CTkFont(family="Tahoma", size=9),
            text_color=WIN_MUTED,
        ).pack(anchor="w", padx=10, pady=(0, 8))

        return box

    def refresh(self):
        """Refresh statistics values from database."""
        stats = get_stats()

        self.useless_card.value_label.configure(text=f"{stats['uselessness_score']}%")
        self.security_card.value_label.configure(text=f"{stats['security_score']}%")

        self.rows["total"].configure(text=str(stats["total_scanned"]))
        self.rows["deleted"].configure(text=str(stats["clean_deleted"]))
        self.rows["preserved"].configure(text=str(stats["threats_preserved"]))
        self.rows["sessions"].configure(text=str(stats["scan_sessions"]))
