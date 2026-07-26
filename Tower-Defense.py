class Player:
    def __init__(self, name, x, y, speed, hp):
        self.name = name
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
p1 = Player("Shawn", 150, 200, 6, 100)
p2 = Player("Lily", 300, 400, 8, 80)

p1.take_damage(100)
p2.take_damage(90)

p1.move(7, 8)
if p1.hp <= 0:
    print(f"{p1.name} is dead!")
if p2.hp <= 0:
    print(f"{p2.name} is dead!")
print(f"{p1.name}在y:{p1.y} x:{p1.x}的地方,血量是{p1.hp}.")