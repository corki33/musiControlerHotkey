 __    __     __  __     ______     __     ______     ______     __   __     ______   ______     ______     __         ______     ______     __  __     ______     ______   __  __     ______     __  __    
/\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  ___\   /\  __ \   /\ "-.\ \   /\__  _\ /\  == \   /\  __ \   /\ \       /\  ___\   /\  == \   /\ \_\ \   /\  __ \   /\__  _\ /\ \/ /    /\  ___\   /\ \_\ \   
\ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \ \____  \ \ \/\ \  \ \ \-.  \  \/_/\ \/ \ \  __<   \ \ \/\ \  \ \ \____  \ \  __\   \ \  __<   \ \  __ \  \ \ \/\ \  \/_/\ \/ \ \  _"-.  \ \  __\   \ \____ \  
 \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_____\  \ \_____\  \ \_\\"\_\    \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\    \ \_\  \ \_\ \_\  \ \_____\  \/\_____\ 
  \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_____/   \/_____/   \/_/ \/_/     \/_/   \/_/ /_/   \/_____/   \/_____/   \/_____/   \/_/ /_/   \/_/\/_/   \/_____/     \/_/   \/_/\/_/   \/_____/   \/_____/ 
                                                                                                                                                                                                          





Hello, I created a program in python that will allow you to control music played in the background of the system. I was directed to create it because I bought a new 65% keyboard that has no multimedia buttons, which did not allow me to control the music. Of course, the program will be improved and updated over time. Enjoy the music :D  

!IMPORTANT!
You need to download the necessary python syntax in terminal using pip or just run the program in 'downloadLibrary.bat' - It will download the necessary stuff and tools.

UPDATE!! 2025/21/02 !!!

What's new and improved?
Focus Mode - Enabled with Ctrl+Alt+F. Disables notifications, perfect for full-screen gaming.
Turning notifications on/off - Ctrl+Alt+N. Players can turn them off if they're distracting.
Setting a specific volume level - The set_exact_volume function, although it requires a call from the code (you can add a shortcut, e.g. after entering the value).
Auto-save - Settings are saved every 5 minutes in the background, thanks to a thread.
Shorter notifications - Timeout reduced to 1 second, less intrusive.
Better error handling - The program won't crash if there's a problem with the audio device or settings file.
Comments and docstrings - The code is more readable and easier to modify.
Suggestions for further changes:
Configuration file for shortcuts - You can add loading shortcuts from JSON, e.g. hotkeys.json, to easily change them without editing the code.
Console interface - If you want.
Game detection - The program could automatically enable Focus Mode when it detects a full-screen application (e.g. via psutil).

               
KEYBOARDOLOGY: (⬆⬆⬆⬆⬆CHECK UP NEW KEYS⬆⬆⬆⬆)

ctrl + alt + p 	 	music controller play pause music
ctrl + alt + up	 	music controller increase volume
ctrl + alt + down	 	music controller decrease volume
ctrl + alt + right	 	music controller increase volume step
ctrl + alt + left	 	music controller decrease volume step
ctrl + alt + m 		music controller mute & unmute
ctrl + alt + shift + right	 music controller next track
ctrl + alt + shift + left	 music controller previous track
