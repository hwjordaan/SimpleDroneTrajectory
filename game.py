import os
from math import sin, radians, degrees, copysign

import pygame
from pygame.math import Vector2

import math

GREEN = (  0, 255,   0)

class Circuit:
    def __init__(self):
        # list of waypoints in the circuit (in order)
        self.waypoints = []

        # embed the image of waypoint in circuit class
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "waypoint.png")
        self.image = pygame.image.load(image_path)

    def addWaypoint(self, x, y):
        waypoint = Vector2(x, y)
        self.waypoints.append(waypoint)


class Drone:
    def __init__(self, x, y, angle=0.0, mass=2.0, max_force=100.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.force = Vector2(0.0, 0.0)
        self.mass = mass
        self.max_force = max_force

        # embed the image of drone in class
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "quad_top_small.png")
        self.image = pygame.image.load(image_path)

        self.int_error = 0.0
        self.position_ref = self.position
        self.next_waypoint = 0

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
        # Create drone instance
        drone = Drone(640, 360)

        # Create circuit and add waypoints
        circuit1 = Circuit()
        circuit1.addWaypoint(500, 100)
        circuit1.addWaypoint(50, 250)
        circuit1.addWaypoint(1000, 600)

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
            drone.position_ref = circuit1.waypoints[drone.next_waypoint]
            error = drone.position_ref - drone.position
            error_size = math.sqrt(error.x*error.x + error.y*error.y)
            if error_size < 2:
                drone.next_waypoint += 1
                if drone.next_waypoint >= len(circuit1.waypoints):
                    drone.next_waypoint = 0
            
            # Drawing
            self.screen.fill((255, 255, 255))

            # display the circuit
            for waypoint in circuit1.waypoints:
                rect = circuit1.image.get_rect()
                self.screen.blit(circuit1.image, waypoint- (rect.width / 2, rect.height))
                pygame.draw.circle(self.screen, GREEN, [int(waypoint.x),int(waypoint.y)], 5)

            # display the drone position
            rect = drone.image.get_rect()            
            self.screen.blit(drone.image, drone.position - (rect.width / 2, rect.height / 2))

            # display some usefull data on screen
            textWriter = pygame.font.SysFont('Arial', 15)
            text = textWriter.render("Position: [" + str.format('{0:.2f}',drone.position.x) + ", " + str.format('{0:.2f}',drone.position.y)+"]", 1, GREEN)
            self.screen.blit(text, (1100, 600))
            text = textWriter.render("Velocity: [" + str.format('{0:.2f}',drone.velocity.x) + ", " + str.format('{0:.2f}',drone.velocity.y)+"]", 1, GREEN)
            self.screen.blit(text, (1100, 600 + textWriter.get_linesize()))
            text = textWriter.render("Next Waypoint: Waypoint " + str(drone.next_waypoint), 1, GREEN)
            self.screen.blit(text, (1100, 600 + 2*textWriter.get_linesize()))

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
