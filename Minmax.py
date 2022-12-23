from copy import deepcopy
import Helper

INFINITY = 9999999999
MAX = 1
MIN = -1


def minmax(game, state, depth, alpha=-INFINITY, beta=INFINITY):
    current_player, _ = state

    if depth == 0:
        return (game.eval(state), state)

    elif abs(game.eval(state) == 10000):
        return (game.eval(state) - current_player * depth, state)

    else:
        # Maximizing player
        if current_player == 1:
            max_eval = - INFINITY
            # evaluates all the next states and finds the one with the higher score
            for i, next in enumerate(game.next_states(state)):
                eval, _ = minmax(game, next, depth-1, alpha, beta)
                if (eval > max_eval):
                    max_eval = eval
                    max_next_state = deepcopy(next) 
                # alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, max_next_state)

        # Minimizing player
        else:
            min_eval = INFINITY
            # evaluates all the next states and finds the one with the lower score
            for i, next in enumerate(game.next_states(state)):
                eval, _ = minmax(game, next, depth-1, alpha, beta)
                if (eval < min_eval):
                    min_eval = eval
                    min_next_state = deepcopy(next)
                # alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, min_next_state)      