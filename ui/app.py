"""
Anti-Antivirus — Main Application Window
Assembles all UI components with sidebar navigation.
"""

import customtkinter as ctk
from tkinter import messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import init_db
from demo_files import create_demo_files, get_demo_dir
from file_manager import ensure_directories

from ui.dashboard import DashboardFrame
from ui.scanner_view import ScannerViewFrame
from ui.museum import MuseumFrame
from ui.history import HistoryFrame
from ui.stats import StatsFrame


class AntiAntivirusApp(ctk.CTk):
    """Main application window for Anti-Antivirus."""

    def __init__(self):
        super().__init__()

        # ── Window Configuration ──
        self.title("Anti-Antivirus — Security, but backwards.")
        self.geometry("1100x750")
        self.minsize(900, 600)

        # Dark theme colors
        self.configure(fg_color="#0f172a")

        # Initialize backend
        init_db()
        ensure_directories()

        # ── Layout: Sidebar + Content ──
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

        # Show dashboard by default
        self._show_frame("dashboard")

        # Force window to front on launch
        self.lift()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _build_sidebar(self):
        """Build the left sidebar navigation."""
        sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0,
            fg_color="#0d1117",
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # ── Logo / Brand ──
        brand_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=15, pady=(20, 5))

        ctk.CTkLabel(
            brand_frame, text="🛡️",
            font=ctk.CTkFont(size=32),
        ).pack()

        ctk.CTkLabel(
            brand_frame, text="ANTI-AV",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ef4444",
        ).pack()

        ctk.CTkLabel(
            brand_frame, text="v1.0.0 — DEMO",
            font=ctk.CTkFont(size=9),
            text_color="#475569",
        ).pack(pady=(0, 5))

        # Separator
        sep = ctk.CTkFrame(sidebar, height=1, fg_color="#1e293b")
        sep.pack(fill="x", padx=15, pady=10)

        # ── Navigation Buttons ──
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠", "Dashboard"),
            ("scanner", "🔬", "Scan File"),
            ("museum", "🏛️", "Malware Museum"),
            ("history", "📜", "Scan History"),
            ("stats", "📊", "Statistics"),
        ]

        for key, icon, label in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {label}",
                font=ctk.CTkFont(size=14),
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#1e293b",
                text_color="#94a3b8",
                anchor="w",
                command=lambda k=key: self._show_frame(k),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = btn

        # ── Bottom Info ──
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(expand=True)

        bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            bottom_frame,
            text="⚠️ JOKE PROJECT\nNo real malware used",
            font=ctk.CTkFont(size=9),
            text_color="#475569",
            justify="center",
        ).pack()

    def _build_content_area(self):
        """Build the main content area with all frames."""
        self.content_area = ctk.CTkFrame(
            self, fg_color="#0f172a", corner_radius=0,
        )
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Create all page frames
        self.frames = {}

        # Dashboard
        self.frames["dashboard"] = DashboardFrame(
            self.content_area,
            scan_callback=lambda: self._show_frame("scanner"),
            generate_callback=self._generate_demo_files,
        )

        # Scanner
        self.frames["scanner"] = ScannerViewFrame(
            self.content_area,
            on_scan_complete=self._on_scan_complete,
        )

        # Museum
        self.frames["museum"] = MuseumFrame(self.content_area)

        # History
        self.frames["history"] = HistoryFrame(self.content_area)

        # Statistics
        self.frames["stats"] = StatsFrame(self.content_area)

        # Place all frames in the same grid cell (stacked)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _show_frame(self, frame_key):
        """Switch to the specified frame and update nav buttons."""
        # Update button colors
        for key, btn in self.nav_buttons.items():
            if key == frame_key:
                btn.configure(
                    fg_color="#1e293b",
                    text_color="#e2e8f0",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#94a3b8",
                )

        # Refresh data on frame switch
        frame = self.frames[frame_key]
        if hasattr(frame, "refresh"):
            frame.refresh()
        if hasattr(frame, "refresh_stats"):
            frame.refresh_stats()

        frame.tkraise()

    def _generate_demo_files(self):
        """Generate demo sample files for testing."""
        try:
            hashes = create_demo_files()
            demo_dir = get_demo_dir()
            messagebox.showinfo(
                "Demo Files Generated",
                f"✅ Created {len(hashes)} demo threat files in:\n"
                f"{demo_dir}\n\n"
                f"Use 'Scan File' to test them!\n"
                f"These are harmless .txt files.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not create demo files:\n{e}")

    def _on_scan_complete(self):
        """Called after a scan is completed — refresh stats across all views."""
        for frame in self.frames.values():
            if hasattr(frame, "refresh"):
                frame.refresh()
            if hasattr(frame, "refresh_stats"):
                frame.refresh_stats()
