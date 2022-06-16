from discord import Color


BotColor = [0, 152, 252]
Prefix= "-"


def botcolor():
    r = BotColor[0]
    g = BotColor[1]
    b = BotColor[2]
    color = Color.from_rgb(r, g, b)
    return color


def devs(self):
    return self.client.db.child("devs").get().val()
