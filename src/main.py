import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Define constants for screen dimensions
WIDTH, HEIGHT = 600, 650  # Increase HEIGHT to allow space below the board
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE


# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 30

# Wall orientation constants
HORIZONTAL = 'H'
VERTICAL = 'V'

WHITE = (252, 250, 250)
BLACK = (0, 0, 0)
GRAY = (212, 235, 248)
RED = (184, 0, 31)
BACKGROUND = (56, 75, 112)  # #384B70
GRID_LINES = (80, 118, 135)  # #507687
PLAYER_USER = "#B8001F"  # #B8001F
PLAYER_BOT = "#FFC55A"  #1F509A
TEXT_COLOR = BACKGROUND
WALL_COLOR = (227, 142, 73)  # #E38E49
INTERFACE_BACKGROUND = "#141E46" # Slightly lighter than BACKGROUND
POPUP_BACKGROUND = (70, 85, 110)  # A touch lighter than INTERFACE_BACKGROUND
POPUP_BORDER = (120, 140, 180)
ORANGE = (227, 142, 73)
BUTTON_COLOR = "#9b9b9b"
BUTTON_HOVER_COLOR = "#797979"
BUTTON_TEXT_COLOR = (255, 255, 255)


def draw_start_screen():
    """Draw the start screen with a play button and an image."""
    screen.fill("#faf9f4")

    # Load and position the image
    image = pygame.image.load("../assets/quoridor.png")   # Replace with your image file path
    image_x = (WIDTH - image.get_width()) // 2
    image_y = (HEIGHT - 600)  # Position above the button
    screen.blit(image, (image_x, image_y))

    # Button dimensions and position
    button_width, button_height = 200, 80
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - 125)

    # Mouse hover effect and cursor change
    mouse_pos = pygame.mouse.get_pos()
    if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
        button_color = BUTTON_HOVER_COLOR
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change cursor to hand
    else:
        button_color = BUTTON_COLOR
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor to default arrow

    # Draw button
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 3, border_radius=10)

    # Draw button text
    font = pygame.font.Font(None, 50)
    play_text = font.render("Play", True, BUTTON_TEXT_COLOR)
    text_rect = play_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(play_text, text_rect)

    pygame.display.flip()
    return button_x, button_y, button_width, button_height


def draw_board():
    """Draw the game board and grid with dark mode colors."""
    pygame.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, WIDTH))
    for x in range(GRID_SIZE):
        pygame.draw.line(screen, GRID_LINES, (x * CELL_SIZE, 0), (x * CELL_SIZE, WIDTH), 2)
        pygame.draw.line(screen, GRID_LINES, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), 2)
    pygame.draw.line(screen, GRID_LINES, (0, WIDTH), (WIDTH, WIDTH), 4)

def draw_interface_background():
    """Draw the interface area below the board with dark mode colors."""
    pygame.draw.rect(screen, GRAY, (0, WIDTH, WIDTH, HEIGHT - WIDTH))

def draw_players(player_positions):
    """Draw the players with specified colors for dark mode."""
    for i, pos in enumerate(player_positions):
        color = PLAYER_USER if i == 0 else PLAYER_BOT
        x, y = pos
        pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def draw_walls(walls):
    """Draw walls with dark mode styling."""
    for wall in walls:
        x, y, orientation = wall
        if orientation == HORIZONTAL:
            pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE - CELL_SIZE // 8, CELL_SIZE * 2, CELL_SIZE // 4))
        elif orientation == VERTICAL:
            pygame.draw.rect(screen, WHITE, (x * CELL_SIZE - CELL_SIZE // 8, y * CELL_SIZE, CELL_SIZE // 4, CELL_SIZE * 2))

def draw_popup(message):
    """Draw a popup window with a dark mode style."""
    popup_width, popup_height = 300, 150
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    pygame.draw.rect(screen, POPUP_BACKGROUND, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, POPUP_BORDER, (popup_x, popup_y, popup_width, popup_height), 3)
    close_button_x = popup_x + popup_width - 30
    close_button_y = popup_y + 10
    pygame.draw.rect(screen, PLAYER_USER, (close_button_x, close_button_y, 20, 20))
    pygame.draw.line(screen, TEXT_COLOR, (close_button_x + 5, close_button_y + 5), (close_button_x + 15, close_button_y + 15), 3)
    pygame.draw.line(screen, TEXT_COLOR, (close_button_x + 15, close_button_y + 5), (close_button_x + 5, close_button_y + 15), 3)
    font = pygame.font.Font(None, 24)
    text_surface = font.render(message, True, TEXT_COLOR)
    text_x = popup_x + (popup_width - text_surface.get_width()) // 2
    text_y = popup_y + (popup_height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))


def is_popup_close_clicked(mouse_pos):
    """Check if the close button on the popup was clicked."""
    popup_width, popup_height = 300, 150
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    close_button_x = popup_x + popup_width - 30
    close_button_y = popup_y + 10
    close_button_rect = pygame.Rect(close_button_x, close_button_y, 20, 20)
    return close_button_rect.collidepoint(mouse_pos)


def display_message(message):
    """Display endgame messages with dark mode colors."""
    font = pygame.font.Font(None, 60)
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BACKGROUND)
    screen.blit(text, text_rect)
    pygame.display.flip()

