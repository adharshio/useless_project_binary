"""
Anti-Antivirus — Main Application Window (Classic Windows Retro Edition)
Assembles all retro UI components with classic Windows XP/98 top navigation bar.
"""

import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from PIL import Image
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

        # ── Layout: Top Nav Bar + Content ──
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Content area expands

        self._build_top_navbar()
        self._build_content_area()

        # Show scanner by default
        self._show_frame("scanner")

        # Clean window close protocol
        self.protocol("WM_DELETE_WINDOW", self._on_close_app)

        # Bring window forward
        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _build_top_navbar(self):
        """Build the classic Windows top navigation bar with brand + tab buttons."""
        # ── Outer nav container ──
        navbar = ctk.CTkFrame(
            self, height=72, corner_radius=0,
            fg_color=WIN_DARK_BG,
            border_width=1,
            border_color=WIN_BORDER,
        )
        navbar.grid(row=0, column=0, sticky="ew", padx=2, pady=(2, 0))
        navbar.grid_propagate(False)

        # ── Top row: Brand header bar (navy blue) ──
        brand_bar = ctk.CTkFrame(navbar, fg_color=WIN_NAVY, height=30, corner_radius=0)
        brand_bar.pack(fill="x")
        brand_bar.pack_propagate(False)

        ctk.CTkLabel(
            brand_bar, text="  🛡️ Windows De-fender 1.0 — Reverse Antivirus Protection",
            font=ctk.CTkFont(family="Tahoma", size=10, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        ).pack(side="left", padx=6)

        ctk.CTkLabel(
            brand_bar, text="⚠️ Competition Edition  |  ClamAV Integrated  ",
            font=ctk.CTkFont(family="Tahoma", size=9),
            text_color="#A6CAF0",
        ).pack(side="right", padx=8)

        # ── Bottom row: Tab navigation buttons ──
        tab_row = ctk.CTkFrame(navbar, fg_color=WIN_DARK_BG, height=38, corner_radius=0)
        tab_row.pack(fill="x", pady=(2, 0))
        tab_row.pack_propagate(False)

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
                tab_row,
                text=f" {icon}  {label} ",
                font=ctk.CTkFont(family="Tahoma", size=10),
                height=30,
                corner_radius=2,
                fg_color=WIN_BG,
                hover_color="#DFDBC9",
                text_color=WIN_TEXT,
                border_width=1,
                border_color=WIN_BORDER,
                command=lambda k=key: self._show_frame(k),
            )
            btn.pack(side="left", padx=3, pady=(2, 4))
            self.nav_buttons[key] = btn

    def _build_content_area(self):
        """Build the main retro content frame."""
        self.content_area = ctk.CTkFrame(
            self, fg_color=WIN_BG, corner_radius=0,
        )
        self.content_area.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))
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

    def _on_close_app(self):
        """Cleanly terminate all background threads, animations, and exit process."""
        try:
            if hasattr(self, "frames") and "scanner" in self.frames:
                self.frames["scanner"].abort_scan()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass
        import os
        os._exit(0)
