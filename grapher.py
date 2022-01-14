from SimpleGraphics import *


def graph_lines():
    line(20, 20, 20, 580)
    line(20, 580, 780, 580)
    for lev in range(20):
        text(38 * lev + 35, 590, str(lev + 1))


def graph_single(damagecurve, text_content):
    graph_lines()

    max_dmg = max(damagecurve.values())
    setFill("")
    setOutline("deep sky blue")
    text(200, 50, text_content)
    for i in range(20):
        rect(38 * i + 20, 580 - (500 * damagecurve[str(i + 1)] / max_dmg), 37.4,
             500 * damagecurve[str(i + 1)] / max_dmg)


def graph_double(damage1, damage2, text1, text2):
    graph_lines()

    max_dmg = max(list(damage1.values())+list(damage2.values()))

    setOutline("blue")
    setFill("")
    text(200, 50, text1)

    for i in range(20):
        rect(38 * i + 20, 580 - (500 * damage1[str(i + 1)] / max_dmg), 37.4,
             500 * damage1[str(i + 1)] / max_dmg)

    setOutline("OrangeRed2")
    setFill("") 
    text(200, 70, text2)
    
    for i in range(20):
        rect(38 * i + 20, 580 - (500 * damage2[str(i + 1)] / max_dmg), 37.4,
             500 * damage2[str(i + 1)] / max_dmg)
