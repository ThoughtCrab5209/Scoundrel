class Player:

    def __init__(self):
        self.actions = 4

        self.health = 20
        self.previously_healed = False

        self.weapon = 0
        self.last_fought_enemy = 15

        self.previous_floor_skipped = False
        self.current_floor_skipped = False
        


    def heal(self, value: int):
        if not self.previously_healed:
            self.health += value

            if self.health > 20:
                self.health = 20
            
            self.previously_healed = True
        
        else:
            # do nothing
            return
    

    def fight(self, value):
        if value == "J":
            value = 11
        elif value == "Q":
            value = 12
        elif value == "K":
            value = 13
        elif value == "A":
            value = 14
        else:
            value = int(value)

        # check if player can fight with their weapon
        if self.weapon != 0 and value < self.last_fought_enemy:
            self.last_fought_enemy = value
            value -= self.weapon

            if value < 0:
                value = 0

            self.health -= value

            if self.health < 0:
                self.health = 0

        # fight barehanded
        else:
            self.health -= value
        
            if self.health < 0:
                self.health = 0


    def change_weapon(self, value: int):
        if value == 0:
            value = 10

        self.weapon = value
        self.last_fought_enemy = 15


    def skip_floor(self):
        self.current_floor_skipped = True

