import json, random, telebot, time, urllib, os
from twitter import *
from helpers import auth, folders, helpers, logger, markov, reddit

CACHE = folders.CACHE
DIR = folders.DIR
CON = logger.CON
DIR = folders.DIR


"""
API and auth keys. Will be located in auth.py.
"""

try:
	file_ = open(DIR + '/config.json', encoding='utf8')
	config = json.loads(file_.read())
	auth = config['auth']
except:
	print(CON['err'], "config.json not found. Be sure to fill out default-config.json and rename it to config.json.")

# Kuma-chan's unique ID.
bot = telebot.TeleBot(auth['telegram']['api_key'])

# Kuma-chan's twitter, @KumaKaiNi.
t = Twitter(auth = OAuth(
	auth['twitter']['access_key'],
	auth['twitter']['access_key_secret'],
	auth['twitter']['consumer_key'],
	auth['twitter']['consumer_key_secret']
))

file_.close()

"""
Command definitions and listeners.
"""

# List off commands.
@bot.message_handler(commands=['help'])
def send_help (m):
	bot.send_message(m.chat.id,
		"First ship of the Kuma-class light cruisers, Kuma, kuma.\n"
		+ "Born in Sasebo, kuma. I got some old parts, but I'll try my best, kuma.\n"
		+ "\n"
		+ "/add x y z - takes your numbers and adds them together.\n"
		+ "/coin - flips a coin.\n"
		+ "/meme - sends a meme.\n"
		+ "/predict - sends a prediction.\n"
		+ "/roll x - rolls a number between 1 and x. Also takes 4d6, etc.\n"
		+ "/say - repeats what you say.\n"
		+ "/search - returns the first Google result.\n"
		+ "/image - returns the first Google Images result.\n"
		+ "/youtube - returns the first YouTube video.\n"
		+ "/danbooru - returns a random Danbooru image by tags (ie, \"kuma (kantai collection)\").\n"
		+ "/ship - posts an image from the top posts of r/warshipporn.\n"
		+ "/tank - posts an image from the top posts of r/tankporn.\n"
		+ "\n"
		+ "Source (v1.1): https://github.com/rekyuu/telegram-kuma")


# Command to let you know she's alive.
@bot.message_handler(commands=['kuma'])
def send_welcome (m):
	out = "Kuma ~"
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Repeats what the user just said.
@bot.message_handler(commands=['say'])
def send_say (m):
	try:
		out = m.text.split(' ', 1)[1]
	except:
		out = 'There is nothing to say, kuma.'
	finally:
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)


# Adds two numbers or makes jokes.
@bot.message_handler(commands=['add'])
def add_num (m):
	msg = m.text.split()
	del msg[0]

	try:
		add = 0
		for n in msg:
			add += int(n)

		if len(msg) == 2 and msg[0] == '1' and msg[1] == '1':
			out = "1 + 1 = 69 get it ?? lol ahahahahaha 69 = sexspoisition 1 = girl + boy ahaha"
		elif len(msg) == 0:
			out = "You didn't submit numbers!"
		else:
			out = "Your sum of numbers is: " + str(add)
	except:
		if m.from_user.username == "Liseda":
			out = "fuck off"
		else:
			out = "Invalid input, sorry!"
	finally:
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)


# Sends the user a boat!
@bot.message_handler(commands=['ship'])
def send_boat (m):
	reddit.send_sub_image (m, 'warshipporn')


# Sends the user a tank!
@bot.message_handler(commands=['tank'])
def send_tonk (m):
	reddit.send_sub_image (m, 'tankporn')


# Sends the user a meme!
@bot.message_handler(commands=['meme'])
def send_meme (m):
	reddit.send_sub_image (m, 'foodporn')


