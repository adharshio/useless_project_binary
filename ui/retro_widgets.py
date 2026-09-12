"""
Anti-Antivirus — Retro Windows Widgets & Styling (Windows 98 / 2000 / XP Edition)
Provides authentic classic Windows components:
- RetroButton (beveled 3D button with normal, pressed, and flat-grey disabled states)
- RetroTitleBar (gradient blue #0A246A -> #A6CAF0 with square beveled [X] and drag support)
- RetroSegmentedProgressBar (authentic segmented rectangular green chunks in sunken 3D bar)
- ClassicProgressBar (segmented blue blocks progress bar)
- RetroDialog (authentic 3D beveled window border, gradient title bar, 64x64 pixelated red X, Tahoma text, 3D buttons)
- RetroProgressDialog (fake scanning / comic purge modal with animated green chunks)
- Color constants and dialog helper functions
"""

import tkinter as tk
import customtkinter as ctk
import os
import sys

# ── Classic Windows Palette ──
WIN_BG = "#ECE9D8"            # Classic Windows XP beige-grey
WIN_DARK_BG = "#D4D0C8"       # Windows 98/2000 dialog grey
WIN_WHITE = "#FFFFFF"          # Pure highlight / inset white
WIN_TEXT = "#000000"           # Pure black text
WIN_MUTED = "#555555"          # Subtitle text
WIN_BORDER_LIGHT = "#FFFFFF"   # 3D outer highlight (top/left)
WIN_BORDER_MIDLIGHT = "#DFDFDF"# 3D inner highlight
WIN_BORDER_SHADOW = "#808080"  # 3D inner shadow
WIN_BORDER_DARK = "#000000"    # 3D outer shadow (bottom/right)
WIN_DISABLED_TEXT = "#808080"  # Disabled button text
WIN_DISABLED_FACE = "#D4D0C8"  # Disabled button background
WIN_BORDER = "#808080"         # General classic border

# Title bar gradient
WIN_NAVY = "#0A246A"           # Windows 2000 deep navy blue
WIN_BLUE_LIGHT = "#A6CAF0"     # Soft gradient blue
WIN_BLUE = "#0055EA"           # Standard XP blue

# Segmented Progress Bar Green & Blue
WIN_GREEN_BLOCK = "#107C10"    # Authentic green rectangular chunk
WIN_GREEN_LIGHT = "#75DA75"    # 3D highlight of green chunk
WIN_GREEN_SHADOW = "#084B08"   # 3D shadow of green chunk
WIN_BLOCK_BLUE = "#2E7BE8"     # Segmented progress bar blue
WIN_BLOCK_SHADOW = "#1D52A0"   # Segmented progress bar block shadow
WIN_RED = "#D32F2F"            # Classic error red
WIN_GREEN = "#2E7D32"          # Classic success green


