#
# Copyright (c) 2005 Canonical
# Copyright (c) 2004 Conectiva, Inc.
#
# Written by Gustavo Niemeyer <niemeyer@conectiva.com>
#
# This file is part of Smart Package Manager.
#
# Smart Package Manager is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# Smart Package Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Smart Package Manager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from smart.interface import getImagePath
from smart import *
import os
import sys

try:
    import pygtk
    pygtk.require("2.0")
    import gtk
except ImportError:
    from smart.const import DEBUG
    if sysconf.get("log-level") == DEBUG:
        import traceback
        traceback.print_exc()
    raise Error, _("System has no support for gtk python interface")

def splitted_error():
	print _("ERROR: The Smartpm package is splitted in two subpackages")
	print _(" - smartpm-core: Core of the Smart Package Manager")
	print _(" - smartpm: The GUI frontend")
	print _("It seems that you tried to run the GUI frontend which is not installed yet")
	print _("You need to install the smartpm package in order to use the GUI frontend")
	sys.exit(1)

def create(ctrl, command=None, argv=None):
    if command:
        try:
            from smart.interfaces.gtk.command import GtkCommandInterface
            return GtkCommandInterface(ctrl)
        except ImportError:
            splitted_error()
    else:
        try:
           from smart.interfaces.gtk.interactive import GtkInteractiveInterface
           return GtkInteractiveInterface(ctrl)
        except ImportError:
           splitted_error()
    
_pixbuf = {}

def getPixbuf(name):
    if name not in _pixbuf:
        filename = getImagePath(name)
        if os.path.isfile(filename):
            icon_size = sysconf.get("gtk-icon-size")
            if icon_size:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename,
                                                              icon_size,
                                                              icon_size)
            else:
                pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
            _pixbuf[name] = pixbuf
        else:
            raise Error, _("Image '%s' not found") % name
    return _pixbuf[name]

import warnings
MESSAGE = r"Class \w+ is already GObject-registered; " \
          r"Please note that classes containing any of the attributes " \
          r"__gtype_name__, __gproperties__, or __gsignals__ are now " \
          r"automatically registered."
warnings.filterwarnings("ignore", MESSAGE)


