from qb import QB
from running_back import RB
import json


class Team:
    all_teams = []

    def __init__(self, name):
        self.name = name
        self.players = {}
        self.recognized_positions = {
            "QB": QB,
            "RB": RB
        }
        Team.all_teams.append(self)

    def instantiate_from_json_file(self, json_file: str):
        with open(json_file) as f:
            player_data_list = json.load(f)
            for player_dict in player_data_list:
                player_name = player_dict["Player"]
                games_list = player_dict["Games"]
                player_position = player_dict["Position"]

                self.add_player(player_position, player_name, games_list)

    def add_player(self, position: str, player_name: str, games_list: list):
        pos_class = self.recognized_positions[position]
        if self.players.get(position) is None:
            self.players[position] = []
        new_player = pos_class(player_name, games_list)
        self.players[position].append(new_player)
