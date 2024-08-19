import pygame
import math
from grid3d import Grid3D
from oscilloscope import Oscilloscope

# --------------------- Components ---------------------

class Component:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pass

class Grid3DComponent(Component):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.grid = Grid3D(width, height)

    def draw(self, surface, vector, offset=(0, 0)):
        self.grid.draw_3d_visualization(surface, vector, (self.rect.x + offset[0], self.rect.y + offset[1]))

class OscilloscopeComponent(Component):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.oscilloscope = Oscilloscope(width, height)

    def update(self, magnitude):
        self.oscilloscope.update(magnitude)

    def draw(self, surface, green_threshold, yellow_threshold):
        self.oscilloscope.draw(surface, green_threshold, yellow_threshold, (self.rect.x, self.rect.y))

class SensorViewComponent(Component):
    def __init__(self, x, y, width, height, logic_handler):
        super().__init__(x, y, width, height)
        self.logic_handler = logic_handler

    def draw(self, surface):
        column_width = self.rect.width // 3
        row_height = 60

        # Draw column headers
        pygame.draw.line(surface, (255, 255, 255), (self.rect.x + column_width, self.rect.y), (self.rect.x + column_width, self.rect.y + self.rect.height))
        pygame.draw.line(surface, (255, 255, 255), (self.rect.x + column_width * 2, self.rect.y), (self.rect.x + column_width * 2, self.rect.y + self.rect.height))

        font = pygame.font.Font(None, 36)
        neutral_title = font.render("Available Ports", True, (255, 255, 255))
        ext_title = font.render("External", True, (255, 255, 255))
        int_title = font.render("Internal", True, (255, 255, 255))
        surface.blit(neutral_title, (self.rect.x + 50, self.rect.y + 20))
        surface.blit(ext_title, (self.rect.x + column_width + 50, self.rect.y + 20))
        surface.blit(int_title, (self.rect.x + column_width * 2 + 50, self.rect.y + 20))

        # Draw sensor buttons
        for sensor in self.logic_handler.sensor_manager.sensors:
            self.draw_sensor_button(surface, sensor, column_width, row_height)

    def draw_sensor_button(self, surface, sensor, column_width, row_height):
        if sensor.column == "neutral":
            x = self.rect.x + 50
        elif sensor.column == "external":
            x = self.rect.x + column_width + 50
        elif sensor.column == "internal":
            x = self.rect.x + column_width * 2 + 50
        
        y = self.rect.y + 70 + (sensor.port - 1) * row_height
        
        button_rect = pygame.Rect(x, y, 100, 40)
        
        if sensor.connected:
            color = (0, 255, 0) if sensor.active else (0, 0, 255)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(surface, color, button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render(f"COM{sensor.port}", True, (255, 255, 255))
        surface.blit(text, (button_rect.x + 10, button_rect.y + 10))

class MenuComponent(Component):
    def __init__(self, x, y, width, height, buttons):
        super().__init__(x, y, width, height)
        self.buttons = buttons

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        
        for i, (text, _) in enumerate(self.buttons):
            button_rect = pygame.Rect(self.rect.x + 10 + i * 210, self.rect.y + 5, 200, 40)
            pygame.draw.rect(surface, (100, 100, 100), button_rect)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))

    def handle_click(self, pos):
        for i, (_, action) in enumerate(self.buttons):
            if self.rect.x + 10 + i * 210 <= pos[0] <= self.rect.x + 210 + i * 210 and self.rect.y <= pos[1] <= self.rect.y + self.rect.height:
                action()
                return True
        return False
