
import math
import pygame

defRadius = 30 #defualt player sprite radius
defSpeed = 15

# the possible statuses of the player
playerStatus = [
    'Dead', 'Alive'
]

class Player():
    fillColor = (255, 255, 255)
    borderColor = (0, 0, 0)

    def __init__(self, x, y, radius = defRadius, speed = defSpeed):
        self.posX = int(x)
        self.posY = int(y)
        self.radius = radius
        self.speed = speed
        self.status = 1  # the status of the player (corresponds to an index in the playerStatus list)

    # update the player object on the game screen
    def update(self, window):
        pygame.draw.circle(window, self.fillColor, (int(self.posX), int(self.posY)), int(self.radius), 0)
        pygame.draw.circle(window, self.borderColor, (int(self.posX), int(self.posY)), int(self.radius), 1)

    # move the player object to the position of the mouse as much as the player object's movement speed will allow
    def move(self, xMove, yMove):
        screen = {
            'width': 500,
            'height': 500
        }

        # get the distance between the current center of this circle and the given points
        move_dist = self.getPointDistance((xMove, yMove))

        if(move_dist > self.speed):
            #print("TOO FAST ")
            # the player's mouse is farther away than the player's movement speed would allow them to travel in one frame
            # make the player move as far as their speed would allow in the same direction as the player mouse is
            #   this is done by calculating the angle the player mouse is at from the center of this circle, and getting the point that is "player speed" pixels away from the center in that direction
            moveAngle = self.getAngle(xMove, yMove)
            newPos = self.getPointFromAngleDistance(moveAngle, self.speed)
           # print(newPos)
            self.posX += newPos[0]
            self.posY += newPos[1]

        else:
            #print("TOO SLOW")
            self.posX = xMove
            self.posY = yMove



    # detect if there is a collision with any of the tiles in the parameter list
    # @param tiles A list with all active tiles (white or gray), and this is used to check all tiles that neighbor the active tiles
    def getTileCollisions(self, tiles):
        collisions = []

        for row in range(len(tiles)):
            for cell in range(len(tiles[row])):
                if(self.rectCollidersIntersect(tiles[row][cell])):
                    if(self.circleInRectangle(tiles[row][cell])):
                        # the player object is inside of this tile - COLLISION - add to list of collisions
                        collisions.append(tiles[row][cell])
                    elif(self.rectIntersect(tiles[row][cell])):
                        # the tile has a side that intersects the circle - COLLISION - add to list of collisions
                        collisions.append(tiles[row][cell])

        return collisions


    # detect if the rectangle colliders that outline this circle and the given tile intersect (used to eliminate the need to further (and more "complicatedly" process collisions if the rectangle colliders don't even collide)
    def rectCollidersIntersect(self, tile):
        selfXMin = self.posX - self.radius  # the minimum x value of this circle's rect collider
        selfYMin = self.posY - self.radius  # the minimum y value of this circle's rect collider
        selfXMax = self.posX + self.radius
        selfYMax = self.posY + self.radius

        if((selfXMin < tile.positionX + tile.width or selfXMax < tile.positionX) and (selfYMin < tile.positionY + tile.height or selfYMax < tile.positionY)):  # rectangle colliders collide
            return True
        else:  # rectangle colliders do not collide
            return False


    def circleInRectangle(self, rect):
        if(self.posX > rect.positionX and self.posX < rect.positionX + rect.width
           and self.posY > rect.positionY and self.posY < rect.positionY + rect.height):
            # the center of this player circle is inside of the given rectangle
            return True
        else:
            return False


    def rectIntersect(self, rect):
        # lists to hold the points that are in the sides of the rectangle
        sides = {
            'topSide': [],
            'leftSide': [],
            'rightSide': [],
            'bottomSide': []
        }

        #populate lists for points that are on the sides of the rectangle
        for i in range(int(rect.width)):
            sides['topSide'].append((rect.positionX + i, rect.positionY))
            sides['bottomSide'].append((rect.positionX + i, rect.positionY + rect.height))
        for i in range(int(rect.height)):
            sides['leftSide'].append((rect.positionX, rect.positionY + i))
            sides['rightSide'].append((rect.positionX + rect.width, rect.positionY + i))

        # go through each side and see if there are any points of intersection with this player circle
        for side in sides:
            for i in range(len(sides[side])):
                # check if this individual point is inside of the player circle
                if(self.getPointDistance(sides[side][i]) < self.radius):
                    # there is a point of intersection on this side of the rectangle, return true
                    return True

        # no points of intersection found on any sides of the rectangle
        return False

    # @param point The point that is being used to get the distance from the center of this circle
    # @return the distance between the center of this circle and the given x,y coordinate
    def getPointDistance(self, point):
       # print(point)
        distance = math.sqrt((self.posX - point[0]) ** 2 + (self.posY - point[1]) ** 2)
        return distance


    # @param x The x coordinate of the point
    # @param y The y coordinate of the point
    # @return the angle of the line between the center of this circle and the given x,y coordinate
    def getAngle(self, x, y):
        deltaX = x - self.posX
        deltaY = y - self.posY
        theta_radians = math.atan2(deltaY, deltaX)

        return theta_radians


    # get a point by specifying the angle and distance away from the center of this circle
    # @param angle The angle in radians
    # @param distance The distance from the center of this circle
    # @return The point
    def getPointFromAngleDistance(self, angle, distance):
        return ((distance * math.cos(angle)), (distance * math.sin(angle)))