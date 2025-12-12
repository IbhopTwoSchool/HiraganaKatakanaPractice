#!/usr/bin/env python3
"""
Hiragana and Katakana Practice Application
A pygame-based application for practicing Japanese character writing with pen/stylus support.
"""

import pygame
import sys
from characters import HIRAGANA, KATAKANA

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 200)
GREEN = (50, 200, 100)

# Drawing settings
PEN_COLOR = BLACK
PEN_WIDTH = 8
ERASER_WIDTH = 30


class HiraganaPracticeApp:
    """Main application class for Hiragana/Katakana practice."""
    
    def __init__(self):
        """Initialize the application."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hiragana & Katakana Practice")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Character selection
        self.character_set = HIRAGANA
        self.character_index = 0
        self.mode = "hiragana"  # "hiragana" or "katakana"
        
        # Drawing state
        self.drawing = False
        self.drawing_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.drawing_surface.fill(WHITE)
        self.drawing_surface.set_colorkey(WHITE)  # Make white transparent
        
        # Pen/stylus support - pygame handles this through mouse events
        # Pressure sensitivity available through pygame.mouse.get_cursor()
        
        # Font for characters and UI
        try:
            # Try to use a Japanese-compatible font
            self.char_font = pygame.font.Font(None, 400)  # Large for character display
            self.ui_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            self.char_font = pygame.font.SysFont('arial', 400)
            self.ui_font = pygame.font.SysFont('arial', 36)
            self.small_font = pygame.font.SysFont('arial', 24)
    
    def get_current_character(self):
        """Get the current character to practice."""
        return self.character_set[self.character_index]
    
    def next_character(self):
        """Move to the next character."""
        self.character_index = (self.character_index + 1) % len(self.character_set)
        self.clear_drawing()
    
    def previous_character(self):
        """Move to the previous character."""
        self.character_index = (self.character_index - 1) % len(self.character_set)
        self.clear_drawing()
    
    def toggle_mode(self):
        """Toggle between Hiragana and Katakana."""
        if self.mode == "hiragana":
            self.mode = "katakana"
            self.character_set = KATAKANA
        else:
            self.mode = "hiragana"
            self.character_set = HIRAGANA
        self.character_index = 0
        self.clear_drawing()
    
    def clear_drawing(self):
        """Clear the drawing surface."""
        self.drawing_surface.fill(WHITE)
    
    def handle_events(self):
        """Handle pygame events."""
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
            
            # Mouse/pen events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click or pen touch
                    self.drawing = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    # Draw on the drawing surface
                    pos = event.pos
                    # Connect previous position to current for smooth lines
                    if hasattr(event, 'rel'):
                        prev_pos = (pos[0] - event.rel[0], pos[1] - event.rel[1])
                        pygame.draw.line(self.drawing_surface, PEN_COLOR, 
                                       prev_pos, pos, PEN_WIDTH)
                    else:
                        pygame.draw.circle(self.drawing_surface, PEN_COLOR, 
                                         pos, PEN_WIDTH // 2)
    
    def draw_character_background(self):
        """Draw the opaque character in the background for tracing."""
        char = self.get_current_character()
        
        # Render character with transparency
        char_surface = self.char_font.render(char, True, (200, 200, 200, 128))
        char_rect = char_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        self.screen.blit(char_surface, char_rect)
    
    def draw_ui(self):
        """Draw the user interface elements."""
        # Draw mode indicator
        mode_text = f"Mode: {self.mode.capitalize()}"
        mode_surface = self.ui_font.render(mode_text, True, BLUE)
        self.screen.blit(mode_surface, (20, 20))
        
        # Draw character counter
        counter_text = f"Character: {self.character_index + 1}/{len(self.character_set)}"
        counter_surface = self.small_font.render(counter_text, True, BLACK)
        self.screen.blit(counter_surface, (20, 60))
        
        # Draw instructions
        instructions = [
            "Instructions:",
            "• Use pen/stylus or mouse to draw",
            "• LEFT/RIGHT arrows: Change character",
            "• SPACE: Next character",
            "• C: Clear drawing",
            "• T: Toggle Hiragana/Katakana",
            "• ESC/Q: Quit"
        ]
        
        y_offset = WINDOW_HEIGHT - 200
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, DARK_GRAY)
            self.screen.blit(text_surface, (20, y_offset + i * 25))
    
    def render(self):
        """Render the application."""
        # Fill background
        self.screen.fill(WHITE)
        
        # Draw the opaque character for tracing
        self.draw_character_background()
        
        # Draw the user's drawing on top
        self.screen.blit(self.drawing_surface, (0, 0))
        
        # Draw UI elements
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main application loop."""
        while self.running:
            self.handle_events()
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
