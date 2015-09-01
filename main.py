import auth, datetime, os, praw, random, telebot, time, urllib.request
from twitter import *

dt = datetime.datetime

# Kuma-chan's unique ID.
bot = telebot.TeleBot(auth.Telegram.api_key)

# Kuma-chan's twitter, @KumaKaiNi.
t = Twitter(auth = OAuth(auth.TwitterAuth.access_key, auth.TwitterAuth.access_key_secret, auth.TwitterAuth.consumer_key, auth.TwitterAuth.consumer_key_secret))

# Reddit stuff.
r = praw.Reddit(user_agent='Telegram:KumaKaiNi:v1.0.0 (by @rekyuu_senkan)')


# Function to populate top posts of a given subreddit
def get_top_posts (sub, list_name, time_got):

   time_got = dt.now()
   subr = r.get_subreddit(sub)

   print("[LOG] Populating list...")
   pid = 0
   for post in subr.get_hot(limit=25):
      url = post.url.encode("utf-8")
      title = post.title.encode("utf-8")
      list_name.append({'pid': pid, 'title': title, 'url': url})
      pid += 1
   print("[LOG] List populated!")


# Function that sends the image
IMAGE_TYPES = ['jpg', 'jpeg', 'gif', 'png']
def send_sub_image (msg, sub, list_name, time_got):

   # Checks to make sure there is a listing.
   if len(list_name) == 0:
      print("[LOG] Nothing in list! Repopulating.")
      get_top_posts(sub, list_name, time_got)
   # Checks freshness of posts.
   elif dt.now() - time_got >= datetime.timedelta(days=1):
      print("[LOG] 24 hours have past since last update!")
      get_top_posts(sub, list_name, time_got)

   # Chooses a random listing and downloads the image.
   while True:
      try:
         rand = random.randint(0, len(list_name) - 1)
         dl = str(list_name[rand]['url']).split("'")[1]
         filename = dl.split('/')[-1]
         print("[LOG] Downloading " + filename + "...")
   
         if filename.split('.')[-1] not in IMAGE_TYPES:
            # If the file is not an image, it will try again.
            print("[LOG] Not an image. Deleting entry and trying again.")
            del list_name[rand]
            if len(list_name) == 0:
               get_top_posts(sub, list_name, time_got)
         else:
            # Downloads the image.
            urllib.request.urlretrieve(dl, filename)
   
            # Sends the downloaded image and the title.
            photo = open(filename, 'rb')
            out = str(list_name[rand]['title']).split("'")[1]
            bot.send_photo(msg.chat.id, photo)
            print('[IMG]', filename)
   
            bot.send_message(msg.chat.id, out)
            print('[MSG]', out)
   
            # Closes the photo and removes it from the system.
            photo.close()
            os.remove(filename)
            del list_name[rand]
            break
      except HTTPError:
         print("[LOG] Error downloading image. Trying again.")
         del list_name[rand]
         if len(list_name) == 0:
            get_top_posts(sub, list_name, time_got)


# Regex function
def to_regex (words, beg='', end=''):
   regex = '^(' + beg + ')('
   for word in words:
      regex += '('
      letters = list(word)
      for letter in letters:
         regex += '('
         regex += letter.upper()
         regex += '|'
         regex += letter.lower()
         regex += ')'
      regex += ')|'
   regex = regex[:-1]
   regex += ')(' + end + ')$'
   return regex


# Command to let you know she's alive.
@bot.message_handler(commands=['kuma'])
def send_welcome (m):
   out = "Kuma ~"
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


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


# Repeats what the user just said.
@bot.message_handler(commands=['say'])
def send_say (m):
   try:
      out = m.text.split(' ', 1)[1]
   except:
      out = 'There is nothing to say, kuma.'
   finally:
      bot.send_message(m.chat.id, out)
      print('[MSG]', out)


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
      print('[MSG]', out)


# Sends the user a boat!
warships = []
warships_got = dt.now()
@bot.message_handler(commands=['ship'])
def send_boat (m):
   global warships
   global warships_got
   send_sub_image (m, 'warshipporn', warships, warships_got)


# Sends the user a tank!
tanks = []
tanks_got = dt.now()
@bot.message_handler(commands=['tank'])
def send_tonk (m):
   global tanks
   global tanks_got
   send_sub_image (m, 'tankporn', tanks, tanks_got)


# Sends the user a meme!
memes = []
memes_got = dt.now()
@bot.message_handler(commands=['meme'])
def send_tonk (m):
   global memes
   global memes_got
   send_sub_image (m, 'foodporn', memes, memes_got)


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
   print('[MSG]', out)
   

# Flips a coin.
@bot.message_handler(commands=['flip', 'coin'])
def send_coinflip (m):
   coin = random.randint(0,1)
   if coin == 0:
      out = "Heads."
   else:
      out = "Tails."
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)
   

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
            out = "Rolled " 
            for x in range (0, int(mult[0])):
               out += str(random.randint(1, int(mult[1])))
               out += ", "
            out = out[:-1] # Remove [ ]
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
      print('[MSG]', out)
      

# Sends a link to /r/botsrights
@bot.message_handler(commands=['botsrights'])
def send_prediction (m):
   out = "http://reddit.com/r/botsrights"
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


# Returns a greeting if a user starts a sentence with the following regex.
GREETINGS = ['sup loser', 'yo', 'ay', 'go away', 'hi', 'wassup']
SEARCH_FOR = ['hi', 'hello', 'hey', 'sup']
@bot.message_handler(regexp=to_regex(SEARCH_FOR,'','()|( ).*'))
def send_hello (m):
   out = GREETINGS[random.randint(0, len(GREETINGS) - 1)]
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


# Replies to thank you's.
THANKS = ['thank you kuma', 'thanks kuma', 'ty kuma']
TY_REPLIES = ['np', 'don\'t mention it', 'anytime', 'sure thing', 'ye whateva']
@bot.message_handler(regexp=to_regex(THANKS))
def send_thanks (m):
   out = TY_REPLIES[random.randint(0, len(TY_REPLIES) - 1)]
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


# 1% chance to tweet an incoming message.
last_msg = ''
@bot.message_handler(regexp=".")
def send_tweet (m):
   global last_msg
   
   if last_msg != m.text:
      last_msg = m.text
      prob = random.randint(1,100)
      if prob <= 1:
         t.statuses.update(status='"' + m.text + '"')
         bot.send_message(m.chat.id, "lmao I'm live tweeting this shit")
         print("[LOG] Sent tweet:", m.text)
   else:
      last_msg = m.text


# Prints available json to the console.
@bot.message_handler(commands=['test'])
def print_json (m):
   print('info:', m.__dict__)
   print('from:', m.from_user.__dict__)
   print('chat:', m.chat.__dict__)


# Listens for commands.
bot.polling(none_stop=True)
print('[LOG] Kuma! Shutsugeki suru, kuma!')
while True:
   time.sleep(100)