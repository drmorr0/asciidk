from asciidk.obj.obj import DungeonObject

class Corpse(DungeonObject):
    def __init__(self, pos, name):
        DungeonObject.__init__(self, pos, "Corpse of {name}".format(name=name), 'X')
        self.solid = False

    def attack(self, opponent):
        pass

    def defend(self, damage_properties):
        pass
