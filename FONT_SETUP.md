# Font Setup Guide

## Why Fonts Matter

This application displays:
- **Japanese characters** (hiragana/katakana) - requires Japanese fonts
- **UI elements with emojis** (📚, 💡, ✏️, etc.) - requires emoji fonts
- **Educational information** - requires Unicode support

If you see empty boxes (□) or missing symbols, you need to install fonts.

## Automatic Detection

The program automatically detects if emoji fonts are available. On startup, if emojis aren't supported, you'll see:
```
⚠️  Emoji font not detected. Using text labels instead.
💡 To enable emojis:
   [Installation instructions for your OS]
```

## Font Installation by Operating System

### Windows 10/11

**Japanese Fonts:** Already included by default
- MS Gothic (msgothic)
- Meiryo (meiryo)
- Yu Gothic (yugothic)

**Emoji Fonts:** Already included by default
- Segoe UI Emoji (automatic)

**If emojis don't work:**
1. Check Windows is up to date: Settings → Windows Update
2. Emoji font might be disabled:
   - Go to Settings → Personalization → Fonts
   - Search for "Segoe UI Emoji"
   - If missing, update Windows or download from Microsoft

### Linux (Debian/Ubuntu)

**Install Japanese fonts:**
```bash
sudo apt update
sudo apt install fonts-noto-cjk fonts-noto-cjk-extra
```

**Install emoji fonts:**
```bash
sudo apt install fonts-noto-color-emoji
```

**Alternative fonts:**
```bash
# IPA fonts (good for Japanese)
sudo apt install fonts-ipafont fonts-ipaexfont

# VL Gothic
sudo apt install fonts-vlgothic

# Takao fonts
sudo apt install fonts-takao-gothic
```

### Linux (Arch/Manjaro)

**Install Japanese fonts:**
```bash
sudo pacman -S noto-fonts-cjk
```

**Install emoji fonts:**
```bash
sudo pacman -S noto-fonts-emoji
```

**Alternative fonts:**
```bash
# Adobe Source Han Sans (excellent quality)
sudo pacman -S adobe-source-han-sans-jp-fonts

# IPA fonts
sudo pacman -S otf-ipafont
```

### macOS

**Japanese Fonts:** Already included by default
- Hiragino Sans
- Hiragino Mincho

**Emoji Fonts:** Already included by default
- Apple Color Emoji (automatic)

**If Japanese characters don't display:**
1. Open Font Book
2. File → Restore Standard Fonts
3. Make sure Hiragino fonts are enabled

## Verifying Font Installation

### Command Line Check

**Linux/macOS:**
```bash
# List Japanese fonts
fc-list :lang=ja

# List emoji fonts
fc-list | grep -i emoji
```

**Windows PowerShell:**
```powershell
# List all fonts
Get-ChildItem C:\Windows\Fonts\ | Select-Object Name
```

### In-Program Check

Run the program. On the console, check the startup messages:
- ✅ If emoji fonts work: No warning messages
- ⚠️ If emoji fonts missing: Warning with installation instructions

## Font Packages Recommended

### For Japanese Language Support

**Best Quality:**
- **Noto Sans CJK JP** - Google's open-source font, excellent Unicode coverage
- **Adobe Source Han Sans** - Professional-grade, used in publishing

**Good Alternatives:**
- **IPA Gothic/Mincho** - Standard Japanese fonts
- **VL Gothic** - Lightweight, good for older systems
- **Takao fonts** - Modified IPA fonts with better metrics

### For Emoji Support

**Color Emojis:**
- **Noto Color Emoji** (Linux/Android) - Full color, comprehensive
- **Segoe UI Emoji** (Windows) - Microsoft's color emoji font
- **Apple Color Emoji** (macOS) - Apple's color emoji font

**Monochrome Emojis:**
- **Noto Emoji** - Black and white version
- **Symbola** - Extensive Unicode symbol coverage

## Troubleshooting

### Issue: Still seeing empty boxes after installing fonts

**Solution 1: Rebuild font cache (Linux)**
```bash
sudo fc-cache -fv
```

**Solution 2: Restart the application**
- Fonts are loaded when the program starts
- Close and reopen after installing fonts

**Solution 3: Check font names**
```python
# Test in Python
import pygame
pygame.init()
print(pygame.font.get_fonts())  # List all available fonts
```

### Issue: Japanese characters work but emojis don't

**This is normal** - the program has fallback text labels:
- Instead of 📚 you'll see `[Words]`
- Instead of 💡 you'll see `[Usage]`
- Instead of ✏️ you'll see `[PEN]`

The program remains fully functional without emoji support.

### Issue: Emojis show as black/white instead of color

**This is fine!** Many emoji fonts are monochrome:
- Noto Emoji (Linux)
- Symbola (cross-platform)

The program works perfectly with monochrome emojis.

## Recommended Font Setup

### Minimal Setup (Required)
```bash
# Linux
sudo apt install fonts-noto-cjk

# Arch
sudo pacman -S noto-fonts-cjk

# Windows/macOS: Already included
```

### Full Setup (Recommended)
```bash
# Linux (Debian/Ubuntu)
sudo apt install fonts-noto-cjk fonts-noto-color-emoji fonts-noto-cjk-extra

# Linux (Arch)
sudo pacman -S noto-fonts-cjk noto-fonts-emoji adobe-source-han-sans-jp-fonts

# Windows/macOS: Check Windows Update / Font Book
```

## Font Sources

### Official Repositories

- **Noto Fonts:** https://github.com/notofonts/
- **Google Fonts:** https://fonts.google.com/noto
- **Adobe Source Han:** https://github.com/adobe-fonts/source-han-sans

### System Font Locations

- **Windows:** `C:\Windows\Fonts\`
- **Linux:** `/usr/share/fonts/`, `~/.fonts/`
- **macOS:** `/Library/Fonts/`, `/System/Library/Fonts/`

## Need Help?

If fonts still don't work:
1. Check the console output when starting the program
2. Verify fonts are installed: run `fc-list` (Linux/Mac) or check Fonts folder (Windows)
3. Try the fallback text mode - the app works perfectly without emojis
4. Open an issue on GitHub with your OS and font list

## Performance Note

Having many fonts installed can slightly slow down font loading. This is normal. The application caches fonts after the first load.
