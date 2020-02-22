

# NOTE: coords below needs to be adaptive if we add adaptive change left hole vs right
# TODO: upgrade!
def build_defences(game_state, units):
    
    # Initial destructors
    destructor_locations = [[2, 13], [3, 13], [10, 13], [17, 13], [24, 13], [25, 13]]
    # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
    game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

    if game_state.turn_number > 3:
            # Filters
            filter_locations = [[0, 13], [1, 13], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13], [11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [18, 13], [19, 13], [20, 13], [21, 13], [22, 13], [23, 13], [26, 13], [27, 13]]
            game_state.attempt_spawn(units.FILTER, filter_locations)

            # Encryptors
            encryptor_locations = [[21, 8], [22, 8], [20, 8]]
            game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)
            
            # Upgrade initial wall
            game_state.attempt_upgrade(destructor_locations)

            # Upgrade filter wall
            game_state.attempt_upgrade(filter_locations)

            # Upgrade encryptors
            game_state.attempt_upgrade(encryptor_locations)

            # More destructors around hole/opening
            destructor_locations = [[2, 12], [3, 11]]
            game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

            # One more encryptor
            encryptor_locations = [[24, 10]]
            game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)

            # Destructors
            destructor_locations = [[3, 10], [17, 11], [6, 8], [10, 11], [15, 9], [12, 9], [15, 6], [12, 6]]
            game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)

            # Encryptors
            encryptor_locations = [[23, 10]]
            game_state.attempt_spawn(units.ENCRYPTOR, encryptor_locations)
