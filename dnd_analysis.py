import random
import math
import json
import copy
import grapher
import SimpleGraphics


def load_data():
    with open("races.json") as file:
        race = json.load(file)
    with open("feats.json") as file:
        feats = json.load(file)
    with open("classes.json") as file:
        classes = json.load(file)
    with open("weapons.json") as file:
        weapons = json.load(file)
    with open('classlevels.json') as file:
        levels = json.load(file)
    with open("classfeats.json") as file:
        classfeats = json.load(file)
    with open("enemy_ac.json") as file:
        enemy_ac = json.load(file)

    return race, feats, classes, weapons, levels, classfeats, enemy_ac


def load_character():
    global char_data
    with open(input("Choose a character file to load. > ")) as file:
        char_data = json.load(file)


def update_feat_uses():
    global feat_uses
    # global for storing total feat uses. only holds feats with turns, and ones that the char has
    feat_uses = {}
    for feat in char_data["feats"]:
        has_uses = "uses" in feats_data[feat]
        recharges = "recharge" in feats_data[feat]
        if has_uses:
            # if the feature has limited uses, it is saved as "feat": [uses(int), recharges on short rest(bool)].
            feat_uses[feat] = [feats_data[feat]["uses"], recharges]

    for classfeat in char_data["classfeats"]:
        if classfeat in classfeats_data[char_data["class"]]:
            feat_info = classfeats_data[char_data["class"]][classfeat]
            # if the feature has limited uses, it is saved as "feat": [uses(int), recharges on short rest(bool)].
            feat_uses[classfeat] = [feat_info["uses"], feat_info["recharge"]]


def choose_asi(asi_info):
    choices = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
    for j in range(asi_info[1], 0, -1):
        while True:
            print("\nFrom ", end="")
            for i in asi_info[2]:
                if asi_info[2][i]:  # if a valid target for ASI:
                    print(i.upper(), end="")
                    print(", ", end="")
            pick = input("select an ability to increase. (" +
                         str(j) + " left) > ").lower()
            if pick in asi_info[2] and asi_info[2][pick]:
                print(pick.upper() + " has been increased by 1.")
                choices[pick] += 1
                break
            else:
                print("Invalid ability.")
    return choices


# crit range: 1 to 20. 20 means a critical hit will happen on a 20 for the attack d20; 19 means crit on 19 or 20, etc.
def round_damage(base, target, features, hit_bonus=0, dmg_bonus=0):
    global feat_uses

    # calculate base damage die's average roll
    die_info = base.split('d')
    die_average = ((int(die_info[1]) + 1) / 2) * int(die_info[0])

    # base modifiers. advantage if True, normal if None, disadvantage if False.
    advantage_status = True
    crit_range = 20

    rolls = 2

    hit_chance = 1 - (target - hit_bonus - 1) / 20
    crit_chance = (21 - crit_range) * 0.05

    hit_chance_adv = 1 - (1 - hit_chance) ** rolls
    hit_chance_dis = hit_chance ** rolls

    crit_chance_adv = 1 - (1 - crit_chance) ** rolls
    crit_chance_dis = crit_chance ** rolls

    # hit_chance, crit_chance = advantage_parser(advantage_status, hit_chance, crit_chance)
    turns = 1

    for item in features:
        # non-specific feats
        if item == "elvenAccuracy" and advantage_status:
            rolls += 1
        elif item == "greatWeaponMaster":
            hit_bonus -= 5
            dmg_bonus += 10
        elif item == "sharpshooter":
            hit_bonus -= 5
            dmg_bonus += 10
        elif item == "lucky":
            rolls += 1

        # fighter feats
        elif item == "archery":
            hit_bonus += 2
        elif item == "dueling":
            dmg_bonus += 2
        elif item == "greatweaponfighting":  # reroll 1s and 2s in die roll
            die_average = round((int(die_info[0])
                                 * (sum(i for i in range(1, int(die_info[1]) + 1)) + 4) / int(die_info[1])), 2)

        elif item == "actionsurge":
            if feat_uses[item][0] > 0:
                turns += 1
        elif item == "improvedcritical":
            if 3 <= char_data["level"] < 15:
                crit_range -= 1
            elif char_data["level"] >= 15:
                crit_range -= 2
        elif item == "fightingspirit":
            if feat_uses[item][0] > 0:
                advantage_status = True
        elif item == "extraattack":
            if 5 <= char_data["level"] < 11:
                turns += 1
            elif 11 <= char_data["level"] < 20:
                turns += 2
            elif char_data["level"] >= 20:
                turns += 3
        else:
            raise Exception("Feat '" + str(item) +
                            "' not found in datafile, is it named correctly?")

        # decrements feat uses to signify it has been expended.
        if item in feat_uses and feat_uses[item][0] > 0:
            feat_uses[item][0] -= 1

        if advantage_status:
            hit_chance, crit_chance = hit_chance_adv, crit_chance_adv
        else:
            hit_chance, crit_chance = hit_chance_dis, crit_chance_dis

    return round(turns * (crit_chance * die_average + hit_chance * (dmg_bonus + die_average)), 2)


