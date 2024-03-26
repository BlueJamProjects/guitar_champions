import pygame

import helpers.redraw_helper as redraw_helper

def draw_update_function(widget, menu):
        color=[0,0,0]
        widget.set_margin(0,50)
        if (widget.is_selected()):
            color=[239,159,20]
            widget.set_font_shadow(True,(0,0,0),None,1)
            widget.shadow(shadow_type='rectangular', shadow_width=20, corner_radius=0, color=(0, 0, 0), aa_amount=4)
            widget.set_padding(3*(abs(pygame.time.get_ticks() % 2000-1000)/500))
            style={
                "color": (255,255,255),
                "antialias": True
            }
        else:
            widget.set_font_shadow(False,(0,0,0),None,1)
            color=[255,187,68]
            widget.shadow(shadow_type='rectangular', shadow_width=0, corner_radius=0, color=(0, 0, 0), aa_amount=4)
            widget.set_padding(4)
            style={
                "color": (0,0,0),
                "antialias": True
            }
        widget.get_decorator().remove_all()
        redraw_helper.redraw(widget,widget.get_decorator(),color)
        widget.update_font(style)