import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle
from matplotlib import cm
import matplotlib.patheffects as path_effects


def degree_range(n, start=0, end=180):
    """
    returns a tuple of an Nx2 array of start and end angles
    and the midpoints of each of those ranges
    """
    start_ = np.linspace(start, end, n+1, endpoint=True)[0:-1]
    end_ = np.linspace(start, end, n+1, endpoint=True)[1::]
    mid_points = start_ + ((end_-start_)/2.)
    return np.c_[start_, end_], mid_points


def rotate(angle):
    rotation = np.degrees(np.radians(angle) * np.pi / np.pi - np.radians(90))
    return rotation


class Speedometer:
    """
    draws a Speedometer Chart

    Args:
    center (tuple): (x, y)-Position of the center
    start_value (float): Start of the range of values plotted
    end_value (float): End of the range of values plotted
    value (float): Value the needle is pointing to
    radius (real): radius of the speedometer chart
    width_ratio (real): ratio of wedges to radius
    colors (list): list of wedge facecolors 
    segments_per_color (int) = 5: number of segments per color
    start_angle (float) = -30: start angle of the speedometer
    end_angle (float) = 210: end angle of the speedometer
    arc_edgecolor (str) = None: linecolor for the wedges
    fade_alpha (float) = 0.25: alpha of wedges that are greater than the value
    patch_lw (float) = 0.25: linewidth between wedges
    snap_to_pos (bool) = False: whether to snap to the arrow to the center of a wedge
    title (str) = None: title
    unit (str) = None: the unit of the value to annotate below the plot
    label_fontsize (int) = 7: label fontsize
    title_fontcolor (str) = None: title fontcolor
    title_facecolor (str) = None: title bbox facecolor
    title_edgecolor (str) = None: title bbox edgecolor
    title_offset (float) = 1.25: title offset above the speedometer in a factor of radius from center
    title_pad (float) = 0: title bbox padding
    title_fontsize (int) = 18: title annotation fontsize
    draw_annotation (bool) = True: whether to annotate the value below the speedometer
    annotation_text (str) = None: the text to annotate, defaults to the value
    annotation_fontcolor (str) = None: annotation fontcolor
    annotation_facecolor (str) = None: annotation bbox facecolor
    annotation_edgecolor (str) = None: annotation bbox edgecolor
    annotation_offset (float) = 0.75: annotation offset below the speedometer in a factor of radius from center
    annotation_pad (float) = 0: padding around the annotation bbox
    annotation_fontsize (int) = 16: annotation fontsize
    label_fontcolor (str) = None: label color
    draw_labels (bool) = True: whether to annotate labels
    labels (list) = None: custom labels, ie ['Slowest', 'Slow', 'Average', 'Fast', 'Fastest']
    rotate_labels (bool) = False: whether to rotate the value labels
    fade_hatch (str) = None: hatch string, ie 'xxx' for all wedges > value
    ax (matplotlib.axes._subplots object) = None: Axes to draw the speedometer onto. None defaults to plt.gca()

    """
    def __init__(self,
                 center,
                 start_value,
                 end_value,
                 value,
                 radius=4,
                 width_ratio=1/4,
                 colors=["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6"],
                 segments_per_color=5,
                 start_angle=-30,
                 end_angle=210,
                 arc_edgecolor=None,
                 fade_alpha=0.25,
                 patch_lw=0.25,
                 snap_to_pos=False,
                 title=None,
                 unit=None,
                 label_fontsize=7,
                 title_fontcolor=None,
                 title_facecolor=None,
                 title_edgecolor=None,
                 title_offset=1.5,
                 title_pad=1,
                 title_fontsize=18,
                 draw_annotation=True,
                 annotation_text=None,
                 annotation_fontcolor=None,
                 annotation_facecolor=None,
                 annotation_edgecolor=None,
                 annotation_offset=0.75,
                 annotation_pad=0,
                 annotation_fontsize=16,
                 label_fontcolor=None,
                 draw_labels=True,
                 labels=None,
                 rotate_labels=False,
                 fade_hatch=None,
                 ax=None
                 ):

        self.ax = ax or plt.gca()

        self.radius = radius
        self.center = center
        self.start_value = start_value
        self.end_value = end_value
        self.value = value
        self.width_ratio = width_ratio

        if arc_edgecolor is None:
            self.arc_edgecolor = self.ax.get_facecolor()

        self.label_fontsize = label_fontsize

        self.title = title

        if title_fontcolor is None:
            self.title_fontcolor = mpl.rcParams['axes.labelcolor']
        else:
            self.title_fontcolor = title_fontcolor

        if title_facecolor is None:
            self.title_facecolor = self.ax.get_facecolor()
        else:
            self.title_facecolor = title_facecolor

        if title_edgecolor is None:
            self.title_edgecolor = self.ax.get_facecolor()
        else:
            self.title_edgecolor = title_edgecolor

        self.title_offset = title_offset
        self.title_pad = title_pad
        self.title_fontsize = title_fontsize

        if annotation_fontcolor is None:
            self.annotation_fontcolor = mpl.rcParams['axes.labelcolor']
        else:
            self.annotation_fontcolor = annotation_fontcolor

        if annotation_facecolor is None:
            self.annotation_facecolor = self.ax.get_facecolor()
        else:
            self.annotation_facecolor = annotation_facecolor

        if annotation_edgecolor is None:
            self.annotation_edgecolor = self.ax.get_facecolor()
        else:
            self.annotation_edgecolor = annotation_edgecolor

        self.annotation_offset = annotation_offset
        self.annotation_pad = annotation_pad
        self.annotation_fontsize = annotation_fontsize

        if unit is None:
            self.unit = ''
        else:
            self.unit = unit

        if label_fontcolor is None:
            self.label_fontcolor = mpl.rcParams['axes.labelcolor']
        else:
            self.label_fontcolor = label_fontcolor

        self.fade_alpha = fade_alpha
        self.fade_hatch = fade_hatch
        self.patch_lw = patch_lw

        self.n_colors = len(colors)

        self.colors = np.repeat(colors, segments_per_color)
        self.midpoints = np.linspace(self.start_value, self.end_value, segments_per_color*self.n_colors, endpoint=True)

        arrow_index = np.argmin(abs(self.midpoints - self.value))
        self.arrow_value = self.midpoints[arrow_index]

        if labels is None:
            self.labels = np.empty_like(self.colors)
            for i, l in zip(range(0, segments_per_color*self.n_colors, segments_per_color+1),
                            np.linspace(self.start_value, self.end_value, self.n_colors, endpoint=True)):
                self.labels[i] = l

        else:
            self.labels = labels

        N = len(self.colors)

        angle_range, mid_points = degree_range(N, start=start_angle, end=end_angle)

        # Speedometer Patches
        self.patches = []
        for ang, c, val in zip(angle_range, self.colors, self.midpoints[-1::-1]):
            if self.arrow_value < val:
                alpha = self.fade_alpha
                hatch = self.fade_hatch
            else:
                alpha = 1
                hatch = None

            # Wedges
            self.patches.append(Wedge(self.center, self.radius, *ang, width=self.width_ratio*self.radius,
                                      facecolor=c, edgecolor=self.arc_edgecolor, lw=self.patch_lw, alpha=alpha, hatch=hatch))
            # Wedges with just an edgecolor (alpha edgecolor issues)
            self.patches.append(Wedge(self.center, self.radius, *ang, width=self.width_ratio*self.radius,
                                      facecolor='None', edgecolor=self.arc_edgecolor, lw=patch_lw))

        [self.ax.add_patch(p) for p in self.patches]

        if draw_labels:
            for mid, label in zip(mid_points, self.labels[-1::-1]):
                if rotate_labels:
                    radius_factor = 0.625
                    if mid < 90:
                        adj = 90
                    else:
                        adj = -90
                else:
                    radius_factor = 0.65
                    if (mid < 0) | (mid > 180):
                        adj = 180
                    else:
                        adj = 0

                if label[-2:] == '.0':
                    label = label[:-2]

                self.ax.text(self.center[0] + radius_factor * self.radius * np.cos(np.radians(mid)),
                             self.center[1] + radius_factor * self.radius * np.sin(np.radians(mid)),
                             label, horizontalalignment='center', verticalalignment='center', fontsize=label_fontsize,
                             fontweight='bold', color=self.label_fontcolor, rotation=rotate(mid) + adj,
                             bbox={'facecolor': self.arc_edgecolor, 'ec': 'None', 'pad': 0},
                             zorder=10)

        # Arrow
        if snap_to_pos:
            pos = mid_points[-1::-1][(arrow_index - N)]
        else:
            deg_range = end_angle - start_angle
            val_range = end_value - start_value
            pos = end_angle - (value - start_value) / val_range * deg_range

        self.arrow = self.ax.arrow(*self.center, .825 * self.radius * np.cos(np.radians(pos)), .825 * self.radius * np.sin(np.radians(pos)),
                                   width=self.radius/20, head_width=self.radius/10, head_length=self.radius/15,
                                   fc=self.ax.get_facecolor(), ec=self.label_fontcolor, zorder=9, lw=2)

        self.ax.add_patch(Circle(self.center, radius=self.radius/20, facecolor=self.ax.get_facecolor(), edgecolor=self.label_fontcolor, lw=2.5, zorder=10))

        if draw_annotation:
            if annotation_text is None:
                self.annotation_text = f'{self.value}{self.unit}'
            else:
                self.annotation_text = annotation_text
            # Bottom Annotation
            self.annotation = self.ax.text(self.center[0], self.center[1] - self.annotation_offset * self.radius, self.annotation_text, horizontalalignment='center',
                                           verticalalignment='center', fontsize=self.annotation_fontsize, fontweight='bold', color=self.annotation_fontcolor,
                                           bbox={'facecolor': self.annotation_facecolor, 'edgecolor': self.annotation_edgecolor, 'pad': self.annotation_pad},
                                           zorder=11)
        # Title Annotation
        if title is not None:
            self.title_annotation = self.ax.text(self.center[0], self.center[1] + self.title_offset * self.radius, self.title, horizontalalignment='center',
                                                 verticalalignment='center', fontsize=self.title_fontsize, fontweight='bold', color=self.title_fontcolor,
                                                 bbox={'facecolor': self.title_facecolor, 'edgecolor': self.title_edgecolor, 'pad': self.title_pad},
                                                 zorder=11)
