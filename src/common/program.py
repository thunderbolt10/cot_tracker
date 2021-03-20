__author__ = 'alang'

print(__name__)

import os
from re import template
import sys
import inspect

def is_frozen():
    if getattr(sys, "frozen", False):
        return True
    return False

def get_base_dir(sub_path=None):
    out_dir = ''
    if sub_path is None:
        folder = '.'
    else:
        folder = os.path.join('.', sub_path)

    if is_frozen():
        # If this is running in the context of a frozen (executable) file,
        # we return the path of the main application executable
        this_dir = os.path.join(os.path.dirname(os.path.abspath(sys.executable)),'..')
        # When frozen the shared resource files (settings, certificates etc) are located up one level (parent folder)

        if sub_path:
            out_dir = os.path.abspath(os.path.join(this_dir, sub_path))
        else:
            out_dif = this_dir

    else:
        this_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        this_dir = os.path.abspath(os.path.join(this_dir, '../..'))
        
        if sub_path:
            out_dir = os.path.abspath(os.path.join(this_dir, sub_path))
        else:
            out_dir = this_dir

    return out_dir


def get_bin_dir(sub_path):
    if is_frozen():
        # If this is running in the context of a frozen (executable) file,
        # we return the path of the main application executable
        this_dir = os.path.dirname(os.path.abspath(sys.executable))
        # When frozen the shared resource files (settings, certificates etc) are located up one level (parent folder)
        out_dir = os.path.abspath(os.path.join(this_dir, sub_path))
        return out_dir

    else:
        this_dir = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '..')
        out_dir = os.path.abspath(os.path.join(this_dir, sub_path))
        return out_dir

def get_local_dir(folder):
    if getattr(sys, "frozen", False):
        outdir = os.path.join(sys._MEIPASS, folder)
    else:
        outdir = get_bin_dir(folder)

    return outdir

template_path = get_bin_dir('')

def set_template_path(tmpl_base_path):
    global template_path 
    template_path = tmpl_base_path

def get_template(template_filename):
    return '%s//%s' % (template_path, template_filename)
