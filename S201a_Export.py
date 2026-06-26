#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

# From: https://docs.gimp.org/3.2/en/gimp-using-python-plug-in-tutorial.html
# Location: "C:\Users\jtb13\AppData\Roaming\GIMP\3.2\plug-ins\S201t_Test\S201t_Test.py"

import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi

from gi.repository import GLib
from gi.repository import Gtk


class MyFirstPlugin (Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "jb-plug-in-second-try" ]

    def do_set_i18n (self, name):
        return False
    
    # def save_as_jpeg_new_name():
    #     # Get the active image and its active layer (drawable)
    #     image = gimp.image_list()[0]
    #     drawable = image.active_drawable

    #     # Define the new filename with .jpg extension
    #     new_filename = "/path/to/new_name.jpg"

    #     # Export the image to JPEG
    #     # Parameters: image, drawable, filename, filename
    #     pdb.gimp_file_export(image, drawable, new_filename, new_filename)
    
    # # Optionally, update the image's filename property if you want subsequent saves to use this name
    # image.filename = new_filename
    
    # def export_current_to_jpeg(image, drawable):
    #     # 1. Flatten the image if it has multiple layers (JPEG doesn't support transparency)
    #     flattened_image = pdb.gimp_image_flatten(image)
    #     layer = pdb.gimp_image_get_active_layer(flattened_image)
        
    #     # 2. Define your desired path and filename
    #     file_path = "C:\\path\\to\\your\\new_image.jpg"
    #     file_path = "C:\\Users\\jtb13\\Downloads\\a.jpg"
        
    #     # 3. Export to JPEG using file-jpeg-save
    #     # Syntax: file_jpeg-save(image, drawable, filename, raw_filename, quality, smoothing, optimize, progressive, comment, subsampling, baseline, restart, dct)
    #     pdb.file_jpeg_save(
    #         flattened_image, 
    #         layer, 
    #         file_path, 
    #         file_path, 
    #         0.85,  # Quality (0.0 to 1.0)
    #         0.0,   # Smoothing
    #         1,     # Optimize
    #         1,     # Progressive
    #         "Exported via Python-Fu", # Comment
    #         0,     # Subsampling (0 = 4:4:4, 1 = 4:2:2, 2 = 4:2:0)
    #         1,     # Force baseline
    #         0,     # Restart markers
    #         1      # DCT method (0 = Integer, 1 = Fast Integer, 2 = Float)
    #     )
        
    #     # 4. Refresh GIMP displays and notify the user
    #     gimp.displays_flush()
    #     gimp.message("Image successfully exported as JPEG!")

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("S201a_Export")
        procedure.add_menu_path('<Image>/Filters/Tutorial/')

        procedure.set_documentation("My first Python plug-in tryout",
                                    "My first Python 3 plug-in for GIMP 3.0",
                                    name)
        procedure.set_attribution("S201a_Export", "S201a_Export", "2023")

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        Gimp.message("Hello world!")

        # Get the file path
        gfile = image.get_file()
        if gfile is not None:
            file_path = gfile.get_path()
        else: file_path = "Error!!!"

        # Create the Gtk Message Dialog
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Hello!"
        )
        dialog.format_secondary_text("Image: " + file_path)



        # Show and wait for user response
        dialog.run()
        dialog.destroy()

        Gimp.message("After dialog box code")

        # Gimp or gimp ?
        ximage = Gimp.get_images()[0]
        ximage = image.get_file()
        Gimp.message("After gimp reference")
        # Better way to get the active drawable (layer, mask, or channel):
        drawables = pdb.gimp_image_get_selected_drawables(ximage)
        Gimp.message("After drawables reference")
        active_drawable = drawables[0] if drawables else None
        # drawable = pdb.gimp_image_get_active_layer(ximage)
        Gimp.message("After pdb reference")
        export_current_to_jpeg(ximage, active_drawable)
        Gimp.message("After export call")

        # save_as_jpeg_new_name()
        # Gimp.message("After export call")

        # do what you want to do, then, in case of success, return:
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(MyFirstPlugin.__gtype__, sys.argv)