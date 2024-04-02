
class ModeCounter:
    mode_counter = 0

    def get(self):
        return self.mode_counter

    def increase(self):
        if self.mode_counter > 5040:
            self.mode_counter = 5040
        else:
            self.mode_counter += 1

    def reset(self):
        self.mode_counter = 0
