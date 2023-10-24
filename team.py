from qb import QB
from running_back import RB
import json


class Team:
    all_teams = []

    def __init__(self, name):
        self.name = name
        self.players = {}
        Team.all_teams.append(self)

    def instantiate_from_json_file(self, json_file: str):
        with open(json_file) as f:
            player_data_list = json.load(f)
            for player_dict in player_data_list:
                player_name = player_dict["Player"]
                games_list = player_dict["Games"]
                player_position = player_dict["Position"]

                if player_position == "QB":
                    if self.players.get("QB") is None:
                        self.players["QB"] = []
                    self.players["QB"].append(QB(player_name, games_list))
                elif player_position == "RB":
                    if self.players.get("RB") is None:
                        self.players["RB"] = []
                    self.players["RB"].append(RB(player_name, games_list))