def draw_interface_text(user_walls_remaining, bot_walls_remaining, message=None):
    """Draw the user interface text for remaining walls and messages."""
    font = pygame.font.Font(None, 28)
    user_text = font.render(f"User Walls: {user_walls_remaining}", True, TEXT_COLOR)
    bot_text = font.render(f"Bot Walls: {bot_walls_remaining}", True, TEXT_COLOR)
    screen.blit(user_text, (10, WIDTH + 10))
    screen.blit(bot_text, (WIDTH - 160, WIDTH + 10))

    if message:
        feedback_font = pygame.font.Font(None, 24)
        feedback_text = feedback_font.render(message, True, PLAYER_USER)
        screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, WIDTH + 50))


def is_wall_blocking_move(position, move, walls):
    """
    Check if a wall is blocking the move.

    Parameters:
    - position: (x, y) - current position of the player.
    - move: (move_x, move_y) - target position after the move.
    - walls: List of walls with each wall as (x, y, orientation).

    Returns:
    - True if a wall blocks the move, False otherwise.
    """
    x, y = position
    move_x, move_y = move

    # Check for horizontal walls blocking upward or downward movement
    if move_y < y:  # Moving up
        for wall_x, wall_y, orientation in walls:
            if orientation == HORIZONTAL and wall_y == y and (wall_x == x or wall_x == x - 1):
                return True
    if move_y > y:  # Moving down
        for wall_x, wall_y, orientation in walls:
            if orientation == HORIZONTAL and wall_y == y + 1 and (wall_x == x or wall_x == x - 1):
                return True

    # Check for vertical walls blocking left or right movement
    if move_x < x:  # Moving left
        for wall_x, wall_y, orientation in walls:
            if orientation == VERTICAL and wall_x == x and (wall_y == y or wall_y == y - 1):
                return True
    if move_x > x:  # Moving right
        for wall_x, wall_y, orientation in walls:
            if orientation == VERTICAL and wall_x == x + 1 and (wall_y == y or wall_y == y - 1):
                return True

    return False


def bot_move(bot_position, user_position, walls, history):
    """
    Determine the bot's next move towards its goal, considering walls and user position.

    Parameters:
    - bot_position: (x, y) tuple representing the bot's current position.
    - user_position: (x, y) tuple representing the user's current position.
    - walls: List of wall positions [(wall_x, wall_y, orientation)].
    - history: Set of previously visited positions to avoid oscillation.

    Returns:
    - (move_x, move_y): The bot's next position.
    """
    x, y = bot_position
    goal_y = 0  # Bot's goal is to reach any cell at y = 0 (user's side)
    possible_moves = []

    # Add all valid moves, ensuring they respect walls and grid boundaries
    for move_x, move_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
        if 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE and \
           not is_wall_blocking_move((x, y), (move_x, move_y), walls) and \
           (move_x, move_y) not in history:
            possible_moves.append((move_x, move_y))

    # If there are valid moves, choose the one that minimizes the path length to the goal
    if possible_moves:
        best_move = min(possible_moves, key=lambda pos: shortest_path_length(pos, goal_y, walls))
        history.add(best_move)
        return best_move

    return bot_position   # No move if no possible moves


def handle_user_move_or_wall(player_positions, walls, event, user_walls_remaining):
    """
    Handles user moves or wall placement based on keyboard input.

    Parameters:
    - player_positions: list of player positions [(user_x, user_y), (bot_x, bot_y)].
    - walls: list of wall positions [(wall_x, wall_y, orientation)].
    - event: pygame event for user input.
    - user_walls_remaining: Number of walls the user has left.

    Returns:
    - move_made: True if a valid move or wall placement was made, False otherwise.
    - user_walls_remaining: Updated wall count for the user.
    - move_message: Feedback message for invalid moves or wall placements.
    """
    x, y = player_positions[0]  # User position
    bot_x, bot_y = player_positions[1]  # Bot position
    move_made = False
    move_message = ""

    # Movement logic
    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
        target_position = None

        if event.key == pygame.K_UP:  # Move up
            target_position = (x, y - 1)
        elif event.key == pygame.K_DOWN:  # Move down
            target_position = (x, y + 1)
        elif event.key == pygame.K_LEFT:  # Move left
            target_position = (x - 1, y)
        elif event.key == pygame.K_RIGHT:  # Move right
            target_position = (x + 1, y)

        if target_position:
            move_x, move_y = target_position

            # Check for jumping over the bot
            if (move_x, move_y) == (bot_x, bot_y):
                # Jump logic
                jump_x, jump_y = bot_x + (bot_x - x), bot_y + (bot_y - y)
                if 0 <= jump_x < GRID_SIZE and 0 <= jump_y < GRID_SIZE and \
                   not is_wall_blocking_move((bot_x, bot_y), (jump_x, jump_y), walls):
                    player_positions[0] = (jump_x, jump_y)
                    move_made = True
                else:
                    move_message = "Jump blocked by a wall or out of bounds!"
            elif 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE:
                # Normal movement
                if not is_wall_blocking_move((x, y), target_position, walls):
                    player_positions[0] = target_position
                    move_made = True
                else:
                    move_message = "Move blocked by a wall!"
            else:
                move_message = "Move out of bounds!"

    return move_made, user_walls_remaining, move_message


