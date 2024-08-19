import pygame
import math

class Grid3D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.origin = (width // 2, height // 2)
        self.scale = 50  # pixels per unit
        self.axis_font = pygame.font.Font(None, 24)

    def project_3d_to_2d(self, x, y, z, offset):
        if y < 0:
            x = -x

        projected_x = self.origin[0] + self.scale * (-x - (-z)) / math.sqrt(2)
        projected_y = self.origin[1] + self.scale * (-y + (-x + (-z)) / math.sqrt(6))
        return (projected_x + offset[0], projected_y + offset[1])

    def draw_3d_visualization(self, surface, vector, offset):
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        DARK_BLUE = (0, 0, 255)

        # Draw the 3D axis lines
        axis_length = 2
        pygame.draw.line(surface, WHITE, self.project_3d_to_2d(-axis_length, 0, 0, offset), self.project_3d_to_2d(axis_length, 0, 0, offset), 2)
        pygame.draw.line(surface, WHITE, self.project_3d_to_2d(0, -axis_length, 0, offset), self.project_3d_to_2d(0, axis_length, 0, offset), 2)
        pygame.draw.line(surface, WHITE, self.project_3d_to_2d(0, 0, -axis_length, offset), self.project_3d_to_2d(0, 0, axis_length, offset), 2)

        # Label axes
        x_label = self.axis_font.render("X", True, WHITE)
        y_label = self.axis_font.render("Y", True, WHITE)
        z_label = self.axis_font.render("Z", True, WHITE)
        
        surface.blit(x_label, self.project_3d_to_2d(axis_length, 0, 0, offset))
        surface.blit(y_label, self.project_3d_to_2d(0, axis_length, 0, offset))
        surface.blit(z_label, self.project_3d_to_2d(0, 0, -axis_length, offset))
        
        # Draw 3D vector (red line)
        start = self.project_3d_to_2d(0, 0, 0, offset)
        end = self.project_3d_to_2d(vector[0], vector[1], vector[2], offset)
        pygame.draw.line(surface, RED, start, end, 3)

        X_value = vector[0]
        Y_value = vector[1]
        Z_value = vector[2]

        if Y_value < 0:
            multiplier = -1
        else:
            multiplier = 1

        box_points = [
            (0, 0, 0),
            (X_value * multiplier, 0, 0),
            (X_value, Y_value, 0),
            (0, Y_value, 0),
            (0, 0, Z_value),
            (X_value * multiplier, 0, Z_value),
            (X_value, Y_value, Z_value),
            (0, Y_value, Z_value)
        ]
        
        for i in range(4):
            pygame.draw.line(surface, DARK_BLUE, self.project_3d_to_2d(*box_points[i], offset), self.project_3d_to_2d(*box_points[(i+1)%4], offset), 2)
            pygame.draw.line(surface, DARK_BLUE, self.project_3d_to_2d(*box_points[i+4], offset), self.project_3d_to_2d(*box_points[(i+1)%4+4], offset), 2)
            pygame.draw.line(surface, DARK_BLUE, self.project_3d_to_2d(*box_points[i], offset), self.project_3d_to_2d(*box_points[i+4], offset), 2)
