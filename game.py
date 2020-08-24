import os
from math import sin, radians, degrees, copysign

import pygame
from pygame.math import Vector2


class Drone:
    def __init__(self, x, y, angle=0.0, mass=2.0, max_force=100.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.force = Vector2(0.0, 0.0)
        self.mass = mass
        self.max_force = max_force

        self.int_error = 0.0

        self.position_ref = self.position

    def update(self, dt):
        # basic position controller
        self.force.x = 0.05*(self.position_ref.x -
                             self.position.x) - 0.2*self.velocity.x
        self.force.y = 0.05*(self.position_ref.y -
                             self.position.y) - 0.2*self.velocity.y

        #self.force = 0.1*(self.position_ref - self.position) +0.01*self.int_error
        #self.int_error += (self.position_ref - self.position)

        # limit control force
        if self.force.x > self.max_force:
            self.force.x = self.max_force

        if self.force.y > self.max_force:
            self.force.y = self.max_force

        # dynamic equation - determine acceleration
        self.force += -0.2*self.velocity  # air drag
        acceleration = self.force / self.mass

        # integrate states
        self.velocity += acceleration*dt
        self.position += self.velocity*dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Simple Drone Path")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "quad_top_small.png")
        drone_image = pygame.image.load(image_path)

        image_path = os.path.join(current_dir, "waypoint.jpg")
        waypoint_image = pygame.image.load(image_path)

        drone = Drone(640, 360)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                drone.velocity.y = 5
            elif pressed[pygame.K_DOWN]:
                drone.velocity.y = -5

            if pressed[pygame.K_RIGHT]:
                drone.velocity.x = 5
            elif pressed[pygame.K_LEFT]:
                drone.velocity.x = -5

            # Logic
            drone.update(dt)

            # Drone logic goes here
            point = Vector2(500, 20)
            drone.position_ref = point

            # Drawing
            self.screen.fill((255, 255, 255))

            rect = drone_image.get_rect()
            self.screen.blit(drone_image, drone.position -
                             (rect.width / 2, rect.height / 2))

            # waypoint 1
            point = Vector2(500, 20)
            self.screen.blit(waypoint_image, point)

            # waypoint 2
            point = Vector2(20, 50)
            self.screen.blit(waypoint_image, point)

            # waypoint 3
            point = Vector2(1000, 600)
            self.screen.blit(waypoint_image, point)

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
