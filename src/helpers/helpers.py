import random

# Regex function
def to_regex (words, beg='', end=''):
   regex = ''.join(['^(', beg, ')('])
   for word in words:
      regex += '('
      letters = list(word)
      for letter in letters:
         regex = ''.join([regex, '(', letter.upper(), '|', letter.lower(), ')'])
      regex += ')|'
   regex = regex[:-1]
   regex = ''.join([regex, ')(', end, ')$'])
   return regex


# Probability function, ie, 1:100, etc.
def prob (x, y):
   rand = random.randint(1, y)
   if rand <= x:
      return True
   else:
      return False