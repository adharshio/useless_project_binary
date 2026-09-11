"""
Anti-Antivirus — Retro Windows Widgets & Styling
Provides authentic Windows XP / 98 / 2000 style components:
- ClassicProgressBar (authentic segmented blue blocks animation)
- ClassicTitleBar (gradient blue bar with retro buttons)
- RetroErrorDialog (matching the user's reference image)
- Classic color constants and styling helpers
"""

import tkinter as tk
import customtkinter as ctk
import os
import sys

# ── Classic Windows XP / 98 Palette ──
WIN_BG = "#ECE9D8"          # Classic Windows XP beige-grey
WIN_DARK_BG = "#D4D0C8"     # Windows 98/2000 grey
WIN_WHITE = "#FFFFFF"        # Inset field white
WIN_TEXT = "#000000"         # Black text
WIN_MUTED = "#555555"        # Subtitle text
WIN_BORDER = "#808080"       # Classic 3D shadow border
WIN_BORDER_LIGHT = "#FFFFFF" # Classic 3D highlight border
WIN_BLUE = "#0055EA"         # Windows XP titlebar blue
WIN_NAVY = "#0A246A"         # Windows 2000 deep navy blue
WIN_BLUE_LIGHT = "#A6CAF0"   # Gradient light blue
WIN_BLOCK_BLUE = "#2E7BE8"   # Segmented progress bar blue
WIN_BLOCK_SHADOW = "#1D52A0" # Segmented progress bar block shadow
WIN_RED = "#D32F2F"          # Classic error red
WIN_GREEN = "#2E7D32"        # Classic success green


class ClassicProgressBar(tk.Canvas):
    """
    Authentic Windows XP / 2000 segmented blue blocks progress bar.
    Draws discrete blue blocks (■ ■ ■) with highlight & shadow borders.
    Supports both determinate progress (0.0 to 1.0) and marquee animation.
    """

    def __init__(self, parent, width=360, height=20, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=WIN_WHITE,
            highlightthickness=1,
            highlightbackground=WIN_BORDER,
            highlightcolor=WIN_BORDER,
            **kwargs
        )
        self.bar_width = width
        self.bar_height = height
        self.progress = 0.0
        self.is_marquee = False
        self.marquee_pos = 0
        self.marquee_timer = None

        # Block dimensions
        self.block_w = 8
        self.block_gap = 2

        self.bind("<Configure>", self._on_resize)
        self._draw_determinate()

    def _on_resize(self, event):
        self.bar_width = event.width
        self.bar_height = event.height
        if not self.is_marquee:
            self._draw_determinate()

    def set_progress(self, val: float):
        """Set determinate progress (0.0 to 1.0)."""
        self.is_marquee = False
        if self.marquee_timer:
            self.after_cancel(self.marquee_timer)
            self.marquee_timer = None
        self.progress = max(0.0, min(1.0, float(val)))
        self._draw_determinate()

    def _draw_determinate(self):
        """Draw discrete blue blocks filling up according to progress."""
        self.delete("all")
        step = self.block_w + self.block_gap
        total_slots = int(self.bar_width / step)
        filled_slots = int(total_slots * self.progress)

        for i in range(filled_slots):
            x1 = 2 + i * step
            y1 = 2
            x2 = x1 + self.block_w
            y2 = self.bar_height - 2
            if x2 > self.bar_width - 2:
                break
            # Block body
            self.create_rectangle(x1, y1, x2, y2, fill=WIN_BLOCK_BLUE, outline=WIN_BLOCK_SHADOW)
            # 3D Highlight on top/left of block
            self.create_line(x1, y1, x2 - 1, y1, fill="#6EA8F7")
            self.create_line(x1, y1, x1, y2 - 1, fill="#6EA8F7")

    def start_marquee(self):
        """Start classic Windows moving blue blocks animation (e.g. while scanning)."""
        if self.is_marquee:
            return
        self.is_marquee = True
        self._animate_marquee()

    def stop_marquee(self):
        """Stop marquee animation."""
        self.is_marquee = False
        if self.marquee_timer:
            self.after_cancel(self.marquee_timer)
            self.marquee_timer = None
        self._draw_determinate()

    def _animate_marquee(self):
        if not self.is_marquee:
            return
        self.delete("all")
        step = self.block_w + self.block_gap
        num_blocks = 4  # A group of 4 blocks moving across

        for i in range(num_blocks):
            x1 = self.marquee_pos + i * step
            if 0 <= x1 < self.bar_width:
                x2 = min(x1 + self.block_w, self.bar_width - 2)
                y1 = 2
                y2 = self.bar_height - 2
                self.create_rectangle(x1, y1, x2, y2, fill=WIN_BLOCK_BLUE, outline=WIN_BLOCK_SHADOW)
                self.create_line(x1, y1, x2 - 1, y1, fill="#6EA8F7")
                self.create_line(x1, y1, x1, y2 - 1, fill="#6EA8F7")

        self.marquee_pos += 4
        if self.marquee_pos > self.bar_width:
            self.marquee_pos = - (num_blocks * step)

        self.marquee_timer = self.after(35, self._animate_marquee)


