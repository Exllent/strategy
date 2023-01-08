from collections import namedtuple

from warrior.models import Warrior


class Warriors:
    _Warrior = namedtuple("Warrior", "name health damage armor speed race")
    orc = _Warrior(name="orc", health=100, damage=100, armor=60, speed=70, race=1)
    orc2 = _Warrior(name="orc2", health=50, damage=50, armor=30, speed=35, race=1)
    elf = _Warrior(name="elf", health=100, damage=100, armor=60, speed=70, race=2)
    elf2 = _Warrior(name="elf2", health=50, damage=50, armor=30, speed=35, race=2)
    gnome = _Warrior(name="gnome", health=100, damage=100, armor=60, speed=70, race=3)
    gnome2 = _Warrior(name="gnome2", health=50, damage=50, armor=30, speed=35, race=3)
    person = _Warrior(name="person", health=100, damage=100, armor=60, speed=70, race=4)
    person2 = _Warrior(name="person2", health=50, damage=50, armor=30, speed=35, race=4)

    def __init__(self):
        if self._check_uquels():
            self._create_warriors()

    def __iter__(self):
        return (v for k, v in self.__class__.__dict__.items() if not k.startswith("_"))

    def _count_warriors(self):
        count = 0
        for _ in self.__iter__():
            count += 1
        return count

    def _check_uquels(self):
        return True if Warrior.get_count() != self._count_warriors() else False

    def _create_warriors(self):
        for warrior in self:
            Warrior.create(
                name=warrior.name,
                health=warrior.health,
                damage=warrior.damage,
                armor=warrior.armor,
                speed=warrior.speed,
                race=warrior.race,
            )
