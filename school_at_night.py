import pygame as py
import math
import winsound

NASA = int(input('?'))

# Initialize Pygame
py.init()
filename = 'bluee.wav'
winsound.PlaySound(filename, winsound.SND_FILENAME)

# Screen setup
screen_width, screen_height = 1920, 1080
screen = py.display.set_mode((screen_width, screen_height), py.FULLSCREEN)
py.display.set_caption('.::SAN::.')
icon = py.image.load('icon.png')
py.display.set_icon(icon)

# Colors
GREEN = (0, 204, 0)

# Load map
map_img = py.image.load('map.png')  # Add a large map image (e.g., 2000x2000 pixels)
map_width, map_height = map_img.get_size()

# Player setup
player_img = py.image.load('player.png')  # Add a player image (e.g., 32x32 pixels)
player_x = map_width // 2
player_y = map_height // 2
player_speed = 1.25
player_angle = 0

# Camera setup
camera_x = 0
camera_y = 0

# Obstacles
obstacles = [
    py.Rect(1650, 1210, 600, 600),  # Example obstacle (x, y, width, height)
    py.Rect(1650, 430, 600, 600),
    py.Rect(860, 430, 625, 610),
    py.Rect(860, 1210, 600, 600)
]

# Bullets setup
bullets = []
bullet_speed = 10

# Zombie setup
zombies = []
zombie_speed = 0.1
spawn_points = [
    (0, 0),  # Example spawn point 1
    (00, 000),  # Example spawn point 2
    (000, 00),  # Example spawn point 3
    (000, 000)  # Example spawn point 4
]

# Function to spawn zombies
def spawn_zombies():
    for spawn_point in spawn_points:
        zombies.append({
            "x": spawn_point[0],
            "y": spawn_point[1],
            "angle": 0
        })

# Call the spawn function at the start
spawn_zombies()

# Game loop
run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            # Get mouse position
            mouse_x, mouse_y = py.mouse.get_pos()
            # Calculate direction
            rel_x, rel_y = mouse_x - screen_width // 2, mouse_y - screen_height // 2
            angle = math.atan2(-rel_y, rel_x)
            # Add bullet to the list
            bullets.append({
                "x": player_x,
                "y": player_y,
                "angle": angle
            })
    # Movement keys
    keys = py.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[py.K_ESCAPE]:
        run = False
    if NASA == 1:
        if keys[py.K_LEFT]:
            new_x -= player_speed
        if keys[py.K_RIGHT]:
            new_x += player_speed
        if keys[py.K_UP]:
            new_y -= player_speed
        if keys[py.K_DOWN]:
            new_y += player_speed
    if NASA == 2:
        if keys[py.K_a]:
            new_x -= player_speed
        if keys[py.K_d]:
            new_x += player_speed
        if keys[py.K_w]:
            new_y -= player_speed
        if keys[py.K_s]:
            new_y += player_speed

    # Create a Rect for the player's new position برخورد موانع
    player_rect = py.Rect(new_x, new_y, player_img.get_width(), player_img.get_height())

    # Check for collisions
    collision = False
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            collision = True
            break

    # Update position if no collision
    if not collision:
        player_x, player_y = new_x, new_y

    # Update camera position
    camera_x = player_x - screen_width // 2
    camera_y = player_y - screen_height // 2

    # Clamp camera to map boundaries
    camera_x = max(0, min(camera_x, map_width - screen_width))
    camera_y = max(0, min(camera_y, map_height - screen_height))

    # Get mouse position and calculate angle
    mouse_x, mouse_y = py.mouse.get_pos()
    rel_x, rel_y = mouse_x - screen_width // 2, mouse_y - screen_height // 2
    player_angle = math.degrees(math.atan2(rel_y, rel_x))  # Calculate angle in degrees

    # Rotate the player image
    rotated_player_img = py.transform.rotate(player_img, -player_angle)

    # Move bullets
    for bullet in bullets:
        bullet["x"] += bullet_speed * math.cos(bullet["angle"])
        bullet["y"] -= bullet_speed * math.sin(bullet["angle"])

    # Move zombies
    for zombie in zombies:
        # Calculate direction towards the center of the map
        rel_x, rel_y = map_width // 2 - zombie["x"], map_height // 2 - zombie["y"]
        zombie["angle"] = math.atan2(rel_y, rel_x)

        # Move zombie towards the center
        zombie["x"] += zombie_speed * math.cos(zombie["angle"])
        zombie["y"] += zombie_speed * math.sin(zombie["angle"])

        # Draw zombie
        zombie_screen_x = zombie["x"] - camera_x
        zombie_screen_y = zombie["y"] - camera_y
        py.draw.circle(screen, (255, 0, 0), (int(zombie_screen_x), int(zombie_screen_y)), 15)  # Draw zombie as a red circle

    # Drawing
    screen.fill(GREEN)  # Background
    screen.blit(map_img, (-camera_x, -camera_y))  # Draw map
    screen.blit(rotated_player_img, (screen_width // 2 - rotated_player_img.get_width() // 2,
                                     screen_height // 2 - rotated_player_img.get_height() // 2))  # Draw rotated player

    # Draw bullets
    for bullet in bullets:
        bullet_screen_x = bullet["x"] - camera_x
        bullet_screen_y = bullet["y"] - camera_y
        py.draw.circle(screen, (255, 0, 0), (screen_width // 2, screen_height // 2), 15)
        for zombie in zombies:
            print(f"Zombie spawned at: x={zombie['x']}, y={zombie['y']}")

    py.display.update()
py.quit()