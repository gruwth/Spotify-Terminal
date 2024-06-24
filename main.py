from rich import print
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.box import MINIMAL
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from time import sleep
from datetime import timedelta as td
import keyboard

import sys
import termios
import tty
import atexit
from select import select

from functions import authenticate_spotify, get_current_playing, toggle_playback

# start :3
console = Console()
layout = Layout()

# Define layout sections
layout.split(
    Layout(name="header", size=3),
    Layout(name="main", ratio=1),
    Layout(name="footer", size=8),
)

layout["main"].split_row(
    Layout(name="side"),
    Layout(name="body", ratio=2)
)


layout["side"].split(Layout(), Layout())

# panel mor like penis hehe
body_panel = Panel("", title="Recently Played", border_style="white", title_align="left")
footer_panel = Panel("", title="Currently Playing", border_style="white", title_align="left")

# bawr go brrrr
progress = Progress(
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.0f}%",
    expand=True
)
progress_task = progress.add_task("Playing...", total=100)  # Placeholder total

layout["body"].update(body_panel)
layout["footer"].update(footer_panel)

# keybwoard things
def setup_key_hooks(sp):
    """Set up keyboard hooks for controlling playback with the spacebar."""

    def on_space_press(event):
        if event.name == 'space':
            is_playing = get_current_playing(sp)['is_playing']
            toggle_playback(sp, is_playing)

    keyboard.on_press(on_space_press)

def disable_echo():
    """Disable the keyboard input echo in the terminal."""
    # Save the terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    # Function to restore the old settings when the program exits
    def restore_settings():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    atexit.register(restore_settings)
    # New terminal settings with no echo
    new_settings = termios.tcgetattr(fd)
    new_settings[3] = new_settings[3] & ~termios.ECHO  # lflags
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

def check_key():
    """Check if a keypress is available."""
    if select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    return None

disable_echo()
# live update für fortnite
with Live(layout, screen=True):
    sp = authenticate_spotify()
    setup_key_hooks(sp)
    while True:
        playing_info = get_current_playing(sp)

        # maths
        total_seconds = playing_info['duration_ms'] / 1000
        elapsed_seconds = playing_info['progress_ms'] / 1000
        total_time_str = str(td(seconds=int(total_seconds)))[2:]
        elapsed_time_str = str(td(seconds=int(elapsed_seconds)))[2:]

        # update bawr
        progress.update(progress_task, completed=elapsed_seconds, total=total_seconds)

        # txet
        track_details = Text(f"{playing_info['track_name']}\n{playing_info['artists']}")
        time_details = Text(f"Elapsed: {elapsed_time_str} / Total: {total_time_str}", style="bold")

        # update info yay working :3
        body_panel.renderable = Panel(
            Text("Recent Tracks", style="bold"),
            border_style="white",
            title_align="left",
            box=MINIMAL
        )
        footer_panel.renderable = Panel(
            Group(track_details, time_details, progress),
            border_style="white",
            title_align="left",
            box=MINIMAL
        )

        sleep(1)
