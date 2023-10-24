from qb import QB
from team import Team


if __name__ == "__main__":

    broncos = Team("Denver Broncos")
    broncos.instantiate_from_json_file("qb_data.json")

    print("1. Which player had the highest single game Completion Percentage?")
    qb, highest_comp_pct = QB.get_highest_single_game_comp_pct_all_qbs()
    print(f"    {qb} with a single game completion percentage of "
          f"{highest_comp_pct}%")

    print("2. Which player had the lowest single game Yards Per Attempt?")
    qb, lowest_ypa = QB.get_lowest_single_game_ypa_all_qbs()
    print(f"    {qb} with a single game yards per attempt of {lowest_ypa}")

    print("3. Which player had the least Passing Yards for the season?")
    qb, least_passing_yards = QB.get_least_season_passing_yards_all_qbs()
    print(f"    {qb} with a season passing yards of {least_passing_yards}")

    print("4. Which player had the most Touchdowns for the season?")
    qb, most_tds = QB.get_most_touchdowns_for_season_all_qbs()
    print(f"    {qb} with {most_tds} total touchdowns")

    print("5. List the player names by their Season Completion Percentage in "
          "descending order. List the names in order, separated by a comma "
          "with no spaces like this: QB1,QB2,QB3,QB4,QB5")
    comp_pct_list = QB.get_season_comp_pct_list_descending_all_qbs()
    print(f"    {comp_pct_list}")

    qb, highest_single_game_passer_rating = (
        QB.get_highest_single_game_passer_rating_all_qbs())
    print("6. Which player had the highest single game Passer Rating?")
    print(f"    {qb}")

    print("7. What was the value of the highest single game Passer Rating? "
          "(Limit to 1 decimal point i.e. 108.3)")
    print(f"    {highest_single_game_passer_rating}")

    qb, lowest_single_game_passer_rating = (
        QB.get_lowest_single_game_passer_rating_all_qbs())
    print("8. Which player had the lowest single game Passer Rating?")
    print(f"    {qb}")

    print("9. What was the value of the lowest single game Passer Rating? "
          "(Limit to 1 decimal point i.e. 108.3)")
    print(f"    {lowest_single_game_passer_rating}")

    print("10.	Which player had the highest season Passer Rating?")
    qb, highest_season_passer_rating = (
        QB.get_highest_season_passer_rating_all_qbs())
    print(f"    {qb} with a passer rating of {highest_season_passer_rating}")

    print("11. Which player had the highest season Passer Rating for the "
          "first 3 games?")
    qb, highest_passer_rating_first_3 = (
        QB.get_highest_passer_rating_first_3_all_qbs())
    print(f"    {qb} with a passer rating of {highest_passer_rating_first_3}")

    print("12. Excluding each player’s highest and lowest single game Passer "
          "Rating, which player had the highest Passer Rating for the season?")
    qb, highest_passer_rating_exclude_best_worst = (
        QB.get_highest_passer_rating_exclude_best_worst_all_qbs())
    print(f"    {qb} with a passer rating of "
          f"{highest_passer_rating_exclude_best_worst}")
