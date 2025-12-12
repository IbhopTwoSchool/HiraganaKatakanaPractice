# HiraganaKatakanaPractice
A program that allows you to write and trace katakana and hiragana characters for practice.

## Features
- Practice all 46 basic Hiragana characters
- Practice all 46 basic Katakana characters
- Pen/stylus support for touch screen devices (tested on Lenovo Yoga)
- Opaque characters for easy tracing
- Simple navigation between characters
- Clear drawing function to retry

## Requirements
- Python 3.7+
- pygame 2.5.0+
- Touch screen device with pen/stylus support (optional, mouse also works)

## Installation

### Arch Linux
```bash
# Install Python and pip if not already installed
sudo pacman -S python python-pip

# Install dependencies
pip install -r requirements.txt
```

### Windows
```bash
# Install Python from python.org if not already installed
# Then install dependencies:
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python practice.py
```

Or make it executable and run directly:
```bash
chmod +x practice.py
./practice.py
```

## Controls
- **Pen/Stylus or Mouse**: Draw over the character
- **LEFT/RIGHT Arrow Keys**: Navigate between characters
- **SPACE**: Next character
- **C**: Clear your drawing
- **T**: Toggle between Hiragana and Katakana modes
- **ESC or Q**: Quit the application

## How to Use
1. Launch the application
2. You'll see a large, opaque Japanese character in the center
3. Use your pen/stylus to trace over the character
4. Press 'C' to clear and try again
5. Use arrow keys or SPACE to move to the next character
6. Press 'T' to switch between Hiragana and Katakana

## Notes
- The application supports pen pressure and stylus input through pygame's event system
- Works best with touch screen devices like Lenovo Yoga series
- Mouse input is also supported for testing without a stylus
- The character display uses semi-transparent rendering for easy tracing

## License
This is an educational project for learning Japanese characters.
