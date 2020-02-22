import random
from operator import itemgetter

""" Adaptive opening defence. 
    Assesses the enemy's defence and makes an opening, so that our EMPs attack weaker side."""
def build_defences_with_adaptive_opening(game_state, units, enemy_vulnerable_side, filter_locs):
        # Place destructors that attack enemy units
        destructor_locations = [[2, 13], [3, 13], [10, 13], [17, 13], [24, 13], [25, 13]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        game_state.attempt_spawn(units.DESTRUCTOR, destructor_locations)
        
        # Find the weaker side of enemy's defence
        # Open up our filter defence towards that side
        if game_state.turn_number > 3 and game_state.turn_number % 4 == 0:
            new_vulnerable_side = find_weaker_side(game_state, units) # change to detect less loaded enemy def's side. 1 is right, 0 is left.
            
            if enemy_vulnerable_side != new_vulnerable_side:
                if new_vulnerable_side == 1:
                    remove_filter_at = [[23, 13]]
                else:
                    remove_filter_at = [[4, 13]]
                
                game_state.attempt_remove(remove_filter_at)

            if new_vulnerable_side == 1:
                try:
                    filter_locs.remove([23, 13]) # Remove blocker FILTER on right
                except ValueError: # Dump the exception if the filter hasn't been built or was destroyed.
                    pass
                
                filter_locs.append([4, 13]) # Add blocker FILTER on left
                filter_locs.sort(key=itemgetter(1))
            else:
                try:
                    filter_locs.remove([4, 13]) # Remove blocker FILTER on left
                except ValueError: # Dump the exception if the filter hasn't been built or was destroyed.
                    pass
                
                filter_locs.append([23, 13]) # Add blocker FILTER on right
                filter_locs.sort(key=itemgetter(0), reverse=True)
       
        # Place filters in front of destructors to soak up damage for them
        game_state.attempt_spawn(units.FILTER, filter_locs)
        # upgrade filters so they soak more damage
        game_state.attempt_upgrade(filter_locs)

""" Assess enemy defence & identify weaker side (for opening)
    Author @RKJ (blame me for the mistakes) """
def find_weaker_side(game_state, units, weights = None):
    if not weights:
        weights = [1, 6] # filter is worth 1 badness pt, destructor - 6 badness pts.
    
    weights_by_def_unit = dict(zip([units.FILTER, units.DESTRUCTOR], weights))

    left_strength, right_strength = (0, 0)

    for location in game_state.game_map:
        if game_state.contains_stationary_unit(location):
            for unit in game_state.game_map[location]:
                if unit.player_index == 1 and (unit.unit_type is units.DESTRUCTOR or unit.unit_type == units.FILTER):
                    if location[0] < 14:
                        left_strength += weights_by_def_unit[unit.unit_type]
                    else:                    
                        right_strength += weights_by_def_unit[unit.unit_type]
    
    # Return side with less strength
    if left_strength > right_strength:
        weaker_side = 1
    elif left_strength < right_strength:
        weaker_side = 0
    else:
        weaker_side = random.randint(0, 1)
    return weaker_side