class RetroButton(tk.Canvas):
    """
    Authentic Windows 95/98/2000 beveled 3D button.
    - Raised look: Thin dark outer border, light inner highlight, sharp corners.
    - Pressed/Active state: Inverted bevel with 1px text depression.
    - Disabled state: Flat grey background (#D4D0C8) with light grey text (#808080).
    - No rounded edges or modern shadows.
    """

    def __init__(self, parent, text="OK", command=None, width=80, height=24,
                 state="normal", is_default=False, font=("Tahoma", 9), **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=WIN_DARK_BG,
            highlightthickness=0,
            bd=0,
            **kwargs
        )
        self.btn_width = width
        self.btn_height = height
        self.text = text
        self.command = command
        self.state = state
        self.is_default = is_default
        self.font = font
        self.is_pressed = False

        self.bind("<Configure>", self._on_resize)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self._redraw()

    def _on_resize(self, event):
        self.btn_width = event.width
        self.btn_height = event.height
        self._redraw()

    def set_state(self, new_state: str):
        """Set state: 'normal' or 'disabled'."""
        self.state = new_state
        self._redraw()

    def configure_button(self, text=None, state=None, command=None):
        """Update button properties dynamically."""
        if text is not None:
            self.text = text
        if state is not None:
            self.state = state
        if command is not None:
            self.command = command
        self._redraw()

    def _on_press(self, event):
        if self.state == "disabled":
            return
        self.is_pressed = True
        self._redraw()

    def _on_release(self, event):
        if self.state == "disabled":
            return
        was_pressed = self.is_pressed
        self.is_pressed = False
        self._redraw()
        if was_pressed and 0 <= event.x <= self.btn_width and 0 <= event.y <= self.btn_height:
            if self.command:
                self.command()

    def _on_enter(self, event):
        pass

    def _on_leave(self, event):
        if self.is_pressed:
            self.is_pressed = False
            self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.btn_width
        h = self.btn_height

        if self.state == "disabled":
            # Flat-grey with light-grey text and thin flat border
            self.create_rectangle(0, 0, w, h, fill=WIN_DISABLED_FACE, outline="")
            self.create_rectangle(0, 0, w - 1, h - 1, outline=WIN_BORDER_SHADOW, width=1)
            # Etched text effect (1px white highlight offset, then grey text)
            self.create_text(w // 2 + 1, h // 2 + 1, text=self.text, font=self.font, fill=WIN_WHITE)
            self.create_text(w // 2, h // 2, text=self.text, font=self.font, fill=WIN_DISABLED_TEXT)
            return

        offset = 0
        if self.is_default:
            # 1px solid black default button frame
            self.create_rectangle(0, 0, w - 1, h - 1, outline=WIN_BORDER_DARK, width=1)
            offset = 1

        bw = w - offset
        bh = h - offset
        ox = offset
        oy = offset

        # Button face
        self.create_rectangle(ox, oy, bw, bh, fill=WIN_DARK_BG, outline="")

        if self.is_pressed:
            # Sunken 3D bevel
            self.create_line(ox, oy, bw - 1, oy, fill=WIN_BORDER_DARK)
            self.create_line(ox, oy, ox, bh - 1, fill=WIN_BORDER_DARK)
            self.create_line(ox + 1, oy + 1, bw - 2, oy + 1, fill=WIN_BORDER_SHADOW)
            self.create_line(ox + 1, oy + 1, ox + 1, bh - 2, fill=WIN_BORDER_SHADOW)
            self.create_line(ox, bh - 1, bw, bh - 1, fill=WIN_BORDER_LIGHT)
            self.create_line(bw - 1, oy, bw - 1, bh, fill=WIN_BORDER_LIGHT)

            tx = (w // 2) + 1
            ty = (h // 2) + 1
        else:
            # Raised 3D bevel
            # Outer white highlight on top & left
            self.create_line(ox, oy, bw - 1, oy, fill=WIN_BORDER_LIGHT)
            self.create_line(ox, oy, ox, bh - 1, fill=WIN_BORDER_LIGHT)
            # Inner mid-light on top & left
            self.create_line(ox + 1, oy + 1, bw - 2, oy + 1, fill=WIN_BORDER_MIDLIGHT)
            self.create_line(ox + 1, oy + 1, ox + 1, bh - 2, fill=WIN_BORDER_MIDLIGHT)
            # Inner shadow on bottom & right
            self.create_line(ox + 1, bh - 2, bw - 1, bh - 2, fill=WIN_BORDER_SHADOW)
            self.create_line(bw - 2, oy + 1, bw - 2, bh - 1, fill=WIN_BORDER_SHADOW)
            # Outer black shadow on bottom & right
            self.create_line(ox, bh - 1, bw, bh - 1, fill=WIN_BORDER_DARK)
            self.create_line(bw - 1, oy, bw - 1, bh, fill=WIN_BORDER_DARK)

            tx = w // 2
            ty = h // 2

        self.create_text(tx, ty, text=self.text, font=self.font, fill=WIN_TEXT)


class RetroTitleBar(tk.Canvas):
    """
    Classic Windows 98/2000 gradient blue title bar (#0A246A to #A6CAF0):
    - White bold title text (e.g. "Error", "Windows De-fender")
    - Small greyed-out / beveled square "X" close button in top-right
    - Draggable window binding
    """

    def __init__(self, parent, title="Error", close_command=None, height=28, **kwargs):
        super().__init__(
            parent,
            height=height,
            bg=WIN_NAVY,
            highlightthickness=0,
            bd=0,
            **kwargs
        )
        self.bar_height = height
        self.title_text = title
        self.close_command = close_command
        self.btn_pressed = False

        # Close button dimensions
        self.close_w = 16
        self.close_h = 14

        self.bind("<Configure>", self._on_resize)
        self.bind("<ButtonPress-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

        # Draggable parent toplevel support
        self._drag_start_x = 0
        self._drag_start_y = 0
        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        if self._is_in_close_btn(event.x, event.y):
            return
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _do_drag(self, event):
        if self._is_in_close_btn(event.x, event.y):
            return
        try:
            top = self.winfo_toplevel()
            dx = event.x - self._drag_start_x
            dy = event.y - self._drag_start_y
            new_x = top.winfo_x() + dx
            new_y = top.winfo_y() + dy
            top.geometry(f"+{new_x}+{new_y}")
        except Exception:
            pass

    def _on_resize(self, event):
        self._draw_titlebar()

    def _is_in_close_btn(self, x, y):
        w = self.winfo_width()
        bx = w - self.close_w - 5
        by = (self.bar_height - self.close_h) // 2
        return (bx <= x <= bx + self.close_w) and (by <= y <= by + self.close_h)

    def _on_click(self, event):
        if self._is_in_close_btn(event.x, event.y):
            self.btn_pressed = True
            self._draw_titlebar()

    def _on_release(self, event):
        if self.btn_pressed:
            self.btn_pressed = False
            self._draw_titlebar()
            if self._is_in_close_btn(event.x, event.y):
                if self.close_command:
                    self.close_command()

    def _draw_titlebar(self):
        self.delete("all")
        w = max(10, self.winfo_width())
        h = self.bar_height

        # ── Draw authentic gradient: #0A246A (navy) to #A6CAF0 (light blue) ──
        r1, g1, b1 = 10, 36, 106
        r2, g2, b2 = 166, 202, 240

        for x in range(0, w, 2):
            t = x / max(1, w)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(x, 0, x, h, fill=color)
            if x + 1 < w:
                self.create_line(x + 1, 0, x + 1, h, fill=color)

        # ── White Bold Title Text ──
        self.create_text(
            10, h // 2,
            text=self.title_text,
            font=("Tahoma", 9, "bold"),
            fill=WIN_WHITE,
            anchor="w"
        )

        # ── Small beveled square "X" close button ──
        bx = w - self.close_w - 5
        by = (h - self.close_h) // 2
        bw = self.close_w
        bh = self.close_h

        self.create_rectangle(bx, by, bx + bw, by + bh, fill=WIN_DARK_BG, outline="")

        if self.btn_pressed:
            # Sunken bevel
            self.create_line(bx, by, bx + bw, by, fill=WIN_BORDER_DARK)
            self.create_line(bx, by, bx, by + bh, fill=WIN_BORDER_DARK)
            self.create_line(bx + 1, by + 1, bx + bw - 1, by + 1, fill=WIN_BORDER_SHADOW)
            self.create_line(bx + 1, by + 1, bx + 1, by + bh - 1, fill=WIN_BORDER_SHADOW)
            self.create_line(bx, by + bh, bx + bw, by + bh, fill=WIN_BORDER_LIGHT)
            self.create_line(bx + bw, by, bx + bw, by + bh, fill=WIN_BORDER_LIGHT)
            cx = bx + bw // 2 + 1
            cy = by + bh // 2 + 1
        else:
            # Raised bevel
            self.create_line(bx, by, bx + bw - 1, by, fill=WIN_BORDER_LIGHT)
            self.create_line(bx, by, bx, by + bh - 1, fill=WIN_BORDER_LIGHT)
            self.create_line(bx + 1, by + bh - 1, bx + bw, by + bh - 1, fill=WIN_BORDER_DARK)
            self.create_line(bx + bw - 1, by + 1, bx + bw - 1, by + bh, fill=WIN_BORDER_DARK)
            self.create_line(bx + 1, by + bh - 2, bx + bw - 1, by + bh - 2, fill=WIN_BORDER_SHADOW)
            self.create_line(bx + bw - 2, by + 1, bx + bw - 2, by + bh - 1, fill=WIN_BORDER_SHADOW)
            cx = bx + bw // 2
            cy = by + bh // 2

        # Draw chunky pixelated "X"
        self.create_line(cx - 3, cy - 3, cx + 4, cy + 4, fill=WIN_TEXT, width=2)
        self.create_line(cx + 3, cy - 3, cx - 4, cy + 4, fill=WIN_TEXT, width=2)


def draw_pixel_error_icon(canvas: tk.Canvas, size=64):
    """
    Draw an authentic circular red error icon with white 'X' inside,
    specifically styled with a classic pixelated/low-res feel.
    Scales smoothly with the size parameter.
    """
    canvas.delete("all")
    w = size
    h = size
    cx = w // 2
    cy = h // 2
    r = max(6, (min(w, h) // 2) - 3)

    # Outer dark outline / shadow for chunky retro look
    canvas.create_oval(cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1, fill="#800000", outline="#400000", width=1)

    # Vibrant red circular base
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#D81818", outline="#A00000", width=2)

    # Subtle inner bevel highlight on top/left of circle
    canvas.create_arc(
        cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2,
        start=45, extent=180, outline="#F87070", width=max(1, int(size * 0.03)), style="arc"
    )

    # Chunky pixelated White 'X'
    arm = max(4, int(r * 0.62))
    line_w = max(3, int(size * 0.11))

    # Shadow for pixel cross
    canvas.create_line(cx - arm + 1, cy - arm + 2, cx + arm + 1, cy + arm + 2, fill="#700000", width=line_w, capstyle="projecting")
    canvas.create_line(cx + arm + 1, cy - arm + 2, cx - arm + 1, cy + arm + 2, fill="#700000", width=line_w, capstyle="projecting")

    # Bright white cross body
    canvas.create_line(cx - arm, cy - arm, cx + arm, cy + arm, fill=WIN_WHITE, width=line_w, capstyle="projecting")
    canvas.create_line(cx + arm, cy - arm, cx - arm, cy + arm, fill=WIN_WHITE, width=line_w, capstyle="projecting")


class RetroSegmentedProgressBar(tk.Canvas):
    """
    Authentic Windows retro segmented-block progress bar.
    - Default style: Green rectangular chunks (WIN_GREEN_BLOCK) with 3D highlight and shadow.
    - Sunken 3D border around the bar.
    - Supports both determinate progress (0.0 to 1.0) and marquee animation.
    """

    def __init__(self, parent, width=320, height=20, chunk_color=WIN_GREEN_BLOCK,
                 chunk_light=WIN_GREEN_LIGHT, chunk_shadow=WIN_GREEN_SHADOW, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=WIN_WHITE,
            highlightthickness=0,
            bd=0,
            **kwargs
        )
        self.bar_width = width
        self.bar_height = height
        self.chunk_color = chunk_color
        self.chunk_light = chunk_light
        self.chunk_shadow = chunk_shadow

        self.progress = 0.0
        self.is_marquee = False
        self.marquee_pos = 0
        self.marquee_timer = None

        # Block dimensions
        self.block_w = 9
        self.block_gap = 2

        self.bind("<Configure>", self._on_resize)
        self._draw_determinate()

    def _on_resize(self, event):
        self.bar_width = event.width
        self.bar_height = event.height
        if not self.is_marquee:
            self._draw_determinate()

    def set_progress(self, val: float):
        """Set progress from 0.0 to 1.0."""
        self.is_marquee = False
        if self.marquee_timer:
            self.after_cancel(self.marquee_timer)
            self.marquee_timer = None
        self.progress = max(0.0, min(1.0, float(val)))
        self._draw_determinate()

    def _draw_determinate(self):
        self.delete("all")
        w = self.bar_width
        h = self.bar_height

        # Inset sunken background & 3D sunken border
        self.create_rectangle(0, 0, w, h, fill=WIN_WHITE, outline="")
        self.create_line(0, 0, w, 0, fill=WIN_BORDER_SHADOW)
        self.create_line(0, 0, 0, h, fill=WIN_BORDER_SHADOW)
        self.create_line(1, 1, w - 1, 1, fill=WIN_BORDER_DARK)
        self.create_line(1, 1, 1, h - 1, fill=WIN_BORDER_DARK)
        self.create_line(0, h - 1, w, h - 1, fill=WIN_BORDER_LIGHT)
        self.create_line(w - 1, 0, w - 1, h, fill=WIN_BORDER_LIGHT)

        step = self.block_w + self.block_gap
        usable_w = w - 6
        total_slots = int(usable_w / step)
        filled_slots = int(total_slots * self.progress)

        for i in range(filled_slots):
            x1 = 3 + i * step
            y1 = 3
            x2 = x1 + self.block_w
            y2 = h - 3
            if x2 > w - 3:
                break
            # Block body
            self.create_rectangle(x1, y1, x2, y2, fill=self.chunk_color, outline="")
            # 3D block highlight (top and left)
            self.create_line(x1, y1, x2 - 1, y1, fill=self.chunk_light)
            self.create_line(x1, y1, x1, y2 - 1, fill=self.chunk_light)
            # 3D block shadow (bottom and right)
            self.create_line(x1, y2 - 1, x2, y2 - 1, fill=self.chunk_shadow)
            self.create_line(x2 - 1, y1, x2 - 1, y2, fill=self.chunk_shadow)

    def start_marquee(self):
        """Start classic moving green chunks animation."""
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
        w = self.bar_width
        h = self.bar_height

        # Sunken borders
        self.create_rectangle(0, 0, w, h, fill=WIN_WHITE, outline="")
        self.create_line(0, 0, w, 0, fill=WIN_BORDER_SHADOW)
        self.create_line(0, 0, 0, h, fill=WIN_BORDER_SHADOW)
        self.create_line(1, 1, w - 1, 1, fill=WIN_BORDER_DARK)
        self.create_line(1, 1, 1, h - 1, fill=WIN_BORDER_DARK)
        self.create_line(0, h - 1, w, h - 1, fill=WIN_BORDER_LIGHT)
        self.create_line(w - 1, 0, w - 1, h, fill=WIN_BORDER_LIGHT)

        step = self.block_w + self.block_gap
        num_blocks = 10  # Wide prominent blue strip sweeping through the white bar

        for i in range(num_blocks):
            raw_x1 = self.marquee_pos + i * step
            raw_x2 = raw_x1 + self.block_w
            if raw_x2 > 3 and raw_x1 < w - 3:
                x1 = max(3, raw_x1)
                x2 = min(w - 3, raw_x2)
                y1 = 3
                y2 = h - 3
                if x2 > x1:
                    self.create_rectangle(x1, y1, x2, y2, fill=self.chunk_color, outline="")
                    self.create_line(x1, y1, x2 - 1, y1, fill=self.chunk_light)
                    self.create_line(x1, y1, x1, y2 - 1, fill=self.chunk_light)
                    self.create_line(x1, y2 - 1, x2, y2 - 1, fill=self.chunk_shadow)
                    self.create_line(x2 - 1, y1, x2 - 1, y2, fill=self.chunk_shadow)

        self.marquee_pos += 8
        if self.marquee_pos > w:
            self.marquee_pos = - (num_blocks * step)

        self.marquee_timer = self.after(40, self._animate_marquee)


class ClassicProgressBar(RetroSegmentedProgressBar):
    """Backwards-compatible segmented blue blocks progress bar."""
    def __init__(self, parent, width=360, height=26, **kwargs):
        super().__init__(
            parent, width=width, height=height,
            chunk_color="#0055EA",
            chunk_light="#75B4FF",
            chunk_shadow="#0A3C96",
            **kwargs
        )


class RetroDialog(tk.Toplevel):
    """
    Authentic Windows 98 / 2000 / XP 3D Beveled Dialog Window:
    - Chromeless (overrideredirect) with sharp corners and authentic 3D beveled outer border
    - Gradient blue title bar (#0A246A to #A6CAF0) with draggable support
    - White bold title text and square beveled [X] close button
    - Window body: light beige/grey background (#ECE9D8)
    - Pixelated circular red X icon
    - Message text in Tahoma (plain sans-serif)
    - Beveled 3D buttons (raised look, dark outer border, light inner highlight)
    - Greyed-out/disabled state in flat-grey with light-grey text
    - Optional blue/green segmented-block progress bar
    """

    def __init__(
        self,
        parent,
        title="Error",
        message='A critical error has occurred.\n\nClick "Fix" to execute correction.',
        buttons=None,
        show_progress=False,
        progress_val=0.0,
        width=320,
        height=140,
    ):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.width = width
        self.height = height

        # If buttons not specified, default to [Fix, Cancel]
        if buttons is None:
            buttons = [("Fix", "ok", True, "normal"), ("Cancel", "cancel", False, "normal")]

        self.buttons_config = buttons
        self.show_progress = show_progress

        # Chromeless for authentic sharp corners & custom bevel border
        self.overrideredirect(True)
        self.configure(bg=WIN_BG)
        self.transient(parent)

        # Center relative to parent window
        self._center_window()

        # ── Draw Chunky 3D Beveled Outer Window Border ──
        self.outer_frame = tk.Frame(self, bg=WIN_BG, bd=0)
        self.outer_frame.pack(fill="both", expand=True)

        self._draw_outer_border()

        # ── Inset Gradient Title Bar ──
        self.title_bar = RetroTitleBar(
            self.content_container,
            title=title,
            close_command=self._on_close,
            height=22
        )
        self.title_bar.pack(fill="x", padx=1, pady=(1, 2))

        # ── Window Body ──
        self.body_frame = tk.Frame(self.content_container, bg=WIN_BG, bd=0)
        self.body_frame.pack(fill="both", expand=True, padx=6, pady=4)

        # Content Row (Icon + Message)
        top_row = tk.Frame(self.body_frame, bg=WIN_BG)
        top_row.pack(fill="x", pady=(2, 2))

        # Pixelated Circular Red X Icon
        self.icon_canvas = tk.Canvas(top_row, width=36, height=36, bg=WIN_BG, highlightthickness=0)
        self.icon_canvas.pack(side="left", padx=(2, 8), anchor="n")
        draw_pixel_error_icon(self.icon_canvas, size=36)

        # Tahoma Message Text
        self.msg_label = tk.Label(
            top_row,
            text=message,
            font=("Tahoma", 8),
            bg=WIN_BG,
            fg=WIN_TEXT,
            justify="left",
            wraplength=240,
            anchor="w",
        )
        self.msg_label.pack(side="left", fill="both", expand=True, anchor="w")

        # Optional Blue Segmented Progress Bar
        self.pbar = None
        if self.show_progress:
            prog_box = tk.Frame(self.body_frame, bg=WIN_BG)
            prog_box.pack(fill="x", pady=(4, 2))
            self.pbar = ClassicProgressBar(prog_box, width=300, height=16)
            self.pbar.pack(fill="x", padx=2)
            if progress_val > 0.0:
                self.pbar.set_progress(progress_val)
            else:
                self.pbar.start_marquee()

        # ── Beveled 3D Buttons Row ──
        btn_row = tk.Frame(self.body_frame, bg=WIN_BG)
        btn_row.pack(fill="x", side="bottom", pady=(4, 2))

        self.button_widgets = {}
        for item in reversed(self.buttons_config):
            label = item[0]
            action = item[1]
            is_def = item[2] if len(item) > 2 else False
            state = item[3] if len(item) > 3 else "normal"

            btn = RetroButton(
                btn_row,
                text=label,
                command=lambda act=action: self._button_clicked(act),
                width=68,
                height=22,
                font=("Tahoma", 8),
                is_default=is_def,
                state=state,
            )
            btn.pack(side="right", padx=3)
            self.button_widgets[action] = btn

        try:
            self.grab_set()
            self.focus_force()
        except Exception:
            pass

    def _center_window(self):
        try:
            px = self.parent.winfo_rootx()
            py = self.parent.winfo_rooty()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            x = px + (pw // 2) - (self.width // 2)
            y = py + (ph // 2) - (self.height // 2)
            self.geometry(f"{self.width}x{self.height}+{max(20, x)}+{max(20, y)}")
        except Exception:
            self.geometry(f"{self.width}x{self.height}+250+200")

    def _draw_outer_border(self):
        """Construct the chunky 3D beveled outer window border with sharp corners."""
        # Top outer highlight
        t_outer = tk.Frame(self.outer_frame, bg=WIN_BORDER_LIGHT, height=1)
        t_outer.pack(fill="x", side="top")
        # Left outer highlight
        l_outer = tk.Frame(self.outer_frame, bg=WIN_BORDER_LIGHT, width=1)
        l_outer.pack(fill="y", side="left")
        # Bottom outer dark shadow
        b_outer = tk.Frame(self.outer_frame, bg=WIN_BORDER_DARK, height=1)
        b_outer.pack(fill="x", side="bottom")
        # Right outer dark shadow
        r_outer = tk.Frame(self.outer_frame, bg=WIN_BORDER_DARK, width=1)
        r_outer.pack(fill="y", side="right")

        # Inner 3D border layer
        inner_wrap = tk.Frame(self.outer_frame, bg=WIN_BG, bd=0)
        inner_wrap.pack(fill="both", expand=True)

        t_inner = tk.Frame(inner_wrap, bg=WIN_BORDER_MIDLIGHT, height=1)
        t_inner.pack(fill="x", side="top")
        l_inner = tk.Frame(inner_wrap, bg=WIN_BORDER_MIDLIGHT, width=1)
        l_inner.pack(fill="y", side="left")
        b_inner = tk.Frame(inner_wrap, bg=WIN_BORDER_SHADOW, height=1)
        b_inner.pack(fill="x", side="bottom")
        r_inner = tk.Frame(inner_wrap, bg=WIN_BORDER_SHADOW, width=1)
        r_inner.pack(fill="y", side="right")

        self.content_container = tk.Frame(inner_wrap, bg=WIN_BG, bd=0)
        self.content_container.pack(fill="both", expand=True)

    def _button_clicked(self, action):
        self.result = action
        if self.pbar:
            self.pbar.stop_marquee()
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()

    def _on_close(self):
        self.result = "cancel"
        if self.pbar:
            self.pbar.stop_marquee()
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()


class RetroProgressDialog(tk.Toplevel):
    """
    Fake scanning / comic purge modal dialog:
    - Displays retro green segmented chunks progress bar
    - Funny status steps ("De-optimizing safe files...", "Corrupting healthy documents...")
    - Beveled 3D button (disabled flat-grey 'Abort' that turns to active 'OK' when complete)
    """

    def __init__(self, parent, title="Windows De-fender - Anti-Scan",
                 headline="Purging Safe Files...", on_complete=None):
        super().__init__(parent)
        self.parent = parent
        self.on_complete = on_complete
        self.width = 330
        self.height = 155
        self.current_step = 0

        self.overrideredirect(True)
        self.configure(bg=WIN_BG)
        self.transient(parent)

        try:
            px = self.parent.winfo_rootx()
            py = self.parent.winfo_rooty()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            x = px + (pw // 2) - (self.width // 2)
            y = py + (ph // 2) - (self.height // 2)
            self.geometry(f"{self.width}x{self.height}+{max(20, x)}+{max(20, y)}")
        except Exception:
            self.geometry(f"{self.width}x{self.height}+250+200")

        # 3D Outer Border
        outer = tk.Frame(self, bg=WIN_BG)
        outer.pack(fill="both", expand=True)

        tk.Frame(outer, bg=WIN_BORDER_LIGHT, height=1).pack(fill="x", side="top")
        tk.Frame(outer, bg=WIN_BORDER_LIGHT, width=1).pack(fill="y", side="left")
        tk.Frame(outer, bg=WIN_BORDER_DARK, height=1).pack(fill="x", side="bottom")
        tk.Frame(outer, bg=WIN_BORDER_DARK, width=1).pack(fill="y", side="right")

        inner = tk.Frame(outer, bg=WIN_BG)
        inner.pack(fill="both", expand=True)

        tk.Frame(inner, bg=WIN_BORDER_MIDLIGHT, height=1).pack(fill="x", side="top")
        tk.Frame(inner, bg=WIN_BORDER_MIDLIGHT, width=1).pack(fill="y", side="left")
        tk.Frame(inner, bg=WIN_BORDER_SHADOW, height=1).pack(fill="x", side="bottom")
        tk.Frame(inner, bg=WIN_BORDER_SHADOW, width=1).pack(fill="y", side="right")

        content = tk.Frame(inner, bg=WIN_BG)
        content.pack(fill="both", expand=True)

        # Title bar
        self.title_bar = RetroTitleBar(
            content,
            title=title,
            close_command=self._on_close,
            height=22,
        )
        self.title_bar.pack(fill="x", padx=1, pady=(1, 2))

        # Body
        body = tk.Frame(content, bg=WIN_BG)
        body.pack(fill="both", expand=True, padx=8, pady=4)

        top_box = tk.Frame(body, bg=WIN_BG)
        top_box.pack(fill="x", pady=(2, 3))

        icon_c = tk.Canvas(top_box, width=36, height=36, bg=WIN_BG, highlightthickness=0)
        icon_c.pack(side="left", padx=(0, 8))
        draw_pixel_error_icon(icon_c, size=36)

        info_box = tk.Frame(top_box, bg=WIN_BG)
        info_box.pack(side="left", fill="both", expand=True)

        tk.Label(
            info_box, text=headline,
            font=("Tahoma", 9, "bold"),
            bg=WIN_BG, fg=WIN_TEXT, anchor="w",
        ).pack(anchor="w", pady=(0, 2))

        self.status_lbl = tk.Label(
            info_box,
            text="Initializing reverse threat engine...",
            font=("Tahoma", 8),
            bg=WIN_BG, fg=WIN_MUTED, anchor="w",
            wraplength=240,
            justify="left",
        )
        self.status_lbl.pack(anchor="w")

        # Segmented Blue Blocks Progress Bar with Blue Strip
        self.pbar = ClassicProgressBar(body, width=300, height=16)
        self.pbar.pack(fill="x", pady=(4, 4))

        # Bottom Button Row
        btn_row = tk.Frame(body, bg=WIN_BG)
        btn_row.pack(fill="x", side="bottom", pady=(2, 2))

        # Abort button starts disabled (flat-grey with light-grey text)
        self.action_btn = RetroButton(
            btn_row,
            text="Abort",
            width=68,
            height=22,
            font=("Tahoma", 8),
            state="disabled",
            command=self._on_close,
        )
        self.action_btn.pack(side="right", padx=3)

        self.steps = [
            ("Scanning for healthy files that offend security...", 0.15),
            ("Bypassing firewalls to welcome harmless malware...", 0.35),
            ("Corrupting innocent documents to ensure 0% safety...", 0.60),
            ("Safely preserving malware specimens into museum vault...", 0.85),
            ("Clean files successfully wiped. System is delightfully unsafe!", 1.0),
        ]
        self._run_next_step()

        try:
            self.grab_set()
        except Exception:
            pass

    def _run_next_step(self):
        if self.current_step < len(self.steps):
            text, prog = self.steps[self.current_step]
            self.status_lbl.configure(text=text)
            self.pbar.set_progress(prog)
            self.current_step += 1
            self.after(350, self._run_next_step)
        else:
            self.action_btn.configure_button(text="OK", state="normal", command=self._on_done)

    def _on_done(self):
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()
        if self.on_complete:
            self.on_complete()

    def _on_close(self):
        try:
            self.grab_release()
        except Exception:
            pass
        self.destroy()


def show_retro_alert(parent, title="Error", message='Click "Fix" to fix error.',
                     ok_text="Fix", cancel_text="Cancel", show_progress=False,
                     buttons=None) -> bool:
    """
    Convenience helper to display the authentic retro Windows 3D beveled dialog.
    Returns True if user clicked ok_text (e.g. 'Fix'), False otherwise.
    """
    if buttons is None:
        buttons = []
        if ok_text:
            buttons.append((ok_text, "ok", True, "normal"))
        if cancel_text:
            buttons.append((cancel_text, "cancel", False, "normal"))

    dialog = RetroDialog(
        parent,
        title=title,
        message=message,
        buttons=buttons,
        show_progress=show_progress,
        width=320,
        height=140 if not show_progress else 175,
    )
    parent.wait_window(dialog)
    return dialog.result == "ok"


def show_comic_purge_modal(parent, on_complete=None):
    """
    Display the fake purge scanning modal with green segmented blocks.
    """
    dialog = RetroProgressDialog(parent, on_complete=on_complete)
    parent.wait_window(dialog)
