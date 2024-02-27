# import pygame asprite package, download by typing "pip3 install pygame_aseprite_animation" into your terminal
from pygame_aseprite_animation import *
# Import the pygame module
import os, pygame

# Import random for random numbers
import random

# Import math for oscillation
import math

# Import the menu library to more easily make menu selction
import pygame_menu

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Import levels
import levels.level1 as level1
import levels.level2 as level2
import tutorials.tutorials_main as tutorials_main




        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT-200),
            )
        )

    # Move the Note based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set aseprite file directory
dirname = os.path.dirname(__file__)
aseprite_file_directory = str(dirname) + '/TheHarvester.aseprite'

# initialize animations - To add new animations, create a new animationmanager the same way its created here and put the Animation in its list
test_animation = Animation(aseprite_file_directory)
animationmanager = AnimationManager([test_animation], screen)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

bg_img = pygame.image.load('assets/images/backgrounds/mario level.png')
bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

# Create custom events for adding a Note
ADDNote = pygame.USEREVENT + 2
pygame.time.set_timer(ADDNote, 2500)

# Create our 'player'
player = Player()

# Create groups to hold Note sprites, and all sprites
# - Notes is used for position updates
# - all_sprites isused for rendering
Notes = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
pygame.mixer.music.load("assets/sounds/background-music/smoke-on-water.mp3")
pygame.mixer.music.play(loops=-1)


# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new Note?
        elif event.type == ADDNote:
            # Create the new Note, and add it to our sprite groups
            new_Note = Note()
            Notes.add(new_Note)
            all_sprites.add(new_Note)


current_level = 0

level_list = [("Mario", level1), ("Mountains", level2)]


def select_level(name, index):
    # This updates current level to the index of the selected level
    global current_level
    current_level = index

    animationmanager.update_self(0, 0)
    # Flip everything to the display
    pygame.display.flip()

def redraw(widget, decos):
    decos.add_rect(-widget.get_width()/2,-widget.get_height()/2+1,pygame.Rect(0,0 , widget.get_width(),widget.get_height()),[255,187,68])
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,-widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(-widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
        

def start_level():
    # This 
    level_list[current_level][1].start()



if __name__ == "__main__":

    pygame.init()   

surface = pygame.display.set_mode((800, 600))
mytheme = pygame_menu.themes.Theme( # transparent background
                title_background_color=(255, 40, 40),
                title_font_color=(255,255,255),
                widget_font_color=(0,0,0),
                background_color=pygame_menu.baseimage.BaseImage("Oreng.jpg"), 
                widget_selection_effect = pygame_menu.widgets.NoneSelection()
                )
menu = pygame_menu.Menu('Guitar Champions', 800, 600,theme=mytheme)
def draw_update_function(widget, menu):

    widget.set_margin(0,50)
    if (widget.is_selected()):
        widget.set_font_shadow(True,(0,0,0),None,1)
        widget.set_background_color([239,159,20])
        widget.shadow(shadow_type='rectangular', shadow_width=20, corner_radius=0, color=(0, 0, 0), aa_amount=4)
        widget.set_padding(3*(abs(pygame.time.get_ticks() % 2000-1000)/500))
        style={
            "color": (255,255,255),
            "antialias": True
        }
        widget.get_decorator().remove_all()
        redraw(widget,widget.get_decorator())
    else:
        widget.set_font_shadow(False,(0,0,0),None,1)
        widget.set_background_color([255,187,68])
        widget.shadow(shadow_type='rectangular', shadow_width=0, corner_radius=0, color=(0, 0, 0), aa_amount=4)
        widget.set_padding(4)
        style={
            "color": (0,0,0),
            "antialias": True
        }
    widget.update_font(style)
        
#array that stores widgets
widgets=[]

#all widgets, must have an update function, be moved into position, and added to the array
levbutt=menu.add.selector('Level Select:', [(level[0], index) for index, level in enumerate(level_list)],float=True, font_name='script', onchange=select_level)
levbutt.add_draw_callback(draw_update_function)
levbutt.translate(0,-170)
widgets.append(levbutt)

playbutt=menu.add.button('Play', start_level, float=True,font_name='script')
playbutt.add_draw_callback(draw_update_function)
playbutt.translate(0,-70)
widgets.append(playbutt)

tutbutt=menu.add.button('Tutorial', tutorials_main.tutorials_menu, float=True,font_name='script')
tutbutt.add_draw_callback(draw_update_function)
tutbutt.translate(0,30)
widgets.append(tutbutt)

quitbutt=menu.add.button('Quit', pygame_menu.events.EXIT, float=True,font_name='script')
quitbutt.add_draw_callback(draw_update_function)
quitbutt.translate(0,140)
widgets.append(quitbutt)

for widget in widgets:
    decos=widget.get_decorator()
    decos.add_rect(-widget.get_width()/2,-widget.get_height()/2+1,pygame.Rect(0,0 , widget.get_width(),widget.get_height()),[255,187,68])
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,-widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(-widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,187,68],True)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)

menu.mainloop(surface)

