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

# Define regions with names, colors, and stats
region_names = ["Region A", "Region B", "Region C"]
region_colors = {"Region A": (255, 0, 0), "Region B": (0, 255, 0), "Region C": (0, 0, 255)}
regions = {
    name: {
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
    } for name in region_names
}

# Define other nations with names, colors, and stats
nation_names = ["Nation A", "Nation B"]
nation_colors = {"Nation A": (255, 165, 0), "Nation B": (0, 0, 255)}
nations = {
    name: {
        "regions": {
            f"{name} Region {i+1}": {
                "food supply": random.randint(30, 70),
                "funds": random.randint(30, 70),
                "population": random.randint(30, 70),
                "health": random.randint(30, 70),
                "education": random.randint(30, 70),
                "environment": random.randint(30, 70),
                "security": random.randint(30, 70),
                "approval": random.randint(30, 70),
                "economy": random.randint(30, 70),
                "military": random.randint(30, 70)
            } for i in range(3)
        },
        "trade_agreement": False,
        "peace_agreement": False,
        "at_war": False
    } for name in nation_names
}

# Function to calculate the nation's average stats
def calculate_nation_stats():
    global stats
    for stat in stats:
        stats[stat] = sum(region[stat] for region in regions.values()) // len(regions)

# Define events
events = [
    {"title": "Economic boom!", "description": "The economy is thriving.", "choices": [{"text": "Celebrate", "approval": 5, "economy": 10}, {"text": "Invest", "economy": 15}]},
    {"title": "Military conflict!", "description": "A conflict has arisen.", "choices": [{"text": "Deploy troops", "approval": -10, "military": -5}, {"text": "Negotiate", "diplomacy": 10}]},
    {"title": "Disease outbreak!", "description": "A disease is spreading.", "choices": [{"text": "Quarantine", "approval": 5, "health": -10}, {"text": "Research cure", "health": 10, "funds": -5}]},
    {"title": "Education funding cut!", "description": "Funding for education has been reduced.", "choices": [{"text": "Increase funding", "education": 10, "funds": -10}, {"text": "Ignore", "education": -10}]},
    {"title": "Environmental disaster!", "description": "An environmental disaster has occurred.", "choices": [{"text": "Clean up", "environment": 10, "funds": -10}, {"text": "Ignore", "environment": -10}]},
    {"title": "Terrorist attack!", "description": "A terrorist attack has taken place.", "choices": [{"text": "Increase security", "security": 10, "approval": -5}, {"text": "Address root causes", "security": -5, "approval": 5}]},
    {"title": "Scandal!", "description": "A scandal has been uncovered.", "choices": [{"text": "Address publicly", "approval": -20, "economy": -5}, {"text": "Ignore", "approval": -10}]},
    {"title": "Natural disaster!", "description": "A natural disaster has struck.", "choices": [{"text": "Provide aid", "approval": 10, "economy": -10, "environment": -5}, {"text": "Ignore", "approval": -20, "environment": -10}]},
    {"title": "Technological breakthrough!", "description": "A new technology has been developed.", "choices": [{"text": "Invest in research", "economy": 10, "approval": 5, "education": 5}, {"text": "Sell patents", "economy": 15}]},
    {"title": "Healthcare crisis!", "description": "The healthcare system is in crisis.", "choices": [{"text": "Increase funding", "approval": 10, "economy": -10, "health": 10}, {"text": "Ignore", "approval": -20, "health": -10}]},
    {"title": "Education reform!", "description": "Reforms in education are proposed.", "choices": [{"text": "Implement changes", "approval": 10, "economy": -5, "education": 10}, {"text": "Delay", "approval": -5, "education": -5}]},
    {"title": "Energy crisis!", "description": "There is an energy shortage.", "choices": [{"text": "Invest in renewable energy", "economy": -10, "approval": 10, "environment": 10}, {"text": "Increase fossil fuel production", "economy": 10, "approval": -10, "environment": -10}]},
    {"title": "Public protest!", "description": "The public is protesting.", "choices": [{"text": "Address concerns", "approval": 10, "diplomacy": 5, "security": -5}, {"text": "Ignore", "approval": -15, "security": 5}]},
    {"title": "Food shortage!", "description": "There is a shortage of food.", "choices": [{"text": "Import food", "funds": -10, "food supply": 10}, {"text": "Ration food", "food supply": 5, "approval": -5}]},
    {"title": "Population growth!", "description": "The population is increasing.", "choices": [{"text": "Celebrate", "approval": 10, "population": 10}, {"text": "Plan for future", "funds": -10, "population": 5}]}
]

