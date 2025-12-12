#!/usr/bin/env python3
"""
Font Installation Script for Hiragana & Katakana Practice

This script checks for required Japanese fonts and helps install them if missing.
"""

import sys
import os
import pygame
import ctypes
from ctypes import wintypes
import subprocess
import urllib.request
import tempfile

# Required fonts for Japanese character display
REQUIRED_FONTS = [
    'msgothic',      # MS Gothic
    'meiryo',        # Meiryo
    'mspgothic',     # MS PGothic
    'yugothic',      # Yu Gothic
    'msmincho'       # MS Mincho
]

# Font download URLs (for open-source alternatives if system fonts not available)
FONT_DOWNLOADS = {
    'Noto Sans CJK JP': {
        'url': 'https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf',
        'filename': 'NotoSansCJKjp-Regular.otf'
    }
}


def init_pygame():
    """Initialize pygame for font detection."""
    try:
        pygame.init()
        return True
    except Exception as e:
        print(f"Error initializing pygame: {e}")
        return False


def check_font_available(font_name):
    """Check if a specific font is available in the system."""
    try:
        # Try to create a font with this name
        font = pygame.font.SysFont(font_name, 24)
        # Get the actual font name pygame is using
        actual_name = pygame.font.get_fonts()
        # Check if our requested font is in the system fonts
        return font_name.lower() in [f.lower() for f in pygame.font.get_fonts()]
    except:
        return False


def list_japanese_fonts():
    """List all available Japanese-compatible fonts."""
    all_fonts = pygame.font.get_fonts()
    japanese_keywords = ['gothic', 'mincho', 'meiryo', 'yu', 'noto', 'cjk']
    
    japanese_fonts = []
    for font in all_fonts:
        for keyword in japanese_keywords:
            if keyword in font.lower():
                japanese_fonts.append(font)
                break
    
    return japanese_fonts


def test_japanese_rendering():
    """Test if Japanese characters can be rendered properly."""
    test_chars = ['あ', 'カ', '漢']
    fonts = ['msgothic', 'meiryo', 'mspgothic', 'yugothic', 'msmincho']
    
    working_fonts = []
    for font_name in fonts:
        try:
            font = pygame.font.SysFont(font_name, 48)
            # Try to render each test character
            all_ok = True
            for char in test_chars:
                try:
                    surface = font.render(char, True, (0, 0, 0))
                    # Check if the surface has content (not just blank)
                    if surface.get_width() > 0 and surface.get_height() > 0:
                        continue
                    else:
                        all_ok = False
                        break
                except:
                    all_ok = False
                    break
            
            if all_ok:
                working_fonts.append(font_name)
        except:
            pass
    
    return working_fonts


def download_noto_sans():
    """Download Noto Sans CJK JP font if needed."""
    print("\nDownloading Noto Sans CJK JP font...")
    print("This is a free, open-source font that supports Japanese characters.\n")
    
    font_info = FONT_DOWNLOADS['Noto Sans CJK JP']
    temp_dir = tempfile.gettempdir()
    font_path = os.path.join(temp_dir, font_info['filename'])
    
    try:
        print(f"Downloading from: {font_info['url']}")
        urllib.request.urlretrieve(font_info['url'], font_path)
        print(f"✓ Downloaded to: {font_path}")
        return font_path
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None


def install_font_windows(font_path):
    """Install a font on Windows."""
    if not os.path.exists(font_path):
        print(f"Font file not found: {font_path}")
        return False
    
    try:
        # Get Windows Fonts folder
        fonts_folder = os.path.join(os.environ['WINDIR'], 'Fonts')
        
        # Copy font to Fonts folder (requires admin)
        font_filename = os.path.basename(font_path)
        dest_path = os.path.join(fonts_folder, font_filename)
        
        # Try to copy the font
        import shutil
        shutil.copy2(font_path, dest_path)
        
        # Register the font in Windows registry
        # This requires admin privileges
        print(f"✓ Font installed to: {dest_path}")
        print("\n⚠️  You may need to restart the application for the font to be available.")
        return True
    except PermissionError:
        print("\n⚠️  Permission denied. Please run this script as Administrator to install fonts.")
        print(f"   Or manually copy the font file to: {fonts_folder}")
        return False
    except Exception as e:
        print(f"✗ Error installing font: {e}")
        return False


def main():
    """Main font checker and installer."""
    print("=" * 60)
    print("Japanese Font Checker for Hiragana & Katakana Practice")
    print("=" * 60)
    
    # Initialize pygame
    if not init_pygame():
        print("✗ Failed to initialize pygame. Please install pygame first:")
        print("  pip install pygame")
        return 1
    
    print("\n[Step 1] Checking for required Japanese fonts...\n")
    
    # Check each required font
    found_fonts = []
    missing_fonts = []
    
    for font_name in REQUIRED_FONTS:
        is_available = check_font_available(font_name)
        status = "✓" if is_available else "✗"
        print(f"  {status} {font_name}")
        
        if is_available:
            found_fonts.append(font_name)
        else:
            missing_fonts.append(font_name)
    
    print(f"\nFound {len(found_fonts)} out of {len(REQUIRED_FONTS)} required fonts.")
    
    # Test Japanese rendering
    print("\n[Step 2] Testing Japanese character rendering...\n")
    working_fonts = test_japanese_rendering()
    
    if working_fonts:
        print(f"✓ Found {len(working_fonts)} working Japanese fonts:")
        for font in working_fonts:
            print(f"  - {font}")
    else:
        print("✗ No working Japanese fonts found!")
    
    # List all available Japanese fonts
    print("\n[Step 3] All available Japanese-compatible fonts:\n")
    japanese_fonts = list_japanese_fonts()
    
    if japanese_fonts:
        for font in japanese_fonts:
            print(f"  - {font}")
    else:
        print("  (none found)")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if len(working_fonts) >= 1:
        print("\n✓ Your system has sufficient Japanese font support!")
        print("  The practice application should work correctly.\n")
        return 0
    else:
        print("\n⚠️  Your system needs Japanese font support!")
        print("\nOption 1: Install Windows Japanese Language Pack (RECOMMENDED)")
        print("  1. Open Settings > Time & Language > Language")
        print("  2. Add 'Japanese' as a language")
        print("  3. This will install all required Japanese fonts automatically")
        
        print("\nOption 2: Download and install Noto Sans CJK JP font")
        print("  This script can download a free Japanese font for you.")
        
        response = input("\nWould you like to download Noto Sans CJK JP now? (y/n): ")
        
        if response.lower() == 'y':
            font_path = download_noto_sans()
            if font_path:
                print("\n[Step 4] Installing font...\n")
                if install_font_windows(font_path):
                    print("\n✓ Font installation successful!")
                else:
                    print(f"\n⚠️  Please manually install the font from: {font_path}")
                    print("   1. Double-click the font file")
                    print("   2. Click 'Install' in the font preview window")
        
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPress Enter to exit...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
