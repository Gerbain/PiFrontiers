import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("Resource Gathering Game")

# Item size and gatherer speed
item_size = 20
gatherer_speed = 2  # Adjust this value to control speed

# Load and scale images for each tribe and their gatherers
tribe_imgs = [pygame.transform.scale(pygame.image.load(f'tribe{i}.png'), (item_size, item_size)) for i in range(1, 4)]
gatherer_imgs = [pygame.transform.scale(pygame.image.load(f'sword{i}.png'), (item_size, item_size)) for i in range(1, 4)]
resource_img = pygame.transform.scale(pygame.image.load('corn.png'), (item_size, item_size))

# Function to generate random resources with a usage count
def generate_resources(num_resources, uses_per_resource):
    resources = []
    for _ in range(num_resources):
        x = random.randint(0, width - item_size)
        y = random.randint(0, height - item_size)
        resources.append({'position': (x, y), 'uses': uses_per_resource})
    return resources

# Generate a list of resources
num_resources = 10  # Fewer resources
uses_per_resource = 5  # Number of times each resource can be used
resources = generate_resources(num_resources, uses_per_resource)

# Tribe class
class Tribe:
    def __init__(self, base_image, gatherer_image, base_position):
        self.base_image = base_image
        self.gatherer_image = gatherer_image
        self.base_position = base_position
        self.gatherers = [{'position': base_position, 'carrying_resource': False}]  # Initial gatherer at the base

    def add_gatherer(self, position):
        # Logic to add a new gatherer
        self.gatherers.append({'position': position, 'carrying_resource': False})

# Initialize tribes with their respective images
# Ensure each tribe starts with exactly one gatherer
tribes = [Tribe(tribe_imgs[i], gatherer_imgs[i], (50 + i * 300, 50)) for i in range(3)]

def move_gatherers():
    search_radius = 100  # Radius within which gatherers can detect resources

    for tribe in tribes:
        for gatherer in tribe.gatherers:
            gx, gy = gatherer['position']

            if gatherer['carrying_resource']:
                # Return to base
                dx, dy = tribe.base_position[0] - gx, tribe.base_position[1] - gy
                target_reached = tribe.base_position
            else:
                # Check for nearby resources
                nearby_resources = [r for r in resources if (r['position'][0] - gx)**2 + (r['position'][1] - gy)**2 < search_radius**2]
                if nearby_resources:
                    nearest_resource = min(nearby_resources, key=lambda r: (r['position'][0] - gx)**2 + (r['position'][1] - gy)**2)
                    dx, dy = nearest_resource['position'][0] - gx, nearest_resource['position'][1] - gy
                    target_reached = nearest_resource['position']
                else:
                    # Random movement
                    dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
                    target_reached = None

            # Normalize and apply speed
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                dx, dy = dx / distance * gatherer_speed, dy / distance * gatherer_speed

            # Update gatherer position
            gatherer['position'] = (gx + dx, gy + dy)

            # Check if gatherer reached the target
            if target_reached and distance < item_size:
                if gatherer['carrying_resource']:
                    # Deliver resource to base
                    gatherer['carrying_resource'] = False
                    tribe.add_gatherer(tribe.base_position)  # Add a new gatherer at the base
                else:
                    # Pick up resource
                    gatherer['carrying_resource'] = True
                    nearest_resource['uses'] -= 1
                    if nearest_resource['uses'] <= 0:
                        resources.remove(nearest_resource)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Move gatherers
    move_gatherers()

    # Draw resources
    for resource in resources:
        screen.blit(resource_img, resource['position'])

    # Draw tribes and gatherers
    for tribe in tribes:
        screen.blit(tribe.base_image, tribe.base_position)
        for gatherer in tribe.gatherers:
            screen.blit(tribe.gatherer_image, gatherer['position'])
            if gatherer['carrying_resource']:
                # Draw resource image with 10px offset
                screen.blit(resource_img, (gatherer['position'][0] + 10, gatherer['position'][1] + 10))

    # Update the display
    pygame.display.update()
