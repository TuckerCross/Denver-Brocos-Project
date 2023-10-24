from player import Player


class RB(Player):
    all_rbs = []

    def __init__(self, name: str, games_list: list):
        super().__init__(
            name=name,
            games_list=games_list
        )

        RB.all_rbs.append(self)
