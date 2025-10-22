from aegis_game.stub import *

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


def think() -> None:
    """Do not remove this function, it must always be defined."""
    log("Thinking")

    # On the first round, send a request for surrounding information
    # by moving to the center (not moving). This will help initiate pathfinding.

    if get_round_number() == 1:
        # move(Direction.CENTER)
        # send_message("hello world", [])  # Broadcast to all teammates
        # log(get_cell_info_at(Location(4, 4)))
        log("Before", get_location())
        log(get_cell_info_at(Location(4, 4)))
        # drone_scan(Location(0, 0))
        drone_scan(Location(4, 4))
        return

    if get_round_number() == 3:
        log("Has anything changed?", get_location())
        # log(get_cell_info_at(Location(0, 0)))
        # log(get_cell_info_at(Location(1, 1)))
        log(get_cell_info_at(Location(4, 4)))

    # On subsequent rounds, read and log all received messages.
    messages = read_messages()
    log(messages)
    # log("Energy =", get_energy_level())

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
