import discord
import threading
import datetime

import config

last_online = None

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec)
		func()
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t

def check_if_online():
	global last_online
	for online_member in client.get_all_members():
		member_id = online_member.id
		if member_id == config.owen_id:
			member_status = online_member.raw_status
			if member_status != 'offline':
				last_online = datetime.datetime.now()

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	set_interval(check_if_online, 3)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$status'):
		for online_member in client.get_all_members():
			member_id = online_member.id
			if member_id == config.owen_id:
				member_status = online_member.raw_status
				await message.channel.send(f'{online_member} is {member_status}. Last online at {last_online}.')

client.run(config.api_key, log_handler=config.handler)