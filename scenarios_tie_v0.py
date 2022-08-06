import copy
import json
import os
import re

START_COM = """1. Choose data source
2. Calculate probability
3. Use existing
4. Exit
5. mad(custom)
6. Next match
"""
PROB_SUB_MENU = """1. Predefined scenarios
2. Custom scenario"""

_standings = {}
_matches = []
_possible_standings = []
_source = ""


def print_start():
    print(START_COM)


def choose_data_source():
    source_name = input("Source name: ")
    globals()["_source"] = source_name
    with open("data/" + source_name + ".txt") as file:
        for line in file.readlines():
            team_score_split = line.split(" ")
            team = team_score_split[0]
            score_split = team_score_split[1].split("-")
            wins = int(score_split[0])
            losses = int(score_split[1])
            _standings[team] = {"w": wins, "l": losses}
    with open("data/" + source_name + "_m.txt") as file:
        for line in file.readlines():
            _matches.append(line.strip().split("-"))


def get_scenarios(next: bool = False):
    if next:
        match = _matches.pop()
        case_one = copy.deepcopy([_standings])
        case_one[0][match[0]]["w"] += 1
        case_one[0][match[1]]["l"] += 1
        case_two = copy.deepcopy([_standings])
        case_two[0][match[0]]["l"] += 1
        case_two[0][match[1]]["w"] += 1

        for match in _matches:
            temp_standings_1 = []
            temp_standings_2 = []
            for possible_standing in case_one:
                temp_standing_case_one = copy.deepcopy(possible_standing)
                temp_standing_case_one[match[0]]["w"] += 1
                temp_standing_case_one[match[1]]["l"] += 1
                temp_standings_1.append(temp_standing_case_one)

                temp_standing_case_two = copy.deepcopy(possible_standing)
                temp_standing_case_two[match[0]]["l"] += 1
                temp_standing_case_two[match[1]]["w"] += 1
                temp_standings_1.append(temp_standing_case_two)
            for possible_standing in case_two:
                temp_standing_case_one = copy.deepcopy(possible_standing)
                temp_standing_case_one[match[0]]["w"] += 1
                temp_standing_case_one[match[1]]["l"] += 1
                temp_standings_2.append(temp_standing_case_one)

                temp_standing_case_two = copy.deepcopy(possible_standing)
                temp_standing_case_two[match[0]]["l"] += 1
                temp_standing_case_two[match[1]]["w"] += 1
                temp_standings_2.append(temp_standing_case_two)

            case_one = copy.deepcopy(temp_standings_1)
            case_two = copy.deepcopy(temp_standings_2)

        return case_one, case_two
    else:
        possible_standings = copy.deepcopy([_standings])
        for match in _matches:
            temp_standings = []
            for possible_standing in possible_standings:
                temp_standing_case_one = copy.deepcopy(possible_standing)
                temp_standing_case_one[match[0]]["w"] += 1
                temp_standing_case_one[match[1]]["l"] += 1
                temp_standings.append(temp_standing_case_one)

                temp_standing_case_two = copy.deepcopy(possible_standing)
                temp_standing_case_two[match[0]]["l"] += 1
                temp_standing_case_two[match[1]]["w"] += 1
                temp_standings.append(temp_standing_case_two)
            possible_standings = copy.copy(temp_standings)
        _possible_standings.extend(possible_standings)
        with open("data/" + _source + "_results.txt", "w") as file:
            file.writelines(json.dumps(possible_standings))
        return possible_standings


def print_calculate_probability_menu():
    get_scenarios()
    print(
        list(map(lambda team: (team, calc_team_top6(team)), _standings.keys()))
    )


def calc_team_top6(team):
    return round(len(list(filter(
        lambda standing: team in sorted(standing, key=lambda position: standing[position]["w"], reverse=True)[:6] or
                         standing[sorted(standing, key=lambda position: standing[position]["w"], reverse=True)[5]]["w"] ==
                         standing[team]["w"],
        _possible_standings))) / len(_possible_standings), 4)


def calc_team_top6_from(team, source):
    return round(len(list(filter(
        lambda standing: team in sorted(standing, key=lambda position: standing[position]["w"], reverse=True)[:6] or
                         standing[sorted(standing, key=lambda position: standing[position]["w"], reverse=True)[5]][
                             "w"] == standing[team]["w"],
        source))) / len(source), 4)


def print_current():
    with open("data/" + _source + "_results.txt", "r") as file:
        globals()["_possible_standings"] = json.load(file)
    print(
        list(map(lambda team: (team, calc_team_top6(team)), _standings.keys()))
    )


def mad():
    with open("data/" + _source + "_results.txt", "r") as file:
        globals()["_possible_standings"] = json.load(file)
    print(len(list(filter(
        lambda standing: "g2" not in sorted(standing, key=lambda position: standing[position]["w"], reverse=True)[:6],
        _possible_standings))))


def next_match():
    case_one, case_two = get_scenarios(True)
    print(
        list(map(lambda team: (team, calc_team_top6_from(team, case_one)), _standings.keys()))
    )
    print(
        list(map(lambda team: (team, calc_team_top6_from(team, case_two)), _standings.keys()))
    )


if __name__ == '__main__':
    while True:
        print_start()
        x = int(input("My action number: "))
        os.system("cls")
        if x == 1:
            choose_data_source()
        elif x == 2:
            print_calculate_probability_menu()
        elif x == 3:
            print_current()
        elif x == 4:
            exit()
        elif x == 5:
            mad()
        elif x == 6:
            next_match()
