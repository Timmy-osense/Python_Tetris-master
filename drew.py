# encoding: utf-8

#-------------------------------------------------------------------------
# 畫Box.
#-------------------------------------------------------------------------
class Box(object):
    #-------------------------------------------------------------------------
    # 建構式.
    #   pygame    : pygame.
    #   canvas    : 畫佈.
    #   name    : 物件名稱.
    #   rect      : 位置、大小.
    #   color     : 顏色.
    #-------------------------------------------------------------------------
    def __init__( self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color

        self.visivle = True
        
    #-------------------------------------------------------------------------
    # 更新.
    #-------------------------------------------------------------------------
    def update(self):
        if(self.visivle):
            # Calculate circle center and radius from rect
            center_x = self.rect[0] + self.rect[2] // 2
            center_y = self.rect[1] + self.rect[3] // 2
            radius = min(self.rect[2], self.rect[3]) // 2
            # Draw circle instead of rectangle
            self.pygame.draw.circle(self.canvas, self.color, (center_x, center_y), radius)

class BoxRect(object):
    #-------------------------------------------------------------------------
    # 建構式.
    #   pygame    : pygame.
    #   canvas    : 畫佈.
    #   name    : 物件名稱.
    #   rect      : 位置、大小.
    #   color     : 顏色.
    #-------------------------------------------------------------------------
    def __init__( self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color

        self.visivle = True
        
    #-------------------------------------------------------------------------
    # 更新.
    #-------------------------------------------------------------------------
    def update(self):
        if(self.visivle):
            self.pygame.draw.rect( self.canvas, self.color, self.rect)