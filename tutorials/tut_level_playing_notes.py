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


    


    complete_tutorial_button = text_button.TextButton(text=" Complete ", width= 96,height= 44, left_padding= SCREEN_WIDTH/2 - 50, top_padding= SCREEN_HEIGHT/2 - 80)
    

    curr_tutorial_info = tutorial_info.TutorialInfo(
         popup_list = [
            #   1
              tutorial_popup.TutorialPopup("Welcome to the Playing Notes tutorial! Press the next button on screen or use the arrow keys to navigate", left_padding=10, top_padding=20),
            # END
            tutorial_popup.TutorialPopup("Press complete to finish the tutorial", top_padding= 220, left_padding= 20, trigger_effect_number=1,),


              ],
         sprites_list = [
            # 1
              [
                   sprite_item.SpriteItem(sprite = bg_img, location = (0,0)),
                   
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

            pygame.draw.rect(screen,current_popup.outline_color,current_popup.outline_position)

            screen.blit(current_popup.line1_render, current_popup.line1_position)
            screen.blit(current_popup.line2_render, current_popup.line2_position)
            screen.blit(current_popup.line3_render, current_popup.line3_position)
            screen.blit(current_popup.line4_render, current_popup.line4_position)
            screen.blit(current_popup.line5_render, current_popup.line5_position)

            screen.blit(current_popup.number_render, current_popup.number_position)

            screen.blit(current_popup.button_render, current_popup.button_position)

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

