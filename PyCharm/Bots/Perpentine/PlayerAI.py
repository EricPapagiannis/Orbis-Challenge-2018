from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team, Direction
from PythonClientAPI.game.World import World
from PythonClientAPI.game.TileUtils import TileUtils
from PythonClientAPI.game.PathFinder import PathFinder
class PlayerAI:

    def __init__(self):
        ''' Initialize! '''
        self.turn_count = 0             # game turn count
        self.target = None              # target to send unit to!
        self.outbound = True            # is the unit leaving, or returning?
        self.direction = None
        self.cornerCount = 0

    def do_move(self, world, friendly_unit, enemy_units):
        '''
        This method is called every turn by the game engine.
        Make sure you call friendly_unit.move(target) somewhere here!

        Below, you'll find a very rudimentary strategy to get you started.
        Feel free to use, or delete any part of the provided code - Good luck!

        :param world: world object (more information on the documentation)
            - world: contains information about the game map.
            - world.path: contains various pathfinding helper methods.
            - world.util: contains various tile-finding helper methods.
            - world.fill: contains various flood-filling helper methods.

        :param friendly_unit: FriendlyUnit object
        :param enemy_units: list of EnemyUnit objects
        '''

        pathfinder = PathFinder(world)
        corners = [(1, 1), (world.get_width()-2, 1), (1, world.get_height()-2), (world.get_width()-2, world.get_height()-2)]
        self.turn_count += 1
        if friendly_unit.status == 'DISABLED':
            self.cornerCount = 0
            self.direction = None
        else:
            if self.cornerCount == 0:
                startpoints = []
                topleft = world.path.get_shortest_path(friendly_unit.position, corners[0], friendly_unit.snake)[0]
                topright = world.path.get_shortest_path(friendly_unit.position, corners[1], friendly_unit.snake)[0]
                botleft = world.path.get_shortest_path(friendly_unit.position, corners[2], friendly_unit.snake)[0]
                botright = world.path.get_shortest_path(friendly_unit.position, corners[3], friendly_unit.snake)[0]
                startpoints.append(topleft)
                startpoints.append(topright)
                startpoints.append(botleft)
                startpoints.append(botright)

                dist = 9999999

                for point in startpoints:
                    newdist = pathfinder.get_taxi_cab_distance(friendly_unit.position, point)
                    if newdist < dist:
                        dist = newdist
                        next_move = point
                if next_move in corners:
                    self.cornerCount += 1
            else:
                print(world.get_neighbours(friendly_unit.position))
                if self.direction is None:
                    print("abba baab @@@@@@@@@@")
                    neighbours = world.get_neighbours(friendly_unit.position)
                    print(neighbours)
                    for direction, position in neighbours.items():
                        if position not in friendly_unit.snake and not world.is_wall(position):

                            print(direction)
                            self.direction = direction

                print(self.direction)
                if self.direction == Direction.SOUTH:
                    next_move = world.path.get_shortest_path(friendly_unit.position, (friendly_unit.position[0], 28), [])[0]
                if self.direction == Direction.NORTH:
                    next_move = world.path.get_shortest_path(friendly_unit.position, (friendly_unit.position[0], 1), [])[0]
                if self.direction == Direction.EAST:
                    next_move = world.path.get_shortest_path(friendly_unit.position, (28, friendly_unit.position[1]), [])[0]
                if self.direction == Direction.WEST:
                    next_move = world.path.get_shortest_path(friendly_unit.position, (1, friendly_unit.position[1]), [])[0]
                    neighbours = world.get_neighbours(friendly_unit.position)
                if self.cornerCount == 4:
                    tileUtils = TileUtils(world, friendly_unit, None)
                    tile = tileUtils.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
                    next_move = \
                    world.path.get_shortest_path(friendly_unit.position, tile.position, friendly_unit.snake)[0]

                if next_move in corners:
                    print("FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUCK")
                    self.direction = None
                    self.cornerCount += 1

            if world.position_to_tile_map[next_move].is_friendly:
                self.cornerCount = 0
                self.direction = None
            friendly_unit.move(next_move)


            print("Turn {0}: currently at {1}, making {2} move to {3}.".format(
                str(self.turn_count),
                str(friendly_unit.position),
                'outbound' if self.outbound else 'inbound',
                str(next_move)
            ))
