# Names:
# Date:
# Course: CPSC383F25
# Tutorial: T02
from aegis_game.stub import *
import heapq
import math


# Return estimated cost of getting from x to y for A*
# Use Chebyshev dist as our heuristic
def heuristic(next: Location, goal: Location):
    x1, y1 = next.x, next.y
    x2, y2 = goal.x, goal.y
    # return ((x2 - x1)**2 + (y2 - y1)**2)**0.5 # Euclidean dist
    # return abs(x1 - x2) + abs(y1 - y2) # Manhattan dist does not account for diagonal!
    return max(abs(x1 - x2),
               abs(y1 - y2))  # Chebyshev dist appears to perform better for v3


# NOTE: Tie break precedence
# N > NE > E > SE > S > SW > W > NW > C
# Apparently dictionaries are ordered since Python 3.7, so
# we can iterate over keys in order to preserve this order
neighbour_offsets = {
    (0, 1): Direction.NORTH,
    (1, 1): Direction.NORTHEAST,
    (1, 0): Direction.EAST,
    (1, -1): Direction.SOUTHEAST,
    (0, -1): Direction.SOUTH,
    (-1, -1): Direction.SOUTHWEST,
    (-1, 0): Direction.WEST,
    (-1, 1): Direction.NORTHWEST,
    # (0, 0): Direction.CENTER
}

# https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Above link referenced for A* implementation


# Get the path from start->goal based on heuristic()
# Implicitly assume unexplored nodes are cost 1,
# while rerunning astar() will allow for seeing more true costs
def astar(start_loc: Location, goal: Location):
    # Frontier tracks "places to visit next"
    # As a min pqueue (using heapq library)
    frontier = []

    # Store 4 things within frontier for priority & convenience
    # 1) priority (for main cost comparison),
    # 2) index # from neighbour_offsets (to handle tie-breaking)
    # 3) Location of the cell itself
    heapq.heappush(frontier, (0, 0, start_loc))

    came_from = dict()
    cost_so_far = dict()
    came_from[start_loc] = None
    cost_so_far[start_loc] = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)

        # Early exit if already on goal
        if (current == goal):
            break

        # Check neighbours of current cell and evaluate their priority
        # Use index for tie-breaking, since keys are ordered by expected
        # order from assignment doc for direction to use
        for index, (x, y) in enumerate(neighbour_offsets.keys()):
            next = Location(current.x + x, current.y + y)
            # Do not consider out of bounds of killer cells as an option
            if not on_map(next) or get_cell_info_at(next).is_killer_cell():
                continue

            # Update data for neighbour nodes & our pqueue
            new_cost = cost_so_far[current] + get_cell_info_at(next).move_cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                heapq.heappush(frontier, (priority, index, next))
                came_from[next] = current

    # Return ability for caller to reconstruct ideal path (known-so-far)
    return came_from


def think() -> None:
    """Do not remove this function, it must always be defined."""
    log("Thinking")

    # On the first round, send a request for surrounding information
    # by moving to the center (not moving). This will help initiate pathfinding.

    if get_round_number() == 1:
        move(Direction.CENTER)
        send_message("hello world", [])  # Broadcast to all teammates
        # drone_scan(Location(0, 0))
        return

    # On subsequent rounds, read and log all received messages.
    messages = read_messages()
    log(messages)

    # Fetch the cell at the agent's current location.
    # If you want to check a different location, use `on_map(loc)` first
    # to ensure it's within the world bounds. The agent's own location is always valid.
    cell = get_cell_info_at(get_location())

    # Get the top layer at the agent's current location.
    # If a survivor is present, save it and end the turn.
    top_layer = cell.top_layer
    if isinstance(top_layer, Survivor):
        save()
        return

    # Default action: Move the agent north if no other specific conditions are met.
    ne_loc = get_location().add(Direction.NORTHEAST)
    if (on_map(ne_loc)):
        move(Direction.NORTHEAST)
    else:
        move(Direction.CENTER)
