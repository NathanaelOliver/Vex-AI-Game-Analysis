from collections import deque
import pygame
import math

class Size:
    TILE = 120
    SCREEN = TILE*7
    ROBOT = TILE*5/16
    MOGO = TILE/4
    RING_WIDTH = MOGO/2
    FIELD_RING_WIDTH = RING_WIDTH/2
    RING_HEIGHT = MOGO/6
    FIELD_RING_HEIGHT = RING_HEIGHT/2
TILE_SIZE = 120 # TODO deprecate TILE_SIZE

class Color:
    TILE = (217, 217, 217)
    BORDER = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    TIER0 = (229, 229, 229)
    TIER1 = (33, 36, 38)
    TIER2 = (76, 79, 81)
    TIER3 = (185, 198, 00)

class Alliance:
    EMPTY = 0
    RED = 1
    BLUE = -1

class Action:
    WAIT = 0            # Robot Does Nothing
    UP = 1              # Move Up
    LEFT = 2            # Move Left
    RIGHT = 3           # Move Right
    DOWN = 4            # Move Down
    MOGO1 = 5           # Pick up Mogo 1
    MOGO2 = 6           # Pick up Mogo 2
    MOGO3 = 7           # Pick up Mogo 3
    MOGO4 = 8           # Pick up Mogo 4
    MOGO5 = 9           # Pick up Mogo 5
    PLACE_MOGO = 10     # Place Mogo
    MOGO_ZONE = 11      # Place Mogo in Zone
    GRAB_ALLIANCE = 12  # Pick Up Red Ring
    GRAB_OPPONENT = 13  # Pick Up Blue Ring
    SCORE_ALLIANCE = 14 # Pick up Red Ring and Place on Mogo
    SCORE_OPPONENT = 15 # Pick up Blue Ring and Place on Mogo
    DESCORE_MOGO = 16   # Grab Top Ring from Mogo
    STAKE_RING = 17     # Score Held Ring On Stake
    DROP_RING = 18      # Place Held Ring
    BLOCK1 = 19         # Block Opponent 1
    BLOCK2 = 20         # Block Opponent 2
    HANG = 21           # Hang +
    LOWER = 22          # Hang -

