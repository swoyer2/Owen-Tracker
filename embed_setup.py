from enum import Enum
import discord

class Emojis(Enum):
    online = '🟢'
    offline = '🔴'
    idle = '🌙'
    dnd = '🔕'
    invisible = '⚪️'

def status_embed(name, pfp, status, last_status_change, most_recent_message):
    description = f"**Status:** {Emojis[status].value}\n**{status.capitalize()} since:** {last_status_change}\n**Last Message:** {most_recent_message}"
    embed = discord.Embed(
        title=f"{name}",
        description=description,
        color=0xff0000  # Red color
	)
    if pfp:
        embed.set_image(url=pfp)
    return embed