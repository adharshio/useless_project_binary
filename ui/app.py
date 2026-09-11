"""
Anti-Antivirus — Main Application Window (Classic Windows Retro Edition)
Assembles all retro UI components with classic Windows XP/98 navigation.
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import init_db
from demo_files import create_demo_files, get_demo_dir
from file_manager import ensure_directories
from ui.retro_widgets import WIN_BG, WIN_DARK_BG, WIN_WHITE, WIN_TEXT, WIN_BORDER, WIN_NAVY, WIN_BLUE

from ui.dashboard import DashboardFrame
from ui.scanner_view import ScannerViewFrame
from ui.museum import MuseumFrame
from ui.history import HistoryFrame
from ui.stats import StatsFrame


class AntiAntivirusApp(ctk.CTk):
    """Main classic desktop application window for Anti-Antivirus (Windows De-fender)."""

    def __init__(self):
        super().__init__()

        # ── Window Configuration ──
        self.title("Windows De-fender 1.0 — Reverse Antivirus Protection")
        self.geometry("1060x720")
        self.minsize(850, 580)

        # Classic Windows beige-grey appearance
        self.configure(fg_color=WIN_BG)

        # Initialize backend
        init_db()
        ensure_directories()

        # ── Layout: Sidebar + Content ──
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

        # Show scanner by default or dashboard
        self._show_frame("scanner")

        # Bring window forward
        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _build_sidebar(self):
        """Build the classic Windows Explorer Task Pane sidebar."""
        sidebar = ctk.CTkFrame(
            self, width=210, corner_radius=0,
            fg_color=WIN_DARK_BG,
            border_width=1,
            border_color=WIN_BORDER,
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)
        sidebar.grid_propagate(False)

        # ── Classic Windows XP Blue Header ──
        brand_frame = ctk.CTkFrame(sidebar, fg_color=WIN_NAVY, height=52, corner_radius=0)
        brand_frame.pack(fill="x", padx=2, pady=2)
        brand_frame.pack_propagate(False)

        ctk.CTkLabel(
            brand_frame, text="🛡️ Windows De-fender",
            font=ctk.CTkFont(family="Tahoma", size=12, weight="bold"),
            text_color=WIN_WHITE,
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            brand_frame, text="Security Tasks & Tools",
            font=ctk.CTkFont(family="Tahoma", size=9),
            text_color="#A6CAF0",
        ).pack()

        # Separator line
        sep = ctk.CTkFrame(sidebar, height=2, fg_color=WIN_BORDER)
        sep.pack(fill="x", padx=4, pady=4)

        # ── Navigation Buttons (Classic Windows 3D Buttons) ──
        self.nav_buttons = {}
        nav_items = [
            ("scanner", "🔬", "Scanner Wizard"),
            ("dashboard", "🏠", "System Overview"),
            ("museum", "🏛️", "Malware Museum"),
            ("history", "📜", "Event History"),
            ("stats", "📊", "Performance Stats"),
        ]

        for key, icon, label in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {label}",
                font=ctk.CTkFont(family="Tahoma", size=11),
                height=36,
                corner_radius=2,
                fg_color=WIN_BG,
                hover_color="#DFDBC9",
                text_color=WIN_TEXT,
                border_width=1,
                border_color=WIN_BORDER,
                anchor="w",
                command=lambda k=key: self._show_frame(k),
            )
            btn.pack(fill="x", padx=6, pady=3)
            self.nav_buttons[key] = btn

        # ── Bottom System Info Box ──
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(expand=True)

        info_box = ctk.CTkFrame(sidebar, fg_color=WIN_BG, border_width=1, border_color=WIN_BORDER, corner_radius=2)
        info_box.pack(fill="x", padx=6, pady=(0, 8))

        ctk.CTkLabel(
            info_box,
            text="⚠️ Competition Edition\nHarmless text threats\nClamAV Engine integrated",
            font=ctk.CTkFont(family="Tahoma", size=9),
            text_color=WIN_TEXT,
            justify="center",
        ).pack(padx=6, pady=8)

    def _build_content_area(self):
        """Build the main retro content frame."""
        self.content_area = ctk.CTkFrame(
            self, fg_color=WIN_BG, corner_radius=0,
        )
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Initialize page frames
        self.frames = {}

        self.frames["scanner"] = ScannerViewFrame(
            self.content_area,
            on_scan_complete=self._on_scan_complete,
        )

        self.frames["dashboard"] = DashboardFrame(
            self.content_area,
            scan_callback=lambda: self._show_frame("scanner"),
            generate_callback=self._generate_demo_files,
        )

        self.frames["museum"] = MuseumFrame(self.content_area)
        self.frames["history"] = HistoryFrame(self.content_area)
        self.frames["stats"] = StatsFrame(self.content_area)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _show_frame(self, frame_key):
        """Switch view and update classic button state."""
        for key, btn in self.nav_buttons.items():
            if key == frame_key:
                btn.configure(
                    fg_color=WIN_NAVY,
                    text_color=WIN_WHITE,
                    border_color="#000000",
                )
            else:
                btn.configure(
                    fg_color=WIN_BG,
                    text_color=WIN_TEXT,
                    border_color=WIN_BORDER,
                )

        frame = self.frames[frame_key]
        if hasattr(frame, "refresh"):
            frame.refresh()
        if hasattr(frame, "refresh_stats"):
            frame.refresh_stats()

        frame.tkraise()

    def _generate_demo_files(self):
        """Generate demo test files."""
        try:
            hashes = create_demo_files()
            demo_dir = get_demo_dir()
            messagebox.showinfo(
                "Windows De-fender",
                f"Created {len(hashes)} demo files in:\n{demo_dir}\n\nYou can scan them now!",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not create demo files:\n{e}")

    def _on_scan_complete(self):
        """Refresh all views upon scan completion."""
        for frame in self.frames.values():
            if hasattr(frame, "refresh"):
                frame.refresh()
            if hasattr(frame, "refresh_stats"):
                frame.refresh_stats()
