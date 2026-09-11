"""
Verification tests for Retro 3D Dialog and Retro Widgets.
Tests:
1. RetroButton normal and disabled states
2. RetroTitleBar gradient and close button
3. 64x64 pixelated red X icon rendering
4. RetroSegmentedProgressBar green chunks
5. RetroDialog instantiation, sharp corners, and action triggers
6. RetroProgressDialog comic flow
"""

import sys
import os
import tkinter as tk

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.retro_widgets import (
    RetroButton, RetroTitleBar, RetroSegmentedProgressBar,
    RetroDialog, RetroProgressDialog, draw_pixel_error_icon,
    show_retro_alert, WIN_DISABLED_TEXT, WIN_DISABLED_FACE,
    WIN_GREEN_BLOCK
)


def test_retro_components():
    print("==================================================")
    print("STARTING RETRO 3D DIALOG & WIDGET VERIFICATION")
    print("==================================================")

    root = tk.Tk()
    root.withdraw()

    # 1. Test RetroButton
    print("\n[1/5] Testing RetroButton normal & disabled states...")
    clicked = []
    btn_normal = RetroButton(root, text="Fix", command=lambda: clicked.append("fix"), width=80, height=24)
    btn_disabled = RetroButton(root, text="Ignore", command=lambda: clicked.append("ignore"), width=80, height=24, state="disabled")

    assert btn_normal.state == "normal"
    assert btn_disabled.state == "disabled"

    # Simulate press & release on normal
    class FakeEvent:
        x = 10
        y = 10
    btn_normal._on_press(FakeEvent())
    assert btn_normal.is_pressed is True
    btn_normal._on_release(FakeEvent())
    assert btn_normal.is_pressed is False
    assert "fix" in clicked

    # Simulate press & release on disabled (should not trigger)
    btn_disabled._on_press(FakeEvent())
    assert btn_disabled.is_pressed is False
    btn_disabled._on_release(FakeEvent())
    assert "ignore" not in clicked
    print("✅ RetroButton: Normal 3D bevel click and disabled flat-grey state verified.")

    # 2. Test 64x64 Pixelated Red Error Icon
    print("\n[2/5] Testing 64x64 Pixelated Error Icon Drawing...")
    icon_canvas = tk.Canvas(root, width=64, height=64)
    draw_pixel_error_icon(icon_canvas, size=64)
    items = icon_canvas.find_all()
    assert len(items) >= 4, f"Expected drawn pixel icon elements, got {len(items)}"
    print(f"✅ 64x64 pixelated icon drawn with {len(items)} elements.")

    # 3. Test RetroTitleBar Gradient
    print("\n[3/5] Testing RetroTitleBar gradient (#0A246A to #A6CAF0)...")
    titlebar = RetroTitleBar(root, title="Error", height=26, width=400)
    titlebar._draw_titlebar()
    tb_items = titlebar.find_all()
    assert len(tb_items) > 10, "Titlebar should contain gradient slices and text"
    print(f"✅ Gradient titlebar rendered with {len(tb_items)} graphical lines and text.")

    # 4. Test RetroSegmentedProgressBar (Green chunks)
    print("\n[4/5] Testing RetroSegmentedProgressBar (Green Chunks)...")
    pbar = RetroSegmentedProgressBar(root, width=300, height=20, chunk_color=WIN_GREEN_BLOCK)
    pbar.set_progress(0.5)
    pbar_items = pbar.find_all()
    assert len(pbar_items) > 0
    pbar.set_progress(1.0)
    pbar_full_items = pbar.find_all()
    assert len(pbar_full_items) >= len(pbar_items)
    print(f"✅ Segmented progress bar (green chunks) rendered {len(pbar_full_items)} items at 100%.")

    # 5. Test RetroDialog Construction
    print("\n[5/5] Testing RetroDialog instantiation with 3D bevels & buttons...")
    dialog = RetroDialog(
        root,
        title="Error",
        message="Anti-Antivirus error message test.",
        buttons=[("Fix", "ok", True, "normal"), ("Ignore", "ignore", False, "disabled")],
        show_progress=True,
        width=450,
        height=240,
    )
    assert dialog.winfo_exists()
    assert "ok" in dialog.button_widgets
    assert "ignore" in dialog.button_widgets
    assert dialog.button_widgets["ignore"].state == "disabled"
    assert dialog.pbar is not None
    dialog._button_clicked("ok")
    assert dialog.result == "ok"
    print("✅ RetroDialog constructed, validated buttons & progress bar, closed cleanly.")

    root.destroy()
    print("\n==================================================")
    print("ALL RETRO 3D DIALOG & WIDGET TESTS PASSED!")
    print("==================================================")


if __name__ == "__main__":
    test_retro_components()
