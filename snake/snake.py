# Import pygame which makes it easy to create games by displaying graphics and handling user input 
import pygame
"""
For every pygame program, we follow this general structure:
initialize game
while running:
    handle input (keyboard, mouse, quit)
    update game objects (movement, collisions, score)
    draw everything (clear screen, draw shapes/images)
    control framerate
quit pygame
"""
import random # place food randomly

# Initialize pygame
pygame.init()

# Define colors used in game in RGB
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display size of game window
width = 600
height = 400

dis = pygame.display.set_mode((width, height)) # creates window
pygame.display.set_caption('Snake') # set title

clock = pygame.time.Clock() # controls game speed
snake_block = 20 # how big each segment of snake is
snake_speed = 15  # how fast the snake moves

# Fonts for displaying score and messages
font = pygame.font.SysFont("bahnschrift", 25) # default font
large_font = pygame.font.SysFont("comicsansms", 40) # larger font for messages 
score_font = pygame.font.SysFont("comicsansms", 30) # font for score display
press_font = pygame.font.SysFont("comicsansms", 20) # font for press key messages

# Function to display score
def your_score(score):
    # Renders the score on screen
    value = score_font.render(f"Score: {score}", True, white)
    # Draws score at (10,10)
    dis.blit(value, [10, 10])

# Function to draw snake in game
def our_snake(snake_block, snake_list):
    # Loop to draw each segment of the snake
    for x in snake_list:
        # Green square for each part
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# Function to display messages on screen
def message_centered(msg, color, y_offset=0):
    # Render message using larger font
    mesg = large_font.render(msg, True, color)
    # Get rectangle for text so we can center it
    text_rect = mesg.get_rect(center=(width / 2, height / 2 + y_offset))
    # Draw the text on the display
    dis.blit(mesg, text_rect)

# Game loop 
def gameLoop():
    # Declare variables for game state
    game_over = False # when game ends
    game_close = False # when player dies

    # Start in the middle 
    x1 = width / 2
    y1 = height / 2
    
    # Declare variables for movement
    x1_change = 0
    y1_change = 0

    # Declare snake list and initial length
    snake_List = [] # made of coordinates stored in a list
    Length_of_snake = 1

    # Place food randomly on (x,y)
    # Divide by 10 and multiply by 10 to align with snake block size
    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # Game loop until quit
    while not game_over:

        # When player dies
        while game_close:
            dis.fill(black) # fill screen with black
            message_centered("You Lost!", red, y_offset=-30)
            mesg = press_font.render("Press P to Play Again or Q to Quit", True, white)
            # get rectangle for text so we can center it
            text_rect = mesg.get_rect(center=(width / 2, height / 2 + 30))  # slightly below "You Lost!"
            dis.blit(mesg, text_rect)            
            your_score(Length_of_snake - 1) 
            pygame.display.update() # update display

            # Events after game over where player can quit or play again
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit
                        game_over = True 
                        game_close = False
                    if event.key == pygame.K_p: # play again
                        gameLoop() # we go back to start of game loop

        # Player controls
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                game_over = True
            # Movement
            if event.type == pygame.KEYDOWN:
                # event.key checks which key is pressed
                if event.key == pygame.K_LEFT: # pygame.K_LEFT is left arrow key
                    x1_change = -snake_block # move left
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block # move right
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block # move up
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block # move down
                    x1_change = 0

        # Wall collsion 
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True # player dies
        
        # Update position after key press
        x1 += x1_change
        y1 += y1_change

        # Drawing the game elements
        dis.fill(blue) # fill screen with blue
        # Draw food
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # Updates snake
        snake_Head = [x1, y1] 
        snake_List.append(snake_Head) # add new head to snake list
        if len(snake_List) > Length_of_snake: # if snake is longer than it should be
            del snake_List[0]  # remove tail segment

        # Check if snake collides with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True # player dies

        # Calls functions to draw snake and score
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        # Update display
        pygame.display.update()

        # If snake eats food
        if x1 == foodx and y1 == foody:
            # Place new food
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1 # increase length

        # Keeps game running at constant speed
        clock.tick(snake_speed)

    # Quit pygame and python
    pygame.quit()
    quit()
# Start the game at bottom since function definitions are above
gameLoop()
