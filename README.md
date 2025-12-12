# HiraganaKatakanaPractice
A program that allows you to write and trace katakana and hiragana characters for practice.

## Features
- Practice all 46 basic Hiragana characters
- Practice all 46 basic Katakana characters
- **Pen/Stylus-Only Mode** - Designed specifically for active stylus input (tested on Lenovo ThinkPad Y1 Yoga)
- **Beautiful Pressure-Sensitive Brush** - Smooth, calligraphy-style strokes with variable pressure
- **Hover Detection** - See preview strokes as your pen approaches the screen
- **Fullscreen Support** - Optimized for Lenovo Y1 Yoga and other high-DPI displays
- Stroke order guides with numbered indicators
- Character completion detection with confetti celebration
- Japanese text-to-speech (TTS) for pronunciation
- Responsive layout that adapts to window resizing
- Toggle between Hiragana and Katakana modes

## Requirements
- Python 3.7+
- pygame 2.5.0+
- gTTS 2.3.0+ (for text-to-speech)
- numpy 1.24.0+ (for audio effects)
- **Active Stylus/Pen** - This application requires a pressure-sensitive stylus
- **Japanese Fonts** - Run `install_fonts.py` to check/install required fonts
- Touch screen device with pen/stylus support (Lenovo ThinkPad Y1 Yoga recommended)

## Installation

### Step 1: Install Python and Dependencies

#### Arch Linux
```bash
# Install Python and pip if not already installed
sudo pacman -S python python-pip

# Install dependencies
pip install -r requirements.txt
```

#### Windows
```bash
# Install Python from python.org if not already installed
# Then install dependencies:
pip install -r requirements.txt
```

### Step 2: Check Japanese Fonts

Run the font checker to ensure you have Japanese character support:
```bash
python install_fonts.py
```

This will:
- Check for required Japanese fonts
- Test Japanese character rendering
- Download/install Noto Sans CJK JP if needed
- Provide instructions for installing Windows Japanese language pack

## Usage

Run the application:
```bash
python practice.py
```

Or make it executable and run directly (Linux):
```bash
chmod +x practice.py
./practice.py
```

## Controls

### Drawing
- **Active Stylus/Pen Only**: Draw over the character with your pressure-sensitive pen
- **Pressure**: Lighter touch = thinner stroke, heavier = thicker stroke
- **Hover**: Hold pen near screen to see preview before drawing
- **Mouse**: Only works for button clicks, NOT for drawing

### Navigation
- **LEFT/RIGHT Arrow Keys**: Navigate between characters
- **SPACE**: Next character

### Actions
- **C**: Clear your drawing
- **T**: Toggle between Hiragana and Katakana modes
- **S**: Speak/pronounce the current character (Japanese TTS)
- **G**: Toggle stroke order guides on/off
- **F or F11**: Toggle fullscreen mode
- **ESC or Q**: Quit the application

### Buttons
All controls are also available as buttons at the bottom of the screen:
- **Previous** / **Next**: Navigate characters
- **Clear**: Clear your drawing
- **Toggle**: Switch Hiragana ↔ Katakana
- **Sound**: Hear pronunciation
- **Guide**: Show/hide stroke order guides
- **Fullscreen**: Toggle fullscreen mode
- **Quit**: Exit application

## How to Use
1. Launch the application on your tablet/convertible PC
2. Remove your stylus from its socket (the app will detect it)
3. You'll see a large, opaque Japanese character in the center with numbered stroke order guides
4. Use your stylus to trace over the character following the numbered guides
5. Hover your pen to see a preview before touching the screen
6. Apply pressure for darker, thicker strokes
7. When you complete the character correctly, confetti will celebrate!
8. Press 'C' to clear and try again
9. Use arrow keys or SPACE to move to the next character
10. Press 'T' to switch between Hiragana and Katakana

## Pen Socket Detection
The application is optimized for devices with pen storage (like Lenovo Y1 Yoga). When you remove your pen from its socket, the app will be ready for input.

## Fullscreen Mode
Press **F11** or click the **Fullscreen** button to enter fullscreen mode. This is optimized for Lenovo Y1 Yoga and other high-DPI displays to prevent off-screen positioning issues.

## Troubleshooting

### No Japanese Characters Showing
Run `python install_fonts.py` to install required Japanese fonts.

### Pen Not Detected
- Make sure you're using an active stylus with pressure sensitivity
- Remove the pen from its socket before using
- Try touching the screen with the pen tip - the app will auto-detect

### Fullscreen Goes Off-Screen
- This should be fixed in the latest version using proper display detection
- If issues persist, press ESC to exit fullscreen and report the issue

## Tested Hardware
- Lenovo ThinkPad Y1 Yoga with active stylus
- Windows 10/11 with high-DPI display support

## License
MIT License

## Notes
- The application supports pen pressure and stylus input through pygame's event system
- Works best with touch screen devices like Lenovo Yoga series
- Mouse input is also supported for testing without a stylus
- The character display uses semi-transparent rendering for easy tracing

## License
This is an educational project for learning Japanese characters.
