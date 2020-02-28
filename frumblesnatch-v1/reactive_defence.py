from collections import Counter
from operator import itemgetter

pink_destructors_points = [
    [2, 13],
    [3, 13],
    [10, 13],
    [17, 13],
    [24, 13],
    [25, 13],
    [2, 12],
    [3, 11],
    [10, 11],
    [17, 11],
    [3, 10],
    [21, 8],
    [22, 8],
]
pink_filters_points = [
    [0, 13],
    [1, 13],
    [5, 13],
    [6, 13],
    [7, 13],
    [8, 13],
    [9, 13],
    [11, 13],
    [12, 13],
    [13, 13],
    [14, 13],
    [15, 13],
    [16, 13],
    [18, 13],
    [19, 13],
    [20, 13],
    [21, 13],
    [22, 13],
    [23, 13],
    [26, 13],
    [27, 13],
]
blue_encryptors_points = [[23, 9]]
yellow_filters_points = [
    [4, 13],
    [4, 12],
    [5, 12],
    [6, 12],
    [7, 12],
    [8, 12],
    [9, 12],
    [10, 12],
    [11, 12],
    [12, 12],
    [13, 12],
    [14, 12],
    [15, 12],
    [16, 12],
    [17, 12],
    [18, 12],
    [19, 12],
    [20, 12],
    [21, 12],
    [20, 11],
    [21, 11],
    [22, 11],
    [21, 10],
    [22, 10],
    [23, 10],
    [22, 9],
]

illegal_locations = set(
    map(
        tuple,
        pink_destructors_points
        + pink_filters_points
        + blue_encryptors_points
        + yellow_filters_points,
    )
)


def build_reactive_defense(
    gamelib, game_state, units, scored_on_locations, build_amount=1
):
    """
    This function builds reactive defenses based on where the enemy scored on us from.
    We can track where the opponent scored by looking at events in action frames 
    as shown in the on_action_frame function
    """
    if len(scored_on_locations) < 1:
        return

    # Get the worst place that we gort scored on
    scored_counter = Counter(map(tuple, scored_on_locations))
    worst_scored_position = scored_counter.most_common(1)[0][0]

    # Find the path that an enemy could've taken
    path = set(map(tuple, game_state.find_path_to_edge(worst_scored_position)))
    legal_path = sorted(
        filter(lambda x: x[1] < 13, path - illegal_locations), key=itemgetter(1)
    )

    # Spawn the desired amount of reactive destructors
    spawned_destructors = 0
    while spawned_destructors < build_amount and len(legal_path) > 0:
        location = legal_path.pop()
        spawned_destructors += game_state.attempt_spawn(units.DESTRUCTOR, location)
