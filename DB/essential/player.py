import discord
import wavelink
from typing import Optional

class Player(wavelink.Player):
    def __init__(self): #dj:Optional[discord.Role]=None):
        #self.dj = dj
        super().__init__()