current_event = None
event_count = 0  # Track the number of events until the next election

# Function to handle event choices
def handle_choice(choice, region_name):
    global current_event
    for stat in regions[region_name]:
        if stat in choice:
            regions[region_name][stat] += choice[stat]
            regions[region_name][stat] = max(0, min(100, regions[region_name][stat]))  # Ensure stats are between 0 and 100
    calculate_nation_stats()
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
    pygame.draw.line(screen, (192, 192, 192), (0, screen.get_height() - 140), (screen.get_width(), screen.get_height() - 140), 2)
    bar_width = (screen.get_width() - 100) // (len(stats) // 2)  # Adjust bar width to fit the screen
    bar_height = 20
    x = 50
    y = screen.get_height() - 100  # Adjusted y position to be lower
    mouse_pos = pygame.mouse.get_pos()
    for i, (stat, value) in enumerate(stats.items()):
        if i == len(stats) // 2:
            x = 50
            y += 50
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # Draw border
        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width * (value / 100), bar_height))  # Draw filled bar
        font = pygame.font.Font(None, 24)
        text = font.render(f"{stat.capitalize()}: {value}", True, (255, 255, 255))
        screen.blit(text, (x + (bar_width - text.get_width()) // 2, y - 25))
        
        # Show region stats on hover
        if pygame.Rect(x, y, bar_width, bar_height).collidepoint(mouse_pos):
            y_offset = y - 150
            for region_name, region_stats in regions.items():
                region_text = font.render(f"{region_name}: {region_stats[stat]}", True, region_colors[region_name])
                screen.blit(region_text, (x, y_offset))
                y_offset += 25

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

# Load icons for stats
icons = {
    "food supply": pygame.image.load("icons/food.png"),
    "funds": pygame.image.load("icons/funds.png"),
    "population": pygame.image.load("icons/population.png"),
    "health": pygame.image.load("icons/health.png"),
    "education": pygame.image.load("icons/education.png"),
    "environment": pygame.image.load("icons/environment.png"),
    "security": pygame.image.load("icons/security.png"),
    "approval": pygame.image.load("icons/approval.png"),
    "economy": pygame.image.load("icons/economy.png"),
    "military": pygame.image.load("icons/military.png")
}

# Function to handle foreign affairs
def handle_foreign_affairs():
    global current_event
    font = pygame.font.Font(None, 36)
    y = 100
    buttons = []
    for nation_name, nation_data in nations.items():
        nation_text = font.render(f"{nation_name}", True, nation_colors[nation_name])
        screen.blit(nation_text, (50, y))
        y += 50
        for region_name, region_stats in nation_data["regions"].items():
            region_text = font.render(f"{region_name}", True, (255, 255, 255))
            screen.blit(region_text, (100, y))
            y += 25  # Add space between region name and stats
            x = 300
            for stat, value in region_stats.items():
                icon = icons[stat]
                screen.blit(icon, (x, y))
                stat_text = font.render(f"{value}", True, (255, 255, 255))
                screen.blit(stat_text, (x + 40, y))
                x += 80
            y += 25
        y += 50

        # Draw buttons for trade and peace agreements
        trade_button = font.render("Trade Agreement", True, (255, 255, 255))
        peace_button = font.render("Peace Agreement", True, (255, 255, 255))
        war_button = font.render("Declare War", True, (255, 255, 255))
        trade_rect = screen.blit(trade_button, (50, y))
        peace_rect = screen.blit(peace_button, (250, y))
        war_rect = screen.blit(war_button, (450, y))
        buttons.append((trade_rect, "trade", nation_name))
        buttons.append((peace_rect, "peace", nation_name))
        buttons.append((war_rect, "war", nation_name))
        y += 50

    pygame.display.flip()
    return buttons

# Function to update other nations' stats
def update_nations_stats():
    for nation_data in nations.values():
        for region_stats in nation_data["regions"].values():
            for stat in region_stats:
                region_stats[stat] = random.randint(30, 70)

# Function to handle button clicks in foreign affairs
def handle_foreign_affairs_click(buttons, pos):
    for rect, action, nation_name in buttons:
        if rect.collidepoint(pos):
            if action == "trade":
                nations[nation_name]["trade_agreement"] = not nations[nation_name]["trade_agreement"]
            elif action == "peace":
                nations[nation_name]["peace_agreement"] = not nations[nation_name]["peace_agreement"]
            elif action == "war":
                nations[nation_name]["at_war"] = not nations[nation_name]["at_war"]
                if nations[nation_name]["at_war"]:
                    # Start war logic
                    pass
                else:
                    # End war logic
                    pass

# Function to draw the main menu tabs
def draw_main_menu():
    font = pygame.font.Font(None, 36)
    issues_tab = font.render("Issues", True, (255, 255, 255))
    foreign_affairs_tab = font.render("Foreign Affairs", True, (255, 255, 255))
    issues_rect = screen.blit(issues_tab, (50, 50))
    foreign_affairs_rect = screen.blit(foreign_affairs_tab, (250, 50))
    pygame.draw.line(screen, (192, 192, 192), (0, 90), (screen.get_width(), 90), 2)
    return issues_rect, foreign_affairs_rect

# Main game loop
running = True
buttons = []
used_events = []
current_region = random.choice(region_names)  # Initialize current_region
current_tab = "issues"  # Track the current tab

# Immediately trigger an event at the start
available_events = [event for event in events if event not in used_events]
current_event = random.choice(available_events)
used_events.append(current_event)
event_count += 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            issues_rect, foreign_affairs_rect = draw_main_menu()
            if issues_rect.collidepoint(event.pos):
                current_tab = "issues"
            elif foreign_affairs_rect.collidepoint(event.pos):
                current_tab = "foreign_affairs"
            elif current_tab == "foreign_affairs":
                handle_foreign_affairs_click(buttons, event.pos)
            elif current_event and current_tab == "issues":
                for rect, choice in buttons:
                    if rect.collidepoint(event.pos):
                        handle_choice(choice, current_region)

    # Check if any region's stat has reached zero
    if any(any(value <= 0 for value in region.values()) for region in regions.values()):
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
            current_region = random.choice(region_names)
            update_nations_stats()  # Update other nations' stats

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw main menu tabs
    issues_rect, foreign_affairs_rect = draw_main_menu()

    # Draw stat bars
    draw_stat_bars()

    # Display current event and choices
    if current_event and current_tab == "issues":
        font_title = pygame.font.Font(None, 48)
        font_description = pygame.font.Font(None, 36)
        title_text = font_title.render(current_event["title"], True, (255, 255, 255))
        description_text = font_description.render(current_event["description"], True, (192, 192, 192))
        region_text = font_description.render(f"Affected Region: {current_region}", True, region_colors[current_region])
        screen.blit(title_text, (50, 200))
        screen.blit(description_text, (50, 250))
        screen.blit(region_text, (20, 20))
        buttons = draw_buttons(current_event["choices"])

    # Handle foreign affairs tab
    if current_tab == "foreign_affairs":
        buttons = handle_foreign_affairs()

    pygame.display.flip()

pygame.quit()