# returns average damage value per encounter
def dnd_encounter(rounds=4):
    total_damage = 0

    prof_bonus = (char_data["level"] - 1) // 4 + 2
    ability_bonus = math.floor(
        (max([char_data["abilityScores"]["str"], char_data["abilityScores"]["dex"]]) - 10) / 2)

    # special case for features that take affect at start of battle
    if "tirelessfighter" in char_data["classfeats"]:
        feat_uses["tirelessfighter"][0] = 1

    for _ in range(rounds):
        total_damage += round_damage(weapons_data[char_data["weapons"]], ac_data[str(char_data["level"])],
                                     char_data["feats"] +
                                     char_data["classfeats"],
                                     ability_bonus + prof_bonus, ability_bonus)

    return total_damage


def dnd_day():
    total_damage = 0

    total_damage += dnd_encounter()
    total_damage += dnd_encounter()
    rest()
    total_damage += dnd_encounter()
    total_damage += dnd_encounter()
    rest()
    total_damage += dnd_encounter()
    total_damage += dnd_encounter()
    rest(True)  # long rest. reset all abilities

    return round(total_damage, 2)


def damage_per_level():
    global char_data
    damage_curve = {}

    for i in range(1, 20 + 1):
        char_data["level"] = i
        level_up(i)
        update_feat_uses()
        damage_curve[str(i)] = dnd_day()

    char_data["damagecurve"] = damage_curve

    print("\nAverage Damage Per Level: " +
          str(round(sum(damage_curve.values()) / 20, 2)))
    print("Max Damage Achieved: " + str(max(damage_curve.values())))
    print()

    SimpleGraphics.clear()
    grapher.graph_single(damage_curve, str(
        round(sum(damage_curve.values()) / 20, 2)))
    print("Graph updated.\n")


# passing True will make it a long rest, where all resources are recharged rather than only short-rest-recharge ones
def rest(is_long=False):
    global feat_uses
    for item in feat_uses:
        # if feat recharges on short rest OR it is a long rest
        if feat_uses[item][1] or is_long:
            # special cases depending on current level
            if item == "actionsurge":
                if char_data["level"] >= 17:
                    feat_uses[item][0] = 2
            else:
                if item in classfeats_data:
                    feat_uses[item][0] = classfeats_data[char_data["class"]
                                                         ][item]["uses"]
                elif item in feats_data:
                    feat_uses[item][0] = feats_data[item]["uses"]


