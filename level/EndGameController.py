class EndGameController:
    dots = 0

    def increase_amount_dots(self, amount: int):
        self.dots += amount

    def decrease_amount_dots(self, amount: int):
        self.dots -= amount
        if self.dots <= 0:
            print("You WIN !!!!")
