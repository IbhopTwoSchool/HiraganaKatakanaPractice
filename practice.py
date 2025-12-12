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

# Calculate scaling factors
SCALE_FACTOR = min(WINDOW_WIDTH / 1024, WINDOW_HEIGHT / 768)

# Constants
FPS = 60

# Button dimensions (scaled)
BUTTON_HEIGHT = int(80 * SCALE_FACTOR)
BUTTON_WIDTH = int(140 * SCALE_FACTOR)
BUTTON_MARGIN = int(15 * SCALE_FACTOR)

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

# Drawing settings (scaled)
PEN_COLOR = BLACK
PEN_WIDTH = max(int(8 * SCALE_FACTOR), 4)
ERASER_WIDTH = int(30 * SCALE_FACTOR)


class HiraganaPracticeApp:
    """Main application class for Hiragana/Katakana practice."""
    
    def __init__(self):
        """Initialize the application."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hiragana & Katakana Practice")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Character selection
        self.character_set = HIRAGANA_DATA
        self.character_index = 0
        self.mode = "hiragana"  # "hiragana" or "katakana"
        
        # Drawing state
        self.drawing = False
        self.drawing_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.drawing_surface.fill(WHITE)
        self.drawing_surface.set_colorkey(WHITE)  # Make white transparent
        
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
        
        # Font for characters and UI (scaled)
        # Use Windows fonts that support Japanese characters
        japanese_fonts = ['msgothic', 'meiryo', 'mspgothic', 'yugothic', 'msmincho']
        self.char_font = pygame.font.SysFont(japanese_fonts, int(350 * SCALE_FACTOR))
        self.ui_font = pygame.font.SysFont(japanese_fonts, int(36 * SCALE_FACTOR))
        self.small_font = pygame.font.SysFont(japanese_fonts, int(24 * SCALE_FACTOR))
        self.button_font = pygame.font.SysFont(japanese_fonts, int(24 * SCALE_FACTOR))
        self.keybind_font = pygame.font.SysFont(japanese_fonts, int(16 * SCALE_FACTOR))
        
        # Create buttons
        self.buttons = self.create_buttons()
        
        # Initialize sound system
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.success_sound = self.create_success_sound()
        
        # Speak the first character
        self.speak_current_character()
    
    def create_buttons(self):
        """Create touch-friendly buttons."""
        buttons = []
        y_pos = WINDOW_HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN
        
        # Previous button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': '← Previous',
            'keybind': 'LEFT',
            'action': 'previous',
            'color': BUTTON_COLOR
        })
        
        # Clear button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_WIDTH, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Clear',
            'keybind': 'C',
            'action': 'clear',
            'color': GREEN
        })
        
        # Next button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_WIDTH * 2, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Next →',
            'keybind': 'RIGHT',
            'action': 'next',
            'color': BUTTON_COLOR
        })
        
        # Toggle mode button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 4 + BUTTON_WIDTH * 3, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Toggle',
            'keybind': 'T',
            'action': 'toggle',
            'color': BLUE
        })
        
        # Repeat sound button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_WIDTH * 4, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': '🔊 Sound',
            'keybind': 'S',
            'action': 'sound',
            'color': GREEN
        })
        
        # Show/Hide background button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 6 + BUTTON_WIDTH * 5, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': '👁 Guide',
            'keybind': 'G',
            'action': 'toggle_bg',
            'color': BLUE
        })
        
        # Stylus mode button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 7 + BUTTON_WIDTH * 6, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': '✏️ Stylus',
            'keybind': 'P',
            'action': 'toggle_stylus',
            'color': PURPLE
        })
        
        # Quit button
        buttons.append({
            'rect': pygame.Rect(BUTTON_MARGIN * 8 + BUTTON_WIDTH * 7, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT),
            'text': 'Quit',
            'keybind': 'ESC',
            'action': 'quit',
            'color': RED
        })
        
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
        brush_size = int(PEN_WIDTH * pressure * 2.5)
        brush_size = max(4, min(brush_size, int(PEN_WIDTH * 3)))
        
        # Create multiple circles with slight offsets for brush effect
        for i in range(3):
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
            alpha = int(100 + (155 * pressure))  # More opaque with more pressure
            
            # Draw semi-transparent circles for brush effect
            brush_surface = pygame.Surface((brush_size * 2, brush_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(brush_surface, (*PEN_COLOR, alpha), 
                             (brush_size, brush_size), brush_size - i)
            
            self.drawing_surface.blit(brush_surface, 
                                     (pos[0] + offset_x - brush_size, 
                                      pos[1] + offset_y - brush_size),
                                     special_flags=pygame.BLEND_RGBA_ADD)
    
    def draw_pen_stroke(self, pos, prev_pos):
        """Draw a regular pen stroke."""
        pygame.draw.line(self.drawing_surface, PEN_COLOR, prev_pos, pos, PEN_WIDTH)
        pygame.draw.circle(self.drawing_surface, PEN_COLOR, pos, PEN_WIDTH // 2)
    
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
    
    def create_confetti(self):
        """Create confetti particles for celebration."""
        for _ in range(50):
            particle = {
                'x': WINDOW_WIDTH // 2,
                'y': WINDOW_HEIGHT // 2 - int(50 * SCALE_FACTOR),
                'vx': random.uniform(-8, 8) * SCALE_FACTOR,
                'vy': random.uniform(-12, -5) * SCALE_FACTOR,
                'gravity': 0.4 * SCALE_FACTOR,
                'size': random.randint(int(5 * SCALE_FACTOR), int(12 * SCALE_FACTOR)),
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
        """Check if the user has traced the character sufficiently."""
        if self.character_completed or not self.show_background:
            return
        
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return
        
        self.last_check_time = current_time
        
        try:
            # Render the target character to a surface
            char, romanji = self.get_current_character()
            char_surface = self.char_font.render(char, True, BLACK)
            char_rect = char_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - int(30 * SCALE_FACTOR)))
            
            # Create a mask from the character
            char_mask = pygame.mask.from_surface(char_surface)
            
            # Create a mask from the user's drawing at the character position
            drawing_subsurface = self.drawing_surface.subsurface(char_rect.clip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)))
            drawing_mask = pygame.mask.from_surface(drawing_subsurface)
            
            # Count overlapping pixels
            char_pixels = char_mask.count()
            if char_pixels == 0:
                return
            
            overlap = char_mask.overlap_area(drawing_mask, (0, 0))
            coverage = overlap / char_pixels
            
            # If user has covered 60% or more of the character, mark as complete
            if coverage >= 0.60:
                self.character_completed = True
                self.create_confetti()
                if self.success_sound:
                    self.success_sound.play()
        
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
    
    def handle_events(self):
        """Handle pygame events."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
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
                elif event.key == pygame.K_g:
                    self.show_background = not self.show_background
                elif event.key == pygame.K_p:
                    self.stylus_mode = not self.stylus_mode
            
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
                            elif button['action'] == 'quit':
                                self.running = False
                            break
                    
                    # If no button was clicked, start drawing
                    if not button_clicked:
                        self.drawing = True
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
                    else:
                        prev_pos = (pos[0] - event.rel[0], pos[1] - event.rel[1])
                        self.draw_pen_stroke(pos, prev_pos)
    
    def draw_character_background(self):
        """Draw the opaque character in the background for tracing."""
        char, romanji = self.get_current_character()
        
        # Render character with transparency
        char_surface = self.char_font.render(char, True, (200, 200, 200))
        char_surface = char_surface.convert_alpha()
        char_surface.set_alpha(128)  # Set transparency level
        char_rect = char_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - int(30 * SCALE_FACTOR)))
        
        self.screen.blit(char_surface, char_rect)
    
    def draw_ui(self):
        """Draw the user interface elements."""
        char, romanji = self.get_current_character()
        
        margin = int(20 * SCALE_FACTOR)
        
        # Draw mode indicator
        mode_text = f"Mode: {self.mode.capitalize()}"
        mode_surface = self.ui_font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (margin, margin))
        
        # Draw stylus status if enabled
        if self.stylus_mode:
            stylus_text = "✏️ Stylus Mode"
            stylus_surface = self.small_font.render(stylus_text, True, PURPLE)
            self.screen.blit(stylus_surface, (WINDOW_WIDTH - margin - stylus_surface.get_width(), margin))
        
        # Draw character counter
        counter_text = f"Character: {self.character_index + 1}/{len(self.character_set)}"
        counter_surface = self.small_font.render(counter_text, True, BLACK)
        self.screen.blit(counter_surface, (margin, margin + int(40 * SCALE_FACTOR)))
        
        # Draw romanji pronunciation (larger and centered)
        romanji_text = f"Romanji: {romanji}"
        romanji_surface = self.ui_font.render(romanji_text, True, GREEN)
        romanji_rect = romanji_surface.get_rect(center=(WINDOW_WIDTH // 2, int(40 * SCALE_FACTOR)))
        self.screen.blit(romanji_surface, romanji_rect)
        
        # Draw buttons with keybinds
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            # Check if mouse is hovering over button
            color = BUTTON_HOVER if button['rect'].collidepoint(mouse_pos) else button['color']
            
            # Draw button background
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=int(10 * SCALE_FACTOR))
            pygame.draw.rect(self.screen, BLACK, button['rect'], max(int(3 * SCALE_FACTOR), 2), border_radius=int(10 * SCALE_FACTOR))
            
            # Draw button text
            text_surface = self.button_font.render(button['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=(button['rect'].centerx, button['rect'].centery - int(8 * SCALE_FACTOR)))
            self.screen.blit(text_surface, text_rect)
            
            # Draw keybind label below button text
            keybind_surface = self.keybind_font.render(f"[{button['keybind']}]", True, WHITE)
            keybind_rect = keybind_surface.get_rect(center=(button['rect'].centerx, button['rect'].centery + int(12 * SCALE_FACTOR)))
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
