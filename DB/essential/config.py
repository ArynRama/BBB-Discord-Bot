from discord import Color
from configparser import ConfigParser
import json

config = ConfigParser()
config.read("options.ini")

def botcolor():
    color = config["Setting"]["BotColor"]
    color = color.strip("[")
    color = color.strip("]")
    color = color.split(",")
    b = 0
    for i in color:
        color[b] = i.strip()
        b = b +1
    r = color[0]
    g = color[1]
    b = color[2]
    botcolor = Color.from_rgb(r, g, b)
    return botcolor

def devs():
    devs = config["Setting"]["Devs"]
    return devs