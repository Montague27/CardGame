from tkinter import *
import copy
import random

Game = 'CardGame'
Version = '0.01'
Author = 'ChuShu'

length , width = 7, 3

'''


考量點
    坦克&膠登人物可共用機制
	如坦克 = 肉盾
      	    SPG(自走炮) = 遠程攻擊
     	    TD(驅逐坦克) = 狙擊手
    紅方為玩家 藍方為電腦 先完成紅方
    連線對戰 需Python技術支援 <<< To do
進度表:
###
基礎卡牌 未完成
    各種卡牌機制 未完成
        主師 未完成
            加資源
        坦克 未完成
            主力
        TD 未完成
            直行攻擊 高攻      
        SPG 未完成
            大射程 低攻
        支援 未完成
            火箭炮
        狗 亂入
        戰術卡 未完成
        
    卡牌圖片 未完成 < 圖片size最大為50x50
    牌組 未完成
    
機制
    發配卡牌 完成
    移動功能 完成
    計cost 完成
    攻擊功能 完成
    AI出牌 未完成
    

    顯示手牌資料 完成
    顯示地圖上卡牌資料 完成
        
To do:
睇下啲code有乜位可以寫得簡潔啲
###

同一牌MAX3
地形X回合改變

牌組
    以敵資源補給自己
    廣域資源/強補給
    戰術卡 加強能力/資源
    情報卡
'''

"""
Comments @ 21:15 HKT 19 Nov
1.For the round actions, you can make them into more specific functions. For example:
instead of if (card.pos == (x,y)), you can try
def findCardAtPos(x,y,playerCards): (or a tuple)
	card = None
	cardList = [c for c in playerCards if c.pos == (x,y)]
	if cardList:
		card = cardList[0]
	return card

2. You can try using dicts for decks. It is simple to use like lists:
{ "sunny dog" : 10 , "ice" : 5, "big cum" : 1 }

3. You can also try to make players into objects, each player have the following attributes/methods:
deck: their current deck
handcard (better call it "hand"): their current hand
playerType: AI or player, which makes it more flexible

4. See below; concerning [x for x in (enumerator)]
"""

