import discord
import threading
import datetime
import pandas as pd
import matplotlib.pyplot as plt

import config

last_online = None
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
	global last_online
	time = datetime.datetime.now().strftime("%Y-%b-%d %I:%M:%S %p")
	for member in client.get_all_members():
		status = member.raw_status
		try: # This is needed if the user is not in db
			last_status = df[df['user_name'] == member.name].iloc[-1:]['status'].values[0]
			if last_status != status:
				update_csv(member.name, time, status)
		except:
			update_csv(member.name, time, status)

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	set_interval(check_status, 3)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$status'):
		member_name_to_check = 'owowowen'
		if "user=" in message.content:
			_, _, user_name = message.content.partition('user=')
			member_name_to_check = user_name
		for member in client.get_all_members():
			if str(member.name) == member_name_to_check:
				online_statuses = df[(df['user_name'] == member.name) & (df['status'] != 'offline')]
				offline_statuses = df[(df['user_name'] == member.name) & (df['status'] == 'offline')]
				try:
					last_online = online_statuses.iloc[-1]['time']
					last_offline = offline_statuses.iloc[-1]['time']
				except:
					last_online = 'Never'
					last_offline = 'Never'
				member_status = member.raw_status

				if member_status != 'offline':
					await message.channel.send(f'{member} is {member_status} since {last_online}')
				else:
					await message.channel.send(f'{member} is {member_status}.\nLast online from {last_online} till {last_offline}.')
	
	if message.content.startswith('$graph'):
		user_name = 'owowowen'
		if "user=" in message.content:
			_, _, user_name = message.content.partition('user=')

		times = df[(df['user_name'] == user_name)]['time'].values
		statuses = df[(df['user_name'] == user_name)]['status'].apply(lambda x: 1 if x == 'online' else 0).values
		plt.step(times, statuses, where='post', label='Online/Offline', color='b')
		plt.yticks([0, 1], ['Offline', 'Online'])
		plt.xlabel('Time')
		plt.ylabel('Status')
		plt.title(f'{user_name} Status Over Time')
		plt.xticks(rotation=45)
		plt.savefig('user_status_over_time.png', bbox_inches='tight')
		await message.channel.send(file=discord.File('user_status_over_time.png'))
		

client.run(config.api_key, log_handler=config.handler)