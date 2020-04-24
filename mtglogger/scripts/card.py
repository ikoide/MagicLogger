from mtgsdk import Card, Set, Type, Supertype, Subtype, Changelog

def find_card(query):
  cards = Card.where(name=query).all()
  actCards = []
  totalCards = 0
  for i in cards:
    if i.name == query:
      if i.image_url:
        totalCards += 1
        actCards.append(i)

  return actCards, totalCards