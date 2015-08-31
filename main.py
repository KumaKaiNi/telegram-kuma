import auth, datetime, os, praw, random, telebot, time, urllib.request
from twitter import *
   
dt = datetime.datetime

# Kuma-chan's unique ID.
bot = telebot.TeleBot(auth.Telegram.api_key)

# Kuma-chan's twitter, @KumaKaiNi.
t = Twitter(auth = OAuth(auth.TwitterAuth.access_key, auth.TwitterAuth.access_key_secret, auth.TwitterAuth.consumer_key, auth.TwitterAuth.consumer_key_secret))

# Reddit stuff.
r = praw.Reddit(user_agent='Telegram:KumaKaiNi:v1.0.0 (by @rekyuu_senkan)')


# Populates ships from r/warshipporn 
ships = []
ships_got = dt.now()
def get_boats():
   global ships
   global ships_got
   warships = r.get_subreddit('warshipporn')
   
   print("[LOG] Populating ships...")
   pid = 0
   for post in warships.get_hot(limit=25):
      url = post.url.encode("utf-8")
      title = post.title.encode("utf-8")
      ships.append({'pid': pid, 'title': title, 'url': url})
      pid += 1
   print("[LOG] Ships populated!")

# Initializes boats!
get_boats()
   

# Other functions
def to_regex(words, beg='', end=''):
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
      + "/mgsv - posts the remaining time until release.\n"
      + "/ship - posts an image from the top posts of r/warshipporn.\n"
      + "\n"
      + "Just as a warning, there is a 1% chance that I will tweet whatever bullshit you just said, kuma. https://twitter.com/KumaKaiNi\n"
      + "\n"
      + "Source: https://github.com/rekyuu/telegram-kuma")


# For Andrew.
@bot.message_handler(commands=['mgsv'])
def send_mgsv (m):   
   mgsv = dt(2015,8,31,22,0,0) - dt.now()
   when = str(mgsv).split('.')[0]
   
   if mgsv <= dt.now() - dt.now():
      out = "Metal Gear Solid V has been released!"
   else:
      out = "Metal Gear Solid V will be released in " + when + "."
   
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)
   

# Repeats what the user just said.
@bot.message_handler(commands=['say'])
def send_say (m):
   try:
      out = m.text.split(' ', 1)[1]
   except:
      out = 'There is nothing to say, kuma.'
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
      else:
         out = "Your sum of numbers is: " + str(add)
   except:
      if m.from_user.username == "Liseda":
         out = "fuck off"
      else:
         out = "Invalid input, sorry!"
   
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


# Sends the user a boat!
@bot.message_handler(commands=['boat', 'ship', 'warship'])
def send_boat (m):
   global ships
   global ships_got
   
   if len(ships) == 0:
      print("[LOG] Out of ships!")
      get_boats()
   elif dt.now() - ships_got >= datetime.timedelta(hours=6):
      print("[LOG] Six hours have past since last update!")
      get_boats()
   
   while True:
      try:
         # Chooses a random listing and downloads the image.
         rand = random.randint(0, len(ships) - 1)
         dl = str(ships[rand]['url']).split("'")[1]
         filename = dl.split('/')[-1]   
         urllib.request.urlretrieve(dl, filename)
         break
      except:
         # Removes the failed entry, and tries again.
         print("[LOG] Error downloading image. Trying again!")
         del ships[rand]
         if len(ships) == 0:
            get_boats()
   try:
      # Sends the downloaded image and the title.
      photo = open(filename, 'rb')
      bot.send_photo(m.chat.id, photo)
      print('[IMG]', filename)
      
      bot.send_message(m.chat.id, str(ships[rand]['title']).split("'")[1])
      print('[MSG]', str(ships[rand]['title']).split("'")[1])
      
      # Closes the photo and removes it from the system.
      photo.close()
      os.remove(filename)
      del ships[rand]
   except:
      # Closes the download, removes it, and tries again.
      print("[LOG] Error sending image.")
      bot.send_message(m.chat.id, "I'm hit, kuma! (Attempted to send a non-image. Listing removed. Try again!)")
      photo.close()
      os.remove(filename)
      del ships[rand]
      if len(ships) == 0:
         get_boats()


# Returns a greeting if a user starts a sentence with the following regex.   
GREETINGS = ['sup loser', 'yo', 'ay', 'go away', 'hi', 'wassup']
SEARCH_FOR = ['hi', 'hello', 'hey', 'sup']
@bot.message_handler(regexp=to_regex(SEARCH_FOR,'','()|( ).*'))
def send_hello (m):
   out = GREETINGS[random.randint(0, len(GREETINGS) - 1)]
   bot.send_message(m.chat.id, out)
   print('[MSG]', out)


# 1% chance to tweet an incoming message.
@bot.message_handler(regexp=".")
def send_tweet (m):
   prob = random.randint(1,100)
   
   if prob <= 1:   
      t.statuses.update(status='"' + m.text + '"')
      bot.send_message(m.chat.id, "lmao I'm live tweeting this shit")
      print("[LOG] Sent tweet:", m.text)


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