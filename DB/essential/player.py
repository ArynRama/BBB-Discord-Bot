import discord
import wavelink
from typing import Union

class Player(wavelink.Player):
    def __init__(self, dj:discord.Role=None):
        self.dj = dj