class Player:

    def __init__(self):
        self.actions = 4

        self.health = 20
        self.previously_healed = False

        self.weapon = 0
        self.last_fought_enemy = 15

        self.previous_floor_skipped = False
        self.current_floor_skipped = False
        

    def reset_status(self, count: int):
        if count < 4:
            self.actions = count
        else:
            self.actions = 4

        self.previously_healed = False
        self.previous_floor_skipped = self.current_floor_skipped
        self.current_floor_skipped = False


    def heal(self, value: int):
        if not self.previously_healed:
            self.health += value

            if self.health > 20:
                self.health = 20
            
            self.previously_healed = True
    

    def fight_with_hands(self, value: int):
        self.health -= value
    
        if self.health < 0:
            self.health = 0


    def fight_with_weapon(self, value: int):
        self.last_fought_enemy = value
        value -= self.weapon

        if value < 0:
            value = 0

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

