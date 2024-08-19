import pygame

class Oscilloscope:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = []
        self.max_data_points = width

    def update(self, magnitude):
        self.data.append(magnitude)
        if len(self.data) > self.max_data_points:
            self.data.pop(0)

    def draw(self, surface, green_threshold, yellow_threshold, offset):
        if not self.data:
            return

        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        RED = (255, 0, 0)

        max_magnitude = max(self.data)
        scale_factor = 3 / max_magnitude if max_magnitude > 3 else 1

        for i in range(len(self.data) - 1):
            x1 = offset[0] + self.width - len(self.data) + i
            x2 = x1 + 1
            y1 = offset[1] + int(self.height - (self.data[i] * scale_factor / 3) * self.height)
            y2 = offset[1] + int(self.height - (self.data[i+1] * scale_factor / 3) * self.height)

            if self.data[i] < green_threshold:
                color = GREEN
            elif self.data[i] < yellow_threshold:
                color = YELLOW
            else:
                color = RED

            pygame.draw.line(surface, color, (x1, y1), (x2, y2), 2)