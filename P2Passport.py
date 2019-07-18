#!/usr/bin/env python
# Project Started By Jahidul Aka A29.
from __future__ import division
from gimpfu import *

def newPaper(name, w=2480, h=3508):
        image = pdb.gimp_image_new(w, h, RGB)
        pdb.gimp_image_set_filename(image, name)
        layer = pdb.gimp_layer_new(image, w, h, RGB_IMAGE, "Background", 100, LAYER_MODE_NORMAL_LEGACY)
        pdb.gimp_image_add_layer(image, layer, 1)
        drawable = pdb.gimp_image_get_active_drawable(image)
        pdb.gimp_display_new(image)
        pdb.gimp_edit_fill(drawable, FILL_WHITE)
        pdb.gimp_item_set_lock_position(drawable, True)
        return image



def getPaper(name, w=2480, h=3508):
        ls = gimp.image_list()
        for i in ls:
                if i.name == name:
                        return i
        return newPaper(name, w, h)

def fromMM(mm):
        if mm > 0:
                return (mm / 25.4 ) * 300

def arrange(paper, w, b):
        x = fromMM(b)
        y = fromMM(b)
        for l in  paper.layers:
                if(l.name != "Background"):
                        if( x + l.width < w-fromMM(b)):
                                l.set_offsets(int(x),int(y))
                                x+= l.width+fromMM(1)
                        else:
                                x = fromMM(b)
                                y += l.height+fromMM(1)
                                l.set_offsets(int(x),int(y))
                                x+= l.width+fromMM(1)
                                

def stroke(image):
        drawable = pdb.gimp_image_active_drawable(image)
        pdb.gimp_image_select_item(image, CHANNEL_OP_ADD, drawable)

        #Stroke Configere.
        pdb.gimp_context_set_stroke_method(STROKE_LINE)
        pdb.gimp_context_set_opacity(100)
        pdb.gimp_context_set_foreground((0,0,0))
        pdb.gimp_context_set_line_width(6)
        
        #pdb.gimp_drawable_edit_stroke_item(drawable, drawable)
        #pdb.gimp_selection_border(image, 3)        
        pdb.gimp_edit_stroke(drawable)
        #pdb.gimp_drawable_fill(drawable, FILL_FOREGROUND)
        #pdb.gimp_image_select_rectangle(image, CHANNEL_OP_ADD, 3, 3, image.width-3, image.height-3)
        #pdb.gimp_selection_border(image, 3)
        # Deselect.
        pdb.gimp_selection_none(image)

        


def Start(img, layer, qnty, size, side):
        #pdb.gimp_message(str(side))
        #stroke(img)
        pdb.gimp_edit_copy_visible(img)
        paper = getPaper("A4")
        drawable = pdb.gimp_image_get_active_drawable(paper)
        layer_new = pdb.gimp_edit_paste(drawable, False)
        pdb.gimp_floating_sel_to_layer(layer_new)
        #pdb.gimp_layer_copy(layer_new, False)        
        if(side == 0):
                ratio = pdb.gimp_drawable_height(layer_new)/pdb.gimp_drawable_width(layer_new)
                pdb.gimp_layer_scale(layer_new, fromMM(size), int(ratio*fromMM(size)) , True)
        else:
                ratio = pdb.gimp_drawable_width(layer_new)/pdb.gimp_drawable_height(layer_new)
                pdb.gimp_layer_scale(layer_new, int(ratio*fromMM(size)), fromMM(size) , True)

        stroke(paper)
                

        for i in range(int(qnty-1)):
                pdb.gimp_image_add_layer(paper, layer_new.copy(), 1)

        arrange(paper, 2480, 3)
        
        
        
        
        

register(
	"python_fu_PreparePhoto",
	"A29",
	"Prepare Passport Photo For Print.",
	"Jahid",
	"Open source (BSD 3-clause license)",
	"2018",
	"<Image>/Image/PreparePhoto",
	"*",
	[(PF_SPINNER, "qnty", "Num Of Copy", 3, (1, 3000, 1)),
         (PF_SPINNER, "size", "Size", 27, (1, 3000, 1)),
         (PF_RADIO, "side", "Set Desauration mode: ", DESATURATE_LIGHTNESS,
            (
                 ("Width", DESATURATE_LIGHTNESS),
                 ( "Height", DESATURATE_LUMINOSITY)
            )
         )
         ],
	[],
	Start)

main()
