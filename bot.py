import discord
import threading
import datetime
import pandas as pd

import config
import embed_setup

df = pd.read_csv('data.csv')

def update_csv(user_name, time, status):
	global df
	new_row = {'user_name': user_name, 'time': time, 'status': status}
	df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
	df.to_csv('data.csv', index=False)

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec)
		func()
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t

def check_status():
	time = datetime.datetime.now().strftime("%Y-%b-%d %I:%M:%S %p")
	for member in client.get_all_members():
		status = member.raw_status
		try: # This is needed if the user is not in db
			last_status = df[df['user_name'] == member.name].iloc[-1:]['status'].values[0]
			if last_status != status:
				update_csv(member.name, time, status)
		except:
			update_csv(member.name, time, status)

def get_last_status_change(user_name):
	return df[(df['user_name'] == user_name)].iloc[-1]['time']

def format_time_difference(last_time_str):
	TIME_FORMAT = "%Y-%b-%d %I:%M:%S %p"
	last_time = datetime.datetime.strptime(last_time_str, TIME_FORMAT)

	now = datetime.datetime.now()
	time_diff = now - last_time

	print(time_diff)
	# If the time is less than 24 hours ago
	if time_diff.days == 0:
		return last_time.strftime('%I:%M %p')  # Hour and minute (am/pm)

	# If it's been between 24 and 48 hours ago
	elif time_diff.days == 1:
		return f"{time_diff.seconds // 3600 + 24} hours ago"  # Hours ago

	# If it's been more than 48 hours ago
	else:
		return f"{time_diff.days} days ago"  # Days ago

async def get_user_messages(user_name, guild, limit=10):
	MAX_SEARCH = 1000
	messages_info = []

	for channel in guild.text_channels:
		async for user_message in channel.history(limit=MAX_SEARCH):
			if str(user_message.author) == user_name:
				if len(messages_info) >= limit:
					break
				message_time = user_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
				messages_info.append((user_message.content, message_time))
		if len(messages_info) >= limit:
			break
	
	if not messages_info:
		messages_info = [('No message in last 1000 messages.', 'N/A')]

	return messages_info

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	set_interval(check_status, 1)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if message.content.startswith('$'):
		user_name =  'owowowen'
		if len(message.content) > 1:
			_, _, user_name = message.content.partition('$')
		
		for user in client.get_all_members():
			if str(user.name) == user_name:
				user_pfp = user.display_avatar
				user_status = user.raw_status
				last_online = format_time_difference(get_last_status_change(user_name))
				user_messages = await get_user_messages(user_name, message.guild, limit=1)
				embed = embed_setup.status_embed(user_name, user_pfp, user_status, last_online, user_messages[0][0])
				await message.channel.send(embed=embed)

client.run(config.api_key, log_handler=config.handler)