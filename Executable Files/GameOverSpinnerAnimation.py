import pygame
import math

class GameOverSpinnerAnimation():


    def __init__(self, screen, text_color_start):
        self.wait_icon_path_radius = 25
        self.wait_icon_counter = 0
        self.wait_icon_radius = screen[0] * 0.01
        self.numIconCircles = 4
        self.text_color = text_color_start
        self.wait_icon_center = (screen[0] * 0.71 + self.wait_icon_radius, screen[1] * 0.45 + self.wait_icon_radius)

    def update(self, gameWindow):
        # iterate the counter for this animation
        if(self.wait_icon_counter >= 100):
            self.wait_icon_counter = 0
        else:
            self.wait_icon_counter += 0.75

        self.points = []
        for i in range(self.numIconCircles):
            index = self.wait_icon_counter + 25 * i
            if (index >= 100):
                index = (index - 100)
            self.points.append(self.getCirclePoint(int(index), 100, self.wait_icon_path_radius, self.wait_icon_center))
            pygame.draw.circle(gameWindow, (self.text_color, self.text_color, self.text_color), (self.points[i]), int(self.wait_icon_radius), 0)

    # get a point that is in the perimeter of a circle
    # @param index The index of the point to return within the list of points on the circle perimeter
    # @param n The number of points to generate for the perimeter of the circle
    # @param r The radius of the circle
    def getCirclePoint(self, index, numPoints, radius, center):
        points = []
        for x in range(0, numPoints + 1):
            points.append((math.cos(2 * math.pi / numPoints * x) * radius + center[0],
                           math.sin(2 * math.pi / numPoints * x) * radius + center[1]))
        return (int(points[index][0]), int(points[index][1]))
