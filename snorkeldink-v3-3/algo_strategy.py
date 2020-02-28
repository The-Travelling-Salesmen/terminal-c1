import json
import math
import random
import warnings
from collections import namedtuple
from sys import maxsize

import gamelib
from adaptive_opening import build_defences_with_adaptive_opening
from defence import build_defences


"""
Strategy-code for the final version of Snorkeldink-V69
"""


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write("Random seed: {}".format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        # Initial setup
        Units = namedtuple("Units", "FILTER ENCRYPTOR DESTRUCTOR PING EMP SCRAMBLER")
        self.units = Units(FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER)

        # Initially assume right side is vulnerable
        self.is_right_opening = True
        self.filter_locs = [
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
            [26, 13],
            [27, 13],
        ]

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write(
            f"Performing turn {game_state.turn_number} of Snorkeldink-V69 algo strategy"
        )

        # Comment or remove this line to enable warnings.
        game_state.suppress_warnings(True)

        # Calculate next moves based on strategy
        self.strategy(game_state)

        # Submit the moves
        game_state.submit_turn()

    def strategy(self, game_state):

        # Initial wall defence
        # Adaptive opening side selection
        filter_locs, self.is_right_opening, save_cores = build_defences_with_adaptive_opening(
            game_state, self.units, self.is_right_opening, self.filter_locs
        )

        if game_state.turn_number > 3:
            # Defence
            if not save_cores:
                build_defences(
                    game_state, self.units, self.is_right_opening, filter_locs
                )

            # Offense
            if self.is_right_opening:
                emp_location = [[4, 9]]
            else:
                emp_location = [[23, 9]]
            game_state.attempt_spawn(EMP, emp_location, 1000)

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x=None, valid_y=None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if (
                        unit.player_index == 1
                        and (unit_type is None or unit.unit_type == unit_type)
                        and (valid_x is None or location[0] in valid_x)
                        and (valid_y is None or location[1] in valid_y)
                    ):
                        total_units += 1
        return total_units


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