# make level up function. fix
def level_up(level):
    global char_data

    print("\nLevel " + str(level) + ":")

    # only proceed if there is a feature for this level
    if levels_data[char_data["class"]].get(str(level)) is not None:
        level_feature = levels_data[char_data["class"]][str(level)]

        # the new feature for the level is subclass-dependent (a dict)
        if type(level_feature) is dict:
            if level_feature.get(char_data["subclass"]) is not None:
                new_feature = level_feature[char_data["subclass"]]

                if new_feature == "fightingstyle":
                    print("Pick a fighting style.")
                    fighting_style = selector(
                        ["archery", "dueling", "greatweaponfighting", "Misc. Fighting Style"])
                    if fighting_style != "Misc. Fighting Style":
                        char_data["classfeats"].append(fighting_style)
                        new_feature = fighting_style
                else:
                    char_data["classfeats"].append(new_feature)
            else:
                new_feature = "No new features."

        elif level_feature == "asi":
            while True:
                asi_choice = input("1. ASI or 2. Feat? > ")
                if asi_choice == "1":
                    choices = choose_asi([True, 2, {"str": True, "dex": True, "con": True,
                                                    "int": True, "wis": True, "cha": True}])
                    # continue after implementing char load
                    for key in choices:
                        char_data["abilityScores"][key] += choices[key]

                    new_feature = "ability score increase"
                    break
                elif asi_choice == "2":
                    print("\nPick a feat.")
                    new_feature = selector(list(feats_data))
                    char_data["feats"].append(new_feature)
                    break
                else:
                    print("Invalid selection.")

        elif level_feature == "fightingstyle":
            print("Pick a fighting style.")
            new_feature = selector(
                ["archery", "dueling", "greatweaponfighting", "Misc. Fighting Style"])
            if new_feature != "Misc. Fighting Style":
                char_data["classfeats"].append(new_feature)

        else:
            new_feature = levels_data[char_data["class"]][str(level)]
            char_data["classfeats"].append(new_feature)

        print("New feature: " + new_feature)
    else:
        print("No new features.")


def create_char():
    # initialize new character information, get char name to begin with
    current_char = {"name": input("What is your character's name? > "), "race": "racename", "subrace": "subracename",
                    "class": "classname", "subclass": None, "level": 1,
                    "abilityScores": {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}, "feats": [],
                    "classfeats": [], "weapons": "", "damagecurve": {}}

    # get race, subrace
    print("\nChoose a race.")
    current_char["race"] = selector(list(race_data))
    print("\nChoose a subrace.")
    current_char["subrace"] = selector(
        list(race_data[current_char["race"]]["subrace"]))

    # load character racial ASI,
    race_asi = race_data[current_char["race"]
                         ]["subrace"][current_char["subrace"]]["asi"]
    # if you have to select abilities to increase manually, call the function for choosing
    if race_asi[0] is True:
        bonus = choose_asi(race_asi)
    else:
        bonus = race_asi[1]

    # get racial feats
    racial_feats = race_data[current_char["race"]
                             ]["subrace"][current_char["subrace"]].get("feat")
    if racial_feats is not None:
        if type(racial_feats) == int:  # if feats have to be chosen, run the related selector
            for i in range(racial_feats, 0, -1):
                print("\nPick a feat. (" + str(i) + " left)")
                current_char["feats"].append(selector(list(feats_data)))
        else:
            current_char["feats"].append(racial_feats)

    # ASIs for racial feats
    for feat in current_char["feats"]:
        if "asi" in feats_data[feat]:
            racial_asi = choose_asi(feats_data[feat]["asi"])
            for key in racial_asi:
                bonus[key] += racial_asi[key]

    # set the six ability scores, randomly or manually
    current_char["abilityScores"] = ability_scores(bonus)

    # get class, subclass
    print("\nChoose a class.")
    current_char["class"] = selector(list(classes_data))
    print("\nChoose a subclass.")
    current_char["subclass"] = selector(
        list(classes_data[current_char["class"]]))

    # get weapons
    print("\nChoose a primary weapon.")
    current_char["weapons"] = selector(list(weapons_data))

    # save file to json
    save_to_json(current_char, current_char["name"])


# function to print all options from a list and obtain legal input
def selector(option_list):
    while True:
        print("The options are:", end=" ")

        for index in range(len(option_list)):
            print(str(index + 1) + ": " +
                  option_list[index].capitalize(), end="")
            if index < len(option_list) - 1:
                print(", ", end="")
            else:
                print(end=". \n")

        option_select = int(input("Select an option by number. > ")) - 1

        if option_select in range(len(option_list)):
            return option_list[option_select]
        else:
            print("Invalid option.\n")


# function that interprets string input to roll dice. inputs are NOT checked for validity
def dice_roll(die):
    # creates a list of integers for [die count, die pip, die dropped]
    die_info = die.split('d')

    roll_list = []

    for _ in range(int(die_info[0])):
        roll_list.append(random.randint(1, int(die_info[1])))

    # if die drop is specified,
    if len(die_info) == 3:
        for _ in range(int(die_info[2])):
            roll_list.remove(min(roll_list))

    return sum(roll_list)


