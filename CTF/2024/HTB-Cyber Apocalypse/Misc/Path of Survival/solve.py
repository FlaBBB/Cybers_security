import math
from itertools import product
from typing import Dict, List, Set, Tuple

import requests

HOST = "94.237.54.170:40396"

MOVE_SET = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
OPPOSITE_MOVE = {"U": "D", "D": "U", "L": "R", "R": "L"}


def get_map():
    url = f"http://{HOST}/map"
    r = requests.post(url)
    return r.json()


def update_pos(move, get_response=True) -> dict | requests.Response:
    assert move in MOVE_SET.keys() or move in MOVE_SET.values()
    if move in MOVE_SET.values():
        move = MOVE_SET.keys()[MOVE_SET.values().index(move)]

    url = f"http://{HOST}/update"
    r = requests.post(url, json={"direction": move})
    if get_response:
        return r.json()
    return r


def updates_poses(moves: List[str], max_attempts=5) -> dict:
    res = dict()
    for move in moves:
        attempts = 0
        while True:
            if attempts > max_attempts:
                raise ValueError(f"Max attempts reached for {move}")
            res = update_pos(move, False)
            if res.status_code == 200:
                res = res.json()
                if res.get("error", None) != None:
                    return res
                break
            attempts += 1
    return res


def regenerate_maps():
    url = f"http://{HOST}/regenerate"
    r = requests.get(url)
    return "Map Regenerated" in r.text


class Terrain:
    def __init__(self, name: str, name_alias: str, allowed_entrances: List[bool]):
        self.name = name
        self.name_alias = name_alias
        self.allowed_entrances = allowed_entrances  # U, D, L, R
        self.cost: Dict["Terrain", int] = {}

    def __repr__(self) -> str:
        return f"Terrain({self.name}:{self.name_alias}, {self.allowed_entrances})"

    def __hash__(self) -> int:
        return hash(self.name + self.name_alias)

    def set_cost_to(self, terrain: "Terrain", cost: int) -> "Terrain":
        self.cost[terrain] = cost
        return self

    def print_cost(self):
        for i in self.cost:
            print(f"{self.name} -> {i.name}: {self.cost[i]}")


class TerrainManager:
    def __init__(self) -> None:
        self.terrains: List[Terrain] = list()
        self._terrains_name: Set[str] = set()
        self._terrains_name_alias: Set[str] = set()

    def add_terrain(
        self,
        name: str,
        name_alias: str,
        allowed_entrances: List[bool] = [True, True, True, True],
    ) -> Terrain:
        if name in self._terrains_name:
            raise ValueError(f"Terrain {name} already exists")
        if name_alias in self._terrains_name_alias:
            raise ValueError(f"Terrain alias {name_alias} already exists")

        terrain = Terrain(name, name_alias, allowed_entrances)
        self._terrains_name.add(name)
        self._terrains_name_alias.add(name_alias)

        self.terrains.append(terrain)
        for t in self.terrains:
            t.cost[terrain] = 1
            terrain.cost[t] = 1
        return terrain

    def __contains__(self, terrain_name: str) -> bool:
        return (
            terrain_name in self._terrains_name
            or terrain_name in self._terrains_name_alias
        )

    def __getitem__(self, terrain_name: str) -> Terrain:
        for t in self.terrains:
            if t.name == terrain_name or t.name_alias == terrain_name:
                return t
        raise KeyError(f"Terrain {terrain_name} not found")

    def get(self, terrain_name: str, default_value: any = None) -> Terrain:
        if terrain_name in self:
            return self[terrain_name]
        return default_value


# INITIALIZE TERRAINS
TM = TerrainManager()
CLIFF = TM.add_terrain("Cliff", "C", [True, False, True, False])
GEYSER = TM.add_terrain("Geyser", "G", [False, True, False, True])
MOUNTAIN = TM.add_terrain("Mountain", "M")
PLAINS = TM.add_terrain("Plains", "P")
RIVER = TM.add_terrain("River", "R")
SAND = TM.add_terrain("Sand", "S")

# SET COSTS
PLAINS.set_cost_to(MOUNTAIN, 5)
PLAINS.set_cost_to(SAND, 2)
PLAINS.set_cost_to(RIVER, 5)
MOUNTAIN.set_cost_to(PLAINS, 2)
MOUNTAIN.set_cost_to(SAND, 5)
MOUNTAIN.set_cost_to(RIVER, 8)
SAND.set_cost_to(PLAINS, 2)
SAND.set_cost_to(RIVER, 8)
SAND.set_cost_to(MOUNTAIN, 7)
RIVER.set_cost_to(PLAINS, 5)
RIVER.set_cost_to(MOUNTAIN, 10)
RIVER.set_cost_to(SAND, 6)


