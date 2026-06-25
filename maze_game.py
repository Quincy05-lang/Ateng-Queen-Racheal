# ── OOP Classes ──────────────────────────────────────────────────

class Entity:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, '@')
        self.__health = 3          # Encapsulation: name-mangled private attribute

    @property
    def health(self):
        return self.__health

    def take_damage(self):
        self.__health -= 1

    def is_alive(self):
        return self.__health > 0

    def move(self, dx, dy, size):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < size and 0 <= ny < size:
            self.x, self.y = nx, ny
            return True
        return False


class Trap(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'X')

    def trigger(self, player):
        player.take_damage()


class Treasure(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'T')


# ── Helpers ───────────────────────────────────────────────────────

import random

SIZE = 5

def render(grid, player):
    print("\n  " + " ".join(str(i) for i in range(SIZE)))
    for row in range(SIZE):
        row_str = f"{row} "
        for col in range(SIZE):
            row_str += grid[row][col] + " "
        print(row_str)
    print(f"\nHealth: {'♥ ' * player.health}{'♡ ' * (3 - player.health)}")


def build_grid(player, traps, treasure):
    grid = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
    grid[treasure.y][treasure.x] = treasure.symbol
    for trap in traps:
        grid[trap.y][trap.x] = trap.symbol
    grid[player.y][player.x] = player.symbol
    return grid


def unique_positions(count):
    positions = random.sample([(x, y) for x in range(SIZE) for y in range(SIZE)], count)
    return positions


# ── Game Setup ────────────────────────────────────────────────────

def init_game():
    positions = unique_positions(7)          # 1 player + 1 treasure + 5 traps
    player   = Player(*positions[0])
    treasure = Treasure(*positions[1])
    traps    = [Trap(*pos) for pos in positions[2:]]
    return player, traps, treasure


# ── Game Loop ─────────────────────────────────────────────────────

def game_loop():
    player, traps, treasure = init_game()
    move_count = 0

    directions = {
        'w': (0, -1),
        's': (0,  1),
        'a': (-1, 0),
        'd': ( 1, 0),
    }

    print("=== MAZE GAME ===")
    print("Find the Treasure (T). Avoid Traps (X). Controls: W A S D\n")

    while True:
        grid = build_grid(player, traps, treasure)
        render(grid, player)

        raw = input("\nMove (WASD) or Q to quit: ").strip().lower()
        if raw == 'q':
            print("Thanks for playing!")
            break

        if raw not in directions:
            print("Invalid input. Use W, A, S, or D.")
            continue

        dx, dy = directions[raw]
        moved = player.move(dx, dy, SIZE)

        if not moved:
            print("You can't move that way!")
            continue

        move_count += 1

        # Check treasure
        if player.x == treasure.x and player.y == treasure.y:
            grid = build_grid(player, traps, treasure)
            render(grid, player)
            print(f"\n🏆 You found the treasure in {move_count} moves! You win!")
            break

        # Check traps
        for trap in traps:
            if player.x == trap.x and player.y == trap.y:
                trap.trigger(player)
                if not player.is_alive():
                    grid = build_grid(player, traps, treasure)
                    render(grid, player)
                    print("\n💀 You stepped on a trap and died! Game over.")
                    return
                print(f"⚠  Trap! You lost 1 health. {player.health} remaining.")
                break


if __name__ == "__main__":
    game_loop()