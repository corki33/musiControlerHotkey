import keyboard
import os
import json
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from plyer import notification

class MusicController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, 
            CLSCTX_ALL, 
            None
        )
        self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
        self.current_volume = self.volume_interface.GetMasterVolumeLevelScalar()
        self.volume_step = 0.05  
        self.is_muted = self.volume_interface.GetMute()
        self.load_settings()
        self.show_notification(f"Initial volume: {self.current_volume * 100:.1f}%")
    
    def play_pause_music(self):
        keyboard.send('play/pause media')

    def next_track(self):
        keyboard.send('next track')

    def previous_track(self):
        keyboard.send('previous track')

    def increase_volume(self):
        if self.current_volume < 1.0:
            self.current_volume = min(self.current_volume + self.volume_step, 1.0)
            self.set_volume(self.current_volume)
            self.show_notification(f"Volume increased to: {self.current_volume * 100:.1f}%")

    def decrease_volume(self):
        if self.current_volume > 0.0:
            self.current_volume = max(self.current_volume - self.volume_step, 0.0)
            self.set_volume(self.current_volume)
            self.show_notification(f"Volume decreased to: {self.current_volume * 100:.1f}%")

    def mute_unmute(self):
        self.is_muted = not self.is_muted
        self.volume_interface.SetMute(self.is_muted, None)
        status = "Muted" if self.is_muted else "Unmuted"
        self.show_notification(status)

    def set_volume(self, volume_level):
        self.volume_interface.SetMasterVolumeLevelScalar(volume_level, None)

    def increase_volume_step(self):
        self.volume_step = min(self.volume_step + 0.01, 0.1)
        self.show_notification(f"Volume step increased to: {self.volume_step:.2f}")

    def decrease_volume_step(self):
        self.volume_step = max(self.volume_step - 0.01, 0.01)
        self.show_notification(f"Volume step decreased to: {self.volume_step:.2f}")

    def show_notification(self, message):
        notification.notify(
            title="Music Controller",
            message=message,
            timeout=2
        )

    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.current_volume = settings.get('volume', self.current_volume)
                self.volume_step = settings.get('volume_step', self.volume_step)
                self.is_muted = settings.get('is_muted', self.is_muted)
                self.set_volume(self.current_volume)
                self.volume_interface.SetMute(self.is_muted, None)

    def save_settings(self):
        settings = {
            'volume': self.current_volume,
            'volume_step': self.volume_step,
            'is_muted': self.is_muted
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

music_controller = MusicController()

keyboard.add_hotkey('ctrl+alt+p', music_controller.play_pause_music)
keyboard.add_hotkey('ctrl+alt+up', music_controller.increase_volume)
keyboard.add_hotkey('ctrl+alt+down', music_controller.decrease_volume)
keyboard.add_hotkey('ctrl+alt+right', music_controller.increase_volume_step)
keyboard.add_hotkey('ctrl+alt+left', music_controller.decrease_volume_step)
keyboard.add_hotkey('ctrl+alt+m', music_controller.mute_unmute)
keyboard.add_hotkey('ctrl+alt+shift+right', music_controller.next_track)
keyboard.add_hotkey('ctrl+alt+shift+left', music_controller.previous_track)

try:
    keyboard.wait()
except KeyboardInterrupt:
    music_controller.save_settings()
    pass
