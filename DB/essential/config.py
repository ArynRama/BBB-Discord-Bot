from discord import Color


BotColor = [0, 152, 252]
Prefix= "-"
Devs = ["419848392223621120","430389637287247882"]


def botcolor():
    r = BotColor[0]
    g = BotColor[1]
    b = BotColor[2]
    color = Color.from_rgb(r, g, b)
    return color


def devs():
    return Devs
