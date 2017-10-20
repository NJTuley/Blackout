import Colors
import pygame
import abc

# class that will handle animations drawn during gameplay


# list holding all valid types of animations handled by this class

types = {
    'Min-Max-Looping': 0,  # this type of animation starts at the minimum state, iterates to the maximum state, then restarts back at the minimum state and repeats for the duration of the animation
    'Min-Max-Rebound': 1,  # this type of animation starts at the minimum state, iterates to the maximum state, then iterates back to the minimum state, and repeats this for the duration of the animation
    'Min-Max-Single': 2,  # this type of animation starts at the minimum state, iterates to the maximum state, then ends the animation, regardless of the stated duration (for animations of this type, a duration should not be specified and duration will default to 0)
    'Center-Max-Looping': 3,  # this type of animation is like the min-max-looping animation, but it starts at the middle state (all values are at the median for their respective ranges), iterates to the maximum state, jumps to the minimum state, then iterates back to the center state, and repeats for the duration of the animation
    'Center-Max-Rebound': 4,  # this type of animation is like the min-max-rebound animation, but it starts at the middle state (see above for explanation of middle state), then iterates to the maximum state, then iterates back to the middle state, then iterates to the minimum state, then iterates back to the middle state, and repeats for the duration of the animation
    'Center-Max-Single-Loop': 5,  # this type of animation is like the min-max-single animation, but it starts at the middle state, iterates to the maximum state, then jumps to the minimum state, then iterates back to the middle state and ends the animation
    'Center-Max-Single-Rebound': 6,  # this type of animation is like the center-max-single-loop animation, but it starts at the middle state, iterates to the maximum state, then iterates back to the middle state, then iterates to the minimum state, and finally iterates back to the middle state and then ends the animation
    'Center-Min-Looping': 7,  # this type of animation is like the center-max-looping animation, but it starts at the middle state, iterates to the minimum state, then jumps to the maximum state, iterates to the center, and then repeats for the duration of the animation
    'Center-Min-Rebound': 8,  # this type of animation is like the center-max-rebound animation, but it starts at the middle state, iterates to the minimum state, iterates back to the middle state, iterates to the maximum state, iterates back to the middle state, and repeats for the duration of the animation
    'Center-Min-Single-Loop': 9,  # this type of animation is like the center-max-single-loop animation, but it starts at the middle state, iterates to the minimum state, jumps to the maximum state, iterates back to the middle state, and ends the animation
    'Center-Min-Single-Rebound': 10,  # this type of animation is like the center-max-single-rebound animation, but it starts at the middle state, iterates to the minimum state, iterates to the middle state, iterates to the maximums state, iterates back to the middle state, and then ends the animation
    'Max-Min-Looping': 11,  # this type of animation is like the min-max-looping animation, but it starts at the maximum state, iterates to the minimum state, jumps back to the maximum state, and repeats for the duration of the animation
    'Max-Min-Rebound': 12,  # this type of animation is like the min-max-rebound animation, but it starts at the maximum state, iterates to the minimum state, iterates back to the maximum state, and repeats for the duration of the animation
    'Max-Min-Single': 13  # this type of animation is like the min-max-single animation, but it starts at the maximum state, iterates to the minimum state, and then ends the animation
}

# list of all valid shapes for an animation that uses this class
shapes = [
    'circle',
    'rectangle',
    'square',
]


class Animation():
    shape = None  # the shape being manipulated for this animation
    # @param type The type of this animation (see list above class definition for all valid types)
    # @param shape The shape that is being used for this animation
    # @param xRange The range of x values that will be used for this animation
    # @param yRange The range of y values that will be used for this animation
    # @param heightRange The range of height values that will be used for this animation
    # @param widthRange The range of width values that will be used for this animation
    # @param fillRange The range of fill color values that will be used for this animation
    # @param borderColorRnage The range of color values that will be used for the border of the shape being animated
    def __init__(self, shape, xRange, yRange, heightRange, widthRange, fillRange, borderColorRange, borderWidthRange, duration = 0, numFullCycles = 1):
        self.xRange = xRange
        self.yRange = yRange
        self.heightRange = heightRange
        self.widthRange = widthRange
        self.fillRange = fillRange
        self.borderColorRange = borderColorRange
        self.borderWidthRange = borderWidthRange
        self.shape = shape
        self.numIterations = 0  # keeps track of how many times this animation has been updated
        self.duration = duration
        self.numCycles = numFullCycles  # this is the number of times that the animation will cycle through its full range of values during the duration of the animation
        self.connected = False

        # depending on the type of this animation, set the initial values of this animation
        try:
            self.setStartValues()
        except Exception as exc:
            print(exc)


    # sets the starting values for this animation based on the type of animation that it is
    #   this function is abstract and will be overloaded by the animation subclasses, so all values in this function are set to None
    @abc.abstractmethod
    def setStartValues(self):
        pass


    # abstract method that subclasses will overload. The overloaded methods will iterate the progress of the animation as defined by their animation type (a min-max animation would increment all of its values, a max-min animation would decrement all of its values, etc.)
    @abc.abstractmethod
    def iterate(self):
        self.numIterations += 1
        pass


    # abstract method to update all graphics for this animation on the pygame screen. Will be overloaded by subclasses
    @abc.abstractmethod
    def update(self, window, alignment):
        pass


    # set the center points for this animation
    def setParentBounds(self, parentLeftBound, parentRightBound, parentTopBound, parentBottomBound):
        self.connected = True  # holds whether or not this object is connected (visually) to another object
        self.connectedObjectBounds = {  # the bounds of the object that this animation is connected to
            'left': parentLeftBound,
            'right': parentRightBound,
            'top': parentTopBound,
            'bottom': parentBottomBound
        }