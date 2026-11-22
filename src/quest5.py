from collections.abc import Iterable

from ecd import get_inputs, submit


def parse_data(data: dict[str, str]) -> dict[str, dict[tuple[int, int], str]]:
    """Parse the input map as a dict of coordinates and their value

    Args:
        data (dict[str, str]): The input data from the ecd interface

    Returns:
        dict[str, dict[tuple[int, int], str]]: Dict for each part with the map as the value
    """
    return {k: {(x, y): c for y, line in enumerate(grid.splitlines()) for x, c in enumerate(line)} for k, grid in data.items()}

def inbounds(bounds: tuple[int, int], land: tuple[int, int]) -> bool:
    """Determine if a coordinate is within the bounds of the grid.
    Assumes grid position starts at 0

    Args:
        bounds (tuple[int, int]): max x and y values of the grid
        land (tuple[int, int]): the coordinate to be tested

    Returns:
        bool: True if land is in bounds
    """
    maxx, maxy = bounds
    x, y = land
    return maxx >= x >= 0 and maxy >= y >= 0

def neighbors(x: int, y: int, rn: int = 1, include_corners: bool = True) -> Iterable[tuple[int, int]]:
    """Get the neighbors of a point.
    Can get the n-neighborhood with the option to remove corners from the neighbors

    Args:
        x (int): x coordinate
        y (int): y coordinate
        rn (int, optional): The selected neighborhood distance (1 corresponds to 8-neighborhood and so on). Defaults to 1.
        include_corners (bool, optional): Include corners in the output. Defaults to True.

    Returns:
        Iterable[tuple[int, int]]: List of neighbors in the defined neighborhood.
    """
    return [(x + xa, y + ya) for xa in range(-rn, 1 + rn, 1) for ya in range(-rn, 1 + rn, 1) 
            if not (xa == 0 and ya == 0)
            and (include_corners or not (xa == -rn and ya == -rn or xa == -rn and ya == rn or xa == rn and ya == rn or xa == rn and ya == -rn))]

def print_grid(grid: dict[tuple[int, int], str]) -> None:
    """Function to print a grid to the console.
    Useful for debugging.

    Args:
        grid (dict[tuple[int, int], str]): Grid to be printed in the console.
    """
    # bounds parameters
    maxx, maxy = max(x for x, _ in grid), max(y for _, y in grid)
    grid_str = '\n'
    for y in range(maxy + 1):
        grid_str += f"{''.join(grid[(x, y)] for x in range(maxx + 1))}\n"
    print(grid_str)

def apply_mask(grid: dict[tuple[int, int], str], maxx: int, maxy: int, p: tuple[int, int]) -> bool:
    """Apply the mask from the input on a point in the grid.
    Assumes grid starts at 0.

    Args:
        grid (dict[tuple[int, int], str]): The input grid
        maxx (int): Bound in the x-direction
        maxy (int): Bound in the y-direction
        p (tuple[int, int]): Point on the grid

    Returns:
        bool: True if the mask can be applied, False otherwise
    """
    x, y = p
    if 2 <= x <= maxx - 2 and 2 <= y <= maxy - 2: # mask can not be applied
        # using index here is safe, because all mask neighbors are guaranteed to be in bounds
        return grid[p] == '#' and all(grid[n] in ('#', '@') for n in neighbors(*p, 2, False))
    return False
    