class MainGame(Frame):
    def __init__(self, parent): 
        Frame.__init__(self, parent)  
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title('Python')
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self)

        self.ObjectID = 0
        
        for y in range(width):
            for x in range(length):
                xy = x, y
                self.canvas.create_rectangle(self.xy(xy), outline = '#000000', fill = '#CDCDCD', tags = 'grids')

        self.canvas.pack(fill = BOTH, expand = YES)
        self.canvas.tag_bind('grids', '<ButtonPress-1>', self.Object_click)
        self.canvas.tag_bind('grids', '<ButtonPress-3>', self.Object_rightclick)
        self.cost = Label(self, text = 0)
        self.cost.place(x = 250, y = 250)
        
        w, h = 85, 145
        self.button1 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(0))
        self.button2 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(1))
        self.button3 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(2))
        self.button4 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(3))
        self.button5 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(4))
        self.button6 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(5))
        self.button7 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(6))
        self.turn_end = Button(self, width = 12, height = 5, text = '結束回合', command = None)
        self.turn_end.place(x = 350, y = 250)

        x1 = -60
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7]
        for button in self.buttons:
            x1 += 93
            button.place(x = x1, y = 375)
            
    def set_card(self, i):
        name = player.hand[i].name
        pos = main.ObjectID 
        xy = self.Object_pos(pos)
        
        player.set_card(player.hand[i], xy, cost=True)
        main.update()
        
    def update(self):
        self.canvas.delete('pics')
        self.cost['text'] = '資源%s' % players[0].cost
        for i in range(width * length):
            self.canvas.itemconfig(i + 1, fill = '#CDCDCD')
        self.canvas.itemconfig(self.ObjectID + 1, fill = '#DCDCDC')

        for card in player.card:
            xy = self.Object_xy(card.pos) + 1
            self.canvas.itemconfig(xy, fill = '#FF7C80')
                
            x, y, z1, z2 = self.xy(card.pos)
            self.canvas.create_image(x + 25, y + 25, image = pics[card.pic], anchor = 'center', tag = 'pics')
            self.canvas.tag_bind('pics', '<ButtonPress-1>', self.Object_click)

        for card in AI.card:
            xy = self.Object_xy(card.pos) + 1
            self.canvas.itemconfig(xy, fill = '#4876FF')
            x, y, z1, z2 = self.xy(card.pos)
            self.canvas.create_image(x + 25, y + 25, image = pics[card.pic], anchor = 'center', tag = 'pics')
            self.canvas.tag_bind('pics', '<ButtonPress-3>', self.Object_rightclick)
            
        for button in self.buttons:
            button['text'] = '---'
            button['state'] = 'disable'
            
        for card, button in zip(player.hand, self.buttons):
            if card:
                card_info = self.cards_show(card)
                button['text'] = card_info
                if player.cost >= card.cost:
                    button['state'] = 'normal'

        for card in player.card:
            xy = self.ObjectID - self.ObjectID // 7 * 7, self.ObjectID // 7
            if card.pos == xy or xy not in [(0, 0), (1, 1), (0, 2)]:
                for button in self.buttons:
                    button['state'] = 'disable'

        if player.hand:
            for i, button in enumerate(self.buttons):
                if i < len(player.hand):
                    card = player.hand[i]
                    button.config(image = pics[card.pic], compound = 'top')               
                else:
                    button.config(image = pics[None], compound = 'top')
                
    def cards_show(self, card):
        card_type = card.card_type
        if card_type == 'leader':
            card_type = '主師'
        elif card_type == 'tank':
            card_type = '坦克'
        elif card_type == 'spg':
            card_type = 'spg'
        elif card_type == 'dog':
            card_type = '狗'
        elif card_type == 'support':
            card_type = '支援'
            
        card_info = '{%s} \n\n[%s]\nCost(%s)\nAtk(%s)\nHp(%s)' % (card_type, card.name, card.cost, card.atk, card.hp)
        return card_info
       
    def Object_click(self, event):
        self.canvas.delete('pics')
        object_closest = event.widget.find_closest(event.x, event.y)
        self.ObjectID = object_closest[0] - 1
        for card in player.card:
            x, y, z1, z2 = self.xy(card.pos) #only use x and y
            self.canvas.create_image(x + 25, y + 25, image = pics[card.pic], anchor = 'center', tag = 'pics')
        self.update()

    def Object_rightclick(self, event):
        self.canvas.delete('pics')
        object_closest = event.widget.find_closest(event.x, event.y)
        self.RightClickID = object_closest[0] - 1

        x, y = self.Object_pos(self.RightClickID)
        x1, y1 = self.Object_pos(self.ObjectID)

        for card in player.card:
            if card.pos == (x1, y1):
                if card.moves > 0:
                    if (x, y) in pos((x1, y1)):
                        card.pos = x, y
                        card.moves -= 1
                        self.ObjectID = self.RightClickID
                    else:
                        for enemyCard in AI.card:
                            if enemyCard.pos == (x, y):
                                player.attack(card, enemyCard, AI.card)
        self.update()

    def Object_pos(self, pos):
        y = pos // 7
        x = pos - y * 7
        return x, y
    
    def Object_xy(self, xy):
        x, y = xy
        pos = x + y * 7
        return pos
        
    def xy(self, xy):
        x, y = xy
        x1 = x * 50 + 20
        y1 = y * 50 + 20
        x2 = x1 + 50
        y2 = y1 + 50
        return [x1, y1, x2, y2]
        
class card(object):
    def __init__(self, name, card_type, pic, cost, atk, hp, moves, atks, *leader):
        self.name = name
        self.card_type = card_type
        self.pic = pic
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.moves = moves
        self.atks = atks

deck1 = ['冰','晴天狗', '晴天狗', '晴天狗','驅逐坦克ZEN',
         '重坦碧琴型', '重坦碧琴型', '自走炮碧琴型', '自走炮碧琴型',
         '重坦松溪型', '重坦松溪型', '虎式', '中坦甲型', '中坦甲型']

deck2 = ['ZEN', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '補給兵', '補給兵', '補給兵', '補給兵', '補給兵',
         '補給兵', '補給兵', '補給兵', '自走炮碧琴型', '自走炮碧琴型',]


