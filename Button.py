class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:  # Якщо зображення не задано, використовується текст
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Прямокутник області зображення
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Прямокутник області тексту

    # Оновлення відображення кнопки на екрані
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Перевірка натискання на кнопку
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # Зміна кольору тексту кнопки при наведенні миші на неї
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)