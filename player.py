

class Player:
    all_players = []

    def __init__(self, name: str, games_list: list):
        self.__name = name
        self.games_list = games_list

        Player.all_players.append(self)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise ValueError(f"Aborting: attempted to change {self.name}'s name to {value}")

    @property
    def games_list(self):
        return self.__games_list

    @games_list.setter
    def games_list(self, games_list):
        if len(games_list) < 1:
            raise ValueError(f"Empty game list provided for player: {self.name}")
        self.__games_list = games_list

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.games_list})"

    def get_season_total(self, stat: str):
        total = 0
        for game in self.games_list:
            game_value = game.get(stat)
            if game_value is None:
                game_value = 0
            total += game_value
        return total

    @staticmethod
    def get_game_total(stat: str, game_data: dict):
        game_value = game_data.get(stat)
        if game_value is None:
            game_value = 0
        return game_value
