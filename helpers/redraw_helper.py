import pygame

def redraw(widget, decos,color):
    decos.add_rect(-widget.get_width()/2,-widget.get_height()/2+1,pygame.Rect(0,0 , widget.get_width(),widget.get_height()),color)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,-widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(-widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,color,True)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,color,True)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,color,True)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,color,True)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)