class Tiles:
    def __init__(
        self, x: int, y: int, has_weapon: bool, terrain: Terrain, parent=None
    ) -> None:
        self.x = x
        self.y = y
        self.has_weapon = has_weapon
        self.terrain = terrain
        self.parent = parent
        self.distance: int = math.inf
        self.visited: bool = False
        self.visited_from: Tuple[str, Tiles] = (None, None)

    def __repr__(self) -> str:
        if self.terrain == None:
            return f"Tiles({self.x}, {self.y}, {self.has_weapon}, Void)"
        return f"Tiles({self.x}, {self.y}, {self.has_weapon}, {self.terrain.name})"

    @staticmethod
    def parse_node_from_json(prop_json: dict, parent=None) -> "Tiles":
        x, y = prop_json["pos"]
        has_weapon = prop_json["has_weapon"]
        terrain = TM.get(prop_json["terrain"])
        return Tiles(x, y, has_weapon, terrain, parent)

    def _followback(self, path: List[str] = []) -> List[str]:
        if self.visited_from[1] == None:
            return path
        path = [self.visited_from[0]] + path
        return self.visited_from[1]._followback(path)

    def _allowed_to(self, move: str) -> bool:
        maps = self.parent

        x, y = MOVE_SET[move]
        new_x = self.x + x
        new_y = self.y + y
        if new_x < 0 or new_y < 0 or new_x >= maps.width or new_y >= maps.height:
            return False

        tiles: Tiles = maps.map_tiles[new_y][new_x]
        if (
            tiles.terrain == None
            or not tiles.terrain.allowed_entrances[
                list(MOVE_SET.keys()).index(OPPOSITE_MOVE[move])
            ]
            or tiles is self.visited_from[1]
        ):
            return False

        return True

    def explore(self, player_time: int) -> Tuple[bool, List[str] | None, int | None]:
        self.visited = True
        if self.distance > player_time:
            return False, None, None

        if self.has_weapon:
            return True, self._followback(), self.distance

        maps = self.parent
        allowed_moves = []

        for move in MOVE_SET.keys():
            x, y = MOVE_SET[move]
            new_x = self.x + x
            new_y = self.y + y

            # check if allowed to enter
            if not self._allowed_to(move):
                continue

            allowed_moves.append(move)

            tiles: Tiles = maps.map_tiles[new_y][new_x]

            tiles_distance = self.distance + self.terrain.cost[tiles.terrain]
            if tiles_distance < tiles.distance:
                tiles.distance = tiles_distance
                tiles.visited_from = (move, self)
                tiles.visited = False

        for move in allowed_moves:
            x, y = MOVE_SET[move]
            new_x = self.x + x
            new_y = self.y + y

            tiles: Tiles = maps.map_tiles[new_y][new_x]

            if not tiles.visited:
                is_get_weapon, path, distance = tiles.explore(player_time)
                if is_get_weapon:
                    return True, path, distance

        return False, None, None


class Maps:
    def __init__(
        self,
        width: int,
        height: int,
        map_tiles: List[List[Tiles]],
        player_pos: Tuple[int, int],
        player_time: int,
    ) -> None:
        self.width = width
        self.height = height
        self.map_tiles = map_tiles
        self.player_pos = player_pos
        self.player_time = player_time

    @staticmethod
    def parse_map_from_json(map_json: dict) -> "Maps":
        width = map_json["width"]
        height = map_json["height"]
        player_pos = tuple(map_json["player"]["position"])
        player_time = map_json["player"]["time"]
        map_tiles = [[None] * width for _ in range(height)]

        maps: Maps = Maps(width, height, map_tiles, player_pos, player_time)

        for x, y in product(range(width), range(height)):
            pos = (x, y)
            prop = map_json["tiles"][str(pos)]
            prop["pos"] = pos
            map_tiles[y][x] = Tiles.parse_node_from_json(prop, maps)

        return maps

    def find_path(self) -> List[str]:
        initial_tiles = self.map_tiles[self.player_pos[1]][self.player_pos[0]]
        initial_tiles.distance = 0
        initial_tiles.visited = True
        return initial_tiles.explore(self.player_time)[1:]


LOG_FILE = "./log.txt"


def main():
    assert regenerate_maps()
    solved_games = 0
    res = ""
    while solved_games < 100:
        map_json = get_map()
        maps = Maps.parse_map_from_json(map_json)
        path, distance = maps.find_path()
        if path == None:
            print(f"Attempt {solved_games + 1} Failed, No path found")
            assert regenerate_maps()
            solved_games = 0
            res = ""
            continue
        res = updates_poses(path)
        if res.get("solved", False):
            print(f"Attempt {solved_games + 1} Success, {distance}, {path}")
        else:
            cause = res.get("error", None)
            if cause == None:
                cause = res
            print(f"Attempt {solved_games + 1} Failed, {cause}")

            with open(LOG_FILE, "a") as f:
                f.write(f"Attempt {solved_games + 1} Failed, {cause}\n")
                f.write(f"Path: {path}\n")
                f.write(f"Player Pos: {maps.player_pos}\n")
                f.write(f"Player Time: {maps.player_time}\n")
                f.write(f"Calculated distances: {distance}\n")
                for y in range(maps.height):
                    f.write(str(maps.map_tiles[y]).replace(",", "") + "\n")
                f.write("\n")
                f.flush()

            solved_games = 0
            res = ""
            break
        solved_games = res["maps_solved"]
    print(res)


if __name__ == "__main__":
    main()
