#!/usr/bin/env python3
"""
Hiragana and Katakana Practice Application
A pygame-based application for practicing Japanese character writing with pen/stylus support.
"""

import pygame
import sys
import threading
import tempfile
import os
import ctypes
import random
import time
import platform
from gtts import gTTS
from characters import HIRAGANA_DATA, KATAKANA_DATA

# Set Windows DPI awareness for proper scaling
if sys.platform == 'win32':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # System DPI aware
    except:
        pass

# Initialize pygame
pygame.init()

# Get display info for responsive sizing
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

# Set window size to 80% of screen size (or smaller for tablets)
WINDOW_WIDTH = min(int(SCREEN_WIDTH * 0.8), 1400)
WINDOW_HEIGHT = min(int(SCREEN_HEIGHT * 0.85), 900)

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
        # Make window resizable and fullscreen-capable
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Hiragana & Katakana Practice")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Window dimensions (will be updated on resize)
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.calculate_layout()
        
        # Character selection
        self.character_set = HIRAGANA_DATA
        self.character_index = 0
        self.mode = "hiragana"  # "hiragana" or "katakana"
        
        # Drawing state
        self.drawing = False
        self.drawing_surface = pygame.Surface((self.window_width, self.window_height))
        self.drawing_surface.fill(WHITE)
        self.drawing_surface.set_colorkey(WHITE)  # Make white transparent
        
        # Stroke tracking for better completion detection
        self.drawing_strokes = []  # List of strokes (each stroke is a list of points)
        self.current_stroke = []  # Current stroke being drawn
        
        # Stylus mode
        self.stylus_mode = False
        self.stylus_detected = False
        self.last_pressure = 1.0
        
        # Detect if running on Lenovo Y1 Yoga or similar touch-enabled device
        self.detect_touch_device()
        
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
        self.current_audio = None
        
        # Font setup with dynamic scaling
        self.update_fonts()
        
        # Create buttons
        self.buttons = self.create_buttons()
        
        # Initialize sound system
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.success_sound = self.create_success_sound()
        
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
        japanese_fonts = ['msgothic', 'meiryo', 'mspgothic', 'yugothic', 'msmincho']
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
            {'text': '✏️ Stylus', 'keybind': 'P', 'action': 'toggle_stylus', 'color': PURPLE},
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
    
    def detect_touch_device(self):
        """Detect if running on a touch-enabled device like Lenovo Y1 Yoga."""
        try:
            # Check Windows system info for touch capability
            if sys.platform == 'win32':
                system_info = platform.machine().lower()
                # Auto-enable stylus mode if touch-capable hardware detected
                if 'yoga' in platform.node().lower() or 'lenovo' in platform.node().lower():
                    self.stylus_mode = True
                    print("Touch-enabled device detected - Stylus mode enabled")
        except:
            pass
    
    def draw_brush_stroke(self, pos, pressure=1.0):
        """Draw a brush-like stroke with pressure sensitivity."""
        # Adjust brush size based on pressure (0.0 to 1.0)
        brush_size = int(self.pen_width * pressure * 2.5)
        brush_size = max(4, min(brush_size, int(self.pen_width * 3)))
        
        # Create multiple circles with slight offsets for brush effect
        for i in range(3):
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            alpha = int(120 + (135 * pressure))  # More opaque with more pressure
            
            # Draw semi-transparent circles for brush effect in BLACK
            brush_surface = pygame.Surface((brush_size * 2, brush_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(brush_surface, (*PEN_COLOR, alpha), 
                             (brush_size, brush_size), brush_size - i)
            
            # Use normal blending to preserve black color
            self.drawing_surface.blit(brush_surface, 
                                     (pos[0] + offset_x - brush_size, 
                                      pos[1] + offset_y - brush_size))
        
        # Track the stroke point
        self.current_stroke.append(pos)
    
    def draw_pen_stroke(self, pos, prev_pos):
        """Draw a regular pen stroke."""
        pygame.draw.line(self.drawing_surface, PEN_COLOR, prev_pos, pos, self.pen_width)
        pygame.draw.circle(self.drawing_surface, PEN_COLOR, pos, self.pen_width // 2)
        # Track the stroke point
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
            
            # Mix waves with envelope
            mixed = (wave1 + wave2 + wave3) / 3 * envelope
            
            # Convert to 16-bit integer stereo
            audio = (mixed * 32767).astype(np.int16)
            audio = np.repeat(audio.reshape(-1, 1), 2, axis=1)  # Make stereo
            
            sound = pygame.sndarray.make_sound(audio)
            return sound
        except Exception as e:
            print(f"Error creating success sound: {e}")
            return None
    
    def get_stroke_order_hints(self, char):
        """Get stroke order hints for a character (simplified for common characters)."""
        # Return list of numbered guide points for stroke order
        # These are approximate positions relative to character center
        # Format: [(number, x_offset, y_offset), ...]
        stroke_hints = {
            # Hiragana vowels
            'あ': [(1, -0.3, -0.4), (2, 0.2, -0.3), (3, 0, 0.3)],
            'い': [(1, 0, -0.4), (2, -0.2, 0.2)],
            'う': [(1, -0.2, -0.3), (2, 0, 0.2)],
            'え': [(1, -0.3, -0.3), (2, 0.2, 0)],
            'お': [(1, -0.3, -0.4), (2, 0, -0.2), (3, -0.1, 0.3)],
            # Add more as needed - for now, default to center
        }
        return stroke_hints.get(char, [(1, 0, -0.3), (2, 0, 0), (3, 0, 0.3)])
    
    def create_confetti(self):
        """Create confetti particles for celebration."""
        for _ in range(50):
            particle = {
                'x': self.window_width // 2,
                'y': self.window_height // 2 - int(50 * self.scale_factor),
                'vx': random.uniform(-8, 8) * self.scale_factor,
                'vy': random.uniform(-12, -5) * self.scale_factor,
                'gravity': 0.4 * self.scale_factor,
                'size': random.randint(int(5 * self.scale_factor), int(12 * self.scale_factor)),
                'color': random.choice(CONFETTI_COLORS),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-10, 10),
                'lifetime': 120  # frames
            }
            self.confetti_particles.append(particle)
    
    def update_confetti(self):
        """Update confetti particle positions and remove dead particles."""
        for particle in self.confetti_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += particle['gravity']
            particle['rotation'] += particle['rotation_speed']
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0 or particle['y'] > WINDOW_HEIGHT:
                self.confetti_particles.remove(particle)
    
    def draw_confetti(self):
        """Draw confetti particles."""
        for particle in self.confetti_particles:
            # Create a small square surface for the confetti
            size = particle['size']
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(surf, particle['color'], (0, 0, size, size))
            
            # Rotate the surface
            rotated = pygame.transform.rotate(surf, particle['rotation'])
            rect = rotated.get_rect(center=(int(particle['x']), int(particle['y'])))
            
            # Apply fade out near end of lifetime
            alpha = min(255, particle['lifetime'] * 4)
            rotated.set_alpha(alpha)
            
            self.screen.blit(rotated, rect)
    
    def check_character_completion(self):
        """Check if the user has traced the character sufficiently using improved detection."""
        if self.character_completed or not self.show_background:
            return
        
        # Don't check while actively drawing - only after cursor is lifted
        if self.drawing:
            return
        
        # Only check if user has made strokes
        if len(self.drawing_strokes) < 1:
            return
        
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return
        
        self.last_check_time = current_time
        
        try:
            # Render the target character to a surface
            char, romanji = self.get_current_character()
            char_surface = self.char_font.render(char, True, BLACK)
            char_rect = char_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 - int(30 * self.scale_factor)))
            
            # Create a mask from the character
            char_mask = pygame.mask.from_surface(char_surface)
            
            # Create a mask from the user's drawing at the character position
            clipped_rect = char_rect.clip(pygame.Rect(0, 0, self.window_width, self.window_height))
            if clipped_rect.width <= 0 or clipped_rect.height <= 0:
                return
            
            drawing_subsurface = self.drawing_surface.subsurface(clipped_rect)
            drawing_mask = pygame.mask.from_surface(drawing_subsurface)
            
            # Count overlapping pixels
            char_pixels = char_mask.count()
            if char_pixels == 0:
                return
            
            # Calculate overlap
            overlap = char_mask.overlap_area(drawing_mask, (0, 0))
            coverage = overlap / char_pixels
            
            # Check stroke count - Japanese characters typically have 2-5 strokes
            stroke_count = len(self.drawing_strokes)
            
            # STRICT completion criteria to prevent early confetti:
            # - Need at least 2 strokes AND 65% coverage
            # - OR single stroke with 80% coverage (for simple characters like "い")
            # - OR 3+ strokes with 60% coverage (completed character)
            completion_criteria_met = (
                (stroke_count >= 2 and coverage >= 0.65) or
                (stroke_count == 1 and coverage >= 0.80) or
                (stroke_count >= 3 and coverage >= 0.60)
            )
            
            if completion_criteria_met:
                self.character_completed = True
                self.create_confetti()
                if self.success_sound:
                    self.success_sound.play()
                print(f"✓ Character completed! Strokes: {stroke_count}, Coverage: {coverage:.1%}")
        
        except Exception as e:
            pass  # Silently ignore errors in completion detection
    
    def speak_current_character(self):
        """Speak the romanji pronunciation of the current character using Japanese TTS."""
        char, romanji = self.get_current_character()
        
        def speak():
            try:
                with self.tts_lock:
                    # Stop any currently playing audio
                    try:
                        pygame.mixer.music.stop()
                    except:
                        pass
                    
                    # Create Japanese TTS audio using the actual character, not romanji
                    # This ensures proper Japanese pronunciation
                    tts = gTTS(text=char, lang='ja', slow=False)
                    
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                        temp_file = fp.name
                        tts.save(temp_file)
                    
                    # Initialize pygame mixer if not already done
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    
                    # Play the audio
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish or be stopped
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    
                    # Clean up temporary file
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                        
            except Exception as e:
                print(f"TTS Error: {e}")
        
        # Run TTS in a separate thread to avoid blocking
        threading.Thread(target=speak, daemon=True).start()
    
    def get_current_character(self):
        """Get the current character and romanji to practice."""
        return self.character_set[self.character_index]
    
    def next_character(self):
        """Move to the next character."""
        # Stop any currently playing audio
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
        # Stop any currently playing audio
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
        # Stop any currently playing audio
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
    
    def handle_events(self):
        """Handle pygame events."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                self.window_width = event.w
                self.window_height = event.h
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                
                # Recalculate layout and recreate surfaces
                self.calculate_layout()
                self.update_fonts()
                self.buttons = self.create_buttons()
                
                # Resize drawing surface (preserve content)
                old_surface = self.drawing_surface.copy()
                self.drawing_surface = pygame.Surface((self.window_width, self.window_height))
                self.drawing_surface.fill(WHITE)
                self.drawing_surface.set_colorkey(WHITE)
                self.drawing_surface.blit(old_surface, (0, 0))
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
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
                elif event.key == pygame.K_g:
                    self.show_background = not self.show_background
                elif event.key == pygame.K_p:
                    # Toggle stylus mode with debug warning
                    self.stylus_mode = not self.stylus_mode
                    if self.stylus_mode and not self.stylus_detected:
                        print("⚠️ DEBUG MODE: Stylus mode enabled with mouse (no stylus detected)")
                        print("   Mouse will simulate pressure-sensitive brush strokes.")
            
            # Button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click or touch
                    # Check if any button was clicked
                    button_clicked = False
                    for button in self.buttons:
                        if button['rect'].collidepoint(event.pos):
                            button_clicked = True
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
                            elif button['action'] == 'toggle_stylus':
                                self.stylus_mode = not self.stylus_mode
                                if self.stylus_mode and not self.stylus_detected:
                                    print("⚠️ DEBUG MODE: Stylus mode enabled with mouse (no stylus detected)")
                                    print("   Mouse will simulate pressure-sensitive brush strokes.")
                            elif button['action'] == 'quit':
                                self.running = False
                            break
                    
                    # If no button was clicked, start drawing
                    if not button_clicked:
                        self.drawing = True
                        self.current_stroke = [event.pos]  # Start new stroke
                        # Get pressure if available (stylus)
                        if hasattr(event, 'pressure'):
                            self.last_pressure = event.pressure
                            if event.pressure > 0:
                                self.stylus_detected = True
                                if not self.stylus_mode:
                                    self.stylus_mode = True  # Auto-enable
                        else:
                            self.last_pressure = 1.0
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing = False
                    # Finish current stroke
                    if len(self.current_stroke) > 2:  # Only save strokes with enough points
                        self.drawing_strokes.append(self.current_stroke.copy())
                    self.current_stroke = []
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    pos = event.pos
                    
                    # Get pressure if available
                    pressure = self.last_pressure
                    if hasattr(event, 'pressure') and event.pressure > 0:
                        pressure = event.pressure
                        self.last_pressure = pressure
                        if not self.stylus_detected:
                            self.stylus_detected = True
                            if not self.stylus_mode:
                                self.stylus_mode = True  # Auto-enable
                    
                    # Draw with stylus brush or regular pen
                    if self.stylus_mode:
                        self.draw_brush_stroke(pos, pressure)
                        self.current_stroke.append(pos)  # Track stroke points
                    else:
                        prev_pos = (pos[0] - event.rel[0], pos[1] - event.rel[1])
                        self.draw_pen_stroke(pos, prev_pos)
    
    def draw_character_background(self):
        """Draw the opaque character in the background for tracing with stroke order guides."""
        char, romanji = self.get_current_character()
        
        # Render character with transparency
        char_surface = self.char_font.render(char, True, (200, 200, 200))
        char_surface = char_surface.convert_alpha()
        char_surface.set_alpha(128)  # Set transparency level
        char_rect = char_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 - int(30 * self.scale_factor)))
        
        self.screen.blit(char_surface, char_rect)
        
        # Draw stroke order guides
        stroke_hints = self.get_stroke_order_hints(char)
        center_x = self.window_width // 2
        center_y = self.window_height // 2 - int(30 * self.scale_factor)
        
        for i, (num, x_offset, y_offset) in enumerate(stroke_hints):
            # Calculate position relative to character center
            guide_x = center_x + int(x_offset * 200 * self.scale_factor)
            guide_y = center_y + int(y_offset * 200 * self.scale_factor)
            
            # Draw numbered circle
            circle_radius = int(18 * self.scale_factor)
            pygame.draw.circle(self.screen, RED, (guide_x, guide_y), circle_radius)
            pygame.draw.circle(self.screen, WHITE, (guide_x, guide_y), circle_radius - 2)
            
            # Draw number
            num_surface = self.guide_font.render(str(num), True, RED)
            num_rect = num_surface.get_rect(center=(guide_x, guide_y))
            self.screen.blit(num_surface, num_rect)
    
    def draw_ui(self):
        """Draw the user interface elements."""
        char, romanji = self.get_current_character()
        
        margin = int(20 * self.scale_factor)
        
        # Draw mode indicator
        mode_text = f"Mode: {self.mode.capitalize()} | Press F11 for fullscreen"
        mode_surface = self.ui_font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (margin, margin))
        
        # Draw stylus status if enabled
        if self.stylus_mode:
            stylus_text = "✏️ Stylus Mode"
            stylus_surface = self.small_font.render(stylus_text, True, PURPLE)
            self.screen.blit(stylus_surface, (self.window_width - margin - stylus_surface.get_width(), margin))
        
        # Draw character counter and stroke count
        counter_text = f"Character: {self.character_index + 1}/{len(self.character_set)} | Strokes: {len(self.drawing_strokes)}"
        counter_surface = self.small_font.render(counter_text, True, BLACK)
        self.screen.blit(counter_surface, (margin, margin + int(40 * self.scale_factor)))
        
        # Draw romanji pronunciation (larger and centered)
        romanji_text = f"Romanji: {romanji}"
        romanji_surface = self.ui_font.render(romanji_text, True, GREEN)
        romanji_rect = romanji_surface.get_rect(center=(self.window_width // 2, int(40 * self.scale_factor)))
        self.screen.blit(romanji_surface, romanji_rect)
        
        # Draw buttons with keybinds
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            # Check if mouse is hovering over button
            color = BUTTON_HOVER if button['rect'].collidepoint(mouse_pos) else button['color']
            
            # Draw button background
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=int(8 * self.scale_factor))
            pygame.draw.rect(self.screen, BLACK, button['rect'], max(int(2 * self.scale_factor), 1), border_radius=int(8 * self.scale_factor))
            
            # Draw button text
            text_surface = self.button_font.render(button['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=(button['rect'].centerx, button['rect'].centery - int(8 * self.scale_factor)))
            self.screen.blit(text_surface, text_rect)
            
            # Draw keybind label below button text
            keybind_surface = self.keybind_font.render(f"[{button['keybind']}]", True, WHITE)
            keybind_rect = keybind_surface.get_rect(center=(button['rect'].centerx, button['rect'].centery + int(12 * self.scale_factor)))
            self.screen.blit(keybind_surface, keybind_rect)
    
    def render(self):
        """Render the application."""
        # Fill background
        self.screen.fill(WHITE)
        
        # Draw the opaque character for tracing (if enabled)
        if self.show_background:
            self.draw_character_background()
        
        # Draw the user's drawing on top
        self.screen.blit(self.drawing_surface, (0, 0))
        
        # Draw confetti
        self.draw_confetti()
        
        # Draw UI elements
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main application loop."""
        while self.running:
            self.handle_events()
            self.check_character_completion()
            self.update_confetti()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point."""
    app = HiraganaPracticeApp()
    app.run()


if __name__ == "__main__":
    main()
