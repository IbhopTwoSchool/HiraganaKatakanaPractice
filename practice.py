#!/usr/bin/env python3
"""
Hiragana and Katakana Practice Application
A pygame-based application for practicing Japanese character writing with pen/stylus support.
Optimized for Linux (Arch/Hyprland) with Wacom pen support.
"""

import pygame
import sys
import threading
import tempfile
import os
import time
import platform
from gtts import gTTS
from characters import HIRAGANA_DATA, KATAKANA_DATA, CHARACTER_INFO, CHARACTER_INFO

# Initialize pygame
pygame.init()

# Get display info for responsive sizing
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

# Default window size - let WM handle fullscreen
WINDOW_WIDTH = SCREEN_WIDTH
WINDOW_HEIGHT = SCREEN_HEIGHT

# Constants
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 200)
GREEN = (50, 200, 100)
RED = (200, 50, 50)
BUTTON_COLOR = (70, 130, 220)
BUTTON_HOVER = (90, 150, 240)
YELLOW = (255, 215, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Drawing color
PEN_COLOR = BLACK


class HiraganaPracticeApp:
    """Main application class for Hiragana/Katakana practice."""
    
    def __init__(self):
        """Initialize the application."""
        # Borderless fullscreen - fills entire screen without window decorations
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.NOFRAME
        )
        
        pygame.display.set_caption("Hiragana & Katakana Practice")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Window dimensions
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.calculate_layout()
        
        # Character selection
        self.character_set = HIRAGANA_DATA
        self.character_index = 0
        self.mode = "hiragana"  # "hiragana" or "katakana"
        
        # Drawing state
        self.drawing_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        self.drawing_surface.fill(WHITE)
        self.drawing_surface.set_colorkey(WHITE)  # Make white transparent
        
        # Stroke tracking for better completion detection
        self.drawing_strokes = []  # List of strokes (each stroke is a list of points)
        self.current_stroke = []  # Current stroke being drawn
        self.previous_pos = None  # Track previous position for smooth lines
        
        # Pen/Stylus state (STYLUS ONLY - no mouse support)
        self.pen_touching = False  # Is pen touching screen?
        self.pen_pressure = 0.0  # Current pen pressure (0.0 to 1.0)
        
        # Background character visibility
        self.show_background = True
        
        # Completion detection
        self.character_completed = False
        self.last_check_time = 0
        self.check_interval = 0.5  # Check every 0.5 seconds
        
        # Progressive stroke guide system
        self.current_stroke_guide = 0  # Which stroke guide to show (0-indexed)
        self.total_stroke_guides = 0  # Total number of strokes for current character
        
        # TTS state
        self.tts_lock = threading.Lock()
        self.tts_enabled = True  # Global TTS enable/disable flag
        self.tts_error_count = 0  # Track consecutive TTS errors
        self.tts_last_error = None  # Last TTS error message
        self.tts_last_success = time.time()  # Time of last successful TTS
        self.tts_failed = False  # Is TTS currently in failed state?
        self.tts_retry_attempts = 0  # Current retry attempt number
        self.current_audio = None
        
        # Font setup with dynamic scaling
        self.update_fonts()
        
        # Create buttons
        self.buttons = self.create_buttons()
        
        # Speak the first character
        self.speak_current_character()
    
    def calculate_layout(self):
        """Calculate layout dimensions based on current window size."""
        # Calculate scaling factors with more conservative scaling for smaller screens
        # Use a logarithmic-like curve to prevent fonts from being too large on small screens
        base_scale = min(self.window_width / 1024, self.window_height / 768)
        
        # Apply dampening for smaller screens - less aggressive scaling
        # For screens smaller than base reference (1024x768), reduce scaling impact
        if base_scale < 1.0:
            # Screens smaller than reference: scale more conservatively
            self.scale_factor = 0.7 + (base_scale * 0.3)  # Min 0.7, max approaches 1.0
        elif base_scale <= 2.0:
            # Screens 1-2x reference: moderate scaling
            self.scale_factor = 0.85 + (base_scale - 1.0) * 0.35  # 0.85 at 1x, 1.2 at 2x
        else:
            # Very large screens: allow more scaling but capped
            self.scale_factor = 1.2 + (base_scale - 2.0) * 0.2  # Slower growth beyond 2x
        
        # Button dimensions (scaled and flexible)
        self.button_height = int(70 * self.scale_factor)
        # Make buttons flexible to window width - divide available width by 8 buttons
        button_area_width = self.window_width - int(20 * self.scale_factor)
        self.button_width = max(int(button_area_width / 8.5), int(100 * self.scale_factor))
        self.button_margin = int(10 * self.scale_factor)
        
        # Drawing settings (scaled)
        self.pen_width = max(int(8 * self.scale_factor), 4)
        self.eraser_width = int(30 * self.scale_factor)
    
    def update_fonts(self):
        """Update fonts based on current scale factor."""
        # Get list of all available fonts for debugging
        available_fonts = pygame.font.get_fonts()
        
        # Try multiple font names (Windows and Linux) with exact system names
        japanese_fonts = [
            'msgothic',           # MS Gothic (Windows) - most common
            'mspgothic',          # MS PGothic (Windows)
            'meiryo',             # Meiryo (Windows)
            'msmincho',           # MS Mincho (Windows)
            'yugothic',           # Yu Gothic (Windows 8.1+)
            'notosanscjkjp',      # Noto Sans CJK JP
            'notosansjp',         # Noto Sans JP
            'notosanscjk',        # Noto Sans CJK
            'takao',              # Takao fonts (Linux)
            'vlgothic',           # VL Gothic (Linux)
            'ipaexgothic',        # IPA fonts (Linux)
            'ipagothic',          # IPA Gothic (Linux)
            'arialunicodems',     # Arial Unicode MS (broad fallback)
            'dejavusans',         # DejaVu Sans (fallback)
            'liberationsans',     # Liberation Sans (fallback)
        ]
        
        # Find which Japanese fonts are actually available
        found_japanese = [f for f in japanese_fonts if f in available_fonts]
        
        if not found_japanese:
            print("⚠️  WARNING: No Japanese fonts detected!")
            print("Available fonts:", ", ".join(sorted(available_fonts)[:20]), "...")
            print("\n💡 Installing fonts:")
            if platform.system() == "Windows":
                print("   Windows should have MS Gothic by default.")
                print("   Check: C:\\Windows\\Fonts\\ for msgothic.ttc")
                print("   If missing, update Windows or install manually.")
            elif platform.system() == "Linux":
                print("   Run: sudo apt install fonts-noto-cjk")
                print("   Or: sudo pacman -S noto-fonts-cjk")
            
            # Use any available font as absolute fallback
            japanese_fonts = ['arial', 'dejavusans', 'freesans', 'liberationsans']
        else:
            print(f"✓ Found Japanese fonts: {', '.join(found_japanese[:3])}")
        
        # Emoji fonts (for UI elements with emojis)
        emoji_fonts = [
            'segoeuiemoji',     # Windows 10/11 emoji font
            'segoeuisymbol',    # Windows symbol font
            'applesymbol',      # macOS emoji
            'notocoloremoji',   # Linux/Android emoji
            'notoemoji',        # Noto Emoji (monochrome)
            'symbola',          # Symbola font (good Unicode coverage)
            'dejavusans',       # DejaVu has some symbols
        ]
        
        # Fallback UI fonts that have good Unicode coverage
        ui_fonts = emoji_fonts + japanese_fonts
        
        # Use SysFont with explicit font priority for best compatibility and scaling
        # SysFont handles font metrics and alignment better than direct Font() loading
        self.char_font = pygame.font.SysFont(japanese_fonts, int(250 * self.scale_factor))
        self.title_char_font = pygame.font.SysFont(japanese_fonts, int(32 * self.scale_factor))
        
        # Use ONLY Japanese fonts for text rendering (no emoji fonts mixed in)
        # This prevents emoji fonts from breaking regular text rendering
        self.ui_font = pygame.font.SysFont(japanese_fonts, int(32 * self.scale_factor))
        self.small_font = pygame.font.SysFont(japanese_fonts, int(24 * self.scale_factor))
        self.button_font = pygame.font.SysFont(japanese_fonts, int(22 * self.scale_factor))
        self.keybind_font = pygame.font.SysFont(japanese_fonts, int(14 * self.scale_factor))
        self.guide_font = pygame.font.SysFont(japanese_fonts, int(20 * self.scale_factor))
        
        # Create emoji fonts matching each text font size for proper scaling
        self.emoji_ui_font = pygame.font.SysFont(emoji_fonts, int(32 * self.scale_factor))
        self.emoji_small_font = pygame.font.SysFont(emoji_fonts, int(24 * self.scale_factor))
        self.emoji_button_font = pygame.font.SysFont(emoji_fonts, int(22 * self.scale_factor))
        self.emoji_keybind_font = pygame.font.SysFont(emoji_fonts, int(14 * self.scale_factor))
        self.emoji_guide_font = pygame.font.SysFont(emoji_fonts, int(20 * self.scale_factor))
        
        print(f"✓ Loaded all fonts using SysFont with scale factor: {self.scale_factor}")
        
        # Test if Japanese characters actually render
        test_char = self.char_font.render('あ', True, (0, 0, 0))
        test_width = test_char.get_width()
        print(f"🧪 Test character 'あ' rendered width: {test_width}px")
        
        if test_width < 10:
            print("❌ CRITICAL: Japanese characters not rendering!")
            print("   The font doesn't support Japanese characters.")
            print("\n🔧 FIX: Install Japanese fonts for your system")
        
        # Check if emoji support is available using the dedicated emoji font
        test_emoji = self.emoji_small_font.render("📚", True, (0, 0, 0))
        has_emoji = test_emoji.get_width() > 10  # If width is small, emoji not supported
        
        if not has_emoji:
            print("⚠️  Emoji font not detected. Using text labels instead.")
            print("💡 To enable emojis:")
            if platform.system() == "Windows":
                print("   - Windows 10/11 includes Segoe UI Emoji by default")
                print("   - If missing, update Windows or install a font pack")
            elif platform.system() == "Linux":
                print("   - Install: sudo apt install fonts-noto-color-emoji")
                print("   - Or: sudo pacman -S noto-fonts-emoji (Arch)")
            else:  # macOS
                print("   - macOS includes Apple Color Emoji by default")
        
        self.has_emoji_support = has_emoji
    
    def get_icon(self, emoji, fallback):
        """Get emoji if supported, otherwise return fallback text."""
        return emoji if self.has_emoji_support else fallback
    
    def render_text_with_emoji(self, emoji, fallback_text, text, font, color):
        """Render emoji and text as separate surfaces if emoji is supported, then combine."""
        if self.has_emoji_support:
            # Select emoji font matching the text font size
            emoji_font = self.emoji_small_font  # Default
            if font == self.ui_font:
                emoji_font = self.emoji_ui_font
            elif font == self.small_font:
                emoji_font = self.emoji_small_font
            elif font == self.button_font:
                emoji_font = self.emoji_button_font
            elif font == self.keybind_font:
                emoji_font = self.emoji_keybind_font
            elif font == self.guide_font:
                emoji_font = self.emoji_guide_font
            
            # Render emoji with matching-sized emoji font and text with regular font
            emoji_surface = emoji_font.render(emoji + " ", True, color)
            text_surface = font.render(text, True, color)
            
            # Create combined surface
            total_width = emoji_surface.get_width() + text_surface.get_width()
            max_height = max(emoji_surface.get_height(), text_surface.get_height())
            combined = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
            combined.blit(emoji_surface, (0, 0))
            combined.blit(text_surface, (emoji_surface.get_width(), 0))
            return combined
        else:
            # Fallback to text-only rendering
            return font.render(f"{fallback_text} {text}", True, color)
    
    def create_buttons(self):
        """Create button objects with positions and actions."""
        buttons = []
        
        # Position buttons at the bottom of the screen
        y_pos = self.window_height - self.button_height - int(15 * self.scale_factor)
        
        # Calculate button positions dynamically based on window width
        x_pos = self.button_margin
        
        button_data = [
            {'text': 'Previous', 'keybind': 'LEFT', 'action': 'previous', 'color': BUTTON_COLOR},
            {'text': 'Clear', 'keybind': 'C', 'action': 'clear', 'color': BUTTON_COLOR},
            {'text': 'Next', 'keybind': 'RIGHT', 'action': 'next', 'color': GREEN},
            {'text': 'Toggle', 'keybind': 'T', 'action': 'toggle', 'color': BUTTON_COLOR},
            {'text': 'Sound', 'keybind': 'S', 'action': 'sound', 'color': BUTTON_COLOR},
            {'text': 'Guide', 'keybind': 'G', 'action': 'toggle_bg', 'color': BUTTON_COLOR},
            {'text': 'Quit', 'keybind': 'ESC', 'action': 'quit', 'color': RED}
        ]
        
        for data in button_data:
            buttons.append({
                'rect': pygame.Rect(x_pos, y_pos, self.button_width, self.button_height),
                'text': data['text'],
                'keybind': data['keybind'],
                'action': data['action'],
                'color': data['color']
            })
            x_pos += self.button_width + self.button_margin
        
        return buttons
    
    def draw_character_info(self, char):
        """Draw educational information panel for the current character."""
        if char not in CHARACTER_INFO:
            return
        
        info = CHARACTER_INFO[char]
        panel_width = int(350 * self.scale_factor)
        panel_x = self.window_width - panel_width - int(10 * self.scale_factor)
        panel_y = int(60 * self.scale_factor)
        panel_height = self.window_height - int(150 * self.scale_factor)
        
        # Draw semi-transparent background panel
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(230)
        panel_surface.fill((250, 250, 255))
        pygame.draw.rect(panel_surface, BLUE, (0, 0, panel_width, panel_height), 3)
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Prepare text rendering
        padding = int(15 * self.scale_factor)
        current_y = panel_y + padding
        text_width = panel_width - (padding * 2)
        
        # Title - render "About" and Japanese character separately with proper fonts
        title_text_surface = self.ui_font.render("About ", True, BLUE)
        title_char_surface = self.title_char_font.render(char, True, BLUE)
        
        # Draw "About" then the character side by side
        self.screen.blit(title_text_surface, (panel_x + padding, current_y))
        self.screen.blit(title_char_surface, (panel_x + padding + title_text_surface.get_width(), current_y))
        current_y += int(45 * self.scale_factor)
        
        # Use the class fonts which have emoji support
        label_font = self.small_font
        text_font = self.small_font
        word_font = self.small_font
        
        # Helper function to render emoji + text separately when emoji is supported
        def render_label_with_emoji(emoji, fallback_text, label_text, font):
            """Render emoji and text as separate surfaces if emoji is supported."""
            if self.has_emoji_support:
                # Select emoji font matching the text font size
                emoji_font = self.emoji_small_font  # Default for info panel
                
                # Render emoji with matching-sized emoji font and text with regular font
                emoji_surface = emoji_font.render(emoji + " ", True, DARK_GRAY)
                text_surface = font.render(label_text, True, DARK_GRAY)
                
                # Create combined surface
                total_width = emoji_surface.get_width() + text_surface.get_width()
                combined = pygame.Surface((total_width, max(emoji_surface.get_height(), text_surface.get_height())), pygame.SRCALPHA)
                combined.blit(emoji_surface, (0, 0))
                combined.blit(text_surface, (emoji_surface.get_width(), 0))
                return combined
            else:
                # Fallback to text-only rendering
                return font.render(f"{fallback_text} {label_text}", True, DARK_GRAY)
        
        # Helper function to wrap and draw text
        def draw_multiline_text(text, y_pos, font, color, label=None):
            if label:
                label_surface = font.render(label, True, DARK_GRAY)
                self.screen.blit(label_surface, (panel_x + padding, y_pos))
                y_pos += int(22 * self.scale_factor)
            
            words = text.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = font.render(test_line, True, color)
                if test_surface.get_width() <= text_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            for line in lines:
                line_surface = font.render(line, True, color)
                self.screen.blit(line_surface, (panel_x + padding, y_pos))
                y_pos += int(20 * self.scale_factor)
            
            return y_pos + int(8 * self.scale_factor)
        
        # Draw origin
        origin_label_surface = render_label_with_emoji("📜", "[Origin]", "Origin:", label_font)
        self.screen.blit(origin_label_surface, (panel_x + padding, current_y))
        current_y += int(22 * self.scale_factor)
        current_y = draw_multiline_text(info['origin'], current_y, text_font, (80, 80, 80))
        
        # Draw usage
        usage_label_surface = render_label_with_emoji("💡", "[Usage]", "Usage:", label_font)
        self.screen.blit(usage_label_surface, (panel_x + padding, current_y))
        current_y += int(22 * self.scale_factor)
        current_y = draw_multiline_text(info['usage'], current_y, text_font, (60, 60, 60))
        
        # Draw notes
        notes_label_surface = render_label_with_emoji("📌", "[Note]", "Note:", label_font)
        self.screen.blit(notes_label_surface, (panel_x + padding, current_y))
        current_y += int(22 * self.scale_factor)
        current_y = draw_multiline_text(info['notes'], current_y, text_font, (40, 40, 100))
        
        # Draw common words
        current_y += int(5 * self.scale_factor)
        words_label_surface = render_label_with_emoji("📚", "[Words]", "Common Words:", label_font)
        self.screen.blit(words_label_surface, (panel_x + padding, current_y))
        current_y += int(22 * self.scale_factor)
        
        for word in info['words']:
            if current_y + int(20 * self.scale_factor) > panel_y + panel_height - padding:
                break  # Don't overflow panel
            word_surface = word_font.render(f"  • {word}", True, (50, 50, 50))
            self.screen.blit(word_surface, (panel_x + padding, current_y))
            current_y += int(18 * self.scale_factor)
    
    def draw_smooth_pressure_stroke(self, pos, pressure=0.0):
        """Draw a beautiful smooth pressure-sensitive stroke like a fine brush.
        
        The pen creates darker, wider strokes as pressure increases.
        When hovering (proximity), shows a light preview.
        """
        # Calculate stroke width based on pressure (2px to 20px)
        if pressure <= 0:  # Hovering/proximity only
            stroke_width = 1
            alpha = 30  # Very faint preview
            color = (*PEN_COLOR, alpha)
        else:
            # Map pressure to width: light touch = thin, heavy = thick
            stroke_width = int(2 + (pressure * 18))  # 2-20px range
            # Map pressure to opacity: light = semi-transparent, heavy = solid
            alpha = int(100 + (pressure * 155))  # 100-255 range
            color = (*PEN_COLOR, alpha)
        
        # Draw smooth line from previous position
        if self.previous_pos and self.previous_pos != pos:
            # Calculate line length and angle for smooth rendering
            dx = pos[0] - self.previous_pos[0]
            dy = pos[1] - self.previous_pos[1]
            distance = max(1, int((dx*dx + dy*dy)**0.5))
            
            # Draw multiple circles along the line for smooth, brush-like appearance
            steps = max(1, distance // 2)
            for i in range(steps + 1):
                t = i / max(1, steps)
                interp_x = int(self.previous_pos[0] + dx * t)
                interp_y = int(self.previous_pos[1] + dy * t)
                
                # Create circle surface with alpha
                circle_surface = pygame.Surface((stroke_width * 2, stroke_width * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, color, (stroke_width, stroke_width), stroke_width)
                
                # Blit to drawing surface
                self.drawing_surface.blit(circle_surface, 
                                        (interp_x - stroke_width, interp_y - stroke_width))
        else:
            # First point or discontinuous - just draw a circle
            circle_surface = pygame.Surface((stroke_width * 2, stroke_width * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, color, (stroke_width, stroke_width), stroke_width)
            self.drawing_surface.blit(circle_surface, (pos[0] - stroke_width, pos[1] - stroke_width))
        
        # Update previous position for next stroke segment
        self.previous_pos = pos
        
        # Track the stroke point (only if actually drawing)
        if pressure > 0:
            self.current_stroke.append(pos)
    
    def check_character_completion(self):
        """Check if the character has been drawn correctly with improved detection."""
        # Only check when not actively drawing and when pen is not touching
        if self.pen_touching:
            return False
        
        # Don't check too frequently
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return False
        self.last_check_time = current_time
        
        # Need at least 2 strokes for basic characters (some simple ones might need 1)
        if len(self.drawing_strokes) < 1:
            return False
        
        # Create a mask of the drawn strokes
        stroke_mask = pygame.Surface((self.window_width, self.window_height))
        stroke_mask.fill(WHITE)
        
        # Draw all strokes onto the mask
        for stroke in self.drawing_strokes:
            if len(stroke) > 1:
                for i in range(len(stroke) - 1):
                    pygame.draw.line(stroke_mask, BLACK, stroke[i], stroke[i + 1], self.pen_width)
        
        # Convert to mask for collision detection
        drawn_mask = pygame.mask.from_surface(stroke_mask)
        drawn_pixels = drawn_mask.count()
        
        # Get character surface to compare
        char, _ = self.get_current_character()
        char_surface = self.char_font.render(char, True, BLACK)
        char_rect = char_surface.get_rect(center=(self.window_width // 2, self.window_height // 3))
        
        # Create mask from character
        char_mask = pygame.mask.from_surface(char_surface)
        char_pixels = char_mask.count()
        
        if char_pixels == 0:
            return False
        
        # Calculate overlap - offset by character position
        overlap = char_mask.overlap_area(drawn_mask, (char_rect.x, char_rect.y))
        coverage = (overlap / char_pixels) * 100
        
        # Adaptive completion based on stroke count and coverage
        # More strokes = character might be more complex, require less coverage
        num_strokes = len(self.drawing_strokes)
        
        if num_strokes >= 2 and coverage >= 65:
            return True
        elif num_strokes == 1 and coverage >= 80:  # Simple characters might need 1 stroke
            return True
        elif num_strokes >= 3 and coverage >= 60:  # Complex characters
            return True
        
        return False
    
    def reset_tts(self):
        """Reset TTS system after failure."""
        try:
            with self.tts_lock:
                # Stop and unload everything
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                except:
                    pass
                
                # Force pygame mixer reset
                try:
                    pygame.mixer.quit()
                    time.sleep(0.2)
                    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                except:
                    pass
                
                # Force garbage collection
                import gc
                gc.collect()
                time.sleep(0.2)
                
                # Reset error tracking
                self.tts_error_count = 0
                self.tts_last_error = None
                self.tts_failed = False
                self.tts_retry_attempts = 0
                self.tts_enabled = True
                
                print("✅ TTS reset")
        except Exception as e:
            print(f"❌ TTS reset failed")
    
    def speak_current_character(self):
        """Speak the current character using Google TTS in Japanese with robust error handling."""
        if not self.tts_enabled:
            print("⚠️ TTS is disabled")
            return
        
        char, romanji = self.get_current_character()
        
        def speak():
            temp_file = None
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    with self.tts_lock:
                        # Check if TTS has been disabled during wait
                        if not self.tts_enabled:
                            print("⚠️ TTS disabled, aborting")
                            return
                        
                        # Stop any currently playing audio and unload
                        try:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                        except:
                            pass
                        
                        # Small delay to ensure cleanup
                        time.sleep(0.1)
                        
                        # Verify mixer is initialized
                        if not pygame.mixer.get_init():
                            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                        
                        # Create Japanese TTS audio
                        tts = gTTS(text=char, lang='ja', slow=False)
                        
                        # Save to temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                            temp_file = fp.name
                            tts.save(temp_file)
                        
                        # Verify file was created and has content
                        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                            raise Exception(f"TTS file creation failed: {temp_file}")
                        
                        # Play the audio
                        pygame.mixer.music.load(temp_file)
                        pygame.mixer.music.play()
                        
                        # Wait for playback to finish
                        max_wait = 50  # 5 seconds max
                        wait_count = 0
                        playback_started = False
                        
                        while wait_count < max_wait:
                            is_busy = pygame.mixer.music.get_busy()
                            if is_busy:
                                playback_started = True
                            elif playback_started:
                                # Playback finished normally
                                break
                            
                            pygame.time.Clock().tick(10)
                            wait_count += 1
                        
                        if not playback_started:
                            raise Exception("Playback never started")
                        
                        # Unload before cleanup
                        pygame.mixer.music.unload()
                        time.sleep(0.1)
                        
                        # SUCCESS - update tracking
                        self.tts_last_success = time.time()
                        self.tts_error_count = 0
                        self.tts_retry_attempts = 0
                        self.tts_failed = False
                        
                        # Break retry loop on success
                        break
                            
                except Exception as e:
                    error_msg = f"TTS Error (attempt {attempt + 1}/{max_retries}): {type(e).__name__}: {e}"
                    print(f"❌ {error_msg}")
                    
                    self.tts_last_error = str(e)
                    self.tts_error_count += 1
                    self.tts_retry_attempts = attempt + 1
                    
                    # If this was the last retry, mark as failed
                    if attempt == max_retries - 1:
                        self.tts_failed = True
                        print(f"❌ TTS FAILED after {max_retries} attempts")
                        print(f"⚠️ Last error: {self.tts_last_error}")
                        print(f"💡 Press 'R' to reset TTS or 'T' to toggle TTS on/off")
                        
                        # Auto-disable TTS after 5 consecutive failures
                        if self.tts_error_count >= 5:
                            self.tts_enabled = False
                            print(f"⛔ TTS auto-disabled after {self.tts_error_count} failures")
                            print(f"💡 Press 'T' to re-enable TTS")
                    else:
                        # Wait before retry
                        time.sleep(0.5 * (attempt + 1))
                        print(f"🔄 Retrying TTS...")
                
                finally:
                    # Always clean up temp file
                    if temp_file:
                        try:
                            import gc
                            gc.collect()
                            time.sleep(0.05)
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                        except Exception as cleanup_error:
                            print(f"⚠️ Temp file cleanup warning: {cleanup_error}")
        
        # Run TTS in a separate thread to avoid blocking
        threading.Thread(target=speak, daemon=True).start()
    
    def get_current_character(self):
        """Get the current character and romanji to practice."""
        return self.character_set[self.character_index]
    
    def next_character(self):
        """Move to the next character."""
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        self.character_index = (self.character_index + 1) % len(self.character_set)
        self.clear_drawing()
        self.character_completed = False
        self.speak_current_character()
    
    def previous_character(self):
        """Move to the previous character."""
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        self.character_index = (self.character_index - 1) % len(self.character_set)
        self.clear_drawing()
        self.character_completed = False
        self.speak_current_character()
    
    def toggle_mode(self):
        """Toggle between Hiragana and Katakana."""
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        # Keep the current character index when switching modes
        current_index = self.character_index
        
        if self.mode == "hiragana":
            self.mode = "katakana"
            self.character_set = KATAKANA_DATA
        else:
            self.mode = "hiragana"
            self.character_set = HIRAGANA_DATA
        
        # Maintain position, but cap at the length of the new character set
        self.character_index = min(current_index, len(self.character_set) - 1)
        self.clear_drawing()
        self.character_completed = False
        self.speak_current_character()
    
    def clear_drawing(self):
        """Clear the drawing surface."""
        self.drawing_surface.fill(WHITE)
        self.drawing_strokes = []
        self.current_stroke = []
        self.previous_pos = None
        self.current_stroke_guide = 0  # Reset to first stroke guide
    

    
    def handle_events(self):
        """Handle pygame events - PEN INPUT ONLY."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                # DO NOT change display mode - stay in NOFRAME
                pass
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                    self.next_character()
                elif event.key == pygame.K_LEFT:
                    self.previous_character()
                elif event.key == pygame.K_c:
                    self.clear_drawing()
                elif event.key == pygame.K_t:
                    self.toggle_mode()
                elif event.key == pygame.K_s:
                    self.speak_current_character()
                elif event.key == pygame.K_r:
                    # R: Reset TTS system
                    self.reset_tts()
                elif event.key == pygame.K_m:
                    # M: Toggle TTS on/off (Mute)
                    self.tts_enabled = not self.tts_enabled
                elif event.key == pygame.K_g:
                    self.show_background = not self.show_background
            
            # PEN EVENTS - Detect pen proximity, touch, and pressure
            # Mouse events used ONLY for button clicks - no drawing
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for button clicks only
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['action'] == 'next':
                            self.next_character()
                        elif button['action'] == 'previous':
                            self.previous_character()
                        elif button['action'] == 'clear':
                            self.clear_drawing()
                        elif button['action'] == 'toggle':
                            self.toggle_mode()
                        elif button['action'] == 'sound':
                            self.speak_current_character()
                        elif button['action'] == 'toggle_bg':
                            self.show_background = not self.show_background
                        elif button['action'] == 'quit':
                            self.running = False
                        break
                
                # Check for pen/stylus input - try ALL buttons for stylus side buttons
                if event.button in [2, 3, 4, 5, 6, 7, 8, 9, 10]:  # Try many button numbers
                    if event.button in [2, 3, 8]:
                        self.previous_character()
                    elif event.button in [4, 5, 9, 10]:
                        self.next_character()
                elif event.button == 1:  # Pen tip
                    if hasattr(event, 'pressure'):
                        raw_pressure = event.pressure
                        if raw_pressure > 1.0:
                            raw_pressure = raw_pressure / 65535.0
                        
                        # Much more aggressive curve - cube root for very gradual buildup
                        self.pen_pressure = pow(raw_pressure, 0.3)  # Was 0.7, now 0.3 for more sensitivity
                    else:
                        self.pen_pressure = 0.5  # Default to 50% instead of 100%
                    
                    self.pen_touching = True
                    self.previous_pos = event.pos
                    self.current_stroke = [self.previous_pos]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Only handle pen lift
                if hasattr(event, 'pressure') or self.pen_touching:
                    self.pen_touching = False
                    self.pen_pressure = 0.0
                    # Finish current stroke and validate before advancing guide
                    if len(self.current_stroke) > 2:
                        self.drawing_strokes.append(self.current_stroke.copy())
                        
                        # Validate stroke against current guide before advancing
                        char, _ = self.get_current_character()
                        stroke_paths = self.get_stroke_paths(char)
                        
                        if self.current_stroke_guide < len(stroke_paths):
                            current_guide = stroke_paths[self.current_stroke_guide]
                            
                            # Check if user's stroke follows the guide
                            if self.validate_stroke_against_guide(self.current_stroke, current_guide):
                                # Valid stroke - advance to next guide
                                if self.current_stroke_guide < len(stroke_paths) - 1:
                                    self.current_stroke_guide += 1
                            # If invalid, don't advance - they need to try again
                    
                    self.current_stroke = []
                    self.previous_pos = None
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle pen/mouse motion
                if hasattr(event, 'pressure'):
                    # Pressure-sensitive input (stylus/pen)
                    raw_pressure = event.pressure
                    
                    # Handle different pressure ranges (0-1 or 0-65535)
                    if raw_pressure > 1.0:
                        raw_pressure = raw_pressure / 65535.0
                    
                    # Much more aggressive curve - cube root
                    adjusted = pow(raw_pressure, 0.3)
                    
                    self.pen_pressure = adjusted
                    pos = event.pos
                    
                    if self.pen_pressure > 0.05:  # Higher threshold
                        # Pen is touching - draw
                        self.pen_touching = True
                        self.draw_smooth_pressure_stroke(pos, self.pen_pressure)
                    else:
                        # Pen is hovering - show preview
                        self.pen_touching = False
                        self.draw_smooth_pressure_stroke(pos, 0.0)
                elif self.pen_touching:
                    # No pressure attribute (basic mouse/touchpad) - only draw if button down
                    pos = event.pos
                    self.draw_smooth_pressure_stroke(pos, self.pen_pressure)
    
    def draw(self):
        """Draw the current frame."""
        self.screen.fill(WHITE)
        
        # Get current character
        char, romanji = self.get_current_character()
        
        # Draw character in background (if enabled)
        if self.show_background:
            char_surface = self.char_font.render(char, True, LIGHT_GRAY)
            char_rect = char_surface.get_rect(center=(self.window_width // 2, self.window_height // 3))
            self.screen.blit(char_surface, char_rect)
        
        # Draw progressive stroke guide - only show current stroke
        # This MUST be drawn AFTER the character so it overlays properly
        stroke_paths = self.get_stroke_paths(char)
        self.total_stroke_guides = len(stroke_paths)
        
        # Only show the current stroke the user should draw
        if self.current_stroke_guide < len(stroke_paths):
            path = stroke_paths[self.current_stroke_guide]
            
            # Use a bright, visible guide color that overlays the character
            guide_color = (0, 150, 255)  # Bright blue guide
            
            # Draw the stroke path as a THICK visible line overlaying the character
            if len(path) >= 2:
                thickness = int(12 * self.scale_factor)  # Thicker for visibility
                pygame.draw.lines(self.screen, guide_color, False, path, thickness)
        
        # Draw user's drawing
        self.screen.blit(self.drawing_surface, (0, 0))
        
        # Draw educational info panel on the right side
        self.draw_character_info(char)
        
        # Draw UI elements
        margin = int(15 * self.scale_factor)
        
        # Draw mode indicator
        mode_text = f"Mode: {self.mode.capitalize()}"
        mode_surface = self.ui_font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (margin, margin))
        
        # Draw pen status
        if self.pen_touching:
            pen_surface = self.render_text_with_emoji("✏️", "[PEN]", f"Drawing (Pressure: {self.pen_pressure:.0%})", self.small_font, GREEN)
        else:
            pen_surface = self.render_text_with_emoji("✏️", "[PEN]", "Pen Ready", self.small_font, BLUE)
        
        self.screen.blit(pen_surface, (self.window_width - margin - pen_surface.get_width(), margin))
        
        # Draw character info with stroke progress
        if self.total_stroke_guides > 0:
            progress_text = f"Stroke {self.current_stroke_guide + 1}/{self.total_stroke_guides}"
            romanji_text = f"({romanji}) - {self.character_index + 1}/{len(self.character_set)} | {progress_text}"
        else:
            romanji_text = f"({romanji}) - {self.character_index + 1}/{len(self.character_set)}"
        romanji_surface = self.ui_font.render(romanji_text, True, DARK_GRAY)
        romanji_rect = romanji_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 + int(150 * self.scale_factor)))
        self.screen.blit(romanji_surface, romanji_rect)
        
        # Draw TTS status indicator
        tts_status_y = self.window_height - int(60 * self.scale_factor)
        if not self.tts_enabled:
            # TTS disabled
            status_surface = self.render_text_with_emoji("🔇", "[MUTE]", "TTS Disabled (Press M to enable)", self.keybind_font, DARK_GRAY)
        elif self.tts_failed:
            # TTS failed
            status_surface = self.render_text_with_emoji("❌", "[X]", "TTS Failed (Press R to reset, M to disable)", self.keybind_font, RED)
        elif self.tts_error_count > 0:
            # TTS has errors but still working
            status_surface = self.render_text_with_emoji("⚠️", "[!]", f"TTS Issues ({self.tts_error_count} errors)", self.keybind_font, ORANGE)
        else:
            # TTS working normally - show time since last success
            time_since = int(time.time() - self.tts_last_success)
            if time_since < 60:
                status_surface = self.render_text_with_emoji("🔊", "[SOUND]", "TTS Active", self.keybind_font, GREEN)
            else:
                status_surface = self.render_text_with_emoji("🔊", "[SOUND]", f"TTS Active ({time_since//60}m since last use)", self.keybind_font, DARK_GRAY)
        
        status_rect = status_surface.get_rect(center=(self.window_width // 2, tts_status_y))
        self.screen.blit(status_surface, status_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            # Check if hovering
            is_hovering = button['rect'].collidepoint(mouse_pos)
            color = BUTTON_HOVER if is_hovering else button['color']
            
            # Draw button
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=8)
            pygame.draw.rect(self.screen, DARK_GRAY, button['rect'], 2, border_radius=8)
            
            # Draw button text with keybind
            button_text = f"{button['text']} [{button['keybind']}]"
            text_surface = self.button_font.render(button_text, True, WHITE)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    def get_stroke_paths(self, char):
        """Get actual stroke paths for Japanese characters.
        Returns list of stroke paths, where each path is a list of (x, y) points.
        Stroke paths are scaled and positioned to match the actual rendered character.
        """
        from stroke_order_data import get_stroke_data
        
        # Center position where character is drawn
        cx = self.window_width // 2
        cy = self.window_height // 3
        
        # Render the character to get its actual bounding box
        char_surface = self.char_font.render(char, True, BLACK)
        char_rect = char_surface.get_rect(center=(cx, cy))
        
        # Get stroke data from comprehensive stroke order database
        # Coordinates are in range -60 to 60
        relative_paths = get_stroke_data(char)
        
        # If character not found, use simple default
        if relative_paths is None:
            relative_paths = [
                [(-20, -40), (0, -20), (20, 0)],  # Default stroke 1
                [(-15, 10), (0, 30), (15, 45)]   # Default stroke 2
            ]
        
        # Scale stroke paths to match the actual character size
        # The stroke data uses a coordinate system of approximately -60 to +60
        # We need to scale this to match the actual rendered character size
        coord_range = 120  # -60 to +60 = 120 unit range
        
        # Use the character width and height for more accurate scaling
        # Scale based on actual dimensions, not just max
        scale_x = char_rect.width / coord_range
        scale_y = char_rect.height / coord_range
        
        # Convert relative to absolute positions with proper scaling and positioning
        # FLIP Y-AXIS: Computer graphics Y goes down, stroke data Y goes up
        absolute_paths = []
        for idx, path in enumerate(relative_paths):
            # Scale coordinates, flip Y-axis, and offset to character center
            absolute_path = [
                (int(cx + x * scale_x), int(cy - y * scale_y))  # Note the MINUS for Y
                for x, y in path
            ]
            absolute_paths.append(absolute_path)
        
        return absolute_paths
    
    def validate_stroke_against_guide(self, user_stroke, guide_path):
        """Check if user's stroke follows the guide path closely enough.
        
        Args:
            user_stroke: List of (x, y) points the user drew
            guide_path: List of (x, y) points in the guide
        
        Returns:
            bool: True if stroke is close enough to guide, False otherwise
        """
        if not user_stroke or not guide_path:
            return False
        
        if len(user_stroke) < 3:
            return False  # Too short to be a real stroke
        
        # Calculate a tolerance based on screen size
        # Allow about 15% of character size as tolerance
        tolerance = int(50 * self.scale_factor)
        
        # Count how many user points are close to the guide path
        points_near_guide = 0
        
        for user_point in user_stroke:
            # Check if this user point is close to ANY point in the guide path
            min_distance = float('inf')
            
            for guide_point in guide_path:
                dx = user_point[0] - guide_point[0]
                dy = user_point[1] - guide_point[1]
                distance = (dx*dx + dy*dy) ** 0.5
                min_distance = min(min_distance, distance)
            
            if min_distance <= tolerance:
                points_near_guide += 1
        
        # Require at least 40% of user's points to be near the guide
        coverage_ratio = points_near_guide / len(user_stroke)
        
        # Also check that user covered a reasonable length of the guide
        # Get start and end regions of guide
        guide_start = guide_path[0]
        guide_end = guide_path[-1]
        
        # Check if user started near the guide start
        user_start = user_stroke[0]
        start_dx = user_start[0] - guide_start[0]
        start_dy = user_start[1] - guide_start[1]
        start_distance = (start_dx*start_dx + start_dy*start_dy) ** 0.5
        
        # Check if user ended near the guide end
        user_end = user_stroke[-1]
        end_dx = user_end[0] - guide_end[0]
        end_dy = user_end[1] - guide_end[1]
        end_distance = (end_dx*end_dx + end_dy*end_dy) ** 0.5
        
        # More lenient tolerance for start/end points
        endpoint_tolerance = tolerance * 1.5
        
        # Stroke is valid if:
        # 1. Reasonable coverage of points near guide (40%+)
        # 2. Started reasonably close to guide start OR ended close to guide end
        is_valid = (
            coverage_ratio >= 0.4 and 
            (start_distance <= endpoint_tolerance or end_distance <= endpoint_tolerance)
        )
        
        return is_valid
    
    def run(self):
        """Main game loop."""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Check for character completion (only when not drawing)
            if not self.character_completed:
                if self.check_character_completion():
                    self.character_completed = True
                    print("✓ Character completed!")
            
            # Draw everything
            self.draw()
            
            # Maintain framerate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point."""
    app = HiraganaPracticeApp()
    app.run()


if __name__ == "__main__":
    main()
