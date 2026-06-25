#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
S201b_Export - GIMP Python-Fu Script
Processes and exports image with filename modifications for GIMP 3.2
"""

from gimpfu import *
import os

def S201b_Export(image, drawable):
    """
    Export image with processed filename:
    1) Remove ".MP" from filename if present
    2) Replace the dot (before extension) with "_gp."
    3) Export with quality 95
    """
    try:
        # Get the current image filename
        filename = image.filename
        
        if not filename:
            pdb.gimp_message("Error: No image filename found. Please load an image first.")
            return
        
        # Get directory and filename
        directory = os.path.dirname(filename)
        base_name = os.path.basename(filename)
        
        # Step 1: If the file name has ".MP" in the name, remove these 3 characters
        processed_name = base_name.replace(".MP", "")
        
        # Step 2: Find the . in the file name, and replace it with "_gp."
        if "." in processed_name:
            # Split from the right to get the extension
            name_parts = processed_name.rsplit(".", 1)
            if len(name_parts) == 2:
                processed_name = name_parts[0] + "_gp." + name_parts[1]
        
        # Construct new full path
        new_filename = os.path.join(directory, processed_name)
        
        # Step 3: Export the image with quality of 95
        # Get file extension
        _, ext = os.path.splitext(new_filename)
        ext = ext.lower()
        
        # Export based on file type
        if ext in ['.jpg', '.jpeg']:
            # JPEG export with quality 95
            pdb.file_jpeg_save(
                image, drawable, new_filename, new_filename,
                0.95, 0, 1, 0, 1
            )
        elif ext == '.png':
            # PNG export
            pdb.file_png_save(
                image, drawable, new_filename, new_filename,
                0, 9, 0, 0, 0, 0, 0
            )
        elif ext in ['.bmp']:
            # BMP export
            pdb.file_bmp_save(image, drawable, new_filename, new_filename)
        elif ext in ['.tif', '.tiff']:
            # TIFF export
            pdb.file_tiff_save(image, drawable, new_filename, new_filename, 0)
        else:
            # Generic export for other formats
            pdb.gimp_file_save(image, drawable, new_filename, new_filename)
        
        pdb.gimp_message(f"Image exported successfully!\nOriginal: {base_name}\nNew file: {processed_name}")
        
    except Exception as e:
        pdb.gimp_message(f"Error during export: {str(e)}")

# Register the script as a GIMP plugin
register(
    "S201b_Export",
    "S201b Export",
    "Export image with filename modifications (remove .MP, add _gp before extension, quality 95)",
    "User",
    "User",
    "2026",
    "<Image>/Filters/S201b_Export",
    "*",
    [],
    [],
    S201b_Export
)

main()