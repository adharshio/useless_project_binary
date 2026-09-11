"""
Windows De-fender — Main Application Window
Assembles all UI components with sidebar navigation.
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

from ui.dashboard import DashboardFrame
from ui.scanner_view import ScannerViewFrame
from ui.museum import MuseumFrame
from ui.history import HistoryFrame


class WindowsDefenderApp(ctk.CTk):
    """Main application window for Windows De-fender."""

    def __init__(self):
        super().__init__()

        # ── Window Configuration (Windows 7 Aero Style) ──
        self.title("Windows De-fender — Security Essentials (Aero Edition)")
        self.geometry("1120x760")
        self.minsize(920, 620)

        # Path to application logo
        self.logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "useless_logo.png")

        # Set OS window icon (using native Tkinter PhotoImage which supports PNG)
        if os.path.exists(self.logo_path):
            try:
                self._icon_img = PhotoImage(file=self.logo_path)
                self.iconphoto(False, self._icon_img)
            except Exception as e:
                print(f"Notice: Could not set window icon: {e}")

        # Windows 7 Aero light window backdrop
        self.configure(fg_color="#e3edf7")

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
        """Build the Windows 7 Control Panel / Explorer style navigation pane."""
        sidebar = ctk.CTkFrame(
            self, width=230, corner_radius=0,
            fg_color="#ebf2f9",
            border_width=1,
            border_color="#b6c9dc",
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # ── Aero Header / Logo ──
        brand_frame = ctk.CTkFrame(
            sidebar, corner_radius=8,
            fg_color="#205886",
            border_width=1,
            border_color="#153e61",
        )
        brand_frame.pack(fill="x", padx=12, pady=(15, 10))

        if os.path.exists(self.logo_path):
            try:
                logo_pil = Image.open(self.logo_path)
                self.sidebar_logo_img = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(48, 40))
                ctk.CTkLabel(
                    brand_frame, image=self.sidebar_logo_img, text=""
                ).pack(pady=(10, 2))
            except Exception:
                ctk.CTkLabel(
                    brand_frame, text="🛡️",
                    font=ctk.CTkFont(size=28),
                ).pack(pady=(10, 0))
        else:
            ctk.CTkLabel(
                brand_frame, text="🛡️",
                font=ctk.CTkFont(size=28),
            ).pack(pady=(10, 0))

        ctk.CTkLabel(
            brand_frame, text="Windows De-fender",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#ffffff",
        ).pack()

        ctk.CTkLabel(
            brand_frame, text="Security Essentials 7.0",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#b9dcfa",
        ).pack(pady=(0, 10))

        # Separator
        sep = ctk.CTkFrame(sidebar, height=1, fg_color="#cadbe8")
        sep.pack(fill="x", padx=15, pady=8)

        # Navigation label
        ctk.CTkLabel(
            sidebar, text="TASKS & NAVIGATION",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#5a7d9a",
            anchor="w",
        ).pack(fill="x", padx=16, pady=(2, 6))

        # ── Navigation Buttons ──
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠", "Home & Status"),
            ("scanner", "🔬", "Scan Computer"),
            ("museum", "🏛️", "Threat Vault"),
            ("history", "📜", "Security History"),
        ]

        for key, icon, label in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {label}",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                height=38,
                corner_radius=6,
                fg_color="transparent",
                hover_color="#dbeaf7",
                text_color="#1d3b58",
                anchor="w",
                border_width=0,
                command=lambda k=key: self._show_frame(k),
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[key] = btn

        # ── Bottom Info / Disclaimer ──
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(expand=True)

        bottom_frame = ctk.CTkFrame(
            sidebar, fg_color="#dfecf7", corner_radius=6,
            border_width=1, border_color="#bed1e3"
        )
        bottom_frame.pack(fill="x", padx=12, pady=(0, 15))

        ctk.CTkLabel(
            bottom_frame,
            text="⚠️ Useless Project 3.0\nInverted Antivirus Demo",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color="#53728f",
            justify="center",
        ).pack(padx=8, pady=8)

    def _build_content_area(self):
        """Build the main content area with all frames."""
        self.content_area = ctk.CTkFrame(
            self, fg_color="#e3edf7", corner_radius=0,
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

        # Place all frames in the same grid cell (stacked)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _show_frame(self, frame_key):
        """Switch to the specified frame and update nav buttons with Windows 7 selection."""
        for key, btn in self.nav_buttons.items():
            if key == frame_key:
                btn.configure(
                    fg_color="#cce6ff",
                    hover_color="#bfe0ff",
                    text_color="#003d7a",
                    border_width=1,
                    border_color="#89c3f8",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color="#dbeaf7",
                    text_color="#1d3b58",
                    border_width=0,
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
        """Called after a scan is completed — refresh stats."""
        if "dashboard" in self.frames:
            self.frames["dashboard"].refresh_stats()


# Alias for backwards compatibility
AntiAntivirusApp = WindowsDefenderApp
