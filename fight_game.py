import random


class Character:
    """
    Базовая модель персонажа
    """
    default_health_point = 100
    default_low_damage_range = (18, 26)
    default_high_damage_range = (10, 36)
    default_increased_healing_chance_limit = 0

    def __init__(self, name, **kwargs):
        self.name = name
        self.health_points = self.max_health_points = kwargs.get('health_points', self.default_health_point)
        self.low_damage_range = kwargs.get('low_damage_range', self.default_low_damage_range)
        self.high_damage_range = kwargs.get('hight_damage_range', self.default_high_damage_range)
        self.increased_healing_chance_limit = kwargs.get(
            'increased_healing_chance_limit', self.default_increased_healing_chance_limit
        )

    def damage(self, character, **kwargs):
        """
        нанесение слабого урона
        """
        damage = min(random.randrange(*self.low_damage_range), character.health_points)
        character.health_points -= damage
        print(f'{self.name} наносит {damage}.ед урона {character.name}у')

    def critical_damage(self, character, **kwargs):
        """
        нанесение сильного урона
        """
        critical_damage = min(random.randrange(*self.high_damage_range), character.health_points)
        character.health_points -= critical_damage
        print(f'{self.name} наносит {critical_damage}.ед критического урона {character.name}у')

    def heal(self, **kwargs):
        """
        Отхил чаров
        """
        heal_power = min(random.randrange(*self.low_damage_range), self.max_health_points - self.health_points)
        self.health_points += heal_power
        print(f'{self.name} востанавливает {heal_power}.ед здоровья')

    def act(self, character):
        """
        выполнение действия персонажем
        """
        choice_of_action = [self.damage, self.critical_damage]

        if self.health_points != self.max_health_points:
            choice_of_action.append(self.heal)

        current_health_points_percentage = self.health_points / self.max_health_points * 100

        # увеличение шанса отхила
        if current_health_points_percentage <= self.increased_healing_chance_limit:
            choice_of_action.append(self.heal)

        action = random.choice(choice_of_action)

        return action(character=character)

    def is_dead(self):
        return self.health_points <= 0


def fight(fighter_1, fighter_2):
    """
    Функция симулирующая бой
    """
    current_round = 1
    fighters = [fighter_1, fighter_2]
    fighters_amount = 2

    while True:
        print(f'\n----- Round {current_round} -----')
        random.shuffle(fighters)

        for i in range(fighters_amount):
            attacking_fighter = fighters[i]
            defending_fighter = fighters[fighters_amount - 1 - i]
            attacking_fighter.act(defending_fighter)

            if defending_fighter.is_dead():
                print(f'\n----- Result -----')
                print(f'{attacking_fighter.name} побеждает {defending_fighter.name}!')
                return

            current_round += 1


if __name__ == '__main__':
    fight(Character('Компьютер', increased_healing_chance_limit=35), Character('Игрок'))
