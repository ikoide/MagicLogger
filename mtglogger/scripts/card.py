import sqlite3

def get_card(card_name):
  conn = sqlite3.connect('/home/lan/Documents/MagicLogger/mtglogger/cards.sqlite')
  c = conn.cursor()
  c.execute("SELECT name, setCode FROM cards WHERE name=?", (card_name,))
  rows = c.fetchall()
  if len(rows) > 0:
    cards = rows
  conn.close()

  return cards