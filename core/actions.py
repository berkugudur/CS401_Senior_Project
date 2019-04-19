import numpy as np

ACTION_MAP = {
    'BASE': ['AIR', 'CROUCH', 'STAND'],
    'MOVE': ['BACK_JUMP', 'BACK_STEP', 'DASH', 'FOR_JUMP', 'FORWARD_WALK', 'JUMP'],
    'GUARD': ['AIR_GUARD', 'CROUCH_GUARD', 'STAND_GUARD'],
    'RECOV': ['AIR_GUARD_RECOV', 'AIR_RECOV', 'CHANGE_DOWN', 'CROUCH_GUARD_RECOV', 'CROUCH_RECOV', 'DOWN', 'LANDING',
              'RISE', 'STAND_GUARD_RECOV', 'STAND_RECOV', 'THROW_HIT', 'THROW_SUFFER'],
    'SKILL': ['AIR_A', 'AIR_B', 'AIR_DA', 'AIR_DB', 'AIR_FA', 'AIR_D_DB_BA', 'AIR_D_DB_BB', 'AIR_D_DF_FA', 'AIR_D_DF_FB',
              'AIR_FA', 'AIR_FB', 'AIR_F_D_DFA', 'AIR_F_D_DFB', 'AIR_UA', 'AIR_UB', 'CROUCH_A', 'CROUCH_B', 'CROUCH_FA',
              'CROUCH_FB', 'STAND_A', 'STAND_B', 'STAND_FA', 'STAND_FB', 'STAND_D_DB_BA', 'STAND_D_DB_BB', 'STAND_D_DF_FA',
              'STAND_D_DF_FB', 'STAND_D_DF_FC', 'STAND_F_D_DFA', 'STAND_F_D_DFB', 'THROW_A', 'THROW_B']
}

DISTINCT_ACTIONS = [
    'JUMP', 'STAND_FA', 'CROUCH', 'THROW_HIT', 'AIR_F_D_DFB', 'STAND_GUARD_RECOV', 'STAND_D_DB_BB', 'AIR_DB', 
    'CROUCH_B', 'CROUCH_FB', 'AIR_FB', 'STAND_D_DF_FB', 'BACK_STEP', 'CHANGE_DOWN', 'BACK_JUMP', 'AIR_GUARD_RECOV', 'AIR_D_DF_FA', 
    'AIR_D_DF_FB', 'AIR_F_D_DFA', 'AIR_UA', 'THROW_A', 'AIR_DA', 'CROUCH_GUARD', 'STAND_RECOV', 'FORWARD_WALK', 'AIR_RECOV', 'AIR_UB', 
    'AIR_D_DB_BA', 'STAND_D_DB_BA', 'LANDING', 'STAND_F_D_DFB', 'STAND_FB', 'CROUCH_GUARD_RECOV', 'STAND_D_DF_FC', 'THROW_B', 'STAND', 
    'AIR_D_DB_BB', 'STAND_D_DF_FA', 'STAND_F_D_DFA', 'STAND_GUARD', 'DOWN', 'STAND_B', 'THROW_SUFFER', 'DASH', 'CROUCH_FA', 'RISE', 
    'AIR_GUARD', 'CROUCH_RECOV', 'STAND_A', 'CROUCH_A', 'AIR_B', 'AIR_FA', 'AIR', 'FOR_JUMP', 'AIR_A'
    ]

HP_DIFS = [-5,-4,-3,-2,-1,0,1,2,3,4,5]

def one_hot_encode(column):
    encoded = []
    for action in column:
        encoded.append(_encode(action))
    return encoded

def decode(action):
    int_rep = np.argmax(action)
    return DISTINCT_ACTIONS[int_rep]

def _encode(action):
    int_rep  = DISTINCT_ACTIONS.index(action)
    one_hot = [0] * len(DISTINCT_ACTIONS)
    one_hot[int_rep] = 1
    return one_hot
	
def one_hot_encode_hpdif(hpdifs):
    encoded = []
    for hpdif in hpdifs:
        one_hot = [0] * len(HP_DIFS)
        one_hot[HP_DIFS.index(hpdif)] = 1
        encoded.append(one_hot)
    return encoded