# Anti-Wayne command
@bot.message_handler(commands=['dank', 'kush', 'pot', 'merrywanna'])
def send_dank (m):
	name = m.from_user.username
	if name is None:
		name = m.from_user.first_name
	out = ''.join(['Shut the fuck up, @', name])
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Sends the user a prediction.
PREDICTIONS = [
	'It is certain.',
	'It is decidedly so.',
	'Without a doubt.',
	'Yes, definitely.',
	'You may rely on it.',
	'As I see it, yes.',
	'Most likely.',
	'Outlook good.',
	'Yes.',
	'Signs point to yes.',
	'Reply hazy, try again.',
	'Ask again later.',
	'Better not tell you now.',
	'Cannot predict now.',
	'Concentrate and ask again.',
	'Don\'t count on it.',
	'My reply is no.',
	'My sources say no.',
	'Outlook not so good.',
	'Very doubtful.'
]
@bot.message_handler(commands=['predict'])
def send_prediction (m):
	if len(m.text.split()) == 1:
		out = "You didn't ask a question ya dingus"
	else:
		out = PREDICTIONS[random.randint(0, len(PREDICTIONS) - 1)]
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Flips a coin.
@bot.message_handler(commands=['flip', 'coin'])
def send_coinflip (m):
	coin = random.randint(0,1)
	if coin == 0:
		out = "Heads."
	else:
		out = "Tails."
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Rolls dice.
@bot.message_handler(commands=['roll'])
def send_diceroll (m):
	try:
		dice = m.text.split()[1]
		mult = dice.split('d')
		if len(m.text.split()) >= 3:
			out = "Please only send one input."
		elif len(mult) == 2:
			if int(mult[0]) <= 1 or int(mult[1]) <= 1:
				out = "Inputs must be 2 or more. Example: 4d6"
			else:
				out = "Rolled"
				for x in range (0, int(mult[0])):
					out = ' '.join([out, str(random.randint(1, int(mult[1]))) + ","])
				out = out[:-1] # Remove [,]
		else:
			if int(dice) <= 1:
				out = "Input must be 2 or more."
			else:
				out = "Rolled a " + str(random.randint(0,int(dice)))
	except:
		out = "Please send only numbers."
	finally:
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)


fights = [
	'{} punches {}.',
	'{} kicks {}.',
	'{} licks {}.',
	'{} pets {}.',
	'{} scratches behind {}\'s ears.',
	'{} gives {} the bed eyes. Nothing happens.',
	'{} attemps at programming a script to defeat {}. It doesn\'t work.',
	'{} sends memes to {}. They\'re not very funny.',
	'{} pulls a knife on {}.',
	'{} unzips {}.',
	'{} unzips dick. {} is displeased.',
	'{} sends {} a love letter.',
	'{} asks {} to take a hike.',
	'{} sniffs {}.',
	'{} cries. {} laughs mockingly.',
	'{} does nothing. {} doesn\'t know how to react.',
	'{} gets nuked by {}.',
	'{} forgets to read {} a bedtime story.',
	'{} makes a surprise punch at {}.'
]
@bot.message_handler(commands=['fight', 'battle', 'faceoff'])
def send_vs (m):
	contestants = m.text.split()
	del contestants[0]
	contestants = ''.join(contestants)
	contestants = contestants.split('vs')

	winner = random.choice(contestants)
	contestants.remove(winner)
	loser = contestants[0]

	for i in range(3):
		contestants = [winner, loser]
		fighter0 = random.choice(contestants)
		contestants.remove(fighter0)
		fighter1 = contestants[0]

		fight = random.choice(fights)

		out = fight.format(fighter0, fighter1)
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)

	win_line = random.choice(fights)
	out = win_line.format(winner, loser)
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)

	out = '{} wins!'.format(winner)
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Sends a link to /r/botsrights
@bot.message_handler(commands=['botsrights'])
def send_rights (m):
	out = "http://reddit.com/r/botsrights"
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Prints available json to the console.
@bot.message_handler(commands=['json'])
def print_json (m):
	print(CON['log'], 'info:', m.__dict__)
	print(CON['log'], 'from_user:', m.from_user.__dict__)
	print(CON['log'], 'chat:', m.chat.__dict__)


