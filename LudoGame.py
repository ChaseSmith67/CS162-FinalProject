# Author: Chase Smith
# GitHub username: ChaseSmith67
# Date: 7/30/22
# Description: A board game called Ludo. Played by 2 to 4 players. Each player has two tokens
#               which they move around a game board by rolling a die. The first player to have
#               both of their tokens reach the end space wins the game


class LudoGame:
    """represents the game as played"""
    def __init__(self):
        """initializes the LudoGame class, creating a player list"""
        self._players_list = []

    def get_player_by_position(self, position):
        """takes as a parameter a player position as a string and
            returns the appropriate Player object"""
        temp_player_list = []
        for player in self._players_list:
            temp_player_list.append(player.get_position())
            if player.get_position() == position:
                return player
        if position not in temp_player_list:
            return "Player Not Found!"

    def move_token(self, position, token, steps):
        """used to move a player's token from one space on the
            board to another"""
        player = self.get_player_by_position(position)

        if token == "p":
            player.set_token_p(steps)
        if token == "q":
            player.set_token_q(steps)

    def play_game(self, players, turns):
        """Takes as parameters a list of players and a list of turns as tuples consisting
        of the player and the number rolled on the die. Returns a list of the players'
        tokens' spaces after all the turns have occurred."""
        for player in players:
            player = Player(player)
            self._players_list.append(player)

        for turn in turns:  # iterate through each turn
            player_position = turn[0]
            steps = turn[1]

            for player in self._players_list:

                if player_position == player.get_position():  # select appropriate player
                    current_p_space = player.get_token_p_space()
                    current_p_index = player.get_board().index(current_p_space)
                    current_q_space = player.get_token_q_space()
                    current_q_index = player.get_board().index(current_q_space)

                    if current_p_space != "E":
                        player.set_token_p_moved()  # These reset the token_moved Boolean for the
                    if current_q_space != "E":      # player, used to prevent accidental double moves
                        player.set_token_q_moved()  # not reset if token is on "E"

                    # check to see if player has already finished the game
                    if current_p_space == current_q_space:
                        if current_p_space == "E":
                            player.set_completed()
                            continue
                    if player.get_completed() == True:
                        continue
                    # first move for player - only moves if a 6 is rolled
                    if current_p_space == "H" and current_q_space == "H":
                        if steps != 6:
                            continue
                        else:
                            self.move_token(player_position, "p", 1)  # first move, p moves first
                            continue

                    # after p moves, q will go if 6 is rolled
                    elif current_p_space != "H" and current_q_space == "H":
                        if steps == 6:
                            self.move_token(player_position, "q", 1)
                            continue
                        else:
                            # check for other player token on space
                            for other_player in self._players_list:
                                if player_position != other_player.get_position():
                                    other_player_p_space = other_player.get_token_p_space()
                                    other_player_p_index = other_player.get_board().index(other_player_p_space)
                                    other_player_q_space = other_player.get_token_q_space()
                                    other_player_q_index = other_player.get_board().index(other_player_q_space)
                                    # kick other player's tokens, if on space
                                    # only check to kick of not in home squares
                                    if (current_p_index + steps) < 52:
                                        if player.get_token_p_moved() == False:
                                            if player.get_board()[current_p_index + steps] == other_player_p_space:
                                                self.move_token(player_position, "p", steps)
                                                other_player.set_token_p("kick")
                                                # if the other player's tokens are stacked
                                                if other_player_q_space == other_player_p_space:
                                                    other_player.set_token_q("kick")
                                                continue
                                            elif player.get_board()[current_p_index + steps] == other_player_q_space:
                                                self.move_token(player_position, "p", steps)
                                                other_player.set_token_q("kick")
                                                # if the other player's tokens are stacked
                                                if other_player_q_space == other_player_p_space:
                                                    other_player.set_token_p("kick")
                                                continue
                                            else:
                                                self.move_token(player_position, "p", steps)
                                                continue
                                    else:
                                        self.move_token(player_position, "p", steps)
                                        continue

                    # if move will put token on "E", make that move
                    if (current_p_index + steps) <= 58 and (current_q_index + steps) <= 58:
                        if player.get_board()[current_p_index + steps] == player.get_board()[58]:
                            if player.get_token_p_moved() == False:
                                self.move_token(player_position, "p", steps)
                                # check to see if tokens are stacked
                                if current_p_space == current_q_space:
                                    self.move_token(player_position, "q", steps)
                                continue
                        if player.get_board()[current_q_index + steps] == player.get_board()[58]:
                            if player.get_token_q_moved() == False:
                                self.move_token(player_position, "q", steps)
                                # check to see if tokens are stacked
                                if current_p_space == current_q_space:
                                    self.move_token(player_position, "p", steps)
                                continue

                    # check for if other player token is on space - make that move to kick
                    for other_player in self._players_list:
                        if player_position != other_player.get_position():
                            other_player_p_space = other_player.get_token_p_space()
                            other_player_q_space = other_player.get_token_q_space()
                            if (current_p_index + steps) <= 58 and (current_q_index + steps) <= 58:
                                if player.get_board()[current_p_index + steps] == other_player_p_space:
                                    self.move_token(player_position, "p", steps)
                                    # check to see if tokens are stacked
                                    if current_p_space == current_q_space:
                                        self.move_token(player_position, "q", steps)
                                    other_player.set_token_p("kick")
                                    # check to see if opponent's tokens are stacked
                                    if other_player_q_space == other_player_p_space:
                                        other_player.set_token_q("kick")
                                    continue
                                elif player.get_board()[current_p_index + steps] == other_player_q_space:
                                    self.move_token(player_position, "p", steps)
                                    # check to see if tokens are stacked
                                    if current_p_space == current_q_space:
                                        self.move_token(player_position, "q", steps)
                                    other_player.set_token_q("kick")
                                    # check to see if opponent's tokens are stacked
                                    if other_player_q_space == other_player_p_space:
                                        other_player.set_token_p("kick")
                                    continue
                                elif player.get_board()[current_q_index + steps] == other_player_p_space:
                                    self.move_token(player_position, "q", steps)
                                    # check to see if tokens are stacked
                                    if current_p_space == current_q_space:
                                        self.move_token(player_position, "p", steps)
                                    other_player.set_token_p("kick")
                                    # check to see if opponent's tokens are stacked
                                    if other_player_q_space == other_player_p_space:
                                        other_player.set_token_q("kick")
                                    continue
                                elif player.get_board()[current_q_index + steps] == other_player_q_space:
                                    self.move_token(player_position, "q", steps)
                                    # check to see if tokens are stacked
                                    if current_p_space == current_q_space:
                                        self.move_token(player_position, "p", steps)
                                    other_player.set_token_q("kick")
                                    # check to see if opponent's tokens are stacked
                                    if other_player_q_space == other_player_p_space:
                                        other_player.set_token_p("kick")
                                    continue

                    # neither token in home yard
                    # check to prevent accidental double moves
                    if player.get_token_p_moved() == False and player.get_token_q_moved() == False:
                        for other_player in self._players_list:
                            if player_position != other_player.get_position():
                                other_player_p_space = other_player.get_token_p_space()
                                other_player_q_space = other_player.get_token_q_space()
                            if current_q_space == "R":
                                if current_p_space == "R":  # edge case - both tokens in "R" - move "p"
                                    if player.get_token_p_moved() == False:
                                        self.move_token(player_position, "p", steps)
                                        continue
                                else:
                                    if player.get_token_q_moved() == False:
                                        self.move_token(player_position, "q", steps)
                                    continue
                            # special case for when token p in home row
                            elif current_p_index > 51 and current_p_space != "E":
                                if (current_p_index + steps) <= 58:
                                    if current_q_index < current_p_index and current_q_space != "H":
                                        if player.get_token_q_moved() == False:
                                            self.move_token(player_position, "q", steps)
                                            if current_q_space == other_player_p_space:
                                                other_player.set_token_p("kick")
                                            if current_q_space == other_player_q_space:
                                                other_player.set_token_q("kick")
                                            continue
                                    else:
                                        if player.get_token_p_moved() == False:
                                            self.move_token(player_position, "p", steps)
                                            continue
                                # bounce back if roll would go past "E"
                                elif (current_p_index + steps) > 58:
                                    if current_q_index < current_p_index and current_q_space != "H":
                                        if player.get_token_q_moved() == False:
                                            self.move_token(player_position, "q", steps)
                                            if current_q_space == other_player_p_space:
                                                other_player.set_token_p("kick")
                                            if current_q_space == other_player_q_space:
                                                other_player.set_token_q("kick")
                                            continue
                                    else:
                                        if player.get_token_p_moved() == False:
                                            self.move_token(player_position, "p", (steps))
                                            # check to see if tokens are stacked
                                            if current_p_space == current_q_space:
                                                self.move_token(player_position, "q", steps)
                                            continue
                            # special case for when token q in home row
                            elif current_q_index > 51 and current_q_space != "E":
                                if (current_q_index + steps) <= 58:
                                    if current_p_index < current_q_index and current_p_space != "H":
                                        if player.get_token_p_moved() == False:
                                            self.move_token(player_position, "p", steps)
                                            if current_p_space == other_player_p_space:
                                                other_player.set_token_p("kick")
                                            if current_p_space == other_player_q_space:
                                                other_player.set_token_q("kick")
                                            continue
                                    else:
                                        if player.get_token_q_moved() == False:
                                            self.move_token(player_position, "q", steps)
                                            continue
                                # bounce back if roll would go past "E"
                                elif (current_q_index + steps) > 58:
                                    bounce = (current_q_index + steps - 58)
                                    self.move_token(player_position, "q", (steps + bounce))
                                    continue
                            elif current_q_index > 0 and current_q_index < current_p_index:
                                if player.get_token_q_moved() == False:
                                    self.move_token(player_position, "q", steps)
                                    continue
                            else:
                                if player.get_token_p_moved() == False:
                                    self.move_token(player_position, "p", steps)
                                    # check to see if tokens are stacked
                                    if current_p_space == current_q_space:
                                        self.move_token(player_position, "q", steps)
                                    continue

                    # if one token is on "E" and the other is not, move other token
                    if current_p_space == "E" and current_q_space != "E":
                        if current_q_space == "H":
                            if steps == 6:
                                self.move_token(player_position, "q", steps)
                                for other_player in self._players_list:
                                    if player_position != other_player.get_position():
                                        other_player_p_space = other_player.get_token_p_space()
                                        other_player_q_space = other_player.get_token_q_space()
                                        if other_player_p_space == current_q_space:
                                            other_player.set_token_p("kick")
                                        if other_player_q_space == current_q_space:
                                            other_player.set_token_q("kick")
                                        continue
                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            if player.get_token_q_moved() == False:
                                self.move_token(player_position, "q", steps)
                                continue
                    elif current_q_space == "E" and current_p_space != "E":
                        if current_p_space == "H":
                            if steps == 6:
                                self.move_token(player_position, "p", steps)
                                for other_player in self._players_list:
                                    if player_position != other_player.get_position():
                                        other_player_p_space = other_player.get_token_p_space()
                                        other_player_q_space = other_player.get_token_q_space()
                                        if other_player_p_space == current_p_space:
                                            other_player.set_token_p("kick")
                                        if other_player_q_space == current_p_space:
                                            other_player.set_token_q("kick")
                                        continue
                                    else:
                                        continue
                            else:
                                continue
                        else:
                            if player.get_token_p_moved() == False:
                                self.move_token(player_position, "p", steps)
                                continue

        result_list = []
        for player in self._players_list:
            result_list.append(str(player.get_token_p_space()))
            result_list.append(str(player.get_token_q_space()))
        return result_list


