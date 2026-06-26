#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# export-image.py  —  GIMP 3.x Python plug-in
#
# Registers a procedure "python-fu-export-image" that accepts one
# argument (a file-path string) and exports the current image to
# that path.  The output format is determined by the file extension
# (e.g. .png, .jpg, .webp, .tiff …).
#
# Menu location: Filters > Export > Export Image to Path

import sys
import os

import gi
gi.require_version('Gimp',   '3.0')
gi.require_version('GimpUi', '3.0')
from gi.repository import Gimp, GimpUi, GLib, Gio, GObject


# ── plug-in entry point ────────────────────────────────────────────────────

def export_image(procedure, run_mode, image, drawables, config, run_data):
    """
    Export *image* to the file path stored in the procedure config.

    Parameters injected by GIMP
    ---------------------------
    procedure  : Gimp.Procedure  — this procedure object
    run_mode   : Gimp.RunMode    — INTERACTIVE or NONINTERACTIVE
    image      : Gimp.Image      — the current image
    drawables  : list[Gimp.Drawable]
    config     : Gimp.ProcedureConfig — holds our registered arguments
    run_data   : object          — user data (None here)
    """

    # ── 1. Retrieve the output path from the procedure's config ────────────
    out_path = config.get_property("output-path")

    if not out_path:
        return procedure.new_return_values(
            Gimp.PDBStatusType.CALLING_ERROR,
            GLib.Error("export-image", 0,
                        "output-path must not be empty."))

    # Normalise to forward slashes (safe on all platforms incl. Windows)
    out_path = out_path.replace("\\", "/")

    # ── 2. Flatten the image so every layer is merged into one drawable ────
    #       (required by most export formats; comment out if you want layers)
    flat_image = image.duplicate()          # work on a copy
    flat_image.flatten()                    # merge all layers
    drawable   = flat_image.get_active_drawable()

    # ── 3. Build a Gio.File for the destination path ───────────────────────
    dest_file = Gio.File.new_for_path(out_path)

    # ── 4. Export via the GIMP PDB "file-overwrite" procedure ─────────────
    #       This writes the file in whichever format the extension implies.
    pdb       = Gimp.get_pdb()
    proc      = pdb.lookup_procedure("gimp-file-overwrite")
    proc_cfg  = proc.create_config()

    proc_cfg.set_property("run-mode",  Gimp.RunMode.NONINTERACTIVE)
    proc_cfg.set_property("image",     flat_image)
    proc_cfg.set_property("drawable",  drawable)
    proc_cfg.set_property("file",      dest_file)

    result = proc.run(proc_cfg)
    status = result.index(0)

    # Clean up the duplicate
    flat_image.delete()

    if status != Gimp.PDBStatusType.SUCCESS:
        return procedure.new_return_values(
            Gimp.PDBStatusType.EXECUTION_ERROR,
            GLib.Error("export-image", 0,
                        f"Export failed for path: {out_path}"))

    Gimp.message(f"Image exported to: {out_path}")
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS,
                                       GLib.Error())


# ── plug-in class ──────────────────────────────────────────────────────────

class ExportImagePlugin(Gimp.PlugIn):

    # 1. Tell GIMP which procedure names this plug-in provides
    def do_query_procedures(self):
        return ["python-fu-export-image"]

    # 2. Opt out of i18n (change to True + supply a .mo file if you need it)
    def do_set_i18n(self, name):
        return False
    Gimp.message("After i18n call")
    
    # 3. Describe the procedure to GIMP
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            export_image,   # the run function defined above
            None            # run_data
        )

        # Works with any image type
        procedure.set_image_types("*")

        # Where it appears in the menu
        procedure.set_menu_label("Export Image to Path")
        procedure.add_menu_path("<Image>/Filters/Export/")

        # Short + long documentation
        procedure.set_documentation(
            "Export the current image to a specified file path",
            "Flattens the image and exports it to the given path. "
            "The file format is determined by the extension "
            "(.png, .jpg, .webp, .tiff, …).",
            name
        )
        procedure.set_attribution("Your Name", "Your Name", "2024")

        # ── Register our one custom argument ──────────────────────────────
        procedure.add_string_argument(
            "output-path",          # property name (used in get_property)
            "Output File Path",     # label shown in dialogs
            "Full path to the file to write, e.g. /home/user/out.png",
            "",                     # default value
            GObject.ParamFlags.READWRITE
        )

        return procedure


# ── boilerplate: hand control to GIMP ─────────────────────────────────────

Gimp.main(ExportImagePlugin.__gtype__, sys.argv)