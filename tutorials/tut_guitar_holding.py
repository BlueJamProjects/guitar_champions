import pygame

import helpers.settings_helper as settings_helper

import helpers.tutorial_info as tutorial_info

import partials.buttons.text_button as text_button

import partials.titlecard.title_card as title_card

import partials.tutorial_popup.tutorial_popup as tutorial_popup

import helpers.sprite_item as sprite_item

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

    guitar_img = pygame.image.load('assets/images/items/Pixel-Guitar.png')

    arrow_img = pygame.image.load('assets/images/items/Arrow.png')
    arrow_left_img = pygame.transform.rotate(arrow_img, 90)
    arrow_down_img = pygame.transform.rotate(arrow_img, 180)

    player_img = pygame.image.load('assets/images/characters/npcs/pixel-art-happy-guitar-player.png')

    example_button = text_button.TextButton(text=" example ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    
    example_button2 = text_button.TextButton(text=" example ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    


    example_pause_background = pygame.Surface((SCREEN_WIDTH/2,3*SCREEN_HEIGHT/4)) 
    example_pause_background.set_alpha(140)                
    example_pause_background.fill((239,159,20))  

    complete_tutorial_button = text_button.TextButton(text=" Complete ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    

    curr_tutorial_info = tutorial_info.TutorialInfo(
         popup_list = [
            #   1
              tutorial_popup.TutorialPopup("Welcome to the How to hold a Guitar tutorial. Press the next button on screen or the right arrowkey on your keyboard to go to the next screen", top_padding= 150, left_padding= 100),
            #  2
              tutorial_popup.TutorialPopup("If you want to go back then press the left arrow key on your keyboard", top_padding= 150, left_padding= 100),
            #   3
              tutorial_popup.TutorialPopup("This is an acoustic guitar with a number of frets and strings on it", top_padding= 150, left_padding= 100,),
            #   4
              tutorial_popup.TutorialPopup("The tabs on the neck of the guitar are called Frets.", top_padding= 150, left_padding= 100, ),
            #   5
              tutorial_popup.TutorialPopup("You should see 6 strings on the guitar ordered from thick to thin strings. Thick strings play the lower notes while thin string play higher notes.", top_padding= 150, left_padding= 100,),
            #   6
              tutorial_popup.TutorialPopup("Tune your guitar using the pegs at the top of the neck. You can use a guitar tuner or there are multiple tuning apps online to help tune acoustic guitars.", top_padding= 150, left_padding= 100,),
            #   7
              tutorial_popup.TutorialPopup("Now, lean your guitar over in a comfortable position. ", top_padding= 150, left_padding= 100,),
            # 8
            tutorial_popup.TutorialPopup("For right handed users, put your left arm under the neck with your hand on the frets. Your right arm should be slung over the guitar ready to strike the strings.", top_padding= 150, left_padding= 100,),
            # 9
            tutorial_popup.TutorialPopup("To play a note, press a finger on your left hand on a string just before a certain fret making sure the string beneath your finger touches the neck of the guitar. Then, pluck that string with your other hand. ", top_padding= 150, left_padding= 100,),
            # 10
            tutorial_popup.TutorialPopup("Congrats! You are now ready to move on to the playing Notes tutorial.", top_padding= 300, left_padding= 20,  trigger_effect_number=2),


              ],
         sprites_list = [
            # 1
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                   
                   ],

                # 2
              [ 
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),

                   ],
                    # 3
                   [
            
                    sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = guitar_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                   ],
                #    4
                [
                    sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = guitar_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    sprite_item.SpriteItem(sprite = arrow_left_img, location = (SCREEN_WIDTH*2/3+83, SCREEN_HEIGHT/4+45)),
                   
                ],

                #    5
                [
                    sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = guitar_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    sprite_item.SpriteItem(sprite = arrow_img, location = (SCREEN_WIDTH*2/3+54, SCREEN_HEIGHT/4+230)),
                    
                ],

                #    6
                [
                    sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = guitar_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    sprite_item.SpriteItem(sprite = arrow_down_img, location = (SCREEN_WIDTH*2/3+54, SCREEN_HEIGHT/4-35)),
                    
                ],

                 #    7
                [
                    sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = player_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    
                ],

                 #    8
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = player_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    
                ],

                 #    9
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = player_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    
                ],

                #    10
                [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0), is_background=True),
                    sprite_item.SpriteItem(sprite = player_img, location = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT/4)),
                    sprite_item.SpriteItem(sprite = complete_tutorial_button.render, location=complete_tutorial_button.button_position),
                    
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
                        restart_level = False
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
                                example_button2.on_hover()
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
                                    if (example_button2.is_pressed() == True):
                                        curr_tutorial_info.next()

                                if (current_popup.trigger_effect_number == 2):
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
                    if curr_sprite_item.is_background == True:
                        # load tutorial box frame
                        tutframe = pygame.image.load('assets/images/backgrounds/frame.png')
                        tutframe.set_alpha(140)
                        tutframe=pygame.transform.scale(tutframe,(381,360))
                        screen.blit(tutframe,(current_popup.outline_position.x-46,current_popup.outline_position.y-70))

            pygame.draw.rect(screen,current_popup.outline_color,current_popup.outline_position)

            screen.blit(current_popup.line1_render, current_popup.line1_position)
            screen.blit(current_popup.line2_render, current_popup.line2_position)
            screen.blit(current_popup.line3_render, current_popup.line3_position)
            screen.blit(current_popup.line4_render, current_popup.line4_position)
            screen.blit(current_popup.line5_render, current_popup.line5_position)

            screen.blit(current_popup.number_render, current_popup.number_position)
            pygame.draw.rect(screen,(209,129,0),current_popup.button_position)
            screen.blit(current_popup.button_render, current_popup.button_position)
            pygame.draw.rect(screen,(255,255,255),current_popup.button_position, 2)

            if (current_popup.show_hightlight_region == True):
                pygame.draw.rect(screen,current_popup.highlight_region_color,current_popup.highlight_region_position, 5)



            pygame.display.update()
            clock.tick_busy_loop(30)





    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    

    # If the level should be restarted the restart it
    if restart_level == True:
        start()

