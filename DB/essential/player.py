import discord
import wavelink
from typing import Optional

class Player(wavelink.Player):
    def __init__(self): #dj:Optional[discord.Role]=None):
        self.Queue: wavelink.Queue = wavelink.Queue()
        super().__init__()