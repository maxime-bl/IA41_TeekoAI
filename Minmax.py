game_over = False
INFINITY = 9999999999
MAX = 1
MIN = -1


def minmax(game, state, depth, alpha=-INFINITY, beta=INFINITY):
    # TODO implementer game over
    if depth == 0 or game_over:
        return (game.eval(state), state)

    else:
        current_player, grid = state
        # Maximizing player
        if current_player == 1:
            max_eval = - INFINITY
            # evaluates all the next states and finds the one with the higher score
            for next in game.next_states(state):
                eval = minmax(game, next, depth-1, alpha, beta)[0]
                if (eval > max_eval):
                    max_eval = eval
                    max_next_state = next
                # alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, max_next_state)

        else:
            min_eval = INFINITY
            # evaluates all the next states and finds the one with the lower score
            for next in game.next_states(state):
                eval = minmax(game, next, depth-1, alpha, beta)[0]
                # min_eval = min(eval, min_eval)
                if (eval < min_eval):
                    min_eval = eval
                    min_next_state = next
                # alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, min_next_state)