def create_land(data: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    """Function to create a map with land (#) characters from the input grid.
    Turns all other points on the map to water characters (.).

    Args:
        data (dict[tuple[int, int], str]): Input data for the part.

    Returns:
        dict[tuple[int, int], str]: Map with land and water characters.
    """
    # bounds parameters
    maxx, maxy = max(x for x, _ in data), max(y for _, y in data)
    # get values for center of the map
    sx, sy = maxx // 2, maxy // 2
    # copy of data to work on in each step
    grid = {k:v for k,v in data.items()}
    # initial values
    grid[(sx, sy)] = '#'
    frontier = {n for n in neighbors(sx, sy)}
    # grow the frontier of land characters
    while len(frontier) != 0:
        # transformations happen in one step from the previous iteration - no input from current iteration
        step = {k:v for k, v in grid.items()}
        new_frontier = set()
        for f in frontier:
            ns = neighbors(*f)
            if len([n for n in ns if grid.get(n) in ('#', '1')]) >= 5:
                step[f] = '#'
                new_frontier = new_frontier.union({n for n in ns if inbounds((maxx, maxy), n) and step.get(n) != '#'})
        grid = step
        frontier = new_frontier
    grid = {k: v if v == '#' else '.' for k, v in grid.items()} # water conversion at the end
    return grid

def create_sand(data: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    """Add sand (=) characters to a map with land and water characters.

    Args:
        data (dict[tuple[int, int], str]): (Square) Map with water and land characters.

    Returns:
        dict[tuple[int, int], str]: Transformed map with water, land and sand characters.
    """
    # bounds parameters
    maxx, maxy = max(x for x, _ in data), max(y for _, y in data)
    # create the shoreline: any land that borders on water or is at the border
    grid = {k: '=' if v == '#' and any(data.get(n, '.') == '.' for n in neighbors(*k)) else v for k,v in data.items()}
    frontier = {n for k, v in grid.items() for n in neighbors(*k) if v == '=' and grid.get(n) == '#'}
    # grow the frontier of the shoreline
    while len(frontier) != 0:
        # transformations happen in one step from the previous iteration - no input from current iteration
        step = {k:v for k, v in grid.items()}
        new_frontier = set()
        for f in frontier:
            ns = neighbors(*f)
            if len([n for n in ns if grid.get(n) == '=']) >= 5:
                step[f] = '='
                new_frontier = new_frontier.union({n for n in ns if inbounds((maxx, maxy), n) and step.get(n) == '#'})
        grid = step
        frontier = new_frontier
    return grid

def create_trees(data: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    """Add tree (@) characters to a map with water, land and sand characters.

    Args:
        data (dict[tuple[int, int], str]): (Square) Map with water, land and sand characters.

    Returns:
        dict[tuple[int, int], str]: Transformed map with water, land, sand and tree characters.
    """
    # bounds parameters
    maxx, maxy = max(x for x, _ in data), max(y for _, y in data)
    # step one: find all trees with the mask
    mask_trees = True
    grid = {k: v for k, v in data.items()}
    while mask_trees:
        # transformations happen in one step from the previous iteration - no input from current iteration
        mask_trees = False
        step = {k: v for k, v in grid.items()}
        for l in filter(lambda l: grid[l] == '#', grid):
            if apply_mask(grid, maxx, maxy, l):
                step[l] = '@'
                mask_trees = True
        grid = step
    # step two: grow the forest for two steps
    for _ in range(2):
        # transformations happen in one step from the previous iteration - no input from current iteration
        step = {k: v for k, v in grid.items()}
        for l in filter(lambda l: grid[l] == '#', grid):
            ns = neighbors(*l)
            if all(grid[n] in ('#', '@') for n in ns) and sum(1 for n in ns if grid[n] == '@') >= 4:
                step[l] = '@'
        grid = step  
    return grid
    
def part1(data: dict[tuple[int, int], str]) -> int:
    grid = create_land(data)
    return sum(1 for _ in filter(lambda l: grid[l] == '#', grid))

def part2(data: dict[tuple[int, int], str]) -> int:
    grid = create_sand(create_land(data))
    return sum(1 for _ in filter(lambda l: grid[l] == '=', grid))

def part3(data: dict[tuple[int, int], str]) -> int:
    grid = create_trees(create_sand(create_land(data)))
    return sum(1 for _ in filter(lambda l: grid[l] == '@', grid))

if __name__ == "__main__":
    QUEST = 5
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))