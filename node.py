class node():
    # OK, lesson learned. Don't use nbs=[].
    # The instances will all *share* this array. This is crazy.
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.neighbors = []