def causes_overlap(new_wall, walls):
    """
    Check if the new wall causes improper overlap, crossing, or intersection in the middle.
    Optimized to avoid redundant checks.
    """
    x, y, orientation = new_wall

    for wall_x, wall_y, wall_orientation in walls:
        if orientation == HORIZONTAL:
            # Overlapping horizontal walls
            if wall_orientation == HORIZONTAL and wall_y == y and abs(wall_x - x) <= 1:
                return True
            # Crossing a vertical wall
            if wall_orientation == VERTICAL and wall_x == x + 1 and wall_y == y - 1:
                return True
        elif orientation == VERTICAL:
            # Overlapping vertical walls
            if wall_orientation == VERTICAL and wall_x == x and abs(wall_y - y) <= 1:
                return True
            # Crossing a horizontal wall
            if wall_orientation == HORIZONTAL and wall_y == y + 1 and wall_x == x - 1:
                return True

    return False



def is_path_open(player_position, goal_y, walls):
    """Check if there is still a valid path to the goal."""
    from collections import deque

    visited = set()
    queue = deque([player_position])

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Check if the player reached the goal row
        if y == goal_y:
            return True

        # Add valid moves to the queue
        for move_x, move_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE and \
               not is_wall_blocking_move((x, y), (move_x, move_y), walls) and \
               (move_x, move_y) not in visited:
                queue.append((move_x, move_y))

    return False


