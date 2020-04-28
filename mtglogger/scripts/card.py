import sqlite3

def by_name(card_name):
  conn = sqlite3.connect('/home/lan/Documents/MagicLogger/mtglogger/cards.sqlite')
  c = conn.cursor()
  c.execute("SELECT name, setCode, multiverseId FROM cards WHERE name=?", (card_name,))
  rows = c.fetchall()
  conn.close()
  if len(rows) > 0:
    cards = rows
  else:
    cards = [['Card Not Found', '']]
  new_cards = []
  for i in cards:
    if i[2]:
      image_url = str('https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + str(i[2]) + '&type=card')
      i = i + (image_url, )
      new_cards.append(i)
  return new_cards

def by_multiverseId(id):
  conn = sqlite3.connect('/home/lan/Documents/MagicLogger/mtglogger/cards.sqlite')
  c = conn.cursor()
  c.execute("SELECT name, setCode, multiverseId FROM cards WHERE multiverseId=?", (id,))
  rows = c.fetchall()
  if len(rows) > 0:
    card = rows[0]
  image_url = str('https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + str(card[2]) + '&type=card')
  card = card + (image_url, )

  return card

def return_card(id):
  conn = sqlite3.connect('/home/lan/Documents/MagicLogger/mtglogger/cards.sqlite')
  c = conn.cursor()
  c.execute("SELECT name, setCode, multiverseId, rarity, originalType, power, toughness, text, flavorText, type FROM cards WHERE multiverseId=?", (id,))
  rows = c.fetchall()
  if len(rows) > 0:
    notDictCard = rows[0]

    card = {}
    card["name"] = notDictCard[0]
    card["set"] = notDictCard[1]
    card["id"] = notDictCard[2]
    card["rarity"] = notDictCard[3]
    card["originalType"] = notDictCard[4]
    card["type"] = notDictCard[9]
    card["power"] = notDictCard[5]
    card["toughness"] = notDictCard[6]
    card["text"] = notDictCard[7]
    card["flavor"] = notDictCard[8]
    card["image_url"] = str('https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + str(card["id"]) + '&type=card')
  else:
    card = None
  return card

