#----UPDATE JUST COMES OUT----# 

import keyboard
import os
import json
import threading
import time
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from plyer import notification

class MusicController:
    """A simple music controller for gamers using a 60% keyboard."""

    def __init__(self):
        """Set up the audio controller and load settings."""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"Error starting audio: {e}")
            raise
        
        self.current_volume = self.volume_interface.GetMasterVolumeLevelScalar()
        self.volume_step = 0.05  # How much volume changes with each press
        self.is_muted = self.volume_interface.GetMute()
        self.notifications_enabled = True  # Show pop-up messages by default
        self.focus_mode = False  # No notifications in focus mode
        self.load_settings()
        self.notify(f"Music Controller started | Volume: {self.current_volume * 100:.1f}%")
        
        # Start auto-saving settings in the background
        self.auto_save_interval = 300  # Save every 5 minutes
        self.start_auto_save()

    # --- Music Control Functions ---
    def play_pause_music(self):
        """Play or pause the current song."""
        keyboard.send('play/pause media')
        if not self.focus_mode:
            self.notify("Play/Pause toggled")

    def next_track(self):
        """Skip to the next song."""
        keyboard.send('next track')
        if not self.focus_mode:
            self.notify("Next track")

    def previous_track(self):
        """Go back to the previous song."""
        keyboard.send('previous track')
        if not self.focus_mode:
            self.notify("Previous track")

    # --- Volume Control Functions ---
    def increase_volume(self):
        """Turn the volume up by a small step."""
        if self.current_volume < 1.0:
            self.current_volume = min(self.current_volume + self.volume_step, 1.0)
            self.set_volume(self.current_volume)
            self.notify(f"Volume: {self.current_volume * 100:.1f}%")

    def decrease_volume(self):
        """Turn the volume down by a small step."""
        if self.current_volume > 0.0:
            self.current_volume = max(self.current_volume - self.volume_step, 0.0)
            self.set_volume(self.current_volume)
            self.notify(f"Volume: {self.current_volume * 100:.1f}%")

    def set_exact_volume(self, percentage):
        """Set the volume to an exact percentage (0-100)."""
        volume = max(0.0, min(float(percentage) / 100, 1.0))
        self.current_volume = volume
        self.set_volume(volume)
        self.notify(f"Volume set to: {volume * 100:.1f}%")

    def mute_unmute(self):
        """Mute or unmute the sound."""
        self.is_muted = not self.is_muted
        self.volume_interface.SetMute(self.is_muted, None)
        self.notify("Muted" if self.is_muted else "Unmuted")

    def set_volume(self, volume_level):
        """Change the system volume to a specific level."""
        try:
            self.volume_interface.SetMasterVolumeLevelScalar(volume_level, None)
        except Exception as e:
            print(f"Error changing volume: {e}")

    def adjust_volume_step(self, delta):
        """Change how big the volume steps are."""
        self.volume_step = max(0.01, min(self.volume_step + delta, 0.2))
        self.notify(f"Volume step: {self.volume_step:.2f}")

    # --- Notifications and Focus Mode ---
    def notify(self, message):
        """Show a pop-up message if notifications are on."""
        if self.notifications_enabled and not self.focus_mode:
            notification.notify(
                title="Music Controller",
                message=message,
                timeout=1  # Message disappears after 1 second
            )

    def toggle_notifications(self):
        """Turn notifications on or off."""
        self.notifications_enabled = not self.notifications_enabled
        self.notify(f"Notifications {'enabled' if self.notifications_enabled else 'disabled'}")

    def toggle_focus_mode(self):
        """Turn focus mode on or off (no notifications in focus mode)."""
        self.focus_mode = not self.focus_mode
        print(f"Focus mode {'enabled' if self.focus_mode else 'disabled'}")

    # --- Settings Functions ---
    def load_settings(self):
        """Load saved settings from a file."""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.current_volume = settings.get('volume', self.current_volume)
                    self.volume_step = settings.get('volume_step', self.volume_step)
                    self.is_muted = settings.get('is_muted', self.is_muted)
                    self.notifications_enabled = settings.get('notifications', True)
                    self.set_volume(self.current_volume)
                    self.volume_interface.SetMute(self.is_muted, None)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save current settings to a file."""
        settings = {
            'volume': self.current_volume,
            'volume_step': self.volume_step,
            'is_muted': self.is_muted,
            'notifications': self.notifications_enabled
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def start_auto_save(self):
        """Start a background task to save settings every few minutes."""
        def auto_save_loop():
            while True:
                time.sleep(self.auto_save_interval)
                self.save_settings()
                print("Settings auto-saved")
        
        threading.Thread(target=auto_save_loop, daemon=True).start()

# Start the controller
try:
    controller = MusicController()

    # Keyboard shortcuts
    keyboard.add_hotkey('ctrl+alt+p', controller.play_pause_music)
    keyboard.add_hotkey('ctrl+alt+up', controller.increase_volume)
    keyboard.add_hotkey('ctrl+alt+down', controller.decrease_volume)
    keyboard.add_hotkey('ctrl+alt+right', lambda: controller.adjust_volume_step(0.01))
    keyboard.add_hotkey('ctrl+alt+left', lambda: controller.adjust_volume_step(-0.01))
    keyboard.add_hotkey('ctrl+alt+m', controller.mute_unmute)
    keyboard.add_hotkey('ctrl+alt+shift+right', controller.next_track)
    keyboard.add_hotkey('ctrl+alt+shift+left', controller.previous_track)
    # New shortcuts
    keyboard.add_hotkey('ctrl+alt+n', controller.toggle_notifications)
    keyboard.add_hotkey('ctrl+alt+f', controller.toggle_focus_mode)

    # Wait for the user to stop the program
    keyboard.wait()
except KeyboardInterrupt:
    controller.save_settings()
    print("Program stopped, settings saved.")
except Exception as e:
    print(f"Something went wrong: {e}")
