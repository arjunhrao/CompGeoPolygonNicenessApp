
# coding: utf-8

# In[1]:


import pygame
from pygame.locals import *
from convexHull import convexHull
# credit to https://github.com/quillyBeans/VisualConvexHull for the convexhull code, which is under the MIT license
from smallestenclosingcircle import make_circle
# credit to https://www.nayuki.io/page/smallest-enclosing-circle?fbclid=IwAR3BVscdXwKYr6Wx0PRO_fl5sFU8ZeA8iWvmGQL4ZcvqqMfEXaO9dOuNFM8 for the enclosing circle code
# which is free software under the GNU Lesser General Public License
from shapely.geometry import Polygon
from math import pi
import numpy as np

def bounding_box(points):
    if len(points) == 0:
        min_x, min_y = 0,0
        max_x, max_y = 0,0
    else:
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")
        for x,y in points:
            # Set min coords
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            # Set max coords
            if x > max_x:
                max_x = x
            elif y > max_y:
                max_y = y
    return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

class Button:
    def __init__(self, button_message, coordinates):
        self.caption = " " + button_message
        self.btn_width = 90
        self.btn_height = 30
        self.rect = pygame.Rect(coordinates[0], coordinates[1], self.btn_width, self.btn_height)
        self.surface = pygame.Surface(self.rect.size)
        self.bg_color = pygame.Color('gray')
        self.fg_color = pygame.Color('black')
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self._update()
        print(pygame.font.get_fonts())

    def pressed(self, mouse):
        # if mouse right or left is within the button
        if mouse[0] > self.rect.topleft[0] and mouse[1] > self.rect.topleft[1]:
            if mouse[0] < self.rect.bottomright[0] and mouse[1] < self.rect.bottomright[1]:
                return True
        return False

    def draw(self, display_surface):
        display_surface.blit(self.surface, self.rect)

    def _update(self):

        # fill the button background
        self.surface.fill(self.bg_color)
        # render the caption and return a rectangle
        caption_surf = self.font.render(self.caption, True, self.fg_color, self.bg_color)
        caption_rect = caption_surf.get_rect()
        # inflate in place, moves the text to a more pleasing spot in the button
        caption_rect.inflate_ip(-10, -17)
        # commits the caption
        self.surface.blit(caption_surf, caption_rect)

        # draw border for normal button
        w = self.rect.width
        h = self.rect.height
        pygame.draw.rect(self.surface, pygame.Color('white'), pygame.Rect((0, 0, w, h)), 1)


class App:
    def __init__(self):
        self.button_width = 20
        self.button_spacing = 100
        self.button_offset = 0
        self.button_right_most = 840
        self.msg_display_top_left = 40, 60
        self.running = True
        self.display_surf = None
        self.size = self.weight, self.height = 960, 720
        self.bg_color = None
        self.point_color = None
        self.hull_color = None
        self.mouse_x, self.mouse_y = 0, 0
        self.font_obj = None
        self.points = []
        self.ch_points = []
        self.msg = "Click points in cw or ccw order to add"
        self.btn_reset = Button("Reset", (self.button_right_most - self.button_offset, self.button_width))
        self.button_offset += self.button_spacing
        self.btn_get_box = Button("Bounding Box", (self.button_right_most - self.button_offset, self.button_width))
        self.button_offset += self.button_spacing
        self.btn_get_circle = Button("Min Circle", (self.button_right_most - self.button_offset, self.button_width))
        self.button_offset += self.button_spacing
        self.btn_get_convex = Button("CHull Ratio", (self.button_right_most - self.button_offset, self.button_width))
        self.circle = []
        self.box = []
    def on_init(self):
        pygame.init()
        self.font_obj = pygame.font.Font('freesansbold.ttf', 24)
        self.bg_color = pygame.Color(255, 255, 255)
        self.point_color = pygame.Color(0, 0, 0)
        self.hull_color = pygame.Color('blue')
        self.circle_color = pygame.Color('red')
        self.box_color = pygame.Color('green')
        self.display_surf = pygame.display.set_mode(self.size)
        self.running = True

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == MOUSEBUTTONUP and event.button in (1, 2, 3):
            print("an event: ", self.points)
            
            if self.btn_get_box.pressed(event.pos):
                self.box = bounding_box(self.points.copy())
                print("get box:" , self.box)
                polyArea = int(self.polygon.area)
                min_x, min_y = self.box[0][0], self.box[0][1]
                max_x, max_y = self.box[2][0], self.box[2][1]
                boxArea = int( (max_x - min_x) * (max_y - min_y) )
                self.msg = "Polygon area: " + str(polyArea) + "   Bounding Box area: " +                     str(boxArea) + "    Ratio: " + str(round(polyArea/boxArea, 5))
            
            elif self.btn_get_circle.pressed(event.pos):
                self.circle = make_circle(self.points.copy())
                print("get circle:" , self.circle)
                polyArea = int(self.polygon.area)
                r = self.circle[2]
                circleArea = int(pi * r**2)
                self.msg = "Polygon area: " + str(polyArea) + "    Min circle area: " +                     str(circleArea) + "    Ratio: " + str(round(polyArea/circleArea, 5))
            
            elif self.btn_get_convex.pressed(event.pos):
                # send in a copy bc it changes the ordering to sorted
                self.ch_points = convexHull(self.points.copy())
                polyArea = int(self.polygon.area)
                chArea = int(Polygon(self.ch_points).area)
                self.msg = "Polygon area: " + str(polyArea) + "    CH area: " +                     str(chArea) + "    Ratio: " + str(round(polyArea/chArea, 5))
                 
                
                print("get hull")