class RetroDialog(ctk.CTkToplevel):
    """
    Authentic retro dialog window styled exactly like the user's reference image:
    - Royal blue title bar with pixelated/bold title and square [X] close button
    - Cream/beige background (#ECE9D8)
    - Classic circular Red 'X' error icon
    - Beveled 3D 'Fix' or action button
    """

    def __init__(self, parent, title="Error", message='Click "Fix" to fix error.',
                 ok_text="Fix", cancel_text="Cancel", is_warning=False):
        super().__init__(parent)
        self.result = False
        self.title(title)
        self.geometry("380x190")
        self.resizable(False, False)
        self.configure(fg_color=WIN_BG)
        self.transient(parent)
        self.grab_set()

        # Center dialog relative to parent
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 190
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 95
            self.geometry(f"+{max(10, x)}+{max(10, y)}")
        except Exception:
            pass

        # ── Classic Title Bar ──
        title_bar = ctk.CTkFrame(self, fg_color=WIN_NAVY, height=30, corner_radius=0)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            title_bar, text=f"  {title}",
            font=ctk.CTkFont(family="Tahoma", size=11, weight="bold"),
            text_color=WIN_WHITE,
            anchor="w",
        )
        title_lbl.pack(side="left", padx=5)

        close_btn = ctk.CTkButton(
            title_bar, text="✕",
            font=ctk.CTkFont(size=10, weight="bold"),
            width=22, height=20,
            corner_radius=2,
            fg_color="#D4D0C8",
            text_color="#000000",
            hover_color="#E81123",
            command=self._on_cancel,
        )
        close_btn.pack(side="right", padx=4, pady=3)

        # ── Dialog Body ──
        body = ctk.CTkFrame(self, fg_color=WIN_BG, corner_radius=0)
        body.pack(fill="both", expand=True, padx=15, pady=10)

        top_content = ctk.CTkFrame(body, fg_color="transparent")
        top_content.pack(fill="x", pady=(10, 10))

        # Canvas drawing the classic pixelated Red Circle with White X
        icon_canvas = tk.Canvas(top_content, width=38, height=38, bg=WIN_BG, highlightthickness=0)
        icon_canvas.pack(side="left", padx=(5, 12))

        # Draw red circle
        icon_canvas.create_oval(3, 3, 35, 35, fill="#E51400", outline="#A80000", width=2)
        # Draw white bold X
        icon_canvas.create_line(12, 12, 26, 26, fill=WIN_WHITE, width=4, capstyle="round")
        icon_canvas.create_line(26, 12, 12, 26, fill=WIN_WHITE, width=4, capstyle="round")

        # Message Text (Tahoma 11 pt)
        msg_lbl = ctk.CTkLabel(
            top_content,
            text=message,
            font=ctk.CTkFont(family="Tahoma", size=11),
            text_color=WIN_TEXT,
            justify="left",
            wraplength=270,
        )
        msg_lbl.pack(side="left", fill="x", expand=True)

        # ── Buttons Row ──
        btn_row = ctk.CTkFrame(body, fg_color="transparent")
        btn_row.pack(fill="x", pady=(10, 5))

        self.ok_btn = ctk.CTkButton(
            btn_row,
            text=ok_text,
            font=ctk.CTkFont(family="Tahoma", size=11),
            width=85, height=26,
            corner_radius=3,
            fg_color="#ECE9D8",
            hover_color="#DFDBC9",
            text_color="#000000",
            border_width=2,
            border_color="#7F9DB9",
            command=self._on_ok,
        )
        self.ok_btn.pack(side="right", padx=(5, 10))

        if cancel_text:
            self.cancel_btn = ctk.CTkButton(
                btn_row,
                text=cancel_text,
                font=ctk.CTkFont(family="Tahoma", size=11),
                width=85, height=26,
                corner_radius=3,
                fg_color="#ECE9D8",
                hover_color="#DFDBC9",
                text_color="#000000",
                border_width=2,
                border_color="#7F9DB9",
                command=self._on_cancel,
            )
            self.cancel_btn.pack(side="right", padx=5)

        self.wait_window()

    def _on_ok(self):
        self.result = True
        self.destroy()

    def _on_cancel(self):
        self.result = False
        self.destroy()


def show_retro_alert(parent, title="Error", message='Click "Fix" to fix error.',
                     ok_text="Fix", cancel_text="Cancel") -> bool:
    """Helper to display the authentic retro Windows dialog."""
    dialog = RetroDialog(parent, title=title, message=message, ok_text=ok_text, cancel_text=cancel_text)
    return dialog.result