# Prints available json to the console.
@bot.message_handler(commands=['test'])
def testing_function (m):
	reddit.send_sub_image (m, 'warshipporn')


# Responds with the first Google result
@bot.message_handler(commands=['s', 'search', 'google', 'find'])
def search (m):
	query = m.text.split()
	del query[0]
	query = '%20'.join(query)

	api = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={0}'.format(query)
	request = urllib.request.urlopen(api)
	response = request.read().decode('utf8')
	results = json.loads(response)
	out = results['responseData']['results'][0]['unescapedUrl']

	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Responds with the first YouTube result (by cheating!)
@bot.message_handler(commands=['yt', 'youtube'])
def search (m):
	query = m.text.split()
	del query[0]
	query = '%20'.join(query)

	api = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=youtube%20{0}'.format(query)
	request = urllib.request.urlopen(api)
	response = request.read().decode('utf8')
	results = json.loads(response)
	out = results['responseData']['results'][0]['unescapedUrl']

	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Responds with the first Google Images result
@bot.message_handler(commands=['i', 'img', 'image', 'pic', 'picture'])
def image_search (m):
	query = m.text.split()
	del query[0]
	query = '%20'.join(query)

	api = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}'.format(query)
	request = urllib.request.urlopen(api)
	response = request.read().decode('utf8')
	results = json.loads(response)
	dl = results['responseData']['results'][0]['unescapedUrl']
	via = results['responseData']['results'][0]['originalContextUrl']
	filename = dl.split('/')[-1]

	try:
		# Downloads the image.
		print(CON['log'], "Downloading", filename + "...")
		if not os.path.exists(CACHE['img']):
			os.makedirs(CACHE['img'])
		urllib.request.urlretrieve(dl, CACHE['img'] + filename)

		# Sends the downloaded image and the title.
		photo = open(CACHE['img'] + filename, 'rb')
		bot.send_photo(m.chat.id, photo)
		print(CON['img'], filename)

		# Closes the photo and removes it from the system.
		photo.close()
		os.remove(CACHE['img'] + filename)

		out = 'via ' + via
	except:
		print(CON['err'], "Unable to download image. Sending link.")
		out = via
	finally:
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)


# Danbooru search and random responder (removed).
NO = ['nope.', 'nuh-uh.', 'no way.', 'no.', 'geeeeet dunked on.', 'not on my watch.']
@bot.message_handler(commands=['dan', 'danbooru'])
def danbooru_search (m):
	out = NO[random.randint(0, len(NO) - 1)]
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)

	"""
	limit = 100
	page = 1

	query = m.text.split()
	del query[0]
	query = ' '.join(query)
	query = query.split(',')
	tags = []
	for tag in query:
		tag = tag.split()
		tag = '_'.join(tag)
		tags.append(tag)
	tags = ';'.join(tags)

	posts = 'https://danbooru.donmai.us/posts.json?limit={0}&page={1}&tags={2}'.format(limit, page, tags)
	request = urllib.request.urlopen(posts)
	response = request.read().decode('utf8')
	results = json.loads(response)
	print(CON['log'], "JSON loaded!")
	print(CON['log'], "Checking for a SFW image...")

	if len(results) == 0:
		sfw = False
		nothing = True
	else:
		nothing = False
		while len(results) >= 1:
			json_id = random.randint(0, len(results) - 1)
			post = results[json_id]
			sfw = True
			if post['rating'] is not 's':
				sfw = False
				del results[json_id]
				print(CON['err'], "NSFW! Trying again...")
			if sfw == True:
				break

	if sfw == True:
		dl = 'https://danbooru.donmai.us' + post['file_url']
		via = 'https://danbooru.donmai.us/posts/' + str(post['id'])
		filename = dl.split('/')[-1]

		try:
			# Downloads the image.
			print(CON['log'], "Downloading", filename + "...")
			if not os.path.exists(CACHE['img']):
				os.makedirs(CACHE['img'])
			urllib.request.urlretrieve(dl, CACHE['img'] + filename)

			# Sends the downloaded image and the title.
			photo = open(CACHE['img'] + filename, 'rb')
			bot.send_photo(m.chat.id, photo)
			print(CON['img'], filename)

			# Closes the photo and removes it from the system.
			photo.close()
			os.remove(CACHE['img'] + filename)

			out = 'via ' + via
		except:
			print(CON['err'], "Unable to download image. Sending link.")
			out = via
		finally:
			bot.send_message(m.chat.id, out)
			print(CON['msg'], out)

	elif nothing == True:
		out = "Nothing found with that query."
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)

	else:
		out = "No SFW images found, sorry!"
		bot.send_message(m.chat.id, out)
		print(CON['msg'], out)
	"""


