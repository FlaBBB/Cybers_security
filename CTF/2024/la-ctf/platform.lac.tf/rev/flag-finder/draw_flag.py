import sys

import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Draw Sprite Lines")


# Function to draw a line on the screen
def draw_sprite_line(screen, sprite_index, thickness, start_x, start_y, end_x, end_y):
    # Draw a line on the screen using pygame
    pygame.draw.line(
        screen, sprite_index, (start_x, start_y), (end_x, end_y), thickness
    )


# Main loop
def main():
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Example usage of draw_sprite_line function
        draw_sprite_line(screen, 60, 1, 20, 20, 20, 60)
        draw_sprite_line(screen, 60, 1, 20, 55, 60, 55)
        draw_sprite_line(screen, 60, 1, 70, 20, 70, 60)
        draw_sprite_line(screen, 60, 1, 70, 20, 105, 20)
        draw_sprite_line(screen, 60, 1, 105, 20, 105, 60)
        draw_sprite_line(screen, 60, 1, 70, 35, 105, 35)
        draw_sprite_line(screen, 60, 1, 115, 20, 115, 60)
        draw_sprite_line(screen, 60, 1, 115, 20, 160, 20)
        draw_sprite_line(screen, 60, 1, 115, 55, 160, 55)
        draw_sprite_line(screen, 60, 1, 170, 20, 210, 20)
        draw_sprite_line(screen, 60, 1, 190, 20, 190, 60)
        draw_sprite_line(screen, 60, 1, 220, 20, 220, 60)
        draw_sprite_line(screen, 60, 1, 220, 20, 260, 20)
        draw_sprite_line(screen, 60, 1, 220, 35, 250, 35)
        draw_sprite_line(screen, 60, 1, 275, 20, 285, 20)
        draw_sprite_line(screen, 60, 1, 275, 20, 275, 35)
        draw_sprite_line(screen, 60, 1, 275, 35, 270, 45)
        draw_sprite_line(screen, 60, 1, 270, 45, 275, 55)
        draw_sprite_line(screen, 60, 1, 275, 55, 275, 70)
        draw_sprite_line(screen, 60, 1, 275, 65, 285, 65)
        draw_sprite_line(screen, 60, 1, 295, 20, 295, 60)
        draw_sprite_line(screen, 60, 1, 295, 40, 325, 60)
        draw_sprite_line(screen, 60, 1, 295, 40, 325, 20)
        draw_sprite_line(screen, 60, 1, 335, 20, 375, 20)
        draw_sprite_line(screen, 60, 1, 335, 35, 375, 35)
        draw_sprite_line(screen, 60, 1, 335, 55, 375, 55)
        draw_sprite_line(screen, 60, 1, 375, 20, 375, 55)
        draw_sprite_line(screen, 60, 1, 385, 20, 415, 35)
        draw_sprite_line(screen, 60, 1, 415, 35, 445, 20)
        draw_sprite_line(screen, 60, 1, 415, 35, 415, 60)
        draw_sprite_line(screen, 60, 1, 455, 60, 500, 60)
        draw_sprite_line(screen, 60, 1, 510, 20, 550, 20)
        draw_sprite_line(screen, 60, 1, 530, 20, 530, 60)
        draw_sprite_line(screen, 60, 1, 560, 20, 600, 20)
        draw_sprite_line(screen, 60, 1, 560, 55, 600, 55)
        draw_sprite_line(screen, 60, 1, 560, 20, 560, 55)
        draw_sprite_line(screen, 60, 1, 600, 20, 600, 55)
        draw_sprite_line(screen, 60, 1, 610, 60, 650, 60)
        draw_sprite_line(screen, 60, 1, 660, 20, 660, 60)
        draw_sprite_line(screen, 60, 1, 660, 20, 690, 35)
        draw_sprite_line(screen, 60, 1, 685, 35, 715, 20)
        draw_sprite_line(screen, 60, 1, 715, 20, 715, 60)
        draw_sprite_line(screen, 60, 1, 725, 20, 755, 35)
        draw_sprite_line(screen, 60, 1, 755, 35, 775, 20)
        draw_sprite_line(screen, 60, 1, 755, 35, 755, 60)
        draw_sprite_line(screen, 60, 1, 765, 60, 800, 60)
        draw_sprite_line(screen, 60, 1, 810, 20, 810, 60)
        draw_sprite_line(screen, 60, 1, 810, 35, 860, 35)
        draw_sprite_line(screen, 60, 1, 860, 20, 860, 60)
        draw_sprite_line(screen, 60, 1, 870, 20, 910, 20)
        draw_sprite_line(screen, 60, 1, 870, 35, 910, 35)
        draw_sprite_line(screen, 60, 1, 870, 55, 910, 55)
        draw_sprite_line(screen, 60, 1, 910, 20, 910, 55)
        draw_sprite_line(screen, 60, 1, 920, 35, 965, 35)
        draw_sprite_line(screen, 60, 1, 920, 35, 960, 20)
        draw_sprite_line(screen, 60, 1, 960, 20, 960, 60)
        draw_sprite_line(screen, 60, 1, 975, 20, 975, 60)
        draw_sprite_line(screen, 60, 1, 975, 20, 1020, 20)
        draw_sprite_line(screen, 60, 1, 1015, 20, 1015, 35)
        draw_sprite_line(screen, 60, 1, 975, 35, 1020, 35)
        draw_sprite_line(screen, 60, 1, 980, 35, 1020, 60)
        draw_sprite_line(screen, 60, 1, 1030, 20, 1070, 20)
        draw_sprite_line(screen, 60, 1, 1050, 20, 1050, 60)
        draw_sprite_line(screen, 60, 1, 1080, 20, 1095, 20)
        draw_sprite_line(screen, 60, 1, 1095, 20, 1095, 35)
        draw_sprite_line(screen, 60, 1, 1095, 35, 1100, 45)
        draw_sprite_line(screen, 60, 1, 1100, 45, 1095, 55)
        draw_sprite_line(screen, 60, 1, 1095, 55, 1095, 70)
        draw_sprite_line(screen, 60, 1, 1095, 70, 1080, 70)
        # Add more draw_sprite_line calls here for additional lines

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
