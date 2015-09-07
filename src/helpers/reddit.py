import datetime, json, os, praw, random, telebot, urllib.request
from helpers import logger
from .. import auth

bot = telebot.TeleBot(auth.Telegram.api_key)
CON = logger.CON
dt = datetime.datetime
r = praw.Reddit(user_agent='Telegram:KumaKaiNi-Py:v1.0.0 (by @rekyuu_senkan)')

# Function to populate top posts of a given subreddit
def get_top_posts (name):

   if not os.path.exists('./subreddits'):
      os.makedirs('./subreddits')
   conf = open('./subreddits/' + name + '.json', 'w', encoding='utf8')

   data = {}
   data['time'] = str(dt.now())
   data['posts'] = []

   sub = r.get_subreddit(name)

   print(CON['log'], "Populating list...")
   pid = 0
   for post in sub.get_hot(limit=25):
      url = post.url
      title = post.title
      data['posts'].append({'pid': pid, 'title': title, 'url': url})
      pid += 1
   json.dump(data, conf, ensure_ascii=False)
   print(CON['log'], "List populated!")

   conf.close()


# Function that sends the image
IMAGE_TYPES = ['jpg', 'jpeg', 'gif', 'png']
def send_sub_image (msg, name):
   while True:
      try:
         conf = open('./subreddits/' + name + '.json', encoding='utf8')
         data = json.loads(conf.read())
         conf.close()
         break
      except:
         print(CON['err'], "List has not been created. Creating.")
         get_top_posts(name)

   # Checks freshness of posts.
   if dt.now() - dt.strptime(data['time'], '%Y-%m-%d %H:%M:%S.%f') >= datetime.timedelta(days=1):
      print(CON['log'], "24 hours have past since last update!")
      get_top_posts(name)

   # Chooses a random listing and downloads the image.
   while True:
      try:
         rand = random.randint(0, len(data['posts']) - 1)
         dl = data['posts'][rand]['url']
         filename = dl.split('/')[-1]
         print(CON['log'], "Downloading", filename + "...")

         if filename.split('.')[-1] not in IMAGE_TYPES:
            # If the file is not an image, it will try again.
            print(CON['err'], "Not an image. Deleting entry and trying again.")
            del data['posts'][rand]
            if len(data['posts']) == 0:
               get_top_posts(name)
         else:
            # Downloads the image.
            if not os.path.exists('./tmp'):
               os.makedirs('./tmp')
            urllib.request.urlretrieve(dl, './tmp/' + filename)

            # Sends the downloaded image and the title.
            photo = open('./tmp/' + filename, 'rb')
            out = str(data['posts'][rand]['title'])
            bot.send_photo(msg.chat.id, photo)
            print(CON['img'], filename)

            bot.send_message(msg.chat.id, out)
            print(CON['msg'], out)

            # Closes the photo and removes it from the system.
            photo.close()
            os.remove(filename)
            del data['posts'][rand]

            conf = open('./subreddits/' + name + '.json', 'w', encoding='utf8')
            json.dump(data, conf, ensure_ascii=False)
            conf.close()
            break
      except:
         print(CON['err'], "Error downloading image. Trying again.")
         raise
         del data['posts'][rand]
         if len(data['posts']) == 0:
            get_top_posts(name)