cards_type = ['leader', 'tank', 'TD', 'spg', 'dog']
cards = [#card('卡名', '卡類', 費用, 攻擊,血量, 移動力, 攻擊次)
         card('冰', 'leader', 'ice.gif', 1, 1, 1, None, None),
         card('大麻', 'leader', None, 1, 1, 1, None, None),
         card('ZEN', 'leader', 'ZEN.gif', 1, 1, 1, None, None),

         card('補給兵', 'support', None, 2, 1, 3, None, None),
         card('油田', 'support', None, 3, 2, 3, None, None),
         card('雷達', 'support', None, 3, 2, 3, None, None),

         card('晴天狗', 'dog', 'SunnyDog.gif', 1, 1, 2, 1, 1),
         card('流氓犬', 'dog', 'SunnyDog.gif', 2, 2, 4, 1, 1),

         card('自走炮松溪型', 'spg', 'SPG1.png', 4, 5, 2, 1, 1),
         card('自走炮碧琴型', 'spg', 'SPG1.png', 3, 3, 1, 1, 1),
         
         card('驅逐坦克ZEN', 'TD', 'ZEN.gif', 6, 6, 2, 1, 1),
         
         card('重坦松溪型', 'tank', 'Tank1.png', 5, 4, 4, 1, 1),
         card('重坦碧琴型', 'tank', 'BigCum.gif', 5, 4, 3, 1, 1),
         card('虎式', 'tank', 'Tiger.png', 5, 4, 3, 1, 1),

         card('中坦甲型', 'tank', 'Tank1.png', 3, 2, 3, 1, 1),
         card('中坦乙型', 'tank', 'Tank1.png', 3, 2, 3, 1, 1),]


class combat(object):
    def __init__(self):
        self.pics = self.set_pics()
    


    
class Player(object):
    def __init__(self, player_type, deck):
        deck = card_in_class(deck)
        deck = random_deck(deck)
        self.deck = list(deck)
        
        self.player_type = player_type
        self.ap = 0
        self.card = []
        self.hand = []
        self.cost = 0
        
    def attack(self, atk_card, def_card, def_deck):
        damage = atk_card.atk
        def_card.hp -= damage
        if def_card.hp <= 0:
            def_deck.remove(def_card)
        main.update()
        
    def dealt(self):
        while len(self.hand) < 7 and len(self.deck) > 0:
            card = self.deck[-1]
            self.hand.append(card)
            self.deck.remove(card)
        
    def set_card(self, card, pos, cost=False, leader=False):
        if leader:
            self.deck.remove(card)
            card.pos = pos
            self.card.append(card)           
        else:
            self.hand.remove(card)
            card.pos = pos
            self.card.append(card)
            if cost:
                self.cost -= card.cost
        main.update()
        
    def turn_end(self):
        for card in self.card:
            card.moves = 1
            card.atks = 1
        self.cost += 5
        self.dealt()
        main.update()
        
def pos(pos):
    x, y = pos
    e, s, w, n = (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)
    dirt = [e, s, w, n]
    dirt_new = dirt
    for j in range(2):
        for i in dirt:
            x, y = i
            nearby = i
            if x < 0 or y < 0 or y > 2:
                dirt_new.remove(nearby)
            else:
                for p in players:
                    for card in p.card:
                        if card.pos == nearby:
                            dirt_new.remove(nearby)
    return dirt_new
    
        
def card_find(name):
    for card in cards:
        if card.name == name:
            return card
            
def card_find_AtPos(x, y, playerCards):
    card = None
    cardList
    
def card_in_class(deck):
    cards = []
    for name in deck:
        found_card = card_find(name)
        card = copy.copy(found_card)
        cards.append(card)
    return cards

def card_info(name, pos):
    card = card_find(name)
    card_data = copy.copy(card)
    print(card_data,name)
    card_data.pos = pos
    return card_data
            
def random_deck(deck):
    old_deck = list(deck)
    new_deck = []
        
    leader = old_deck[0]
    old_deck.remove(leader)
        
    while len(old_deck) > 0:
        r = random.choice(old_deck)
        old_deck.remove(r)
        new_deck.append(r)
    new_deck.insert(0, leader)
    return new_deck

def set_pics():
    pic_none = PhotoImage(file = 'None.png')
    pics = {None: pic_none}
    for card in cards:
        if card.pic:
            pic = PhotoImage(file = card.pic)
            pics[card.pic] = pic
    return pics

def start():
    x = 0
    for player in players:
        player.dealt()
        player.cost = 5

        player.set_card(player.deck[0], (x, 1), leader=True)
        x += 6
        
root = Tk()
root.geometry('850x650+0+0')
main = MainGame(root)

player = Player('player', deck1)
AI = Player('AI', deck2)
players = [player, AI]
pics = set_pics()
main.turn_end['command'] = player.turn_end
start()
