import pygame

import os

from pygame_aseprite_animation import *

import helpers.settings_helper as settings_helper

import helpers.tutorial_info as tutorial_info

import partials.buttons.text_button as text_button

import partials.titlecard.title_card as title_card

import partials.tutorial_popup.tutorial_popup as tutorial_popup

import helpers.sprite_item as sprite_item

import partials.notes.text_note as note

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_RIGHT,
    K_LEFT,
    KEYDOWN,
    QUIT,
)

def start():

    running = True
    paused = False
    restart_level = False

    pauserendered = False

    user_settings = settings_helper.get_settings()

    # Define constants for the screen width and height
    SCREEN_WIDTH = pygame.display.get_surface().get_size()[0]
    SCREEN_HEIGHT = pygame.display.get_surface().get_size()[1]


    # Setup for sounds, defaults are good
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    pause_title = title_card.Titlecard(text="   Paused   ", width= 350,height= 59, left_padding= SCREEN_WIDTH/2 - 175, top_padding= SCREEN_HEIGHT/2 - 180)
    

    # These are the buttons for the pause menu
    resume_button = text_button.TextButton(text=" Resume ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    restart_button = text_button.TextButton(text=" Restart ", width= 94,height= 44, left_padding= SCREEN_WIDTH/2 - 48, top_padding= SCREEN_HEIGHT/2 - 10)
    main_menu_button = text_button.TextButton(text=" Main Menu ", width= 128,height= 44, left_padding= SCREEN_WIDTH/2 - 62, top_padding= SCREEN_HEIGHT/2 +60)
    quit_button = text_button.TextButton(text=" Quit ", width= 60,height= 44, left_padding= SCREEN_WIDTH/2 -30, top_padding= SCREEN_HEIGHT/2 + 120)

    
    # TODO make the custom sprites for the tutorial
    # START/////////
    bg_img = pygame.image.load('assets/images/backgrounds/glacier_night.jpeg')
    bg_img = pygame.transform.scale(bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))

    #  the background image of the tabs
    tabs_image = pygame.image.load("assets/images/backgrounds/tabs_outline.png").convert()
    tabs_image.set_colorkey((255, 255, 255), RLEACCEL)

    # the image of the line where the ntoes should be when played
    play_line_image = pygame.image.load("assets/images/backgrounds/play_line.png").convert()
    play_line_image.set_colorkey((255, 255, 255), RLEACCEL)

    # set aseprite file directory
    dirname = os.path.dirname(__file__)
    aseprite_file_directory = 'assets/animations/rjgwgMOVINGHANDTOPLAY1.aseprite'

    #guitar guy animations
    test_animation = Animation(aseprite_file_directory)
    animationmanager = AnimationManager([test_animation], screen)
    strumAnimation = Animation('assets/animations/rjgwgSTRUMMINGGUITAR1.aseprite')
    animationmanager2 = AnimationManager([strumAnimation], screen)

    example_note1 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note1.set_x_location(500)

    example_note2 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note2.set_x_location(290)
    example_note2.set_active_color()

    example_note3 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note3.set_x_location(210)
    example_note3.set_played_color()

    example_note4 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=3, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note4.set_x_location(210)
    example_note4.set_missed_color()

    example_note5 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=1, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note5.set_x_location(500)
    example_note5.set_active_color()

    example_note6 = note.Note(text="0", midi=55, time_to_next_note=1, tab_line=6, Screen_Width=SCREEN_WIDTH, Screen_Height=SCREEN_HEIGHT, id=0)
    example_note6.set_x_location(500)
    example_note6.set_active_color()

    complete_tutorial_button = text_button.TextButton(text=" Complete ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    

    curr_tutorial_info = tutorial_info.TutorialInfo(
         popup_list = [
            #   1
              tutorial_popup.TutorialPopup("Welcome to the Playing Notes tutorial! Press the next button on screen or use the arrow keys to navigate", left_padding=10, top_padding=20),
             #   2
              tutorial_popup.TutorialPopup("In this game, notes, like this will glide across the screen and you'll need to play them once they change to blue", left_padding=100, top_padding=20, show_hightlight_region=True, highlight_region_position=example_note1.rect),
            #   3
              tutorial_popup.TutorialPopup("When they change to Blue they'll look like this", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note2.rect),
             #   4
              tutorial_popup.TutorialPopup("If you play them correctly they'll change to Green", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note3.rect),
             #   5
              tutorial_popup.TutorialPopup("But if you play them incorrectly they'll change to Red", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note4.rect),
            #   6
              tutorial_popup.TutorialPopup("We are using tab notation to represent notes. So a note on the top line here would be played on the bottom string.", left_padding=10, top_padding=20, show_hightlight_region=True, highlight_region_position=example_note5.rect),
            #   7
              tutorial_popup.TutorialPopup("While a note on the bottom line here would be played on the top string.", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note6.rect),
            #   8
              tutorial_popup.TutorialPopup("The fret of the note is represented by its number", left_padding=10, top_padding=250, show_hightlight_region=True, highlight_region_position=example_note6.rect),
            
            
            # END
            tutorial_popup.TutorialPopup("Press complete to finish the tutorial", top_padding= 220, left_padding= 20, trigger_effect_number=1,),


              ],
         sprites_list = [
            # 1
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   
                   ],
                   # 2
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note1.surf, location=example_note1.rect),
                   
                   ],
                   # 3
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note2.surf, location=example_note2.rect),
                   
                   ],
                   # 4
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note3.surf, location=example_note3.rect),
                   
                   ],
                   # 5
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note4.surf, location=example_note4.rect),
                   
                   ],
                #    6
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note5.surf, location=example_note5.rect),
                   
                   ],
                #    7
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note6.surf, location=example_note6.rect),
                   
                   ],
                    #    8
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite = tabs_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite = play_line_image, location = (0,0)),
                   sprite_item.SpriteItem(sprite= example_note6.surf, location=example_note6.rect),
                   
                   ],

                   # END
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   sprite_item.SpriteItem(sprite= complete_tutorial_button.render, location=complete_tutorial_button.button_position)
                   ],


              

            
         ],
    )


    # END/////////

    current_popup = curr_tutorial_info.current_popup

   
    current_sprites = curr_tutorial_info.current_sprites

    
    
    


    # The main loop
    while running:

        # PAUSED LOOP
        if paused == True:
              
            for event in pygame.event.get():

                # Did the user hit a key?
                if event.type == KEYDOWN:

                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        paused = False
                        

                    # Did the user click the window close button? If so, exit
                    elif event.type == QUIT:
                        exit()


                 # Here we check for hover events 
                if event.type==pygame.MOUSEMOTION:
                    resume_button.on_hover()
                    restart_button.on_hover()
                    main_menu_button.on_hover()
                    quit_button.on_hover()
                # Here we check for clicks events 
                if event.type==pygame.MOUSEBUTTONDOWN:
                    # text_buttons should be pressed like this
                    if (resume_button.is_pressed() == True):
                        paused = False
                        pygame.mixer.music.unpause()
                    elif(restart_button.is_pressed() == True):
                        restart_level = True
                        running = False
                    elif(main_menu_button.is_pressed() == True):
                        running = False
                    elif(quit_button.is_pressed() == True):
                        exit()



            if(not pauserendered):
                    s = pygame.Surface((SCREEN_WIDTH/2,3*SCREEN_HEIGHT/4)) 
                    s.set_alpha(140)                
                    s.fill((239,159,20))           
                    screen.blit(s, (SCREEN_WIDTH/4,SCREEN_HEIGHT/8))
                    pauserendered=True

            #border around entire pause menu
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(SCREEN_WIDTH/4,SCREEN_HEIGHT/8,SCREEN_WIDTH/2,3*SCREEN_HEIGHT/4),5)  
            # This visually updates the buttons on the pause screen and draws borders around them on render
            screen.blit(pause_title.render, pause_title.button_position)  
            pygame.draw.rect(screen,(0,0,0),pause_title.button_position,3)  
            screen.blit(resume_button.render, resume_button.button_position)
            pygame.draw.rect(screen,(255,255,255),resume_button.button_position,2)
            screen.blit(restart_button.render, restart_button.button_position)
            pygame.draw.rect(screen,(255,255,255),restart_button.button_position,2)
            screen.blit(main_menu_button.render, main_menu_button.button_position)
            pygame.draw.rect(screen,(255,255,255),main_menu_button.button_position,2)
            
            screen.blit(quit_button.render, quit_button.button_position)
            pygame.draw.rect(screen,(255,255,255),quit_button.button_position,2)

            pygame.display.update()
            clock.tick_busy_loop(30)
        

        # NON-PAUSED LOOP

        else:

            for event in pygame.event.get():

                            # Did the user hit a key?
                            if event.type == KEYDOWN:

                                # Was it the Escape key? If so, stop the loop
                                if event.key == K_ESCAPE:
                                    paused = True
                                    pauserendered = False
                                    print("paused the game")

                                elif event.key == K_RIGHT:
                                     
                                     # TODO Add custom next code here
                                    # START/////////
                                    if current_popup.trigger_effect_number == 1:
                                        print("Trigger effect 1")

                                    # END/////////
                                    curr_tutorial_info.next()
                                    

                                elif event.key == K_LEFT:
                                    # TODO Add custom previous code here
                                    # START/////////

                                    # END/////////
                                    curr_tutorial_info.previous()

                            # Did the user click the window close button? If so, exit
                            elif event.type == QUIT:
                                exit()

                            # Here we check for hover events 
                            if event.type==pygame.MOUSEMOTION:
                                current_popup.button_on_hover()

                                # TODO Add the hover effects for this tutorials example buttons
                                # START/////////
                                
                                complete_tutorial_button.on_hover()
                                # END/////////
                                
                        

                            # Here we check for clicks events 
                            if event.type==pygame.MOUSEBUTTONDOWN:

                                # text_buttons should be pressed like this
                                if (current_popup.button_is_pressed() == True):
                                    print("Current popup pressed")
                                    curr_tutorial_info.next()

                                    # TODO Add custom next code here
                                    # START/////////

                                    if current_popup.trigger_effect_number == 1:
                                        print("Trigger effect 1")

                                    # END/////////


                                 # TODO Add the click effects for this tutorials example buttons
                                    # START/////////
                                        # you should make certain you're on the correct screen before allowing the button to be pressed

                                

                                if (current_popup.trigger_effect_number == 1):
                                    if (complete_tutorial_button.is_pressed() == True):
                                        running = False
                                # END/////////


            current_popup = curr_tutorial_info.current_popup
            current_sprites = curr_tutorial_info.current_sprites

            
            for curr_sprite_item in current_sprites:
                if curr_sprite_item.is_box == True:
                    # If the current sprite is a box

                    if curr_sprite_item.box_has_border == True:
                        #  If the box does have a border
                        pygame.draw.rect(screen,curr_sprite_item.box_color,curr_sprite_item.box_rect, curr_sprite_item.box_border)
                    else:
                        # If the box has no border
                        pygame.draw.rect(screen,curr_sprite_item.box_color,curr_sprite_item.box_rect)
                else:
                    # If the current sprite is not a box
                    screen.blit(curr_sprite_item.sprite, curr_sprite_item.location)


            # TODO This is the animation of the player
            animationmanager2.update_self(30, 390)

            pygame.draw.rect(screen,current_popup.outline_color,current_popup.outline_position)

            screen.blit(current_popup.line1_render, current_popup.line1_position)
            screen.blit(current_popup.line2_render, current_popup.line2_position)
            screen.blit(current_popup.line3_render, current_popup.line3_position)
            screen.blit(current_popup.line4_render, current_popup.line4_position)
            screen.blit(current_popup.line5_render, current_popup.line5_position)

            screen.blit(current_popup.number_render, current_popup.number_position)

            screen.blit(current_popup.button_render, current_popup.button_position)

            if (current_popup.show_hightlight_region == True):
                pygame.draw.rect(screen,current_popup.highlight_region_color,current_popup.highlight_region_position.scale_by(1.4), 5)

            


            pygame.display.update()
            clock.tick_busy_loop(30)





    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    

    # If the level should be restarted the restart it
    if restart_level == True:
        start()

