# min-max-looping type animation

from Animation import shapes
from Animation import types
from Animation import Animation
import pygame
import Colors


class MinMaxLoopAnimation(Animation):

    def __init__(self, shape, xRange, yRange, heightRange, widthRange, fillRange, borderColorRange, borderWidthRange, duration = 1, numFullCycles = 0):
        super(Animation, self).__init__()
        self.xRange = xRange
        self.yRange = yRange
        self.heightRange = heightRange
        self.widthRange = widthRange
        self.fillRange = fillRange
        self.borderColorRange = borderColorRange
        self.borderWidthRange = borderWidthRange
        if(shape in shapes): # either a circle, rectangle, or sqaure
            self.shape = shape
        else:
            raise Exception("Invalid animation shape")
        self.type = types['Min-Max-Looping']
        self.numIterations = 0  # keeps track of how many times this animation has been updated
        if(duration != 0):
            self.duration = duration
        else:
            raise Exception("Cannot have an animation with a duration of 0")
        if(numFullCycles != 0):
            self.numCycles = numFullCycles
        else:
            raise Exception("Cannot have an animation with 0 full cycles to complete")

        # set the iteration values for each variable
        if(len(self.xRange) > 1):
            self.xIter = (max(self.xRange) - min(self.xRange)) / self.duration * self.numCycles
        else:
            self.xIter = 0
        if(len(self.yRange) != 0):
            self.yIter = (max(self.yRange) - min(self.yRange)) / self.duration * self.numCycles
        else:
            self.yIter = 0
        if(len(self.heightRange) != 0):
            self.heightIter = (max(self.heightRange) - min(self.heightRange)) / self.duration * self.numCycles
        else:
            self.heightIter = 0
        if(len(self.widthRange) != 0):
            self.widthIter = (max(self.widthRange) - min(self.widthRange)) / self.duration * self.numCycles
        else:
            self.widthIter = 0
        if(len(self.fillRange) != 0):
            self.fillIter = (max(self.fillRange) - min(self.fillRange)) / self.duration * self.numCycles
        else:
            self.fillIter = 0
        if(len(self.borderWidthRange) != 0):
            self.borderWidthIter = (max(self.borderWidthRange) - min(self.borderWidthRange)) / self.duration * self.numCycles
        else:
            self.borderWidthIter = 0
        if(len(self.borderColorRange) != 0):
            self.borderColorIter = (max(self.borderColorRange) - min(self.borderColorRange)) / self.duration * self.numCycles
        else:
            self.borderColorIter = 0

        self.setStartValues()

    def setStartValues(self):
        self.x = self.validateRangeGetMin(self.xRange)
        self.y = self.validateRangeGetMin(self.yRange)
        self.height = self.validateRangeGetMin(self.heightRange)
        self.width = self.validateRangeGetMin(self.widthRange)
        newFill = self.validateRangeGetMin(self.fillRange)
        self.fill = (newFill, newFill, newFill)
        self.borderWidth = self.validateRangeGetMin(self.borderWidthRange)
        newBorderFill = self.validateRangeGetMin(self.borderColorRange)
        self.borderColor = (newBorderFill, newBorderFill, newBorderFill)


    # iterate all values for this animation to the next value in their range
    def iterate(self):
        if(self.x > max(self.xRange) - self.xIter):
            # reached maximum value for the x range of this animation
            self.x = max(self.xRange) - self.xIter
            self.xIter *= -1
        elif(self.x < min(self.xRange) - self.xIter):
            self.x = min(self.xRange) - self.xIter
            self.xIter *= -1
        else:
            self.x += self.xIter
        if(self.y > max(self.yRange) - self.yIter):
            self.y = max(self.yRange) - self.yIter
            self.yIter *= -1
        elif(self.y < min(self.yRange) - self.yIter):
            self.y = min(self.yRange) - self.yIter
            self.yIter *= -1
        else:
            self.y += self.yIter
        if(self.fill[0] > int(max(self.fillRange)) - self.fillIter):
            newColor = int(max(self.fillRange) - self.fillIter)
            self.fill = (newColor, newColor, newColor)
            self.yIter *= -1
        elif(self.fill[0] < int(min(self.fillRange)) - self.fillIter):
            newColor = int(min(self.fillRange) - self.fillIter)
            self.fill = (newColor, newColor, newColor)
            self.fillIter *= -1
        else:
            newFill = self.fill[0] + self.fillIter
            self.fill = (newFill, newFill, newFill)
        if(self.borderWidth > max(self.borderWidthRange) - self.borderWidthIter):
            self.borderWidth = min(self.borderWidthRange) + self.borderWidthIter
        else:
            self.borderWidth += self.borderWidthIter

        self.height = self.connectedObjectBounds['bottom'] - self.connectedObjectBounds['top']
        self.width = self.connectedObjectBounds['right'] - self.connectedObjectBounds['left']

        if(self.borderColor[0] > max(self.borderColorRange) - self.borderColorIter):
            newColor = min(self.borderColorRange)
            self.borderColor = (newColor, newColor, newColor)
        else:
            newColor = self.borderColor[0] + self.borderColorIter
            self.borderColor = (newColor, newColor, newColor)

        self.numIterations += 1


    # update the graphical display of this animation on the pygame screen
    def update(self, window, alignment):
        if(self.shape == 'rectangle' or self.shape == 'square'):
            x = self.connectedObjectBounds['left'] - (self.x - min(self.xRange))
            y = self.connectedObjectBounds['top'] - (self.y - min(self.yRange))
            if(self.shape == 'square' and self.height != self.width):
                raise Exception("Invalid square. Height must equal width")

            direction = 1

            #pygame.draw.rect(window, self.fill, pygame.Rect(int(x), int(y), int(self.height), int(self.width)), 0)
            #pygame.draw.rect(window, self.borderColor, pygame.Rect(int(x - self.borderWidth), int(y - self.borderWidth), int(self.height + 2 * self.borderWidth), int(self.width + 2 * self.borderWidth)), int(self.borderWidth))
            for i in range(int(min(self.borderWidthRange)), int(max(self.borderWidthRange))):
                newX = x - i
                newY = y - i
                newWidth = self.width + 2 * i
                newHeight = self.height + 2 * i

                if(i < self.borderWidth):
                    newColor = 0 + self.borderColorIter * (self.borderWidth - i + 1)
                else:
                    newColor = Colors.black[0]

                if(newColor < 0):
                    newColor = 0
                elif(newColor > max(self.borderColorRange)):
                    newColor = max(self.borderColorRange)

                #pygame.draw.rect(window, (255 - newColor, 255 - newColor, 255 - newColor), pygame.Rect((newX - int(max(self.borderWidthRange) / 2), (newY - int(max(self.borderWidthRange) / 2))), (newWidth + int(max(self.borderWidthRange)) , newHeight + int(max(self.borderWidthRange)))), 1)
                pygame.draw.rect(window, (newColor, newColor, newColor), pygame.Rect((newX, newY), (newWidth, newHeight)), 1)

            pygame.draw.rect(window, self.fill, (pygame.Rect((x, y), (self.width, self.height))))
        else:
            raise Exception("Invalid animation shape")


    # @return Whether or not this animation is completed based on its duration (True if animation is complete, false otherwise)
    def isDone(self):
        if(self.numIterations >= self.duration):
            return True
        else:
            return False


    # validates that the given range is not empty, and returns the minimum value of the list if the list is not empty
    # @return the minimum value of the list
    def validateRangeGetMin(self, list):
        if (len(list) > 1):
            return min(list)
        elif (len(list) == 1):
            return list[0]
        else:
            raise Exception("Invalid Empty List for animation")