from image import crop_bag_items
from emulator import Emulator

class Bag():

    def __init__(self) -> None:
        self.em = Emulator()
        self.cont = self.em.cont
        # self.items = items
        # self.quant = quant

    def open_bag(self):
        self.cont.press_start()
        self.cont.move_down(2, 0.5)
        self.cont.press_a()
        
    
if __name__ == "__main__":
    bag = Bag()
    bag.open_bag()