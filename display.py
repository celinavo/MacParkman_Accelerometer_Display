import pygame
import sys
from sensors_logic import LogicHandler
from components import Grid3DComponent, OscilloscopeComponent, SensorViewComponent, MenuComponent

class Game:
    def __init__(self):
        # Initialize Pygame and set up the display
        pygame.init()
        self.width, self.height = 1000, 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("XYZ Data Visualization")

        # Set up the clock and font
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Initialize logic handler
        self.logic = LogicHandler()
        
        # Create components
        self.grid_external = Grid3DComponent(0, 0, self.width // 2 - 50, self.height - 100)
        self.grid_internal = Grid3DComponent(self.width // 2, 0, self.width // 2 - 50, self.height - 100)

        self.oscilloscope_external = OscilloscopeComponent(0, 0, self.width - 200, (self.height - 150) // 2)
        self.oscilloscope_internal = OscilloscopeComponent(0, (self.height) // 2, self.width - 200, (self.height - 150) // 2)

        self.sensor_view = SensorViewComponent(0, 0, self.width, self.height - 50, self.logic)
        
        self.menu = MenuComponent(0, self.height - 50, self.width, 50, [
            ("Grid", lambda: setattr(self, 'view_mode', 'grid')),
            ("Oscilloscope", lambda: setattr(self, 'view_mode', 'oscilloscope')),
            ("Sensors", lambda: setattr(self, 'view_mode', 'sensors'))
        ])

        # Set initial view mode and thresholds
        self.view_mode = "grid"
        self.green_threshold_external = 1.0
        self.yellow_threshold_external = 2.0
        self.green_threshold_internal = 1.0
        self.yellow_threshold_internal = 2.0
        self.max_threshold_value = 10  # Max value for sliders

        self.dragging_port = None

    def run(self):
        # Connect to sensors
        self.logic.connect_to_sensors()

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_release(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button
                        self.handle_drag(event.pos)

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw the current view
            if self.view_mode == "grid":
                self.draw_grid_view()
            elif self.view_mode == "oscilloscope":
                self.draw_oscilloscope_view()
            elif self.view_mode == "sensors":
                self.draw_sensor_view()

            # Draw bottom menu
            self.menu.draw(self.screen)

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        # Clean up
        self.logic.close_sensors()
        pygame.quit()
        sys.exit()

    def draw_grid_view(self):
        # Draw the grid view with external and internal XYZ data
        external_xyz, internal_xyz = self.logic.read_xyz_data()
        
        if external_xyz:
            self.grid_external.draw(self.screen, external_xyz)
            magnitude = self.logic.calculate_magnitude(external_xyz)
            text = self.font.render(f"External - X: {external_xyz[0]:.2f}, Y: {external_xyz[1]:.2f}, Z: {external_xyz[2]:.2f}", True, (255, 255, 255))
            magnitude_text = self.font.render(f"Magnitude: {magnitude:.2f}", True, (255, 255, 255))
            self.screen.blit(text, (10, 50))
            self.screen.blit(magnitude_text, (10, 90))

        if internal_xyz:
            self.grid_internal.draw(self.screen, internal_xyz)
            magnitude = self.logic.calculate_magnitude(internal_xyz)
            text = self.font.render(f"Internal - X: {internal_xyz[0]:.2f}, Y: {internal_xyz[1]:.2f}, Z: {internal_xyz[2]:.2f}", True, (255, 255, 255))
            magnitude_text = self.font.render(f"Magnitude: {magnitude:.2f}", True, (255, 255, 255))
            self.screen.blit(text, (self.width // 2 + 10, 50))
            self.screen.blit(magnitude_text, (self.width // 2 + 10, 90))

    def draw_oscilloscope_view(self):
        # Draw the oscilloscope view with external and internal XYZ data
        external_xyz, internal_xyz = self.logic.read_xyz_data()
        
        if external_xyz:
            magnitude = self.logic.calculate_magnitude(external_xyz)
            self.oscilloscope_external.update(magnitude)
            self.oscilloscope_external.draw(self.screen, self.green_threshold_external, self.yellow_threshold_external)

        if internal_xyz:
            magnitude = self.logic.calculate_magnitude(internal_xyz)
            self.oscilloscope_internal.update(magnitude)
            self.oscilloscope_internal.draw(self.screen, self.green_threshold_internal, self.yellow_threshold_internal)

        # Draw threshold sliders
        self.draw_threshold_slider(self.green_threshold_external, self.yellow_threshold_external, 0)
        self.draw_threshold_slider(self.green_threshold_internal, self.yellow_threshold_internal, self.height // 2)

        # Labels
        external_label = self.font.render("External Sensor Oscilloscope", True, (255, 255, 255))
        internal_label = self.font.render("Internal Sensor Oscilloscope", True, (255, 255, 255))
        self.screen.blit(external_label, (10, 10))
        self.screen.blit(internal_label, (10, self.height // 2 + 10))

    def draw_sensor_view(self):
        # Draw the sensor view
        self.sensor_view.draw(self.screen)

    def draw_threshold_slider(self, green_threshold, yellow_threshold, y_offset):
        # Draw the threshold slider for the oscilloscope view
        slider_width = 40
        slider_height = self.height // 2 - 100
        x = self.width - 70
        y = 50 + y_offset

        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, slider_width, slider_height))

        green_pos = int(y + (1 - green_threshold / self.max_threshold_value) * slider_height)
        yellow_pos = int(y + (1 - yellow_threshold / self.max_threshold_value) * slider_height)

        pygame.draw.rect(self.screen, (0, 255, 0), (x - 5, green_pos - 5, slider_width + 10, 10))
        pygame.draw.rect(self.screen, (255, 255, 0), (x - 5, yellow_pos - 5, slider_width + 10, 10))

        green_text = self.font.render(f"G: {green_threshold:.2f}", True, (255, 255, 255))
        yellow_text = self.font.render(f"Y: {yellow_threshold:.2f}", True, (255, 255, 255))
        self.screen.blit(green_text, (x - 100, green_pos - 10))
        self.screen.blit(yellow_text, (x - 100, yellow_pos - 10))
    
    def handle_click(self, pos):
        # Handle mouse click events
        if self.menu.handle_click(pos):
            return

        if self.view_mode == "sensors":
            self.handle_sensor_click(pos)
        elif self.view_mode == "oscilloscope":
            self.handle_slider_click(pos)

    def handle_sensor_click(self, pos):
        # Handle sensor click events
        for sensor in self.logic.sensor_manager.sensors:
            button_rect = self.get_sensor_button_rect(sensor)
            if button_rect.collidepoint(pos):
                if sensor.connected:
                    sensor.active = not sensor.active
                self.dragging_port = sensor
                return

    def handle_release(self, pos):
        # Handle mouse release events
        if self.dragging_port:
            column_width = self.width // 3
            if column_width <= pos[0] < column_width * 2:
                self.dragging_port.column = "external"
            elif column_width * 2 <= pos[0]:
                self.dragging_port.column = "internal"
            else:
                self.dragging_port.column = "neutral"
            self.dragging_port = None

    def handle_slider_click(self, pos):
        # Handle slider click events
        self.handle_slider_drag(pos)

    def handle_drag(self, pos):
        # Handle mouse drag events
        if self.view_mode == "oscilloscope":
            self.handle_slider_drag(pos)
        elif self.view_mode == "sensors" and self.dragging_port:
            # Update the position of the dragged port
            pass

    def get_sensor_button_rect(self, sensor):
        # Get the rectangle for the sensor button
        column_width = self.width // 3
        row_height = 60
        
        if sensor.column == "neutral":
            x = 50
        elif sensor.column == "external":
            x = column_width + 50
        elif sensor.column == "internal":
            x = column_width * 2 + 50
        
        y = 70 + (sensor.port - 1) * row_height
        
        return pygame.Rect(x, y, 100, 40)

    def handle_slider_drag(self, pos):
        # Handle slider drag events
        x, y = pos
        slider_x = self.width - 70
        slider_height = self.height // 2 - 100

        if slider_x - 5 <= x <= slider_x + 45:
            if 50 <= y <= 50 + slider_height:  # External oscilloscope
                normalized_pos = 1 - (y - 50) / slider_height
                value = normalized_pos * self.max_threshold_value
                if abs(value - self.green_threshold_external) < abs(value - self.yellow_threshold_external):
                    self.green_threshold_external = max(0, min(self.yellow_threshold_external, value))
                else:
                    self.yellow_threshold_external = max(self.green_threshold_external, min(self.max_threshold_value, value))
            elif self.height // 2 + 50 <= y <= self.height // 2 + 50 + slider_height:  # Internal oscilloscope
                normalized_pos = 1 - (y - (self.height // 2 + 50)) / slider_height
                value = normalized_pos * self.max_threshold_value
                if abs(value - self.green_threshold_internal) < abs(value - self.yellow_threshold_internal):
                    self.green_threshold_internal = max(0, min(self.yellow_threshold_internal, value))
                else:
                    self.yellow_threshold_internal = max(self.green_threshold_internal, min(self.max_threshold_value, value))

if __name__ == "__main__":
    game = Game()
    game.run()