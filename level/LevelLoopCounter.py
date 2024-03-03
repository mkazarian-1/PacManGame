class LevelLoopCounter:
    __level_loop_counter = 0

    def get(self):
        return self.__level_loop_counter

    def increase(self):
        if self.__level_loop_counter > 19:
            self.__level_loop_counter = 0
        else:
            self.__level_loop_counter += 1