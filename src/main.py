import auth, logging, random, telebot
from twitter import *
from helpers import helpers, logger, markov, reddit

CON = logger.CON

"""
API and auth keys. Will be located in auth.py.
"""

# Kuma-chan's unique ID.
bot = telebot.TeleBot(auth.Telegram.api_key)

# Kuma-chan's twitter, @KumaKaiNi.
t = Twitter(auth = OAuth(auth.TwitterAuth.access_key, auth.TwitterAuth.access_key_secret, auth.TwitterAuth.consumer_key, auth.TwitterAuth.consumer_key_secret))


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
      + "/ship - posts an image from the top posts of r/warshipporn.\n"
      + "/tank - posts an image from the top posts of r/tankporn.\n"
      + "\n"
      + "Just as a warning, there is a 1% chance that I will tweet whatever bullshit you just said, kuma. https://twitter.com/KumaKaiNi\n"
      + "\n"
      + "Source: https://github.com/rekyuu/telegram-kuma")


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


"""
Regex listeners.
"""

# Returns a greeting if a user starts a sentence with the following regex.
GREETS = ['hi', 'hello', 'yo', 'sup']
GREET_REPLIES = ['sup loser', 'yo', 'ay', 'go away', 'hi', 'wassup']
@bot.message_handler(regexp=to_regex(GREETS,'','()|( ).*'))
def send_hello (m):
   out = GREET_REPLIES[random.randint(0, len(GREET_REPLIES) - 1)]
   bot.send_message(m.chat.id, out)
   print(CON['msg'], out)


# Replies to thank you's.
THANKS = ['thank you kuma', 'thanks kuma', 'ty kuma']
TY_REPLIES = ['np', 'don\'t mention it', 'anytime', 'sure thing', 'ye whateva']
@bot.message_handler(regexp=to_regex(THANKS))
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

   # 1:20 chance of firing a markov chain message
   if prob(1,20) == True:
      file_ = open('./wordlogs/' + str(m.chat.id) + '.log', encoding='utf8')

      # Will file once the log reaches 100 lines or more
      if len(file_.read().splitlines()) >= 100:
         word_count, msg_total = 0
         for line in file_.read().splitlines():
            word_count += int(len(line.split()))
            msg_total += 1
         word_avg = word_count / msg_total

         markov = markov.Markov(file_)
         out = markov.generate_markov_text(word_avg + random.randint(0,5))

         bot.send_message(m.chat.id, out)
         print(CON['msg'], out)
         t.statuses.update(status=out + ' *Kuma Kai Ni')
         print(CON['twt'], out + ' *Kuma Kai Ni')
      file_.close()

   # Really simple and lazy spam protection
   if last_msg != m.text:
      last_msg = m.text
      # 1:100 chance to tweet the last message recieved
      if prob(1,100) == True:
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
Main command listener.
"""

bot.polling(none_stop=True)
print(CON['log'], 'Kuma! Shutsugeki suru, kuma!')
while True:
   time.sleep(100)