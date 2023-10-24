from player import Player


def calc_passer_rating(comps: int, atts: int, yds: int, tds: int,
                       intercepts: int):
    """
    Calculate the passer rating based on the formula provided here:
    https://en.wikipedia.org/wiki/Passer_rating#NFL_and_CFL_formula

    :param comps: int: Number of completions
    :param atts: int: Number of attempts
    :param yds: int: Number of yards
    :param tds: int: Number of touchdowns
    :param intercepts: int: Number of interceptions
    :return: float: The calculated passer rating
    """
    def calc_a():
        value = ((comps / atts) - 0.3) * 5
        return validate_value(value)

    def calc_b():
        value = ((yds / atts) - 3) * 0.25
        return validate_value(value)

    def calc_c():
        value = (tds / atts) * 20
        return validate_value(value)

    def calc_d():
        value = 2.375 - ((intercepts / atts) * 25)
        return validate_value(value)

    def validate_value(value):
        if value > 2.375:
            value = 2.375
        elif value < 0:
            value = 0
        return value

    a = calc_a()
    b = calc_b()
    c = calc_c()
    d = calc_d()

    passer_rating = ((a + b + c + d) / 6) * 100

    return passer_rating


class QB(Player):
    all_qbs = []

    def __init__(self, name: str, games_list: list):
        super().__init__(
            name=name,
            games_list=games_list
        )

        self.total_completions = self.get_season_total("Completions")
        self.total_attempts = self.get_season_total("Attempts")
        self.total_interceptions = self.get_season_total("Interceptions")
        self.total_touchdowns = self.get_season_total("Touchdowns")
        self.total_passing_yards = self.get_season_total("Yards")
        self.total_sacks = self.get_season_total("Sacks")

        self.season_comp_pct = self.total_completions / self.total_attempts
        self.highest_single_game_comp_pct = (
            self.get_highest_single_game_comp_pct())
        self.lowest_single_game_ypa = self.get_lowest_single_game_ypa()

        self.passer_ratings = self.get_passer_ratings()
        (self.best_passer_rating_week,
         self.highest_single_game_passer_rating) = (
            self.get_highest_passer_rating())
        (self.worst_passer_rating_week,
         self.lowest_single_game_passer_rating) = (
            self.get_lowest_passer_rating())
        self.season_passer_rating = self.get_season_passer_rating()

        first_3_weeks = ["Game1", "Game2", "Game3"]
        self.passer_rating_first_3 = (
            self.get_combined_passer_rating_for_game_list(first_3_weeks))

        exclude_weeks = [
            self.worst_passer_rating_week,
            self.best_passer_rating_week
        ]
        self.passer_rating_exclude_best_worst = (
            self.get_combined_passer_rating_for_game_list(exclude_weeks,
                                                          exclude=True))

        QB.all_qbs.append(self)

    def get_highest_single_game_comp_pct(self):
        highest = 0.0
        for game in self.games_list:
            attempts = game["Attempts"]
            completions = game["Completions"]
            comp_pct = completions / attempts
            if comp_pct > highest:
                highest = comp_pct
        return highest

    def get_lowest_single_game_ypa(self):
        lowest = float('inf')
        for game in self.games_list:
            attempts = game["Attempts"]
            yards = game["Yards"]
            ypa = yards / attempts
            if ypa < lowest:
                lowest = ypa
        return lowest

    def get_passer_ratings(self):
        passer_ratings_dict = {}
        for game in self.games_list:
            comps = self.get_game_total("Completions", game)
            atts = self.get_game_total("Attempts", game)
            yds = self.get_game_total("Yards", game)
            tds = self.get_game_total("Touchdowns", game)
            intercepts = self.get_game_total("Interceptions", game)

            passer_rating = calc_passer_rating(comps, atts, yds, tds,
                                               intercepts)

            game_name = game.get("Game")
            passer_ratings_dict[game_name] = round(passer_rating, 1)
        return passer_ratings_dict

    def get_highest_passer_rating(self):
        highest = 0
        best_week = None
        for game, rating in self.passer_ratings.items():
            if rating > highest:
                highest = rating
                best_week = game
        return best_week, highest

    def get_lowest_passer_rating(self):
        lowest = float('inf')
        worst_week = None
        for game, rating in self.passer_ratings.items():
            if rating < lowest:
                lowest = rating
                worst_week = game
        return worst_week, lowest

    def get_season_passer_rating(self):
        passer_rating = calc_passer_rating(self.total_completions,
                                           self.total_attempts,
                                           self.total_passing_yards,
                                           self.total_touchdowns,
                                           self.total_interceptions)
        return round(passer_rating, 1)

    def get_combined_passer_rating_for_game_list(self, list_of_weeks,
                                                 exclude=False):
        total_comps = 0
        total_atts = 0
        total_yds = 0
        total_tds = 0
        total_intercepts = 0

        for game in self.games_list:
            game_name = game.get("Game")
            if ((not exclude and game_name in list_of_weeks) or
                    (exclude and game_name not in list_of_weeks)):
                total_comps += self.get_game_total("Completions", game)
                total_atts += self.get_game_total("Attempts", game)
                total_yds += self.get_game_total("Yards", game)
                total_tds += self.get_game_total("Touchdowns", game)
                total_intercepts += self.get_game_total("Interceptions", game)

        passer_rating = calc_passer_rating(total_comps, total_atts,
                                           total_yds, total_tds,
                                           total_intercepts)
        return round(passer_rating, 1)

    @classmethod
    def get_highest_single_game_comp_pct_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the highest
        single game completion percentage.

        :return: the player name and the single game completion percentage of
                 the player that has the highest single game completion percentage.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.highest_single_game_comp_pct > highest:
                highest = qb_obj.highest_single_game_comp_pct
                player = qb_obj.name
        return player, round(highest * 100, 3)

    @classmethod
    def get_lowest_single_game_ypa_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the lowest
        single game yards per attempt.

        :return: the player name and the single game yards per attempt of
                 the player that has the lowest single game yards per attempt.
        """
        lowest = float('inf')
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.lowest_single_game_ypa < lowest:
                lowest = qb_obj.lowest_single_game_ypa
                player = qb_obj.name
        return player, round(lowest, 3)

    @classmethod
    def get_least_season_passing_yards_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the least
        season passing yards.

        :return: the player name and the season passing yards of the player
                 that has the least season passing yards.
        """
        least = float('inf')
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.total_passing_yards < least:
                least = qb_obj.total_passing_yards
                player = qb_obj.name
        return player, least

    @classmethod
    def get_most_touchdowns_for_season_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the most
        touchdowns for the season.

        :return: the player name and the total touchdowns of the player that
                 has the most touchdowns for the season.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.total_touchdowns > highest:
                highest = qb_obj.total_touchdowns
                player = qb_obj.name
        return player, highest

    @classmethod
    def get_season_comp_pct_list_descending_all_qbs(cls):
        """
        Iterates the list of QB objects to display the players in
        descending order based on their season completion percentage.

        :return: a string containing a comma separated list of players in
                 descending order based on their season completion percentage.
        """
        qb_name_and_comp_pct_list = []
        final_list = []

        # Add all qb names and their season completion percentage to a list.
        for qb_obj in cls.all_qbs:
            qb_name_and_comp_pct_list.append((qb_obj.name, qb_obj.season_comp_pct))

        # Sort the list based on the completion percentage, which is in index 1 of
        # each tuple, in descending order.
        sorted_descending = sorted(qb_name_and_comp_pct_list, key=lambda x: x[1],
                                   reverse=True)

        # Now that the list is sorted, create a final list that only contains the
        # qb names, which are located in index 0 of each tuple.
        for i in sorted_descending:
            final_list.append(i[0])

        # Join the final list into a string that separates each qb name by a comma.
        return ",".join(final_list)

    @classmethod
    def get_highest_single_game_passer_rating_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the highest
        single game passer rating.

        :return: the player name and the single game passer rating of the player
                 that has the highest single game passer rating.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.highest_single_game_passer_rating > highest:
                highest = qb_obj.highest_single_game_passer_rating
                player = qb_obj.name
        return player, highest

    @classmethod
    def get_lowest_single_game_passer_rating_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the lowest
        single game passer rating.

        :return: the player name and the single game passer rating of the player
                 that has the lowest single game passer rating.
        """
        lowest = float('inf')
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.lowest_single_game_passer_rating < lowest:
                lowest = qb_obj.lowest_single_game_passer_rating
                player = qb_obj.name
        return player, lowest

    @classmethod
    def get_highest_season_passer_rating_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the highest
        season passer rating.

        :return: the player name and the single game passer rating of the player
                 that has the highest season passer rating.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.season_passer_rating > highest:
                highest = qb_obj.season_passer_rating
                player = qb_obj.name
        return player, highest

    @classmethod
    def get_highest_passer_rating_first_3_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the highest
        passer rating over the first three games.

        :return: the player name and the single game passer rating of the player
                 that has the highest passer rating over the first three games.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.passer_rating_first_3 > highest:
                highest = qb_obj.passer_rating_first_3
                player = qb_obj.name
        return player, highest

    @classmethod
    def get_highest_passer_rating_exclude_best_worst_all_qbs(cls):
        """
        Iterates the list of QB objects to find the QB with the highest
        passer rating after excluding the best and worst passer rating games of
        the season.

        :return: the player name and the passer rating of the player that has the
                 highest passer rating after excluding their best and worst passer
                 rating games of the season.
        """
        highest = 0
        player = None
        for qb_obj in cls.all_qbs:
            if qb_obj.passer_rating_exclude_best_worst > highest:
                highest = qb_obj.passer_rating_exclude_best_worst
                player = qb_obj.name
        return player, highest