def draw_preview_wall(preview_wall, walls):
    """Draw a visually distinct preview wall."""
    x, y, orientation = preview_wall['x'], preview_wall['y'], preview_wall['orientation']

    # Use red color for invalid placement, otherwise light gray
    color = (255, 0, 0) if preview_wall.get('invalid', False) else "#96C9F4"  # Red or light gray

    if orientation == HORIZONTAL:
        pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE - CELL_SIZE // 8, CELL_SIZE * 2, CELL_SIZE // 4))
    elif orientation == VERTICAL:
        pygame.draw.rect(screen, color, (x * CELL_SIZE - CELL_SIZE // 8, y * CELL_SIZE, CELL_SIZE // 4, CELL_SIZE * 2))


def handle_preview_wall_input(preview_wall, event, walls, player_positions, user_walls_remaining):
    """
    Handle preview wall input, ensuring valid placement and no boundary violations.
    """
    x, y, orientation = preview_wall['x'], preview_wall['y'], preview_wall['orientation']

    if event.key == pygame.K_SPACE:  # Toggle orientation
        if orientation == HORIZONTAL:
            # Switching to vertical
            preview_wall['orientation'] = VERTICAL
            if x == 0:  # If on the left border, move to the first valid column
                preview_wall['x'] = 1
            if x == GRID_SIZE - 2:
                preview_wall['x'] = GRID_SIZE - 1

            if y == GRID_SIZE - 1:
                preview_wall['y'] = GRID_SIZE - 2
            elif y == 1:
                preview_wall['y'] = 0

        elif orientation == VERTICAL:
            # Switching to horizontal
            preview_wall['orientation'] = HORIZONTAL
            if y == GRID_SIZE - 2:  # If endpoint is at the bottom border
                preview_wall['y'] = GRID_SIZE - 1  # Move to the first valid row from the bottom
            elif y == 0:  # If at the top border
                preview_wall['y'] = 1  # Move to the first valid row from the top

            if x == GRID_SIZE - 1:  # If endpoint is at the right border
                preview_wall['x'] = GRID_SIZE - 2  # Move to the first valid column from the right
            elif x == 1:
                preview_wall['x'] = 0  # Move to the first valid column from the right

    elif event.key == pygame.K_UP:  # Move up
        if orientation == HORIZONTAL:
            preview_wall['y'] = max(1, y - 1)  # Horizontal walls cannot be on the top border
        else:
            preview_wall['y'] = max(0, y - 1)  # Vertical walls can extend up to the topmost row

    elif event.key == pygame.K_DOWN:  # Move down
        if orientation == HORIZONTAL:
            preview_wall['y'] = min(GRID_SIZE - 1, y + 1)  # Horizontal walls cannot end on the bottom border
        else:
            preview_wall['y'] = min(GRID_SIZE - 2, y + 1)  # Vertical walls must fully fit before the bottom border

    elif event.key == pygame.K_LEFT:  # Move left
        if orientation == VERTICAL:
            preview_wall['x'] = max(1, x - 1)  # Vertical walls cannot be on the left border
        else:
            preview_wall['x'] = max(0, x - 1)  # Horizontal walls can start at the leftmost column

    elif event.key == pygame.K_RIGHT:  # Move right
        if orientation == VERTICAL:
            preview_wall['x'] = min(GRID_SIZE - 1, x + 1)  # Vertical walls cannot end on the right border
        else:
            preview_wall['x'] = min(GRID_SIZE - 2, x + 1)  # Horizontal walls must fully fit before the right border

    elif event.key == pygame.K_RETURN:  # Confirm placement
        new_wall = (x, y, orientation)

        # Check if wall placement is valid
        if user_walls_remaining <= 0:
            preview_wall['invalid'] = True
            pygame.time.set_timer(pygame.USEREVENT, 500)  # Reset invalid state timer

        elif new_wall in walls:
            preview_wall['invalid'] = True
            pygame.time.set_timer(pygame.USEREVENT, 500)

        elif causes_overlap(new_wall, walls):
            preview_wall['invalid'] = True
            pygame.time.set_timer(pygame.USEREVENT, 500)

        elif not is_path_open(player_positions[0], GRID_SIZE - 1, walls + [new_wall]):
            preview_wall['invalid'] = True
            pygame.time.set_timer(pygame.USEREVENT, 500)

        elif not is_path_open(player_positions[1], 0, walls + [new_wall]):
            preview_wall['invalid'] = True
            pygame.time.set_timer(pygame.USEREVENT, 500)

        else:
            # Valid placement
            walls.append(new_wall)
            user_walls_remaining -= 1
            preview_wall['active'] = False  # Exit placement mode
            preview_wall['invalid'] = False  # Reset invalid state
            return True, user_walls_remaining  # Valid move

    return False, user_walls_remaining  # Invalid move or no move


def evaluate_board(player_positions, user_last_position, walls, bot_walls_remaining, user_walls_remaining):
    """
    Evaluate the game state for the bot.
    """
    user_position, bot_position = player_positions

    # Calculate shortest paths
    user_distance = shortest_path_length(user_position, GRID_SIZE - 1, walls)
    bot_distance = shortest_path_length(bot_position, 0, walls)

    # Wall advantage
    wall_advantage = bot_walls_remaining - user_walls_remaining

    # Choke point proximity
    choke_points = find_choke_points(player_positions, user_last_position, walls)
    choke_score = len(choke_points)

    # Scoring formula
    return (10 * bot_distance) - (15 * user_distance) + (2 * wall_advantage) + (5 * choke_score)


def minimax(player_positions, walls, depth, alpha, beta, maximizing_player, bot_walls_remaining, user_walls_remaining,
            user_last_position):
    """
    Minimax algorithm with Alpha-Beta Pruning for both moves and wall placements.

    Parameters:
    - player_positions: List of player positions [(user_x, user_y), (bot_x, bot_y)].
    - walls: List of currently placed walls.
    - depth: Current depth of the Minimax recursion.
    - alpha: Alpha value for pruning.
    - beta: Beta value for pruning.
    - maximizing_player: Boolean indicating whether it's the bot's turn.
    - bot_walls_remaining: Number of walls the bot has left.
    - user_walls_remaining: Number of walls the user has left.
    - user_last_position: Last position of the user (x, y).

    Returns:
    - The best score from the evaluated actions.
    """
    if depth == 0 or game_over(player_positions):
        return evaluate_board(player_positions, user_last_position, walls, bot_walls_remaining, user_walls_remaining)

    if maximizing_player:  # Bot's turn
        max_eval = float('-inf')

        # Get all possible bot actions
        bot_position = player_positions[1]
        user_position = player_positions[0]
        possible_actions = get_all_possible_bot_actions(
            bot_position, walls, bot_walls_remaining, user_position, user_last_position
        )

        for action in possible_actions:
            # Apply the action
            new_positions, new_walls, new_bot_walls_remaining, new_user_walls_remaining = apply_action(
                player_positions, walls, action, is_bot=True, bot_walls_remaining=bot_walls_remaining,
                user_walls_remaining=user_walls_remaining
            )

            # Recursively call Minimax
            eval = minimax(
                new_positions,
                new_walls,
                depth - 1,
                alpha,
                beta,
                False,  # Switch to minimizing player
                new_bot_walls_remaining,
                new_user_walls_remaining,
                user_last_position  # Pass user_last_position unchanged
            )
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:  # User's turn
        min_eval = float('inf')

        # Get all possible user actions
        user_position = player_positions[0]
        bot_position = player_positions[1]
        possible_actions = get_all_possible_bot_actions(
            user_position, walls, user_walls_remaining, bot_position, user_last_position
        )

        for action in possible_actions:
            # Apply the action
            new_positions, new_walls, new_bot_walls_remaining, new_user_walls_remaining = apply_action(
                player_positions, walls, action, is_bot=False, bot_walls_remaining=bot_walls_remaining,
                user_walls_remaining=user_walls_remaining
            )

            # Recursively call Minimax
            eval = minimax(
                new_positions,
                new_walls,
                depth - 1,
                alpha,
                beta,
                True,  # Switch to maximizing player
                new_bot_walls_remaining,
                new_user_walls_remaining,
                user_last_position  # Pass user_last_position unchanged
            )
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def shortest_path_length(start, goal_y, walls):
    """
    Calculate the shortest path length from a position to the goal row using BFS.

    Parameters:
    - start: (x, y) tuple for the starting position.
    - goal_y: Integer for the target row (0 or GRID_SIZE - 1).
    - walls: List of wall positions.

    Returns:
    - Length of the shortest path to the goal row.
    """
    queue = deque([(start, 0)])  # (position, distance)
    visited = set()

    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Check if the goal row is reached
        if y == goal_y:
            return dist

        # Add valid moves to the queue, considering walls
        for move_x, move_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE and \
               not is_wall_blocking_move((x, y), (move_x, move_y), walls) and \
               (move_x, move_y) not in visited:
                queue.append(((move_x, move_y), dist + 1))

    # If no path is found, return a large value
    return float('inf')


def get_all_possible_moves(position, walls):
    """
    Generate all valid moves for a player based on the current position and wall placements.

    Parameters:
    - position: (x, y) tuple for the player's current position.
    - walls: List of wall positions.

    Returns:
    - List of valid (x, y) positions.
    """
    x, y = position
    possible_moves = []

    # Check all potential directions
    for move_x, move_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
        if 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE and \
           not is_wall_blocking_move((x, y), (move_x, move_y), walls):
            possible_moves.append((move_x, move_y))

    return possible_moves

def game_over(player_positions):
    """
    Check if the game is over.

    Parameters:
    - player_positions: List of player positions [(user_x, user_y), (bot_x, bot_y)].

    Returns:
    - True if either player has reached their goal, False otherwise.
    """
    user_position, bot_position = player_positions
    return user_position[1] == GRID_SIZE - 1 or bot_position[1] == 0


def calculate_shortest_path(start, goal_y, walls):
    """
    Calculate the shortest path from a position to the goal row using BFS.

    Parameters:
    - start: (x, y) tuple for the starting position.
    - goal_y: Integer for the target row (0 or GRID_SIZE - 1).
    - walls: List of wall positions.

    Returns:
    - List of positions representing the shortest path to the goal row.
    """
    queue = deque([(start, [])])  # (current position, path taken)
    visited = set()

    while queue:
        current, path = queue.popleft()
        x, y = current

        if current in visited:
            continue
        visited.add(current)

        # Check if the goal row is reached
        if y == goal_y:
            return path + [current]

        # Add valid moves to the queue
        for move_x, move_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= move_x < GRID_SIZE and 0 <= move_y < GRID_SIZE and \
               not is_wall_blocking_move((x, y), (move_x, move_y), walls) and \
               (move_x, move_y) not in visited:
                queue.append(((move_x, move_y), path + [current]))

    return []  # No path found


def find_choke_points(player_positions, user_last_position, walls):
    """
    Analyze choke points to prioritize placing a front wall for the bot first.
    Validate that walls do not block paths for both players.

    Parameters:
    - player_positions: List of current player positions [(user_x, user_y), (bot_x, bot_y)].
    - user_last_position: Last position of the user (x, y).
    - walls: List of currently placed walls.

    Returns:
    - List of choke points to block the user's path.
    """
    choke_points = []

    # Extract positions
    user_position = player_positions[0]
    bot_position = player_positions[1]

    user_x, user_y = user_position
    bot_x, bot_y = bot_position
    last_x, last_y = user_last_position

    # Step 1: Prioritize placing a front wall (same x first)
    # The bot's goal is to move upward (towards y = 0)
    if user_y > 0:  # Ensure the bot is not already at the top
        # Check directly in front of the user (same x)
        front_wall = (user_x, user_y + 1, HORIZONTAL)
        if (
                front_wall not in walls
                and not causes_overlap(front_wall, walls)
                and is_valid_wall(front_wall, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [front_wall])
                and is_path_open(bot_position, 0, walls + [front_wall])
        ):
            choke_points.append(front_wall)
            print(f"Choke point found directly in front of the user at: {front_wall}")
            return choke_points  # Prioritize and return immediately

        # Check to the left of the user (x - 1)
        left_wall = (user_x - 1, user_y + 1, HORIZONTAL)
        if (
                user_x > 0
                and left_wall not in walls
                and not causes_overlap(left_wall, walls)
                and is_valid_wall(left_wall, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [left_wall])
                and is_path_open(bot_position, 0, walls + [left_wall])
        ):
            choke_points.append(left_wall)
            print(f"Choke point found to the left in front of the user at: {left_wall}")
            return choke_points  # Prioritize and return immediately

    # Step 2: Analyze the user's movement direction
    # Determine vertical movement
    if user_y > last_y:  # User moved down
        choke_point = (user_x, user_y + 1, HORIZONTAL)
        if (
                is_valid_wall(choke_point, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [choke_point])
                and is_path_open(bot_position, 0, walls + [choke_point])
        ):
            choke_points.append(choke_point)

    elif user_y < last_y:  # User moved up
        choke_point = (user_x, user_y, HORIZONTAL)
        if (
                is_valid_wall(choke_point, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [choke_point])
                and is_path_open(bot_position, 0, walls + [choke_point])
        ):
            choke_points.append(choke_point)

    # Determine horizontal movement
    elif user_x > last_x:  # User moved right
        choke_point = (user_x + 1, user_y, VERTICAL)
        if (
                is_valid_wall(choke_point, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [choke_point])
                and is_path_open(bot_position, 0, walls + [choke_point])
        ):
            choke_points.append(choke_point)

    elif user_x < last_x:  # User moved left
        choke_point = (user_x, user_y, VERTICAL)
        if (
                is_valid_wall(choke_point, walls)
                and is_path_open(user_position, GRID_SIZE - 1, walls + [choke_point])
                and is_path_open(bot_position, 0, walls + [choke_point])
        ):
            choke_points.append(choke_point)

    return choke_points


def bot_turn(player_positions, walls, bot_walls_remaining, user_walls_remaining, user_last_position, turn_count):
    """
    Bot's turn logic, prioritizing winning moves, blocking user paths, and fallback Minimax evaluation.

    Parameters:
    - player_positions: List of player positions [(user_x, user_y), (bot_x, bot_y)].
    - walls: List of currently placed walls [(x, y, orientation)].
    - bot_walls_remaining: Number of walls the bot has left.
    - user_walls_remaining: Number of walls the user has left.
    - user_last_position: The user's last position (x, y).
    - turn_count: Number of turns that have occurred in the game.

    Returns:
    - Updated number of bot walls remaining.
    """
    bot_position = player_positions[1]
    user_position = player_positions[0]

    # Calculate distances to goals
    bot_distance = shortest_path_length(bot_position, 0, walls)
    user_distance = shortest_path_length(user_position, GRID_SIZE - 1, walls)

    # Determine the game phase and dynamic depth
    if turn_count < 6 or bot_distance > user_distance:  # Early phase
        phase = "early"
        depth = 2  # Shallow exploration
    else:  # Mid/Late phase
        phase = "mid_late"
        depth = 4  # Deeper exploration

    # Step 1: Winning Move
    possible_moves = get_all_possible_moves(bot_position, walls)
    for move in possible_moves:
        if move[1] == 0:  # Bot's goal row is y = 0
            player_positions[1] = move
            print(f"Bot moved to goal: {move}.")
            return bot_walls_remaining

    # Step 2: Block User if Close to Goal
    if user_distance <= 2 and bot_walls_remaining > 0:  # User is 2 or fewer steps from their goal
        choke_points = find_choke_points(player_positions, user_last_position, walls)
        for choke_point in choke_points:
            if is_valid_wall(choke_point, walls):
                walls.append(choke_point)
                bot_walls_remaining -= 1
                print(f"Bot placed wall at {choke_point} to block user close to goal.")
                return bot_walls_remaining

    # Step 3: Handle Adjacent to User (Conditional Jump Logic)
    x, y = bot_position
    user_x, user_y = user_position
    if abs(x - user_x) + abs(y - user_y) == 1:  # Adjacent to user
        # Check if user is in the bot's direct path
        best_move = min(
            possible_moves,
            key=lambda move: shortest_path_length(move, 0, walls),
            default=None
        )

        if best_move and best_move == (user_x, user_y):  # User is in the bot's shortest path
            jump_x, jump_y = user_x + (user_x - x), user_y + (user_y - y)
            if 0 <= jump_x < GRID_SIZE and 0 <= jump_y < GRID_SIZE:
                if not is_wall_blocking_move((x, y), (user_x, user_y), walls) and \
                   not is_wall_blocking_move((user_x, user_y), (jump_x, jump_y), walls):
                    player_positions[1] = (jump_x, jump_y)
                    print(f"Bot jumped over the user to: {(jump_x, jump_y)}.")
                    return bot_walls_remaining
            else:
                # If jump is not possible, find an alternate move
                print("Jump not possible, finding alternate move.")
                for move in possible_moves:
                    if move != (user_x, user_y):
                        player_positions[1] = move
                        print(f"Bot moved to avoid stepping on user: {move}.")
                        return bot_walls_remaining

    # Step 4: Logical Movement to Avoid Oscillation and Prioritize Wall Placement
    best_move = None
    best_distance = float('inf')

    for move in possible_moves:
        move_distance = shortest_path_length(move, 0, walls)
        if move_distance < best_distance and move != (user_x, user_y):
            best_move = move
            best_distance = move_distance

    if best_move:
        if best_distance > bot_distance and bot_walls_remaining > 0:
            print("All available moves increase path length; bot will prioritize placing a wall.")
            choke_points = find_choke_points(player_positions, user_last_position, walls)
            for choke_point in choke_points:
                if is_valid_wall(choke_point, walls):
                    walls.append(choke_point)
                    bot_walls_remaining -= 1
                    print(f"Bot placed wall at {choke_point} instead of moving to a worse position.")
                    return bot_walls_remaining
        elif best_distance <= bot_distance:
            player_positions[1] = best_move
            print(f"Bot moved to: {best_move}.")
            return bot_walls_remaining

    # Step 5: Strategic Wall Placement in Early Phase
    if phase == "early" and bot_walls_remaining > 0:
        choke_points = find_choke_points(player_positions, user_last_position, walls)
        for choke_point in choke_points:
            if is_valid_wall(choke_point, walls):
                walls.append(choke_point)
                bot_walls_remaining -= 1
                print(f"Bot placed wall at {choke_point} to slow user.")
                return bot_walls_remaining

    # Step 6: Fallback to Minimax in Mid/Late Phases
    if phase == "mid_late":
        print("Bot is deciding using Minimax...")
        best_action = None
        best_score = float('-inf')

        possible_actions = get_all_possible_bot_actions(
            bot_position, walls, bot_walls_remaining, user_position, user_last_position
        )

        for action in possible_actions:
            new_positions, new_walls, new_bot_walls_remaining, new_user_walls_remaining = apply_action(
                player_positions, walls, action, is_bot=True, bot_walls_remaining=bot_walls_remaining,
                user_walls_remaining=user_walls_remaining
            )

            score = minimax(
                new_positions,
                new_walls,
                depth - 1,
                float('-inf'),
                float('inf'),
                False,  # User's turn
                new_bot_walls_remaining,
                new_user_walls_remaining,
                user_last_position
            )

            if score > best_score:
                best_score = score
                best_action = action

        if best_action:
            if best_action[0] == "move":
                player_positions[1] = best_action[1]
                print(f"Bot decided to move to {best_action[1]} using Minimax.")
            elif best_action[0] == "wall":
                if is_valid_wall(best_action[1], walls):
                    walls.append(best_action[1])
                    bot_walls_remaining -= 1
                    print(f"Bot placed wall at {best_action[1]} using Minimax.")
            return bot_walls_remaining

    # Step 7: No Good Moves, Stay in Place
    print("No advantageous moves found; bot will stay in place.")
    return bot_walls_remaining


def get_all_possible_user_actions(user_position, walls, user_walls_remaining, bot_position):
    actions = []

    # Add all valid moves
    possible_moves = get_all_possible_moves(user_position, walls)
    for move in possible_moves:
        actions.append(("move", move))

    # Add all valid wall placements if walls are remaining
    if user_walls_remaining > 0:
        for x in range(1, GRID_SIZE - 1):  # Exclude borders
            for y in range(1, GRID_SIZE - 1):  # Exclude borders
                for orientation in [HORIZONTAL, VERTICAL]:
                    new_wall = (x, y, orientation)
                    if new_wall not in walls and not causes_overlap(new_wall, walls):
                        # Ensure the wall does not block paths
                        if is_path_open(user_position, GRID_SIZE - 1, walls + [new_wall]) and \
                           is_path_open(bot_position, 0, walls + [new_wall]):
                            actions.append(("wall", new_wall))

    return actions


def evaluate_action_priority(action, bot_position, user_position, walls):
    """
    Rank actions by their impact.
    Moves are ranked by distance to the bot's goal, and walls by impact on the user's path.
    """
    if action[0] == "move":
        # Rank moves by proximity to the bot's goal (closer is better)
        return shortest_path_length(action[1], 0, walls)
    elif action[0] == "wall":
        # Rank walls by their impact on the user's shortest path
        wall = action[1]
        original_user_path = shortest_path_length(user_position, GRID_SIZE - 1, walls)
        new_user_path = shortest_path_length(user_position, GRID_SIZE - 1, walls + [wall])
        return -(new_user_path - original_user_path)  # Negative to prioritize walls that block more
    return float('inf')  # Lowest priority for invalid actions


def is_valid_wall(wall, walls):
    """
    Check if the wall position is valid (not on borders and does not overlap).

    Parameters:
    - wall: Tuple (x, y, orientation) representing the wall's position and orientation.
    - walls: List of currently placed walls.

    Returns:
    - True if the wall is valid, False otherwise.
    """
    x, y, orientation = wall

    # Grid size constant
    GRID_SIZE = 9  # Update this to match your grid size

    # Wall is invalid if it's on the borders
    if orientation == HORIZONTAL:
        if y <= 0 or y >= GRID_SIZE or x < 0 or x >= GRID_SIZE - 1:
            return False
    elif orientation == VERTICAL:
        if x <= 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE - 1:
            return False

    # Wall is invalid if it overlaps existing walls
    if wall in walls or causes_overlap(wall, walls):
        return False

    return True


def get_all_possible_bot_actions(bot_position, walls, bot_walls_remaining, user_position, user_last_position):
    """
    Generate all valid actions for the bot, including moves and wall placements.
    Exclude walls placed on the borders, sort actions by their strategic impact, and limit irrelevant placements.

    Parameters:
    - bot_position: Current position of the bot (x, y).
    - walls: List of currently placed walls.
    - bot_walls_remaining: Number of walls the bot has left.
    - user_position: Current position of the user (x, y).
    - user_last_position: Last position of the user (x, y).

    Returns:
    - List of valid actions: [("move", position), ("wall", wall_position)].
    """
    actions = []
    player_positions = [user_position, bot_position]
    # Step 1: Add valid moves
    possible_moves = get_all_possible_moves(bot_position, walls)
    for move in possible_moves:
        actions.append(("move", move))

    # Step 2: Add wall placements if walls are remaining
    if bot_walls_remaining > 0:
        # Use find_choke_points to generate strategic wall positions
        choke_points = find_choke_points(player_positions, user_last_position, walls)

        for choke_point in choke_points:
            # Validate the wall placement with is_valid_wall
            if is_valid_wall(choke_point, walls):
                actions.append(("wall", choke_point))

        # Sort wall actions by their impact on the user's path length
        actions = sorted(
            actions,
            key=lambda action: evaluate_action_priority(action, bot_position, user_position, walls)
        )

    # Step 3: Limit total actions to prevent irrelevant placements
    max_actions = 10  # Limit the number of actions to evaluate
    return actions[:max_actions]


def apply_action(player_positions, walls, action, is_bot, bot_walls_remaining, user_walls_remaining):
    """
    Apply an action and return the resulting game state.

    Parameters:
    - player_positions: Current player positions [(user_x, user_y), (bot_x, bot_y)].
    - walls: List of current walls.
    - action: The action to be applied ("move", position) or ("wall", wall_placement).
    - is_bot: Boolean indicating if the bot is performing the action.
    - bot_walls_remaining: Remaining walls for the bot.
    - user_walls_remaining: Remaining walls for the user.

    Returns:
    - Updated player positions, walls, and the updated wall count for the acting player.
    """
    # Copy current state
    new_positions = player_positions[:]
    new_walls = walls.copy()

    if action[0] == "move":  # Move action
        if is_bot:
            new_positions[1] = action[1]  # Update bot's position
        else:
            new_positions[0] = action[1]  # Update user's position
        # Return updated positions, unchanged walls, and unchanged wall counts
        return new_positions, new_walls, bot_walls_remaining, user_walls_remaining

    elif action[0] == "wall":  # Wall placement action
        new_walls.append(action[1])  # Add new wall
        if is_bot:
            bot_walls_remaining = max(0, bot_walls_remaining - 1)  # Decrement bot's wall count
        else:
            user_walls_remaining = max(0, user_walls_remaining - 1)  # Decrement user's wall count
        return new_positions, new_walls, bot_walls_remaining, user_walls_remaining


def start_game():
    """Start the game with an initial start screen and wait for play button click."""
    running = True
    while running:
        button_x, button_y, button_width, button_height = draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if button_x < event.pos[0] < button_x + button_width and button_y < event.pos[1] < button_y + button_height:
                        running = False  # Exit the start screen to start the game


def main():
    """Main function to run the game."""
    # Show start screen
    start_game()

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Initialize game state
    running = True
    player_positions = [(4, 0), (4, 8)]  # User (Red) starts at (4, 0), Bot (Blue) starts at (4, 8)
    walls = []  # List to store wall positions
    user_walls_remaining = 10  # User starts with 10 walls
    bot_walls_remaining = 10  # Bot starts with 10 walls
    user_moved = False
    bot_move_timer = 0  # Timer for bot's delayed move
    preview_wall = {'x': 4, 'y': 4, 'orientation': HORIZONTAL, 'active': False, 'invalid': False}  # Wall preview state
    user_last_position = player_positions[0]  # Track user's last position
    turn_count = 0  # Track the number of turns
    show_popup = False  # Popup window visibility flag
    message = ""  # Feedback message
    message_timer = 0  # Timer for message display

    while running:
        # Fill the screen background
        screen.fill(BACKGROUND)

        # Draw the game board and grid
        draw_board()

        # Draw the background for the interface area
        draw_interface_background()

        # Draw players and walls
        draw_players(player_positions)
        draw_walls(walls)

        # Draw the preview wall if active
        if preview_wall['active']:
            draw_preview_wall(preview_wall, walls)

        # Display remaining walls below the board
        draw_interface_text(user_walls_remaining, bot_walls_remaining, message)

        # Show popup window if triggered
        if show_popup:
            draw_popup("No walls remaining!")

        pygame.display.flip()

        # Check for win condition
        if player_positions[0][1] == GRID_SIZE - 1:  # User reaches the bot's side
            display_message("You Win!")
            pygame.time.delay(2000)
            running = False
        elif player_positions[1][1] == 0:  # Bot reaches the user's side
            display_message("You Lose!")
            pygame.time.delay(2000)
            running = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if preview_wall['active']:  # Wall placement mode
                    if event.key == pygame.K_m:  # Exit wall preview mode
                        preview_wall['active'] = False
                    else:
                        valid_placement, user_walls_remaining = handle_preview_wall_input(
                            preview_wall, event, walls, player_positions, user_walls_remaining
                        )
                        if valid_placement:  # If wall was successfully placed
                            user_moved = True  # Switch turn to the bot
                            bot_move_timer = pygame.time.get_ticks()
                        else:  # Feedback for invalid placement
                            message = "Invalid wall placement!"
                            message_timer = pygame.time.get_ticks()
                else:
                    if event.key == pygame.K_w:  # Activate wall placement mode
                        if user_walls_remaining > 0:  # Only activate if walls are remaining
                            preview_wall['active'] = True
                            preview_wall['x'], preview_wall['y'], preview_wall['orientation'] = 4, 4, HORIZONTAL
                        else:
                            show_popup = True  # Show the popup window
                    elif event.key == pygame.K_m:  # Ensure moving mode is active
                        preview_wall['active'] = False
                    elif not user_moved:
                        move_made, user_walls_remaining, move_message = handle_user_move_or_wall(
                            player_positions, walls, event, user_walls_remaining
                        )
                        if move_made:
                            user_moved = True  # Switch turn to the bot
                            bot_move_timer = pygame.time.get_ticks()
                        elif move_message:  # Feedback for invalid moves
                            message = move_message
                            message_timer = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_popup and is_popup_close_clicked(event.pos):  # Handle popup close
                    show_popup = False

            elif event.type == pygame.USEREVENT:
                # Reset invalid preview wall state after 0.5 seconds
                preview_wall['invalid'] = False
                pygame.time.set_timer(pygame.USEREVENT, 0)

        # Bot's turn
        if user_moved and pygame.time.get_ticks() - bot_move_timer >= 1000:
            bot_walls_remaining = bot_turn(
                player_positions,
                walls,
                bot_walls_remaining,
                user_walls_remaining,
                user_last_position,
                turn_count
            )
            user_last_position = player_positions[0]  # Update user's last position
            user_moved = False
            turn_count += 1  # Increment turn count

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
