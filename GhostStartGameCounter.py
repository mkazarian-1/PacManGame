class GhostStartGameCounter:
    time_counter = 0

    def get(self):
        return self.time_counter

    def increase(self):
        if self.time_counter > 250:
            self.time_counter = 250
        else:
            self.time_counter += 1