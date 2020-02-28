# NOTE: coords below needs to be adaptive if we add adaptive change left hole vs right
# TODO: upgrade!
def build_defences(game_state, units, is_right_opening, filter_locs):

    # Encryptors
    encryptor_locations = [[13, 10], [14, 10]]
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

    # One more encryptor
    # encryptor_locations = [[24, 10]]
    # game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)

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

    # Encryptors
    # encryptor_locations = [[23, 10]]
    # game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)
