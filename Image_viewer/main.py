import ezpygame
import pygame
import os
import sys
import random
import tkinter as tk
from tkinter import filedialog

#TODO Buttons eyecandy
#TODO Center fonts at buttons

def isPointInsideRect(x, y, rect):
    """
    Checks if point is inside some rectangle (Rect object)
    :param x: horizontal
    :param y: vertical
    :param rect: rect to check inside
    :return: bool
    """
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def doRectsOverlap(rect1, rect2):
    """
    Checks if rectangles (Rect objects) overlap
    :param rect1: first Rect object
    :param rect2: second Rect object
    :return: bool
    """
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if((isPointInsideRect(a.left, a.top, b)) or
               (isPointInsideRect(a.left, a.bottom, b)) or
               (isPointInsideRect(a.right, a.top, b)) or
               (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False


class MainView(ezpygame.Scene):
    def __init__(self):
        #self.application.title = 'Gesture drawing'
        #self.application.resolution = (1280, 720)
        #self.application.update_rate = 60
        self.font = pygame.font.SysFont("Arial", 16)
        self.set_font = pygame.font.SysFont("Arial", 26)
        self.images = ["./placeholder.jpg"]
        self.current_image = 0
        #self.loaded_image = None
        self.loaded_image = pygame.image.load(self.images[self.current_image]).convert_alpha()
        self.loaded_image_scaled = pygame.Surface((32, 32))
        #self.loaded_image_scaled = pygame.transform.smoothscale(self.loaded_image, (int((self.loaded_image.get_size()[0]/self.loaded_image.get_size()[1])*self.application.resolution[1]), self.application.resolution[1]))
        self.unpause = pygame.image.load("./unpause.png").convert_alpha()
        self.icons = {"right": pygame.image.load("./right.png"),
                      "left": pygame.image.load("./left.png"),
                      "pause": pygame.image.load("./pause.png"),
                      "play": pygame.image.load("./play.png"),
                      "cog": pygame.image.load("./cog.png"),
                      "tick": pygame.image.load("./tick.png"),
                      "folder": pygame.image.load("./folder.png")}
        self.hide_timer = 0
        self.show_flag = True
        self.absolute_timer = 0
        self.absolute_termination = 0
        self.absolute_timer_pause = False
        self.settings_flag = False
        self.shuffle_flag = False
        try:
            #self.load_images("D:/osu/x/drawing/inspiration/Ilya")
            self.load_images(sys.argv[1])
        except IndexError:
            pass

    def on_enter(self, previous_scene):
        pygame.display.set_icon(pygame.Surface((1, 1), pygame.SRCALPHA, 32).convert_alpha())
        self.scale_main_image()
    
    def scale_main_image(self):
        self.loaded_image_scaled = pygame.transform.smoothscale(self.loaded_image, (int((self.loaded_image.get_size()[0]/self.loaded_image.get_size()[1])*self.application.resolution[1]), self.application.resolution[1]))
    
    def load_images(self, path):
        self.images = [os.path.join(path,fn) for fn in next(os.walk(path))[2]]
        self.images = self.process_images(self.images)
        self.current_image = 0
        self.loaded_image = pygame.image.load(self.images[self.current_image])
        #print(self.images)

    def process_images(self, arr):
        x = []
        supported = [".jpg", "jpeg", ".png", ".gif", ".bmp", ".pcx", ".tga", ".tif", ".lbm", ".pbm", ".pgm", ".ppm", ".xpm"]
        for i in arr:
            #print(i[-4:].lower())
            if not(i[-4:].lower() in supported):
                continue
            else:
                x += [i]
        if self.shuffle_flag:
            random.shuffle(x)
            return x
        else:
            x.sort()
            return x
        
    def draw(self, screen):
        per_x = lambda x: (self.application.resolution[0]/100)*x
        per_y = lambda x: (self.application.resolution[1]/100)*x
        nav_y = self.application.resolution[1]-32
        transparent_blank_surface = lambda w, h: pygame.Surface( (w, h), pygame.SRCALPHA, 32).convert_alpha()
        current_image = self.loaded_image_scaled
        screen.fill(pygame.transform.average_color(current_image))
        if not(self.absolute_timer_pause) and not(self.settings_flag):
            scaled = current_image
            if not(scaled == None):
                screen.blit(scaled, ((self.application.resolution[0]-scaled.get_size()[0])/2, 0))
        else:
            scaled = pygame.transform.smoothscale(self.unpause, (int((self.unpause.get_size()[0]/self.unpause.get_size()[1])*self.application.resolution[1]), self.application.resolution[1]))
            screen.blit(scaled, ((self.application.resolution[0]-scaled.get_size()[0])/2, 0))
        if ((self.hide_timer <= 3) and self.show_flag):
            navbar = transparent_blank_surface(self.application.resolution[0], 32)
            navbar.fill((110, 110, 110, 100))
            screen.blit(navbar, (0, nav_y))
            #draw icons
            screen.blit(self.icons["folder"], (per_x(10), per_y(2)))
            screen.blit(self.icons["cog"], (per_x(90), per_y(2)))
            screen.blit(self.icons["left"], (per_x(10), nav_y))
            screen.blit(self.icons["right"], (per_x(90), nav_y))
            if self.absolute_timer_pause:
                screen.blit(self.icons["pause"], (per_x(50), nav_y))
            else:
                screen.blit(self.icons["play"], (per_x(50), nav_y))
        if not(self.absolute_termination == 0):
            #absolute timer render
            bar = transparent_blank_surface((self.absolute_timer/self.absolute_termination)*per_x(100), 5)
            hue = self.absolute_timer*15
            if hue > 360:
                hue = int(hue/360)
            color = pygame.Color(0, 0, 0, 255)
            color.hsva = (hue, 100, 50, 100)
            #print(color)
            bar.fill(color)
            screen.blit(bar, (0, 0))
            #screen.blit(self.font.render(str(int(self.absolute_timer)), True, (115, 115, 115), (255, 255, 255)), (per_x(50), 24))
        if self.settings_flag:
            set_x = (per_x(100)-per_x(70))/2
            set_y = (per_y(100)-per_y(70))/2
            set_per_x = lambda x: (per_x(70)/100)*x
            set_per_y = lambda x: (per_y(70)/100)*x
            settings_box = transparent_blank_surface(set_per_x(100), per_y(80))
            settings_box.fill((130, 130, 130, 245))
            screen.blit(settings_box, (set_x, set_y))
            
            """
                 Directory:
                [....................]
                
                 Time:
                [0] [5]
                [15] [30]
                [60] [90]
                [300] [custom]
                [Randomize]
            """
            #Directory
            dir_text = self.set_font.render("Directory:", True, (200, 200, 200))
            screen.blit(dir_text, (set_per_x(5)+set_x, set_per_y(5)+set_y))
            dir_button = transparent_blank_surface(set_per_x(90), set_per_y(4))
            dir_button.fill((110, 110, 110, 255))
            screen.blit(dir_button, (set_per_x(5)+set_x, set_per_y(11)+set_y))
            ps = ( int( (set_per_x(100)-set_per_x(5))/2+set_x), set_per_y(11)+set_y)
            screen.blit(self.font.render("Click to set!", True, (200, 200, 200)), ps)
            #Time
            time_text = self.set_font.render("Time:", True, (200, 200, 200))
            screen.blit(time_text, (set_per_x(5)+set_x, set_per_y(16)+set_y))
            #   Time buttons
            buttons = ("empty", 0, 5, 15, 30, 60, 90, 300, "custom (not yet)")
            x_start = set_per_x(5)
            y_start = set_per_y(25)
            y_off = 2
            x_off = 0
            #print("a")
            for button in buttons:
                #start x=5, y=21
                bg = transparent_blank_surface(set_per_x(40), set_per_y(10))
                bg.fill((110, 110, 110, 255))
                if x_off == 1:
                    x_off = 0
                else:
                    x_off = 1
                #print(button, (set_per_x(5)+(set_per_x(40)*x_off)+set_x, (set_per_x(10)*y_off)+set_x))
                #print(button, "(set_per_x(%i)+(set_per_x(%i)*%i)+set_x, (set_per_x(%i)*%i)+set_x)" % (5, 40, x_off, 8, y_off))
                screen.blit(bg, (set_per_x(5)+(set_per_x(40)*x_off)+set_x, (set_per_x(8)*y_off)+set_y))
                text = self.set_font.render(str(button), True, (200, 200, 200))
                screen.blit(text, (set_per_x(5)+(set_per_x(40)*x_off)+set_x, (set_per_x(8)*y_off)+set_y))
                if self.absolute_termination == button:
                    screen.blit(self.icons["tick"], (set_per_x(5*3)+(set_per_x(40)*x_off)+set_x, (set_per_x(8)*y_off)+set_y))
                if (buttons.index(button)%2 == 0) and not(buttons.index(button) == 0):
                    y_off += 1
            
            #shuffle button
            bg = transparent_blank_surface(set_per_x(40), set_per_y(10))
            bg.fill((110, 110, 110, 255))
            text = self.set_font.render("Randomize?", True, (200, 200, 200))
            screen.blit(bg, (set_per_x(5)+set_x, (set_per_x(8)*y_off)+set_y))
            screen.blit(text, (set_per_x(5)+set_x, (set_per_x(8)*y_off)+set_y))
            if self.shuffle_flag:
                screen.blit(self.icons["tick"], (set_per_x(5*5)+set_x, (set_per_x(8)*y_off)+set_y))
            
        #screen.blit(self.current_image, (0, 0))
    
    def update(self, dt):
        if not(self.settings_flag):
            self.hide_timer += dt/1000
            if not(self.absolute_timer_pause):
                self.absolute_timer += dt/1000
            if self.absolute_timer >= self.absolute_termination:
                if self.absolute_termination == 0:
                    pass
                else:
                    self._go_right()
    
    #Event methods
    def _settings(self):
        self.settings_flag = not(self.settings_flag)
        if self.absolute_timer_pause:
            self.absolute_timer_pause = not(self.absolute_timer_pause)
    
    def _pause(self):
        if not(self.settings_flag):
            self.absolute_timer_pause = not(self.absolute_timer_pause)
    
    def _go_left(self):
        try:
            assert self.images[self.current_image-1]
            self.loaded_image = pygame.image.load(self.images[self.current_image-1])
            self.scale_main_image()
            self.current_image -= 1
            self.absolute_timer = 0
        except IndexError:
            #print("Can't go backwards")
            pass
    
    def _go_right(self):
        try:
            assert self.images[self.current_image+1]
            self.loaded_image = pygame.image.load(self.images[self.current_image+1])
            self.scale_main_image()
            self.current_image += 1
            self.absolute_timer = 0
        except IndexError:
            #print("Can't go forwards")
            pass
    
    def _choose_directory(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        del root
        if not(file_path == ""):
            self.load_images(file_path)
            self.absolute_timer = 0
            self.scale_main_image()
            #print(file_path)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            self.hide_timer = 0
        if event.type == pygame.MOUSEBUTTONUP:
            self.hide_timer = 0
            if event.button == 1:
                #GUI elements
                per_x = lambda x: (self.application.resolution[0]/100)*x
                per_y = lambda x: (self.application.resolution[1]/100)*x
                nav_y = self.application.resolution[1]-32
                if ((self.hide_timer <= 3) and self.show_flag):
                    #folder
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(per_x(10), per_y(2), 32, 32)):
                        self._choose_directory()
                    #cog
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(per_x(90), per_y(2), 32, 32)):
                        self._settings()
                    #left
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(per_x(10), nav_y, 32, 32)):
                        self._go_left()
                    #right
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(per_x(90), nav_y, 32, 32)):
                        self._go_right()
                    #pauseplay
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(per_x(50), nav_y, 32, 32)):
                        self._pause()
                #Settings
                if self.settings_flag:
                    set_x = (per_x(100)-per_x(70))/2
                    set_y = (per_y(100)-per_y(70))/2
                    set_per_x = lambda x: (per_x(70)/100)*x
                    set_per_y = lambda x: (per_y(70)/100)*x
                    w = set_per_x(40)
                    h = set_per_y(10)
                    """
                    https://img.fireden.net/v/image/1486/43/1486431272926.png
                    DO THIS IN LOOP YOU FUCKING TWAT
                    """
                    y_off = 1
                    #0
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*0)+set_x, (set_per_x(8)*(1+y_off))+set_y,w, h)):
                        self.absolute_termination = 0
                        self.absolute_timer = 0
                    #5
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*1)+set_x, (set_per_x(8)*(1+y_off))+set_y,w, h)):
                        self.absolute_termination = 5
                        self.absolute_timer = 0
                    #15
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*0)+set_x, (set_per_x(8)*(2+y_off))+set_y,w, h)):
                        self.absolute_termination = 15
                        self.absolute_timer = 0
                    #30
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*1)+set_x, (set_per_x(8)*(2+y_off))+set_y,w, h)):
                        self.absolute_termination = 30
                        self.absolute_timer = 0
                    #60
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*0)+set_x, (set_per_x(8)*(3+y_off))+set_y,w, h)):
                        self.absolute_termination = 60
                        self.absolute_timer = 0
                    #90
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*1)+set_x, (set_per_x(8)*(3+y_off))+set_y,w, h)):
                        self.absolute_termination = 90
                        self.absolute_timer = 0
                    #300
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*0)+set_x, (set_per_x(8)*(4+y_off))+set_y,w, h)):
                        self.absolute_termination = 300
                        self.absolute_timer = 0
                    #custom
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+(set_per_x(40)*1)+set_x, (set_per_x(8)*(4+y_off))+set_y,w, h)):
                        pass
                    #Choose directory
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+set_x, set_per_y(11)+set_y, set_per_x(90), set_per_y(4))):
                        self._choose_directory()
                    #Randomize
                    if isPointInsideRect(event.pos[0], event.pos[1], pygame.Rect(set_per_x(5)+set_x, (set_per_x(8)*(5+y_off))+set_y, set_per_x(40), set_per_y(10))):
                        self.shuffle_flag = not(self.shuffle_flag)
                        if self.shuffle_flag:
                            random.shuffle(self.images)
                        else:
                            self.images.sort()
                pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self._settings()
            if event.key == pygame.K_SPACE:
                self._pause()
            if event.key == pygame.K_LEFT:
                self._go_left()
            if event.key == pygame.K_RIGHT:
                self._go_right()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_F5:
                self.hide_timer = 0
                self.show_flag = not(self.show_flag)
        if event.type == pygame.VIDEORESIZE:
            # The main code that resizes the window:
            # (recreate the window with the new size)
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            self.scale_main_image()
        if event.type == pygame.USEREVENT:
            print(event.code)

app = ezpygame.Application(
    title="Gesture drawing",
    resolution=(1280, 720),
    update_rate=60,)
    
app._screen = pygame.display.set_mode(app.resolution, pygame.RESIZABLE)

app.run(MainView())