import json

races = {"human": {"subrace": {"vanilla": {"asi": [False, {"str": 1, "dex": 1, "con": 1,
                                                           "int": 1, "wis": 1, "cha": 1}]},
                               "variant": {"asi": [True, 2, {"str": True, "dex": True, "con": True,
                                                             "int": True, "wis": True, "cha": True}], "feat": 1}}
                   },
         "elf": {"subrace": {"wood": {"asi": [False, {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 1, "cha": 0}],
                                      "weapons": ["longsword, shortsword, shortbow, longbow"]},
                             "drow": {"asi": [False, {"str": 0, "dex": 2, "con": 0, "int": 0, "wis": 0, "cha": 1}],
                                      "weapons": ["rapier, shortsword, hand_crossbow"]}}
                 },
         "halfling": {"subrace": {"lightfoot": {"asi": [False, {"str": 0, "dex": 2, "con": 0,
                                                                "int": 0, "wis": 0, "cha": 1}],
                                                "feat": "halfling_lucky"},
                                  "ghostwise": {"asi": [False, {"str": 0, "dex": 2, "con": 0,
                                                                "int": 0, "wis": 1, "cha": 0}],
                                                "feat": "halfling_lucky"}}
                      }
         }

# all bonus feats. do not confuse with class feats!
feats = {"elvenAccuracy": {"asi": [True, 2, {"str": False, "dex": True, "con": False,
                                             "int": True, "wis": True, "cha": True}]},
         "greatWeaponMaster": {},
         "sharpshooter": {},
         "lucky": {"uses": 3, "recharge": True}}

# class feats. this file lists only feats with uses
classfeats = {"fighter": {"actionsurge": {"uses": 1, "recharge": True},
                          "fightingspirit": {"uses": 3, "recharge": False}}}

classes = {"fighter": ["champion", "samurai"]}

# levelled feats need to check level and scale accordingly!
# make separate fighting style function! ["archery", "dueling", "greatweaponfighting", "twoweaponfighting"]
classlevels = {"fighter": {1: "fightingstyle",
                           2: "actionsurge",
                           3: {"champion": "improvedcritical",
                               "samurai": "fightingspirit"},
                           4: "asi",
                           5: "extraattack",
                           6: "asi",
                           8: "asi",
                           10: {"champion": "fightingstyle"},
                           12: "asi",
                           14: "asi",
                           16: "asi",
                           19: "asi"
                           }}

# weapons. data can be added later
weapons = {"dagger": "1d4", "mace": "1d6", "greatclub": "1d8",
           "shortbow": "1d6", "lightcrossbow": "1d8", "shortsword": "1d6", "rapier": "1d8", "longsword": "1d8",
           "greataxe": "1d12", "greatsword": "2d6", "handcrossbow": "1d6", "longbow": "1d8", "heavycrossbow": "1d10"}

# enemy AC per CR
enemy_ac = {1: 13, 2: 13, 3: 13, 4: 14, 5: 15, 6: 15, 7: 15, 8: 16, 9: 16, 10: 17,
            11: 17, 12: 17, 13: 18, 14: 18, 15: 18, 16: 18, 17: 19, 18: 19, 19: 19, 20: 19}


def save_to_json(dic, filename):
    # creates/edits file with character name as filename, converted to a filename-appropriate string
    file = open(filename.lower().replace(" ", "_") + ".json", "w")

    # save beautified JSON datafile for programs
    with file as output:
        output.write(json.dumps(dic, indent=4))

    file.close()


save_to_json(classes, "classes")
save_to_json(feats, "feats")
save_to_json(races, "races")
save_to_json(weapons, "weapons")
save_to_json(classlevels, "classlevels")
save_to_json(classfeats, "classfeats")
save_to_json(enemy_ac, "enemy_ac")
