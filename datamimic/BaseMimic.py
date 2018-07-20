###############################################################################
# Project: Data Mimic
# Purpose: Base class to encapsulate default mimic behaviour
# Author:  Paul M. Breen
# Date:    2018-06-24
###############################################################################

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from PIL import Image
import numpy as np

class BaseMimic(object):
    def __init__(self, id):
        self.id = id
        self.bg = None
        self.fig = None
        self.ax = None
        self.objects = []
        self.patches = []
        self.variables = {}

    def get_id(self):
        return self.id

    def init(self, figsize=(16,8), bg_image=None, objects=[],
             design_mode=False):
        """
        Initialise the mimic

        :returns: The mimic figure
        """

        self.objects = objects
        self.collect_variables_from_objects()

        self.setup_figure(figsize)

        if bg_image:
            self.setup_bg(bg_image)

        if design_mode:
            self.setup_design_mode()

        return self.fig

    def setup_figure(self, figsize):

        self.fig, self.ax = plt.subplots(figsize=figsize)

        plt.axis('equal')
        plt.axis('off')
        self.ax.axis('off')
        plt.tight_layout()

        return self.fig

    def setup_bg(self, bg_image):

        self.bg = np.array(Image.open(bg_image), dtype=np.uint8)
        self.ax.imshow(self.bg)

    def setup_design_mode(self, grid_on=True, tick_spacing=50):

        self.ax.grid(b=grid_on)
        self.ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
        self.ax.yaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))

    def collect_variables_from_objects(self):
        """
        Collect all dynamic variables from the mimic objects
        """

        for o in self.objects:
            try:
                for item_map_name in o['dynamics']:
                    item_map = o['dynamics'][item_map_name]
                    var_name = item_map['state']
                    self.variables[var_name] = None
            except KeyError:
                pass

    def get_data(self):
        """
        Get the data for all variables
        """

        for name in self.variables:
            value = self.get_variable(name)
            self.variables[name] = value

    def get_variable(self, name):
        """
        Get the data for the given variable
        """

        pass

    def update(self):
        """
        Update the mimic

        :returns: The mimic figure
        """

        self.remove_patches()
        self.get_data()
        self.add_patches()

        return self.fig

    def add_patches(self):
        """
        Add the patches of the mimic
        """

        # Add patches for the configured drawing objects
        for o in self.objects:
            layout = self.compute_layout(o['layout'])
            options = self.compute_options(o['options'], o['dynamics'])

            if o['type'] == "rectangle":
                self.add_rectangle(*layout, **options)
            elif o['type'] == "line2d":
                self.add_line2d(*layout, **options)
            elif o['type'] == "text_box":
                text = self.compute_text(o['text'], o['dynamics'])
                label = self.create_text_label(**text)
                self.add_text_box(*layout, label, **options)

    def remove_patches(self):
        """
        Remove the patches of the mimic
        """

        for p in self.patches:
            p.remove()

        self.patches = []

    def add_text(self, xy, text, ha='left', family='sans-serif', size=14):
        """
        Add text to the mimic

        See matplotlib.pyplot.text() for details
        """

        text = plt.text(xy[0], xy[1], text, ha=ha, family=family, size=size)
        self.patches.append(text)

    def add_rectangle(self, *args, **kwargs):
        """
        Add a rectangle to the mimic

        See matplotlib.patches.Rectangle() for details
        """

        rect = mpatches.Rectangle(*args, **kwargs)
        self.patches.append(rect)
        self.ax.add_patch(rect)

    def add_line2d(self, *args, **kwargs):
        """
        Add a 2D line to the mimic

        See matplotlib.lines.Line2D() for details
        """

        line = mlines.Line2D(*args, **kwargs)
        self.patches.append(line)
        self.ax.add_line(line)

    def add_text_box(self, xy, width, height, text,
                     box_options={'ec': 'b', 'fc': 'none', 'alpha': 0.5},
                     text_options={},
                     layout_options={'x_offset': 5, 'y_offset': 14}):
        """
        Add text surrounded by a box to the mimic

        N.B.: The text_options default to those of add_text()
        """

        self.add_rectangle(xy, width, height, **box_options)

        x_offset = 5
        y_offset = 14

        try:
            x_offset = layout_options['x_offset']
            y_offset = layout_options['y_offset']
        except KeyError:
            pass

        xy_offset = (xy[0] + x_offset, xy[1] + y_offset)
        self.add_text((xy_offset[0], xy_offset[1]), text, **text_options)

    def create_text_label(self, prefix="", infix="", postfix=""):
        return '{}{}{}'.format(prefix, infix, postfix)

    def compute_layout(self, layout):
        return layout

    def compute_options(self, options, dynamics):
        for key in ['alpha', 'color']:
            item = self.get_computed_item(key, dynamics)

            if item is not None:
                options.update({key: item})

        return options

    def compute_text(self, text, dynamics):
        for key in ['prefix', 'infix', 'postfix']:
            item = self.get_computed_item(key, dynamics)

            if item is not None:
                text.update({key: item})

        return text

    def get_computed_item(self, item_map_name, dynamics):
        item = None

        try:
            item_map = dynamics[item_map_name]
            var_name = item_map['state']
            var_value = self.variables[var_name]

            for transform in item_map['transforms']:
                item = self.transform_item(var_value, transform)

                if item is not None:
                    break

            if item is None:
                item = item_map['default']
        except KeyError:
            pass

        return item

    def transform_item(self, state, transform):
        item = None
        t_in = transform['in']
        t_out = transform['out']

        # If the transform output is configured as 'null', then it takes the
        # value of the state variable
        if t_out is None:
            t_out = state

        if isinstance(t_in, (list, tuple)):
            if t_in[0] <= state <= t_in[1]:
                item = t_out
        elif state == t_in:
                item = t_out

        return item

