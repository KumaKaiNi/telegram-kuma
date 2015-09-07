import os
from colorama import init, Fore
from helpers import folders

init()
CACHE = folders.CACHE

# Logging definitions.
CON = {
   'log': ''.join(['[', Fore.YELLOW, 'LOG', Fore.RESET, ']']),
   'err': ''.join(['[', Fore.RED,    'ERR', Fore.RESET, ']']),
   'img': ''.join(['[', Fore.GREEN,  'IMG', Fore.RESET, ']']),
   'msg': ''.join(['[', Fore.GREEN,  'MSG', Fore.RESET, ']']),
   'twt': ''.join(['[', Fore.CYAN,   'TWT', Fore.RESET, ']']),
}

# Logs all words to a file for later use with Markov.
def word_log (m):
   if not os.path.exists(CACHE['wordlogs']):
      os.makedirs(CACHE['wordlogs'])
   try:
      log = open(CACHE['wordlogs'] + str(m.chat.id) + '.log', 'a+', encoding='utf8')
   except:
      print(CON['err'], 'Log file does not exist. Creating.')
      log = open(CACHE['wordlogs'] + str(m.chat.id) + '.log', 'w', encoding='utf8')
   finally:
      # Ignores messages that start with links or are just links
      if m.text.split(':')[0] not in ['http', 'https']:
         log.write(m.text + '\n')
      log.close()