class Field:
    def __init__(self):
        self.tiles = ([
            [Multiplier_Zone(2,2),               Tile(0,0), Tile(0,0), High_Stake(1,1), Tile(0,0), Tile(0,0), Multiplier_Zone(2,2)              ], 
            [Tile(0,0),                          Tile(1,1), Tile(1,1), Tile(0,0),       Tile(1,1), Tile(1,1), Tile(0,0)                         ], 
            [Tile(0,0),                          Tile(0,0), Tile(0,1), Tile(0,0),       Tile(1,0), Tile(0,0), Tile(0,0)                         ], 
            [Alliance_Stake(1,1, Alliance.RED),  Tile(0,0), Tile(0,0), Tile(0,0),       Tile(0,0), Tile(0,0), Alliance_Stake(1,1, Alliance.BLUE)], 
            [Tile(0,0),                          Tile(0,0), Tile(0,1), Tile(0,0),       Tile(1,0), Tile(0,0), Tile(0,0)                         ], 
            [Tile(0,0),                          Tile(1,1), Tile(1,1), Tile(0,0),       Tile(1,1), Tile(1,1), Tile(0,0)                         ], 
            [Multiplier_Zone(2,2),               Tile(0,0), Tile(0,0), High_Stake(1,1), Tile(0,0), Tile(0,0), Multiplier_Zone(2,2)              ]
        ])
    def get_score(self, alliance):
        return (self.tiles[0][3].get_score(alliance) + self.tiles[3][0].get_score(alliance) 
            + self.tiles[6][3].get_score(alliance) + self.tiles[3][6].get_score(alliance))
    def get_state(self,alliance):
        state = []
        for row in self.tiles:
            for tile in row:
                state.extend(tile.get_state(alliance))
        return state
    def display(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                tile.display(screen, x, y)

class Robot:
    def __init__(self, id, alliance, x, y):
        self.id = id
        self.mogo_id = 0
        self.ring = alliance
        self.x = x
        self.y = y
        self.hang = 0
        self.pinning = 0
        self.alliance = alliance
        self.action = Action.WAIT
    def get_state(self):
        return [self.x, self.y, self.hang, self.action, self.mogo_id, self.ring, self.pinning]
    def display(self, screen, position):
        robot_display = pygame.Rect(position[0], position[1], Size.ROBOT, Size.ROBOT)
        pygame.draw.rect(screen, (Color.RED if self.alliance == Alliance.RED else Color.BLUE), robot_display, 0)
        hang_tier = [Color.TIER0, Color.TIER1, Color.TIER1, Color.TIER2, Color.TIER2, Color.TIER3]
        pygame.draw.rect(screen, hang_tier[self.hang], robot_display, 2)
        ring_color = Color.RED if self.ring == Alliance.RED else Color.BLUE if self.ring == Color.BLUE else Color.WHITE
        ring_display = pygame.Rect(position[0] + Size.ROBOT - Size.RING_WIDTH - 3, position[1] + 3, Size.RING_WIDTH, Size.RING_HEIGHT)
        pygame.draw.rect(screen, ring_color, ring_display, 0)
        pygame.draw.rect(screen, Color.BORDER, ring_display, 1)
    def remember(self):
        pass # TODO remember moves
    def train_step(self):
        pass # TODO train at each step
    def train_batch(self):
        pass # TODO train batch
    def get_action(self, state):
        self.action = int(input()) # TODO perform inference

class Tile:
    def __init__(self, red, blue):
        self.red = red
        self.blue = blue
    def has_rings(self, alliance):
        if alliance == Alliance.RED:
            return self.red
        elif alliance == Alliance.BLUE:
            return self.blue
        else: 
            return 0
    def add_ring(self, alliance):
        if alliance == Alliance.RED:
            self.red += 1
        elif alliance == Alliance.BLUE:
            self.blue += 1
    def subtract_ring(self, alliance):
        if alliance == Alliance.RED:
            self.red -= 1
        elif alliance == Alliance.BLUE:
            self.blue -= 1
    def get_state(self, alliance):
        return [self.red, self.blue] if alliance == Alliance.RED else [self.blue, self.red]
    def display(self, screen, x, y):
        tile = pygame.Rect(x * Size.TILE, y * Size.TILE, Size.TILE, Size.TILE)
        pygame.draw.rect(screen, Color.TILE, tile, 0)
        pygame.draw.rect(screen, Color.BORDER, tile, 1)
        red_ring_display = pygame.Rect((x + 1) * Size.TILE - 2*Size.FIELD_RING_WIDTH, y * Size.TILE + 1,Size.FIELD_RING_WIDTH, Size.FIELD_RING_HEIGHT*self.red)
        pygame.draw.rect(screen, Color.RED, red_ring_display, 0)
        # TODO draw red and blue rings

class Multiplier_Zone(Tile):
    def __init__(self, red, blue):
        Tile.__init__(self, red, blue)
        self.mogo = 0
    def get_state(self, alliance):
        return Tile.get_state(self, alliance)
    def score_mogo(self, id):
        self.mogo, ret = id, self.mogo
        return ret
    def display(self, screen, x, y):
        Tile.display(self, screen, x, y)
        # TODO add multiplier positive vs negative


class Stake:
    def __init__(self, ring_count):
        self.rings = [Alliance.EMPTY for _ in range(0,ring_count)]
    def get_score(self, alliance):
        score = 0
        top_ring = Alliance.EMPTY
        for ring in self.rings:
            if ring == alliance:
                score += 1
            if ring != Alliance.EMPTY:
                top_ring = ring
        if top_ring == alliance:
            score += 2
        return score
    def get_state(self):
        return self.rings
    def add_ring(self, ring):
        for i, e in  enumerate(self.rings):
            if e == Alliance.EMPTY:
                self.rings[i] = ring
                break
    def remove_ring(self):
        for i, ring in enumerate(self.rings):
            if ring != Alliance.EMPTY:
                index = i
                top_ring = ring
        self.rings[index] = Alliance.EMPTY
        return top_ring
    def display(self, screen, x, y):
        for i, ring in enumerate(self.rings):
            rect = pygame.Rect(x, y + (5-i)*Size.RING_HEIGHT, Size.RING_WIDTH, Size.RING_HEIGHT)
            pygame.draw.rect(screen, (Color.RED if ring == Alliance.RED else Color.BLUE if ring == Alliance.BLUE else Color.WHITE), rect, 0)
            pygame.draw.rect(screen, Color.BORDER, rect, 1)

class High_Stake(Tile, Stake):
    def __init__(self, red, blue):
        Tile.__init__(self, red, blue)
        Stake.__init__(self, 6)
    def get_state(self, alliance):
        return Tile.get_state(self, alliance) + Stake.get_state(self)
    def display(self, screen, x, y):
        Tile.display(self, screen, x, y)
        Stake.display(self, screen, x*Size.TILE + 2*Size.ROBOT + Size.RING_WIDTH/2, y*Size.TILE)

class Alliance_Stake(Tile, Stake):
    def __init__(self, red, blue, alliance):
        Tile.__init__(self, red, blue)
        Stake.__init__(self, 2)
        self.alliance = alliance
    def get_state(self, alliance):
        return Tile.get_state(self, alliance) + Stake.get_state(self)
    def display(self, screen, x, y):
        Tile.display(self, screen, x, y)
        Stake.display(self, screen, (x+.6875)*TILE_SIZE, y*TILE_SIZE)

class Mogo(Stake):
    def __init__(self, id, x, y):
        Stake.__init__(self, 6)
        self.x = x
        self.y = y
        self.id = id
        self.multiplier = 1
    def get_score(self, alliance):
        return Stake.get_score(self, alliance) * self.multiplier
    def get_state(self):
        return [self.x, self.y] + Stake.get_state(self) + [self.multiplier]
    def display(self, screen, position):
        points = [((self.x + position[0] + .125 * math.cos(math.radians(60 * i)))*TILE_SIZE, (self.y + position[1] + .125 * math.sin(math.radians(60 * i)))*TILE_SIZE) for i in range(6)]
        pygame.draw.polygon(screen, Color.GREEN, points, 0)
        pygame.draw.polygon(screen, Color.BORDER, points, 1)
        Stake.display(self, screen, (self.x + position[0] - 1/16)*TILE_SIZE, (self.y + position[1]-.125)*TILE_SIZE)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((TILE_SIZE * 7, TILE_SIZE * 7))
        self.field = Field()
        self.red_score = 0
        self.blue_score = 0
        self.robots = [Robot(1, Alliance.RED, 0, 2), Robot(2, Alliance.RED, 0, 5), Robot(3, Alliance.BLUE, 6, 2), Robot(4, Alliance.BLUE, 6, 5)]
        self.mogos = [Mogo(1,1,3), Mogo(2,3,1), Mogo(3,3,3), Mogo(4,3,5), Mogo(5,5,3)]

    def run(self):
        score = self.calculate_score()
        running = True
        for time_step in range(120):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if running == False:
                break
            for i, robot in enumerate(self.robots):
                if i != 0:
                    continue
                prev_score = score
                self.apply_action(i)
                # Calculate State of Game
                state = self.field.get_state(robot.alliance)
                for mogo in self.mogos:
                    state.extend(mogo.get_state())
                for robot_index in [((i + j) if i % 2 == 0 else i - j) % 4 for j in range(4)]:
                    state.extend(self.robots[robot_index].get_state())
                state.extend([score[0 if i < 2 else 1], score[1 if i < 2 else 1], time_step])

                self.clock.tick(25)
                self.update_ui()

                # Get Robot Next Move
                robot.get_action(state)
                if robot.action == Action.BLOCK1 or robot.action == Action.BLOCK2:
                    self.apply_action(i)
                    robot.pinning += 1
                else:
                    robot.pinning = max(0, robot.pinning - 1)

                score = self.calculate_score()

                # TODO calculate Reward
                reward = 0
                if robot.pinning >= 5:
                    reward -= 10*robot.pinning
        pygame.quit()

    def calculate_score(self):
        red = 0
        blue = 0
        for mogo in self.mogos:
            red += mogo.get_score(Alliance.RED)
            blue += mogo.get_score(Alliance.BLUE)
        red += self.field.get_score(Alliance.RED)
        blue += self.field.get_score(Alliance.BLUE)
        return (red, blue)

    def apply_action(self, robot_index):
        action = self.robots[robot_index].action
        robot = self.robots[robot_index]
        if action == Action.WAIT: # Wait
            pass
        elif action == Action.UP: # Move Up
            if robot.hang == 0:
                robot.y = max(robot.y - 1, 0)
                if robot.mogo_id != 0:
                    self.mogos[robot.mogo_id - 1].y = robot.y
        elif action == Action.LEFT: # Move Left
            if robot.hang == 0:
                robot.x = max(robot.x - 1, 0)
                if robot.mogo_id != 0:
                    self.mogos[robot.mogo_id - 1].x = robot.x
        elif action == Action.RIGHT: # Move Right
            if robot.hang == 0:
                robot.x = min(robot.x + 1, 6)
                if robot.mogo_id != 0:
                    self.mogos[robot.mogo_id - 1].x = robot.x
        elif action == Action.DOWN: # Move Down
            if robot.hang == 0:
                robot.y = min(robot.y + 1, 6)
                if robot.mogo_id != 0:
                    self.mogos[robot.mogo_id - 1].y = robot.y
        elif action == Action.MOGO1 or action == Action.MOGO2 or action == Action.MOGO3 or action == Action.MOGO4 or action == Action.MOGO5: # Pick up Mogo 1
            mogo_num = action - 4
            for robots in self.robots:
                if robots.mogo_id == mogo_num:
                    break
            else:
                if robot.mogo_id == 0 and robot.x == self.mogos[mogo_num - 1].x and robot.y == self.mogos[mogo_num - 1].y:
                    robot.mogo_id = mogo_num
        elif action == Action.PLACE_MOGO: # Place Mogo
            robot.mogo_id = 0
        elif action == Action.MOGO_ZONE: # Place Mogo in Zone
            if (robot.x == 0 or robot.x == 6) and (robot.y == 0 or robot.y == 6):
                self.mogos[(self.field.tiles[robot.y][robot.x].score_mogo(robot.mogo_id)) - 1].multiplier = 1
                self.mogos[robot.mogo_id - 1].multiplier = -1 if robot.x == robot.y else 2
            robot.mogo_id = 0
        elif action == Action.GRAB_ALLIANCE: # Pick Up Red Ring
            if self.field.tiles[robot.y][robot.x].has_rings(robot.alliance) > 0 and robot.ring == Alliance.EMPTY:
                robot.ring = robot.alliance
                self.field.tiles[robot.y][robot.x].subtract_ring(robot.alliance)
        elif action == Action.GRAB_OPPONENT: # Pick Up Blue Ring
            if self.field.tiles[robot.y][robot.x].has_rings(-robot.alliance) > 0 and robot.ring == Alliance.EMPTY:
                robot.ring = -robot.alliance
                self.field.tiles[robot.y][robot.x].subtract_ring(-robot.alliance)
        elif action == Action.SCORE_ALLIANCE:
            if self.field.tiles[robot.y][robot.x].has_rings(robot.alliance) > 0 and robot.mogo_id != 0 and self.mogos[robot.mogo_id - 1].rings.__contains__(Alliance.EMPTY):
                self.mogos[robot.mogo_id - 1].add_ring(robot.alliance)
                self.field.tiles[robot.y][robot.x].subtract_ring(robot.alliance)
        elif action == Action.SCORE_OPPONENT:
            if self.field.tiles[robot.y][robot.x].has_rings(-robot.alliance) > 0 and robot.mogo_id != 0 and self.mogos[robot.mogo_id - 1].rings.__contains__(Alliance.EMPTY):
                self.mogos[robot.mogo_id - 1].add_ring(-robot.alliance)
                self.field.tiles[robot.y][robot.x].subtract_ring(-robot.alliance)
        elif action == Action.DESCORE_MOGO: # Grab Top Ring from Mogo
            if robot.ring == Alliance.EMPTY and robot.mogo_id != 0:
                robot.ring = self.mogos[robot.mogo_id - 1].remove_ring()
        elif action == Action.STAKE_RING: # Score Held Ring On Stake
            if (robot.x == 3 and (robot.y == 0 and robot.y == 6)) or (robot.y == 3 and ((robot.alliance == Alliance.RED and robot.x == 0) or (robot.alliance == Alliance.BLUE and robot.x == 6))):
                if self.field.tiles[robot.y][robot.x].rings.__contains__(0):
                    self.field.tiles[robot.y][robot.x].add_ring(robot.ring)
                    robot.ring = Alliance.EMPTY
        elif action == Action.DROP_RING: # Drop Held Ring
            self.field.tiles[robot.y][robot.x].add_ring(robot.ring)
            robot.ring = Alliance.EMPTY
        elif action == Action.BLOCK1 or action == Action.BLOCK2: # Block Opponents
            self.robots[action - 18 + robot.alliance].action = Action.WAIT
        elif action == Action.HANG: # Hang +
            if 1 < robot.x < 5 and 1 < robot.y < 5 and robot.hang < 5:
                robot.hang += 1
        elif action == Action.LOWER: # Hang -
            if robot.hang > 0:
                robot.hang -= 1

    def update_ui(self):
        print("Updating UI")
        self.field.display(self.screen)
        mogo_positions = [((0.125 + 0.1875 * i), (0.875 if i % 2 == 0 else .75)) for i in range(5)]
        for i, robot in enumerate(self.robots):
            robot.display(self.screen, (robot.x*Size.TILE if robot.alliance == Alliance.RED else robot.x*Size.TILE + Size.ROBOT, robot.y*Size.TILE if i % 2 == 0 else robot.y*Size.TILE + Size.ROBOT))
            if robot.mogo_id != 0:
                mogo_positions[robot.mogo_id - 1] = (.125 if robot.alliance == Alliance.RED else .4375, (.1875 if i%2 == 0 else .5))
        for i in range(5):
            self.mogos[i].display(self.screen, mogo_positions[i])
        pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.run()