import tkinter


class ScreenSettings:
    def __init__(self):
        self.current_screen_size = "Large"
        self.current_background_color = "Black"
        self.background_image = None
        self.image_inserted = False

        self.SCREEN_SIZES = {
            "Small": (tkinter.Tk().winfo_screenheight() // 2, tkinter.Tk().winfo_screenheight() * 0.95 // 2),
            "Medium": (tkinter.Tk().winfo_screenheight() // 1.5, tkinter.Tk().winfo_screenheight() * 0.95 // 1.5),
            "Large": (tkinter.Tk().winfo_screenheight() - 70, (tkinter.Tk().winfo_screenheight() - 70) * 0.95)
        }
        self.BACKGROUND_COLORS = {
            "Black": (0, 0, 0),
            "Blue": (97, 146, 178),
            "Brown": (77, 33, 34),
            "Pink": (200, 7, 111)
        }

    def set_screen_size(self, size):
        if size in self.SCREEN_SIZES:
            self.current_screen_size = size

    def set_background_color(self, color):
        if color in self.BACKGROUND_COLORS:
            self.current_background_color = color

    def set_background_image(self, image):
        self.background_image = image

    def set_image_inserted(self, value):
        self.image_inserted = value

    def get_screen_size(self):
        return self.current_screen_size

    def get_background_color(self):
        return self.BACKGROUND_COLORS[self.current_background_color]

    def get_background_image(self):
        return self.background_image

    def is_image_inserted(self):
        return self.image_inserted

    def get_ind(self):
        if self.current_screen_size == "Large":
            return 1
        elif self.current_screen_size == "Medium":
            return 0.7
        elif self.current_screen_size == "Small":
            return 0.5