#                 print("convex hull event: ", self.points)
            elif self.btn_reset.pressed(event.pos):
                self.points, self.ch_points, self.circle, self.polygon, self.box = [], [], [], [], []
                self.msg = "Click points in cw or ccw order to add"
                print("reset")
            else:
                # don't add if the point isn't already in there
                # (note: currently linear scan which is ok bc small # of pts. Can be improved later)
                if event.pos not in self.points:
                    self.points.append(event.pos)
                # the polygon must be updated - the only time it is is when you add a point
                if len(self.points) > 2:
                    self.polygon = Polygon(self.points)
                    self.msg = "Added (x,y): " + str(event.pos) + "     Polygon area: " + str(int(self.polygon.area))
                else:
                    self.msg = "Added (x,y): " + str(event.pos)
                
                
    def on_loop(self):
        #print("enter on loop")
        self.display_surf.fill(self.bg_color)
        self.btn_get_convex.draw(self.display_surf)
        self.btn_get_circle.draw(self.display_surf)
        self.btn_get_box.draw(self.display_surf)
        self.btn_reset.draw(self.display_surf)

        # draws out the regular coordinate dots if populated
        #print(self.points)
        for coord in self.points:
            pygame.draw.circle(self.display_surf, self.point_color, coord, 5, 0)
        if len(self.points) > 1:
            pygame.draw.lines(self.display_surf, self.point_color, True, self.points, 1)

        # draws out the convex hull coordinate dots if populated
        #print(self.points)
        for coord in self.ch_points:
            pygame.draw.circle(self.display_surf, self.hull_color, coord, 5, 0)
        # draws the edges to show the convex hull if populated
        if len(self.ch_points) > 1:
            pygame.draw.lines(self.display_surf, self.hull_color, True, self.ch_points, 1)
            
        # draw the min enclosing circle
        if len(self.circle) > 1:
            x, y, r = int(self.circle[0]), int(self.circle[1]), int(self.circle[2])
            pygame.draw.circle(self.display_surf, self.circle_color, (x,y), r, 1)
        
        # draw the bounding box
        if len(self.box) == 4:
            pygame.draw.lines(self.display_surf, self.box_color, True, self.box, 1)
        
        # message display window
        #for line in self.msg.split("\n"):
        msg_surface_obj = self.font_obj.render(self.msg, False, self.point_color)
        msg_rect_obj = msg_surface_obj.get_rect()
        msg_rect_obj.topleft = (self.msg_display_top_left[0], self.msg_display_top_left[1])
        self.display_surf.blit(msg_surface_obj, msg_rect_obj)

    def on_render(self):
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def execute(self):
        self.on_init()
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    lets_go = App()
    lets_go.execute()


# In[1]:


# trying something i saw on stackoverflow to see why i program isn't working - conclusion is that i need
# to run it in python from the command line and it crashes in jupyter notebook

# import pygame
# import sys

# pygame.init()
# gameDispaly=pygame.display.set_mode((800,600))
# pygame.display.set_caption('FIRST GAME')

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: 
#              sys.exit(0)


# In[2]:


# testing area of a polygon using shapely

# from shapely.geometry import Polygon

# coords  = ((-1, 0), (-1, 1), (0, 0.5), (1, 1), (1, 0), (-1, 0))

# polygon = Polygon(coords)

# polygon.area

