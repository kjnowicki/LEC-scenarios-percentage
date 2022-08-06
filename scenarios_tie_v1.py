import copy
import json
import os
import re

START = """1. Read
2. Current
3. Next match
4. Exit"""


def print_start():
    print(START)


def read():
    matches = []
    standings = {}
    with open("data/lec_m_2.txt", "r") as file:
        for line in file.readlines():
            line_split = re.split("[-><]", line.strip())
            team1 = line_split[0]
            team2 = line_split[1]
            if "-" in line:
                matches.append([team1, team2])
            elif ">" in line:
                if team1 in standings:
                    standings[team1]["w"] += 1
                    standings[team1]["wins"].append(team2)
                else:
                    standings[team1] = {"w": 1, "l": 0, "wins": [team2], "losses": []}
                if team2 in standings:
                    standings[team2]["l"] += 1
                    standings[team2]["losses"].append(team1)
                else:
                    standings[team2] = {"w": 0, "l": 1, "wins": [], "losses": [team1]}
            elif "<" in line:
                if team1 in standings:
                    standings[team1]["l"] += 1
                    standings[team1]["losses"].append(team2)
                else:
                    standings[team1] = {"w": 0, "l": 1, "wins": [], "losses": [team2]}
                if team2 in standings:
                    standings[team2]["w"] += 1
                    standings[team2]["wins"].append(team1)
                else:
                    standings[team2] = {"w": 1, "l": 0, "wins": [team1], "losses": []}
    return matches, standings


def predict(matches, standings):
    future_standings = copy.deepcopy([standings])
    for match in matches:
        team1 = match[0]
        team2 = match[1]
        ftr_standings = []
        for future_standing in copy.deepcopy(future_standings):
            case_one = copy.deepcopy(future_standing)
            case_two = copy.deepcopy(future_standing)

            case_one[team1]["w"] += 1
            case_one[team1]["wins"].append(team2)
            case_one[team2]["l"] += 1
            case_one[team2]["losses"].append(team1)
            case_two[team2]["w"] += 1
            case_two[team2]["wins"].append(team1)
            case_two[team1]["l"] += 1
            case_two[team1]["losses"].append(team2)

            ftr_standings.append(case_one)
            ftr_standings.append(case_two)
        future_standings = copy.deepcopy(ftr_standings)
    with open("data/lec_results_2.txt", "w") as file:
        file.writelines(json.dumps(future_standings))
    return future_standings


def top6_team_perc(team, standings):
    n_in_top6 = sum(list(
        map(lambda standing: int(
            team in sorted(standing, key=lambda _team: standing[team]["w"], reverse=True)[:6] or
            (
                    standing[sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5]]["w"] ==
                    standing[team]["w"]
                    and
                    sorted(standing, key=lambda _team: standing[team]["w"], reverse=True)[5] in standing[team]["wins"]
            )
        ), standings)
    ))
    return round(n_in_top6 / len(standings), 3)


def print_teams(teams, future_standings):
    for team in teams:
        print(f"#{team.upper()}: {top6_team_perc(team, future_standings)}")


def print_all_teams(future_standings):
    for team in future_standings[0]:
        k = len(list(filter(
            lambda standing: team in sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[:6]
                             or (
                                     standing[
                                         sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5]][
                                         "w"] == standing[team]["w"]
                                     and
                                     sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5] in
                                     standing[team]["wins"]
                             ), future_standings)))
        print(f"#{team.upper()}: {round(k / len(future_standings),3)}")


def from_file():
    with open("data/lec_results_2.txt", "r") as file:
        _standings = json.load(file)
        for team in _standings[0]:
            k = len(list(filter(
                lambda standing: team in sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[:6]
                                 or (
                                         standing[
                                             sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5]][
                                             "w"] == standing[team]["w"]
                                         and
                                         sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5] in
                                         standing[team]["wins"]
                                 ), _standings)))
            print(f"#{team.upper()}: {round(k / len(_standings),3)}")


def next_dif_2standings(match, standings):
    case_one = copy.deepcopy(standings)
    case_two = copy.deepcopy(standings)
    team1 = match[0]
    team2 = match[1]

    case_one[team1]["w"] += 1
    case_one[team1]["wins"].append(team2)
    case_one[team2]["l"] += 1
    case_one[team2]["losses"].append(team1)
    case_two[team2]["w"] += 1
    case_two[team2]["wins"].append(team1)
    case_two[team1]["l"] += 1
    case_two[team1]["losses"].append(team2)
    return case_one, case_two


def custom():
    with open("data/lec_results_2.txt", "r") as file:
        _standings = json.load(file)
        team = "g2"
        print(list(filter(
            lambda standing: not(team in sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[:6]
                             or (
                                     standing[
                                         sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5]][
                                         "w"] == standing[team]["w"]
                                     and
                                     sorted(standing, key=lambda _team: standing[_team]["w"], reverse=True)[5] in
                                     standing[team]["wins"]
                             )), _standings))[0:1])


if __name__ == '__main__':
    matches = []
    standings = {}
    future_standings = []
    while True:
        print_start()
        x = int(input("My action number: "))
        os.system("cls")
        if x == 1:
            matches, standings = read()
        elif x == 2:
            future_standings = predict(matches, standings)
            print_all_teams(future_standings)
        elif x == 3:
            standings1, standings2 = next_dif_2standings(matches.pop(), standings)
            future_standings1 = predict(matches, standings1)
            future_standings2 = predict(matches, standings2)
            print_all_teams(future_standings1)
            print_all_teams(future_standings2)
        elif x == 4:
            exit()
        elif x == 5:
            from_file()
        elif x ==6:
            custom()