def ability_scores(bonus=None):
    scores_dict = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

    # option selection for rolling ability scores or manually inputting
    while True:
        score_choice = input(
            "\nRoll ability scores randomly, or input them manually? (1: roll, 2: manual) > ").lower()
        if score_choice == "1":
            print(
                "The six ability scores are determined with four d6s each, lowest value dropped.")
            for key in scores_dict:
                roll = dice_roll("4d6d1")
                print("Rolling 4d6d1...", end=" ")
                print(key.upper() + " is " + str(roll), end="")
                if bonus[key] != 0:
                    print(" + " + str(bonus[key]))
                else:
                    print()
                scores_dict[key] = roll
            break

        elif score_choice == "2":
            print(
                "Input Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma manually.")
            print("Note that racial bonuses will be applied separately afterwards.")
            for key in scores_dict:
                scores_dict[key] = int(
                    input("Score for " + key.upper() + "? > "))
            break

        else:
            print("Invalid option.")

    for key in bonus:
        scores_dict[key] += bonus[key]

    return scores_dict


def save_to_json(char_dict, filename):
    # creates/edits file with character name as filename, converted to a filename-appropriate string
    file = open(filename.lower().replace(" ", "_") + ".json", "w")

    # save beautified JSON file for character info
    with file as output:
        output.write(json.dumps(char_dict, indent=4))

    file.close()


def main():
    global race_data, feats_data, classes_data, weapons_data, levels_data, classfeats_data, ac_data

    # load data files for races, feats, and classes
    race_data, feats_data, classes_data, weapons_data, levels_data, classfeats_data, ac_data = load_data()

    while True:
        print("Options: ",
              "1: Create Character",
              "2: Load Character and Initialize Potential Damage",
              "3: Load Character Damage Curve",
              "4: Load and Compare two character damage curves",
              "5: Exit Program",
              sep="\n")

        choice = input("What will you do? > ")

        if choice == "1":  # create character
            create_char()
        elif choice == "2":
            load_character()

            char_init = copy.deepcopy(char_data)

            # run damage calculator
            damage_per_level()
            char_init["damagecurve"] = char_data["damagecurve"]

            save_to_json(char_init, char_init["name"])

        elif choice == "3":
            load_character()
            if char_data["damagecurve"] == {}:
                print("Please run option 2 first to initialize the potential damage.\n")

            else:
                text = char_data["name"] + " - Average Damage: " + \
                    str(round(sum(char_data["damagecurve"].values()) / 20))

                # draw graph
                SimpleGraphics.clear()
                grapher.graph_single(char_data["damagecurve"], text)
                print("Graph updated.\n")
        elif choice == "4":
            while True:
                SimpleGraphics.clear()

                print("\nFirst character.")
                load_character()
                if char_data["damagecurve"] == {}:
                    print(
                        "Please run option 2 first to initialize the potential damage.\n")
                    break

                first_dmg = dict(char_data["damagecurve"])
                first_text = str(char_data["name"]) + " - blue - Average Damage: " + \
                    str(round(sum(char_data["damagecurve"].values()) // 20, 2))

                print("\nSecond character.")
                load_character()
                if char_data["damagecurve"] == {}:
                    print(
                        "Please run option 2 first to initialize the potential damage.\n")
                    break
                second_dmg = dict(char_data["damagecurve"])
                second_text = str(char_data["name"]) + " - red - Average Damage: " + \
                    str(round(sum(char_data["damagecurve"].values()) // 20, 2))

                grapher.graph_double(first_dmg, second_dmg,
                                     first_text, second_text)

                print("Graph updated.\n")
                break
        elif choice == "5":
            print("\nThank you. Please close the Simplegraphics window separately.")
            break
        else:
            print("Invalid selection.\n")


if __name__ == '__main__':
    # initializing globals
    char_data = {}
    feat_uses = {}
    race_data, feats_data, classes_data, weapons_data, levels_data, classfeats_data, ac_data = \
        {}, {}, {}, {}, {}, {}, {}

    main()
