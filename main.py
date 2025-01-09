import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -10
FPS = 60
BIRD_COLOR = (255, 255, 0)  # Yellow

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define fonts
font = pygame.font.SysFont('Arial', 30)

# Define game variables
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
pipes = []
score = 0

# Define clock for FPS control
clock = pygame.time.Clock()

def add_pipe():
    """Add a new pipe pair."""
    pipe_height = random.randint(100, 400)
    pipes.append([SCREEN_WIDTH, pipe_height])

def draw_pipes():
    """Draw all pipes on the screen."""
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), (pipe[0], 0, PIPE_WIDTH, pipe[1]))  # Top pipe
        pygame.draw.rect(screen, (0, 255, 0), (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - pipe[1] - PIPE_GAP))  # Bottom pipe

def move_pipes():
    """Move the pipes and remove the ones that go out of the screen."""
    global score
    for pipe in pipes:
        pipe[0] -= 5  # Move pipes to the left
    if pipes and pipes[0][0] < 0:
        pipes.pop(0)  # Remove the pipe when it's out of screen
        score += 1  # Increment score for every passed pipe

def check_collision():
    """Check if the bird collides with pipes or the ground."""
    global bird_y
    # Check if the bird hits the ground or the ceiling
    if bird_y <= 0 or bird_y >= SCREEN_HEIGHT:
        return True

    # Check if the bird hits any pipes
    for pipe in pipes:
        if pipe[0] < bird_x + BIRD_WIDTH and pipe[0] + PIPE_WIDTH > bird_x:
            if bird_y < pipe[1] or bird_y > pipe[1] + PIPE_GAP:
                return True
    return False

def draw_bird():
    """Draw the bird on the screen."""
    pygame.draw.rect(screen, BIRD_COLOR, (bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT))

def draw_score():
    """Display the score on the screen."""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

def reset_game():
    """Reset the game variables."""
    global bird_y, bird_velocity, pipes, score
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0

# Main game loop
running = True
while running:
    screen.fill((0, 0, 255))  # Fill the screen with a blue background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Spacebar to make the bird jump
                bird_velocity = JUMP_STRENGTH

    # Move the bird
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Move pipes and add new ones
    move_pipes()
    if not pipes or pipes[-1][0] < SCREEN_WIDTH - 200:
        add_pipe()

    # Check for collisions
    if check_collision():
        reset_game()  # Reset the game if there's a collision

    # Draw everything
    draw_pipes()
    draw_bird()
    draw_score()

    # Update the display
    pygame.display.update()

    # Control FPS
    clock.tick(FPS)

# Quit pygame
pygame.quit()
