#!/usr/bin/env python3
"""
Quick test to verify pygame pen/stylus event attributes
Run this on your Lenovo Y1 Yoga to test pen input
"""

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Pen Detection Test")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

events_log = []
max_log = 20

print("\n" + "="*60)
print("PEN DETECTION TEST")
print("="*60)
print("Touch the screen with your stylus to test pen detection.")
print("This will show if pygame detects pressure attributes.\n")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        # Log all mouse/touch events
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event_info = {
                'type': pygame.event.event_name(event.type),
                'has_pressure': hasattr(event, 'pressure'),
                'pressure': getattr(event, 'pressure', None),
                'has_touch': hasattr(event, 'touch'),
                'pos': event.pos if hasattr(event, 'pos') else None
            }
            
            # Print to console
            print(f"\n{event_info['type']}")
            print(f"  Has pressure attribute: {event_info['has_pressure']}")
            if event_info['has_pressure']:
                print(f"  Pressure value: {event_info['pressure']:.3f}")
            print(f"  Has touch attribute: {event_info['has_touch']}")
            
            # Add to log
            log_text = f"{event_info['type']}: "
            if event_info['has_pressure']:
                log_text += f"P={event_info['pressure']:.2f}"
            else:
                log_text += "No pressure"
            
            events_log.append(log_text)
            if len(events_log) > max_log:
                events_log.pop(0)
        
        elif event.type in [pygame.FINGERDOWN, pygame.FINGERUP, pygame.FINGERMOTION]:
            event_info = {
                'type': pygame.event.event_name(event.type),
                'has_pressure': hasattr(event, 'pressure'),
                'pressure': getattr(event, 'pressure', None),
            }
            
            print(f"\n{event_info['type']} (FINGER EVENT)")
            print(f"  Has pressure attribute: {event_info['has_pressure']}")
            if event_info['has_pressure']:
                print(f"  Pressure value: {event_info['pressure']:.3f}")
            
            log_text = f"{event_info['type']}: "
            if event_info['has_pressure']:
                log_text += f"P={event_info['pressure']:.2f}"
            else:
                log_text += "No pressure"
            
            events_log.append(log_text)
            if len(events_log) > max_log:
                events_log.pop(0)
    
    # Clear screen
    screen.fill((255, 255, 255))
    
    # Draw title
    title = font.render("Pen Detection Test", True, (0, 0, 0))
    screen.blit(title, (20, 20))
    
    # Draw instructions
    inst = font.render("Touch screen with stylus to test. Press ESC to exit.", True, (100, 100, 100))
    screen.blit(inst, (20, 60))
    
    # Draw event log
    y_pos = 120
    for log_entry in events_log:
        text = font.render(log_entry, True, (0, 0, 200))
        screen.blit(text, (20, y_pos))
        y_pos += 25
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("\nTest completed.")
sys.exit()
