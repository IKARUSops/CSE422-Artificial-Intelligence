# Part 1

import random

class MortalKombat:
    def __init__(self):
        self.LEAF_VALUES = [random.choice([-1, 1]) for _ in range(8)]

    def minimax(self, node_index, depth, is_maximizing):
        if depth == 0 or node_index >= len(self.LEAF_VALUES):
            return self.LEAF_VALUES[node_index]
        
        if is_maximizing:
            return max(self.minimax(node_index * 2 + i, depth - 1, False) for i in range(2))
        else:
            return min(self.minimax(node_index * 2 + i, depth - 1, True) for i in range(2))

    def simulate_game(self, start_player):
        depth = 3
        root_node = 0
        players = {1: 'Sub-Zero', -1: 'Scorpion'}
        rounds = 5
        round_results = []
        scorpion_wins = 0
        sub_zero_wins = 0

        for round_num in range(1, rounds + 1):
            self.LEAF_VALUES = [random.choice([-1, 1]) for _ in range(8)]
            winner_value = self.minimax(root_node, depth, start_player == 1)
            winner = players[winner_value]
            round_results.append(f"Winner of Round {round_num}: {winner}")

            if winner_value == -1:
                scorpion_wins += 1
            else:
                sub_zero_wins += 1

            start_player = 1 - start_player

        game_winner = "Scorpion" if scorpion_wins > sub_zero_wins else "Sub-Zero"

        print(f"Game Winner: {game_winner}")
        print(f"Total Rounds Played: {rounds}")
        for result in round_results:
            print(result)

inp = int(input('Select starting player (0 for Scorpion, 1 for Sub-Zero): '))

game = MortalKombat()
game.simulate_game(start_player=inp)


class MortalKombatPrune:
    def __init__(self):
        # Define utility values for leaf nodes (same across all rounds)
        self.LEAF_VALUES = [random.choice([-1, 1]) for _ in range(8)]
        # print(f"Leaf Values: {self.LEAF_VALUES}\n")

    def alpha_beta(self, node_index, depth, alpha, beta, is_maximizing):
        """Alpha-beta pruning algorithm."""
        if depth == 0 or node_index >= len(self.LEAF_VALUES):
            return self.LEAF_VALUES[node_index]

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(2):  # Two children per node
                eval = self.alpha_beta(node_index * 2 + i, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Prune remaining branches
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(2):  # Two children per node
                eval = self.alpha_beta(node_index * 2 + i, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Prune remaining branches
                    break
            return min_eval

    def simulate_game(self, start_player):
        """Simulate the Mortal Kombat game."""
        depth = 3  # Tree depth
        root_node = 0  # Start at the root
        players = {1: 'Sub-Zero', -1: 'Scorpion'}
        rounds = 5  # Number of rounds
        round_results = []
        scorpion_wins = 0
        sub_zero_wins = 0

        for round_num in range(1, rounds + 1):
            # print(f"\n--- Round {round_num} ---")
            winner_value = self.alpha_beta(root_node, depth, float('-inf'), float('inf'), start_player == 1)
            winner = players[winner_value]
            round_results.append(f"Winner of Round {round_num}: {winner}")

            # Update win counts
            if winner_value == -1:
                scorpion_wins += 1
            else:
                sub_zero_wins += 1

            # Alternate starting player for the next round
            start_player = 1 - start_player

        # Determine the overall game winner
        game_winner = "Scorpion" if scorpion_wins > sub_zero_wins else "Sub-Zero"

        # Display results
        print(f"Game Winner: {game_winner}")
        print(f"Total Rounds Played: {rounds}")
        for result in round_results:
            print(result)

# Input from user for starting player
inp = int(input('Select starting player (0 for Scorpion, 1 for Sub-Zero): '))

# Create Mortal Kombat game instance and run the simulation
game = MortalKombatPrune()
game.simulate_game(start_player=inp)





# Part 2



def pacman_game(c):
    # Leaf node values
    leaf_values = [3, 6, 2, 3, 7, 1, 2, 0]

    # Minimax function with dark magic consideration
    def minimax(depth, index, is_pacman, cost):
        if depth == 3:  # Leaf nodes
            return leaf_values[index]

        if is_pacman:  # Pacman's turn
            left_value = minimax(depth + 1, index * 2, False, cost)
            right_value = minimax(depth + 1, index * 2 + 1, False, cost)
            return max(left_value, right_value)
        else:  # Ghost's turn
            # Without dark magic
            without_magic_left = minimax(depth + 1, index * 2, True, cost)
            without_magic_right = minimax(depth + 1, index * 2 + 1, True, cost)
            without_magic = min(without_magic_left, without_magic_right)

            # With dark magic
            with_magic_left = minimax(depth + 1, index * 2, True, cost)
            with_magic_right = minimax(depth + 1, index * 2 + 1, True, cost)
            with_magic = max(with_magic_left, with_magic_right) - cost

            # Compare the two strategies
            if without_magic > with_magic:
                return without_magic
            else:
                return with_magic

    # Determine Pacman's first move
    left_value = minimax(1, 0, False, c)  # Pacman goes left
    right_value = minimax(1, 1, False, c)  # Pacman goes right

    if left_value > right_value:
        first_move = "left"
    else:
        first_move = "right"

    # Check if dark magic was used
    dark_magic_used = left_value <= right_value

    if dark_magic_used:
        return f"The new minimax value is {max(left_value, right_value)}. Pacman goes {first_move} and uses dark magic."
    else:
        return f"The new minimax value is {max(left_value, right_value)}. Pacman goes {first_move} and doesnot use dark magic.."

# Example usage
c = int(input("Enter the cost of dark magic(c): "))
print(pacman_game(c))



def pacman_alpha_beta(c):
    # Leaf node values
    leaf_values = [3, 6, 2, 3, 7, 1, 2, 0]

    # Minimax function with Alpha-Beta pruning
    def minimax(depth, index, is_pacman, alpha, beta):
        if depth == 3:  # Leaf nodes
            return leaf_values[index]

        if is_pacman:  # Pacman's turn
            max_value = float('-inf')

            for i in range(2):
                value = minimax(depth + 1, index * 2 + i, False, alpha, beta)
                max_value = max(max_value, value)
                alpha = max(alpha, max_value)

                if beta <= alpha:
                    break

            return max_value

        else:  # Ghost's turn
            min_value = float('inf')

            for i in range(2):
                value = minimax(depth + 1, index * 2 + i, True, alpha, beta)
                min_value = min(min_value, value)
                beta = min(beta, min_value)

                if beta <= alpha:
                    break

            return min_value

    # Final value of the root node without using dark magic
    root_value = minimax(0, 0, True, float('-inf'), float('inf'))

    # Determine Pacman's first move without dark magic
    left_value = minimax(1, 0, False, float('-inf'), float('inf'))  # Pacman goes left
    right_value = minimax(1, 1, False, float('-inf'), float('inf'))  # Pacman goes right

    # Determine Pacman's first move without dark magic
    first_move = "left" if left_value > right_value else "right"

    # Check if using dark magic is advantageous
    dark_magic_used = False
    if root_value - c > right_value:
        dark_magic_used = True

    # Determine whether dark magic is advantageous
    if dark_magic_used:
        print(f"The new minimax value is {root_value - c}. Pacman goes {first_move} and uses dark magic.")
    else:
        print(f"The new minimax value is {root_value}. Pacman goes {first_move} and does not use dark magic.")

# Example usage
c = int(input("Enter the cost of dark magic (c): "))
pacman_alpha_beta(c)