class Player:
    """represents a Player in the game - takes player Position as a string. Has the following
        private data members: position, current state, completed, step count, board, token p
        steps, token p space, token p moved, token q steps, token q space, token q moved"""
    def __init__(self, position):
        """initializes the Player object with appropriate data members"""
        self._position = position
        self._current_state = "Still Playing"
        self._completed = False
        self._step_count = -1

        if position == "A":
            self._board = ["H", "R", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                           13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                           26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                           39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                           "A1", "A2", "A3", "A4", "A5", "A6", "E"]
        if position == "B":
            self._board = ["H", "R", 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                           25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                           38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                           51, 52, 53, 54, 55, 56, 1, 2, 3, 4, 5, 6, 7, 8,
                           "B1", "B2", "B3", "B4", "B5", "B6", "E"]
        if position == "C":
            self._board = ["H", "R", 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                           39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
                           52, 53, 54, 55, 56, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                           11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                           "C1", "C2", "C3", "C4", "C5", "C6", "E"]
        if position == "D":
            self._board = ["H", "R", 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                           53, 54, 55, 56, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                           12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                           25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                           "D1", "D2", "D3", "D4", "D5", "D6", "E"]

        self._token_p = -1
        self._token_p_space = self._board[0]
        self._token_q = -1
        self._token_q_space = self._board[0]
        self._token_p_moved = False
        self._token_q_moved = False

    def get_board(self):
        """returns the list representing the board from Player's starting position"""
        return self._board

    def get_position(self):
        """returns the player's position as a string"""
        return self._position

    def set_token_p(self, steps):
        """moves the player's p token, takes the number of steps to move that token
            as a parameter"""
        if steps != "kick":
            self._token_p_moved = True
        if steps != "kick":
            bounce = 0
            current_space = self.get_token_p_space()
            current_index = self._board.index(current_space)
            if (current_index + steps) >= 58:
                bounce += (current_index + steps) - 58
            adjusted_steps = steps - bounce
            self._token_p_space = self._board[current_index + (adjusted_steps - bounce)]
            self._token_p += (adjusted_steps - bounce)
        else:
            self._token_p = -1
            self._token_p_space = self._board[0]

    def set_token_p_moved(self):
        """Boolean used to prevent accidental double moves. This setter function changes
            the value to False, indicating that the token has not moved that turn"""
        self._token_p_moved = False

    def set_token_q(self, steps):
        """moves the player's q token, takes the number of steps to move that token
            as a parameter"""
        if steps != "kick":
            self._token_q_moved = True
        if steps != "kick":
            bounce = 0
            current_space = self.get_token_q_space()
            current_index = self._board.index(current_space)
            if (current_index + steps) >= 58:
                bounce += (current_index + steps) - 58
            adjusted_steps = steps - bounce
            self._token_q_space = self._board[current_index + (adjusted_steps - bounce)]
            self._token_q += (adjusted_steps - bounce)
        else:
            self._token_q = -1
            self._token_q_space = self._board[0]

    def set_token_q_moved(self):
        """Boolean used to prevent accidental double moves. This setter function changes
            the value to False, indicating that the token has not moved that turn"""
        self._token_q_moved = False

    def get_token_p_moved(self):
        """returns the Boolean value indicating whether the p token has moved
            on a given turn"""
        return self._token_p_moved

    def get_token_q_moved(self):
        """returns the Boolean value indicating whether the q token has moved
            on a given turn"""
        return self._token_q_moved

    def get_space_name(self, total_steps):
        """takes a total number of steps and returns a specific space name as a
            string that a player's token will be on after that many steps."""
        space = self._board[total_steps + 1]
        return str(space)

    def get_completed(self):
        """returns the Boolean value that indicates whether both of the Player's
            tokens have reached the E space on the board"""
        return self._completed

    def get_token_p_space(self):
        """returns the space on the board, as a string, that the Player's p token
            is currently on at that point in time"""
        if self._token_p == -1:
            return self._board[0]
        elif self._token_p == 0:
            return self._board[1]
        elif self._token_p == 58:
            return self._board[58]
        else:
            return self._board[(self.get_token_p_step_count() + 1)]

    def get_token_q_space(self):
        """returns the space on the board, as a string, that the Player's q token
            is currently on at that point in time"""
        if self._token_q == -1:
            return self._board[0]
        elif self._token_q == 0:
            return self._board[1]
        elif self._token_q == 58:
            return self._board[58]
        else:
            return self._board[(self.get_token_q_step_count() + 1)]

    def get_token_p_step_count(self):
        """returns the number of steps that the Player's p token has moved"""
        return self._token_p

    def get_token_q_step_count(self):
        """returns the number of steps that the Player's q token has moved"""
        return self._token_q

    def set_completed(self):
        """this method is used when both of the player's tokens have reached
            "E", indicating that they are finished with the game"""
        self._completed = True
        self._current_state = "Finished Playing"