"""
Regex listeners.
"""

# Returns a greeting if a user starts a sentence with the following regex.
GREETS = ['hi', 'hello', 'yo', 'sup']
GREET_REPLIES = ['sup loser', 'yo', 'ay', 'go away', 'hi', 'wassup']
@bot.message_handler(regexp=helpers.to_regex(GREETS,'','()|( ).*'))
def send_hello (m):
	out = GREET_REPLIES[random.randint(0, len(GREET_REPLIES) - 1)]
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# Replies to thank you's.
THANKS = ['thank you kuma', 'thanks kuma', 'ty kuma']
TY_REPLIES = ['np', 'don\'t mention it', 'anytime', 'sure thing', 'ye whateva']
@bot.message_handler(regexp=helpers.to_regex(THANKS))
def send_thanks (m):
	out = TY_REPLIES[random.randint(0, len(TY_REPLIES) - 1)]
	bot.send_message(m.chat.id, out)
	print(CON['msg'], out)


# 1% chance to tweet an incoming message, if none of the above were processed.
last_msg = ''
@bot.message_handler(regexp=".")
def all_other_messages (m):
	global last_msg

	# Logs incoming messages to a file
	logger.word_log(m)

	# 1% chance of firing a markov chain message
	if helpers.prob(1,100) == True:
		file_ = open(CACHE['wordlogs'] + str(m.chat.id) + '.log', encoding='utf8')
		messages = file_.read().splitlines()
		# Will file once the log reaches 100 lines or more
		if len(messages) >= 100:
			word_count = 0
			for message in messages:
				words = message.split()
				word_count += int(len(words))
			word_avg = word_count / len(messages)

			mk = markov.Markov(file_)
			out = mk.generate_markov_text(int(word_avg) + random.randint(0,5))

			bot.send_message(m.chat.id, out)
			print(CON['msg'], out)
			t.statuses.update(status=out + ' *KumaKaiNi')
			print(CON['twt'], out + ' *KumaKaiNi')
		file_.close()

	# Really simple and lazy spam protection
	# Only for lame meme-chat (currently completely disabled)
	"""
	if m.chat.id == -22706117:
		if last_msg != m.text:
			last_msg = m.text
			# 0.5% chance to tweet the last message recieved
			if helpers.prob(1,200) == True:
				if m.text.split(':')[0] in ['http', 'https']:
					pass
				else:
					name = m.from_user.username
					if name is None:
						name = m.from_user.first_name
					out = m.text + ' *' + name
					t.statuses.update(status=out)
					bot.send_message(m.chat.id, "lmao I'm live tweeting this shit")
					print(CON['twt'], out)
		else:
			last_msg = m.text
	"""


"""
Main command listener.
"""

bot.polling(none_stop=True)
print(CON['log'], 'Kuma! Shutsugeki suru, kuma!')
while True:
	time.sleep(100)
