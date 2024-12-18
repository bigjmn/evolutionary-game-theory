import numpy as np 
# Array shufflers for creating random indices (for matches)
def play_round(arr_len, pnum_in_game):
    cutoff_needed = arr_len%pnum_in_game 
    rand_shuff = np.random.choice(arr_len, arr_len, replace=False)
    rand_groups = np.reshape(rand_shuff[cutoff_needed:],(-1, pnum_in_game))
    return rand_groups

def iterate_matches(arr_len, pnum_in_game, iters):
    matchlist = [np.random.choice(arr_len, pnum_in_game, replace=False) for _ in range(iters)]
    return np.array(matchlist)