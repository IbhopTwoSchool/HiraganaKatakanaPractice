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
from characters import HIRAGANA_DATA, KATAKANA_DATA

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
CONFETTI_COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK]

# Drawing color
PEN_COLOR = BLACK


class HiraganaPracticeApp:
    """Main application class for Hiragana/Katakana practice."""
    
    def __init__(self):
        """Initialize the application."""
        # DEBUG: Show what we're trying to create
        print(f"🖥️  INITIALIZING: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"🖥️  Screen detected: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Borderless fullscreen - fills entire screen without window decorations
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.NOFRAME
        )
        
        # DEBUG: Verify what we actually got
        actual_size = self.screen.get_size()
        print(f"✅ WINDOW CREATED: {actual_size[0]}x{actual_size[1]}")
        
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
        
        # Confetti particles
        self.confetti_particles = []
        
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
        
        # Initialize sound system
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.success_sound = self.create_success_sound()
        
        # Display pen mode message
        print("\n✏️  PEN-ONLY MODE ACTIVE")
        print("This application requires a stylus/pen input.")
        print("Remove your pen from its socket to begin.\n")
        
        # Speak the first character
        self.speak_current_character()
    
    def calculate_layout(self):
        """Calculate layout dimensions based on current window size."""
        # Calculate scaling factors
        self.scale_factor = min(self.window_width / 1024, self.window_height / 768)
        
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
        # Try multiple font names (Windows and Linux)
        japanese_fonts = [
            'notosanscjkjp',  # Noto Sans CJK JP (installed by install_fonts.py)
            'notosansjp',
            'notosanscjk',
            'msgothic',       # MS Gothic (Windows)
            'meiryo',         # Meiryo (Windows)
            'mspgothic',      # MS PGothic (Windows)
            'yugothic',       # Yu Gothic (Windows)
            'msmincho',       # MS Mincho (Windows)
            'takao',          # Takao fonts (Linux)
            'vlgothic',       # VL Gothic (Linux)
            'ipaexgothic',    # IPA fonts (Linux)
            'ipagothic',
            'dejavusans',     # DejaVu Sans (fallback)
            'liberationsans', # Liberation Sans (fallback)
        ]
        self.char_font = pygame.font.SysFont(japanese_fonts, int(250 * self.scale_factor))
        self.ui_font = pygame.font.SysFont(japanese_fonts, int(32 * self.scale_factor))
        self.small_font = pygame.font.SysFont(japanese_fonts, int(24 * self.scale_factor))
        self.button_font = pygame.font.SysFont(japanese_fonts, int(22 * self.scale_factor))
        self.keybind_font = pygame.font.SysFont(japanese_fonts, int(14 * self.scale_factor))
        self.guide_font = pygame.font.SysFont(japanese_fonts, int(20 * self.scale_factor))
    
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
            {'text': 'Fullscreen', 'keybind': 'F11', 'action': 'fullscreen', 'color': PURPLE},
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
    
    def create_success_sound(self):
        """Create a success sound effect programmatically."""
        try:
            import numpy as np
            sample_rate = 22050
            duration = 0.3  # seconds
            frequency1 = 523.25  # C5
            frequency2 = 659.25  # E5
            frequency3 = 783.99  # G5
            
            # Generate samples for a pleasant chord
            num_samples = int(sample_rate * duration)
            t = np.linspace(0, duration, num_samples, False)
            
            # Create envelope (fade out)
            envelope = 1 - (t / duration)
            
            # Create a chord with three notes
            wave1 = np.sin(frequency1 * 2 * np.pi * t)
            wave2 = np.sin(frequency2 * 2 * np.pi * t)
            wave3 = np.sin(frequency3 * 2 * np.pi * t)
            
            # Mix waves together with envelope
            wave = (wave1 + wave2 + wave3) / 3 * envelope * 32767
            wave = wave.astype(np.int16)
            
            # Convert to stereo
            stereo_wave = np.column_stack((wave, wave))
            
            # Create pygame Sound from numpy array
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
        except Exception as e:
            print(f"Could not create success sound: {e}")
            return None
    
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
    
    def create_confetti(self):
        """Create confetti particles for celebration."""
        for _ in range(100):
            self.confetti_particles.append({
                'x': self.window_width // 2,
                'y': self.window_height // 3,
                'vx': (pygame.time.get_ticks() % 100 - 50) * 0.2,
                'vy': -(pygame.time.get_ticks() % 50 + 50) * 0.2,
                'color': CONFETTI_COLORS[pygame.time.get_ticks() % len(CONFETTI_COLORS)],
                'size': int(5 * self.scale_factor),
                'life': 100
            })
    
    def update_confetti(self):
        """Update confetti particle positions."""
        for particle in self.confetti_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.5  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0 or particle['y'] > self.window_height:
                self.confetti_particles.remove(particle)
    
    def draw_confetti(self):
        """Draw confetti particles."""
        for particle in self.confetti_particles:
            alpha = int(255 * (particle['life'] / 100))
            s = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            color = (*particle['color'], alpha)
            pygame.draw.rect(s, color, (0, 0, particle['size'], particle['size']))
            self.screen.blit(s, (int(particle['x']), int(particle['y'])))
    
    def reset_tts(self):
        """Reset TTS system after failure."""
        print("🔄 Resetting TTS system...")
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
                except Exception as e:
                    print(f"Mixer reset error: {e}")
                
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
                
                print("✅ TTS system reset complete")
        except Exception as e:
            print(f"❌ TTS reset failed: {e}")
    
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
                        except Exception as cleanup_err:
                            print(f"Pre-cleanup warning: {cleanup_err}")
                        
                        # Small delay to ensure cleanup
                        time.sleep(0.1)
                        
                        # Verify mixer is initialized
                        if not pygame.mixer.get_init():
                            print("🔧 Reinitializing pygame mixer")
                            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                        
                        # Create Japanese TTS audio
                        print(f"🔊 Generating TTS for '{char}' (attempt {attempt + 1}/{max_retries})")
                        tts = gTTS(text=char, lang='ja', slow=False)
                        
                        # Save to temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                            temp_file = fp.name
                            tts.save(temp_file)
                        
                        # Verify file was created and has content
                        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                            raise Exception(f"TTS file creation failed: {temp_file}")
                        
                        print(f"✅ TTS file created: {os.path.getsize(temp_file)} bytes")
                        
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
                        print(f"✅ TTS playback successful for '{char}'")
                        
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
        
        if self.mode == "hiragana":
            self.mode = "katakana"
            self.character_set = KATAKANA_DATA
        else:
            self.mode = "hiragana"
            self.character_set = HIRAGANA_DATA
        self.character_index = 0
        self.clear_drawing()
        self.character_completed = False
        self.speak_current_character()
    
    def clear_drawing(self):
        """Clear the drawing surface."""
        self.drawing_surface.fill(WHITE)
        self.drawing_strokes = []
        self.current_stroke = []
        self.previous_pos = None
    

    
    def handle_events(self):
        """Handle pygame events - PEN INPUT ONLY."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                # DEBUG: Track any resize attempts
                print(f"⚠️  VIDEORESIZE EVENT: {event.w}x{event.h}")
                print(f"⚠️  This should NOT happen with NOFRAME!")
                # DO NOT change display mode - stay in NOFRAME
            
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
                    status = "enabled" if self.tts_enabled else "disabled"
                    print(f"🔊 TTS {status}")
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
                    print(f"🔘 STYLUS BUTTON DETECTED: {event.button}")
                    if event.button in [2, 3, 8]:
                        print("   → Previous character")
                        self.previous_character()
                    elif event.button in [4, 5, 9, 10]:
                        print("   → Next character")
                        self.next_character()
                elif event.button == 1:  # Pen tip
                    # DEBUG: Show ALL event attributes
                    print(f"\n🔍 MOUSEBUTTONDOWN EVENT DEBUG:")
                    print(f"   All attributes: {dir(event)}")
                    print(f"   Has 'pressure': {hasattr(event, 'pressure')}")
                    if hasattr(event, 'pressure'):
                        print(f"   event.pressure = {event.pressure}")
                    if hasattr(event, 'touch'):
                        print(f"   event.touch = {event.touch}")
                    if hasattr(event, 'window'):
                        print(f"   event.window = {event.window}")
                    
                    if hasattr(event, 'pressure'):
                        raw_pressure = event.pressure
                        if raw_pressure > 1.0:
                            raw_pressure = raw_pressure / 65535.0
                        
                        # Much more aggressive curve - cube root for very gradual buildup
                        self.pen_pressure = pow(raw_pressure, 0.3)  # Was 0.7, now 0.3 for more sensitivity
                        print(f"✏️  Pen down - Raw: {raw_pressure:.4f}, Adjusted: {self.pen_pressure:.4f}")
                    else:
                        print(f"⚠️  NO PRESSURE ATTRIBUTE - Using default 0.5")
                        self.pen_pressure = 0.5  # Default to 50% instead of 100%
                    
                    self.pen_touching = True
                    self.previous_pos = event.pos
                    self.current_stroke = [self.previous_pos]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Only handle pen lift
                if hasattr(event, 'pressure') or self.pen_touching:
                    self.pen_touching = False
                    self.pen_pressure = 0.0
                    # Finish current stroke
                    if len(self.current_stroke) > 2:
                        self.drawing_strokes.append(self.current_stroke.copy())
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
                    
                    # Only print occasionally to avoid spam (every 10th frame)
                    if not hasattr(self, '_motion_debug_counter'):
                        self._motion_debug_counter = 0
                    self._motion_debug_counter += 1
                    if self._motion_debug_counter % 10 == 0:
                        print(f"📍 MOTION - Raw: {raw_pressure:.4f}, Adjusted: {adjusted:.4f}")
                    
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
            
            # Draw stroke order guides as lines with arrows
            stroke_paths = self.get_stroke_paths(char)
            for i, path in enumerate(stroke_paths):
                # Color gradient for each stroke
                progress = i / max(1, len(stroke_paths) - 1)
                stroke_color = (
                    int(255 - 100 * progress),  # R: 255->155
                    int(50 + 150 * progress),   # G: 50->200
                    int(50)                      # B: constant
                )
                
                # Draw the stroke path as a thick line
                if len(path) >= 2:
                    thickness = int(6 * self.scale_factor)
                    pygame.draw.lines(self.screen, stroke_color, False, path, thickness)
                    
                    # Draw arrowhead at the end of the stroke
                    end_point = path[-1]
                    if len(path) >= 2:
                        # Calculate arrow direction from last two points
                        prev_point = path[-2]
                        dx = end_point[0] - prev_point[0]
                        dy = end_point[1] - prev_point[1]
                        length = max(1, (dx*dx + dy*dy)**0.5)
                        
                        # Normalize direction
                        dx /= length
                        dy /= length
                        
                        # Arrow size
                        arrow_size = int(20 * self.scale_factor)
                        arrow_width = int(12 * self.scale_factor)
                        
                        # Calculate arrow points (triangular arrowhead)
                        arrow_tip = end_point
                        arrow_base = (
                            int(end_point[0] - dx * arrow_size),
                            int(end_point[1] - dy * arrow_size)
                        )
                        # Perpendicular vector for arrow wings
                        perp_x, perp_y = -dy, dx
                        arrow_left = (
                            int(arrow_base[0] + perp_x * arrow_width),
                            int(arrow_base[1] + perp_y * arrow_width)
                        )
                        arrow_right = (
                            int(arrow_base[0] - perp_x * arrow_width),
                            int(arrow_base[1] - perp_y * arrow_width)
                        )
                        
                        # Draw filled arrow
                        pygame.draw.polygon(self.screen, stroke_color, 
                                          [arrow_tip, arrow_left, arrow_right])
        
        # Draw user's drawing
        self.screen.blit(self.drawing_surface, (0, 0))
        
        # Draw UI elements
        margin = int(15 * self.scale_factor)
        
        # Draw mode indicator
        mode_text = f"Mode: {self.mode.capitalize()} | Use Super+F to fullscreen in Hyprland"
        mode_surface = self.ui_font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (margin, margin))
        
        # Draw pen status
        if self.pen_touching:
            pen_status = f"✏️ Drawing (Pressure: {self.pen_pressure:.0%})"
            pen_color = GREEN
        else:
            pen_status = "✏️ Pen Ready"
            pen_color = BLUE
        
        pen_surface = self.small_font.render(pen_status, True, pen_color)
        self.screen.blit(pen_surface, (self.window_width - margin - pen_surface.get_width(), margin))
        
        # Draw character info
        romanji_text = f"({romanji}) - {self.character_index + 1}/{len(self.character_set)}"
        romanji_surface = self.ui_font.render(romanji_text, True, DARK_GRAY)
        romanji_rect = romanji_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 + int(150 * self.scale_factor)))
        self.screen.blit(romanji_surface, romanji_rect)
        
        # Draw TTS status indicator
        tts_status_y = self.window_height - int(60 * self.scale_factor)
        if not self.tts_enabled:
            # TTS disabled
            status_text = "🔇 TTS Disabled (Press M to enable)"
            status_color = DARK_GRAY
        elif self.tts_failed:
            # TTS failed
            status_text = f"❌ TTS Failed (Press R to reset, M to disable)"
            status_color = RED
        elif self.tts_error_count > 0:
            # TTS has errors but still working
            status_text = f"⚠️ TTS Issues ({self.tts_error_count} errors)"
            status_color = ORANGE
        else:
            # TTS working normally - show time since last success
            time_since = int(time.time() - self.tts_last_success)
            if time_since < 60:
                status_text = f"🔊 TTS Active"
                status_color = GREEN
            else:
                status_text = f"🔊 TTS Active ({time_since//60}m since last use)"
                status_color = DARK_GRAY
        
        status_surface = self.keybind_font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(self.window_width // 2, tts_status_y))
        self.screen.blit(status_surface, status_rect)
        
        # Draw TTS status indicator
        tts_status_y = self.window_height - int(60 * self.scale_factor)
        if not self.tts_enabled:
            # TTS disabled
            status_text = "🔇 TTS Disabled (Press T to enable)"
            status_color = DARK_GRAY
        elif self.tts_failed:
            # TTS failed
            status_text = f"❌ TTS Failed (Press R to reset, T to disable)"
            status_color = RED
        elif self.tts_error_count > 0:
            # TTS has errors but still working
            status_text = f"⚠️ TTS Issues ({self.tts_error_count} errors)"
            status_color = ORANGE
        else:
            # TTS working normally - show time since last success
            time_since = int(time.time() - self.tts_last_success)
            if time_since < 60:
                status_text = f"🔊 TTS Active"
                status_color = GREEN
            else:
                status_text = f"🔊 TTS Active ({time_since//60}m since last use)"
                status_color = DARK_GRAY
        
        status_surface = self.keybind_font.render(status_text, True, status_color)
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
            
            # Draw button text
            text_surface = self.button_font.render(button['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
            # Draw keybind hint
            keybind_surface = self.keybind_font.render(f"[{button['keybind']}]", True, WHITE)
            keybind_rect = keybind_surface.get_rect(centerx=button['rect'].centerx, 
                                                    top=button['rect'].bottom + 2)
            self.screen.blit(keybind_surface, keybind_rect)
        
        # Draw confetti if celebrating
        self.draw_confetti()
        
        pygame.display.flip()
    
    def get_stroke_paths(self, char):
        """Get actual stroke paths for Japanese characters.
        Returns list of stroke paths, where each path is a list of (x, y) points.
        """
        from stroke_order_data import get_stroke_data
        
        cx = self.window_width // 2
        cy = self.window_height // 3
        s = self.scale_factor
        
        # Get stroke data from comprehensive stroke order database
        relative_paths = get_stroke_data(char)
        
        # If character not found, use simple default
        if relative_paths is None:
            relative_paths = [
                [(-20, -40), (0, -20), (20, 0)],  # Default stroke 1
                [(-15, 10), (0, 30), (15, 45)]   # Default stroke 2
            ]
        
        # Convert relative to absolute positions with scaling
        absolute_paths = []
        for path in relative_paths:
            absolute_path = [(int(cx + x*s), int(cy + y*s)) for x, y in path]
            absolute_paths.append(absolute_path)
        
        return absolute_paths
    
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
                    if self.success_sound:
                        self.success_sound.play()
                    self.create_confetti()
            
            # Update confetti
            self.update_confetti()
            
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
