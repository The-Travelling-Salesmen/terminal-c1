"""
Defensive part of Snorkeldink strategy
"""


def build_defences(game_state, units, is_right_opening, filter_locs):

    # Encryptors
    encryptor_locations = [[10, 10], [17, 10]]
    game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)

    # Upgrade encryptors
    game_state.attempt_upgrade(encryptor_locations)

    # More destructors around hole/opening
    destructor_locations = (
        [[25, 12], [24, 11], [24, 10]]
        if is_right_opening
        else [[2, 12], [3, 11], [3, 10]]
    )
    game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

    # Two more encryptors
    encryptor_locations = [[10, 8], [17, 8]]
    game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)
    game_state.attempt_upgrade(encryptor_locations)

    # Upgrade filter wall if additional destructors are added
    # TODO: upgrade only some of the filters
    if all(map(game_state.contains_stationary_unit, destructor_locations)):
        game_state.attempt_upgrade(filter_locs)

    # Center Destructors
    destructor_locations = [
        [17, 11],
        [6, 8],
        [10, 11],
        [15, 9],
        [12, 9],
        [15, 6],
        [12, 6],
    ]
    game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

    # Upgrade destructors in the back
    game_state.attempt_upgrade([[3, 10], [24, 10]])
