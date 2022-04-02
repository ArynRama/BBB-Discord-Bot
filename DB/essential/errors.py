from discord.ext.commands.errors import CheckFailure

class NotDev(CheckFailure):
    """User is not a dev."""
    pass