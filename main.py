# Import necessary tools
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
pygame.display.set_caption("President Simulator")

# Define stats
stats = {
    "food supply": 50,
    "funds": 50,
    "population": 50,
    "health": 50,
    "education": 50,
    "environment": 50,
    "security": 50,
    "approval": 50,
    "economy": 50,
    "military": 50
}

# Define events
events = [
    {"description": "Economic boom!", "choices": [{"text": "Celebrate", "approval": 5, "economy": 10}, {"text": "Invest", "economy": 15}]},
    {"description": "Military conflict!", "choices": [{"text": "Deploy troops", "approval": -10, "military": -5}, {"text": "Negotiate", "diplomacy": 10}]},
    {"description": "Disease outbreak!", "choices": [{"text": "Quarantine", "approval": 5, "health": -10}, {"text": "Research cure", "health": 10, "funds": -5}]},
    {"description": "Education funding cut!", "choices": [{"text": "Increase funding", "education": 10, "funds": -10}, {"text": "Ignore", "education": -10}]},
    {"description": "Environmental disaster!", "choices": [{"text": "Clean up", "environment": 10, "funds": -10}, {"text": "Ignore", "environment": -10}]},
    {"description": "Terrorist attack!", "choices": [{"text": "Increase security", "security": 10, "approval": -5}, {"text": "Address root causes", "security": -5, "approval": 5}]},
    {"description": "Scandal!", "choices": [{"text": "Address publicly", "approval": -20, "economy": -5}, {"text": "Ignore", "approval": -10}]},
    {"description": "Natural disaster!", "choices": [{"text": "Provide aid", "approval": 10, "economy": -10, "environment": -5}, {"text": "Ignore", "approval": -20, "environment": -10}]},
    {"description": "Technological breakthrough!", "choices": [{"text": "Invest in research", "economy": 10, "approval": 5, "education": 5}, {"text": "Sell patents", "economy": 15}]},
    {"description": "Healthcare crisis!", "choices": [{"text": "Increase funding", "approval": 10, "economy": -10, "health": 10}, {"text": "Ignore", "approval": -20, "health": -10}]},
    {"description": "Education reform!", "choices": [{"text": "Implement changes", "approval": 10, "economy": -5, "education": 10}, {"text": "Delay", "approval": -5, "education": -5}]},
    {"description": "Energy crisis!", "choices": [{"text": "Invest in renewable energy", "economy": -10, "approval": 10, "environment": 10}, {"text": "Increase fossil fuel production", "economy": 10, "approval": -10, "environment": -10}]},
    {"description": "Public protest!", "choices": [{"text": "Address concerns", "approval": 10, "diplomacy": 5, "security": -5}, {"text": "Ignore", "approval": -15, "security": 5}]},
    {"description": "Food shortage!", "choices": [{"text": "Import food", "funds": -10, "food supply": 10}, {"text": "Ration food", "food supply": 5, "approval": -5}]},
    {"description": "Population growth!", "choices": [{"text": "Celebrate", "approval": 10, "population": 10}, {"text": "Plan for future", "funds": -10, "population": 5}]}
]

current_event = None
event_count = 0  # Track the number of events until the next election

# Function to handle event choices
def handle_choice(choice):
    global current_event
    for stat in stats:
        if stat in choice:
            stats[stat] += choice[stat]
            stats[stat] = max(0, min(100, stats[stat]))  # Ensure stats are between 0 and 100
    current_event = None

# Function to handle elections
def handle_election():
    global event_count
    show_election_screen("Election in Progress...")
    pygame.time.wait(5000)  # Wait for 5 seconds

    approval = stats["approval"]
    if approval == 100:
        win = True
    else:
        win = random.random() < (approval / 100)
    
    if win:
        event_count = 0  # Reset event count for next term
        show_election_screen("You Won the Election!")
        pygame.time.wait(5000)  # Wait for 5 seconds
        return True
    else:
        show_election_screen("You Lost the Election!")
        pygame.time.wait(5000)  # Wait for 5 seconds
        return False

def show_election_screen(message):
    screen.fill((0, 0, 0))  # Fill the screen with black
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 255, 255))
    
    # Calculate the position to center the text
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect.topleft)
    
    pygame.display.flip()

# Function to draw buttons
def draw_buttons(choices):
    font = pygame.font.Font(None, 36)
    y = 300
    buttons = []
    for choice in choices:
        text = font.render(choice["text"], True, (255, 255, 255))
        rect = text.get_rect(topleft=(50, y))
        screen.blit(text, rect.topleft)
        buttons.append((rect, choice))
        y += 50
    return buttons

# Function to draw stat bars
def draw_stat_bars():
    bar_width = (screen.get_width() - 100) // (len(stats) // 2)  # Adjust bar width to fit the screen
    bar_height = 20
    x = 50
    y = screen.get_height() - 100  # Adjusted y position to be lower
    for i, (stat, value) in enumerate(stats.items()):
        if i == len(stats) // 2:
            x = 50
            y += 50
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # Draw border
        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width * (value / 100), bar_height))  # Draw filled bar
        font = pygame.font.Font(None, 24)
        text = font.render(f"{stat.capitalize()}: {value}", True, (255, 255, 255))
        screen.blit(text, (x + (bar_width - text.get_width()) // 2, y - 25))
        x += bar_width + 10  # Adjust spacing between bars

    # Draw remaining events text
    font = pygame.font.Font(None, 36)
    remaining_events_text = font.render(f"Events left: {15 - event_count}", True, (192, 192, 192))
    screen.blit(remaining_events_text, (screen.get_width() - remaining_events_text.get_width() - 20, 20))

def draw_fail_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    
    # Calculate the position to center the text
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(text, text_rect.topleft)
    
    # Display stats below the "Game Over" text
    font = pygame.font.Font(None, 36)
    y_offset = text_rect.bottom + 20
    for stat, value in stats.items():
        stat_text = font.render(f"{stat.capitalize()}: {value}", True, (255, 255, 255))
        stat_rect = stat_text.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(stat_text, stat_rect.topleft)
        y_offset += 40  # Adjust spacing between stats
    
    pygame.display.flip()
    pygame.time.wait(5000)  # Wait for 5 seconds before closing the game

# Main game loop
running = True
buttons = []
used_events = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and current_event:
            for rect, choice in buttons:
                if rect.collidepoint(event.pos):
                    handle_choice(choice)

    # Check if any stat has reached zero
    if any(value <= 0 for value in stats.values()):
        draw_fail_screen()
        running = False
        break

    # Handle a random event every 5 seconds if no current event
    if not current_event and pygame.time.get_ticks() % 5000 < 100:
        if event_count >= 15:
            if not handle_election():
                draw_fail_screen()
                running = False
                break
        else:
            available_events = [event for event in events if event not in used_events]
            if not available_events:
                used_events = []
                available_events = events[:]
            current_event = random.choice(available_events)
            used_events.append(current_event)
            event_count += 1

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw stat bars
    draw_stat_bars()

    # Display current event and choices
    if current_event:
        font = pygame.font.Font(None, 48)
        text = font.render(current_event["description"], True, (255, 255, 255))
        screen.blit(text, (50, 200))
        buttons = draw_buttons(current_event["choices"])

    pygame.display.flip()

pygame.quit()