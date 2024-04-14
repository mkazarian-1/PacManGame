class EndGameController:
    __dots = 0
    __is_win = False

    @property
    def get_dots(self):
        return self.__dots

    @property
    def get_is_win(self):
        return self.__is_win

    def increase_amount_dots(self, amount: int):
        self.__dots += amount

    def decrease_amount_dots(self, amount: int):
        self.__dots -= amount
        if self.__dots <= 0:
            self.__is_win = True

    def is_win(self):
        return self.__is_win
