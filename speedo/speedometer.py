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
                 ax=None):

        self.ax = ax or plt.gca()

        self.radius = radius
        self.center = center
        self.start_value = start_value
        self.end_value = end_value
        self.value = value
        self.width_ratio = width_ratio
        self.start_angle = start_angle
        self.end_angle = end_angle

        self.snap_to_pos = snap_to_pos

        if arc_edgecolor is None:
            self.arc_edgecolor = self.ax.get_facecolor()
        else:
            self.arc_edgecolor = arc_edgecolor

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

        self.annotation_text = annotation_text

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
        self.midpoint_values = np.linspace(self.start_value, self.end_value, segments_per_color*self.n_colors, endpoint=True)
        self.edge_values = np.linspace(self.start_value, self.end_value, segments_per_color*self.n_colors+1, endpoint=True)

        self.arrow_index = np.argmin(abs(self.midpoint_values - self.value))
        self.arrow_value = self.midpoint_values[self.arrow_index]

        if labels is None:
            self.labels = ['' for i in range(len(self.colors)+1)]
            for i, l in zip(range(0, segments_per_color*self.n_colors+1, segments_per_color),
                            np.linspace(self.start_value, self.end_value, self.n_colors+1, endpoint=True)):
                self.labels[i] = l

        else:
            self.labels = labels

        N = len(self.colors)

        self.angle_range, self.midpoints = degree_range(N, start=start_angle, end=end_angle)
        self.annotation_angles = np.concatenate([self.angle_range[:, 0], self.angle_range[-1:, 1]])

        # Speedometer Patches
        self.patches = []
        for ang, c, val in zip(self.angle_range, self.colors, self.edge_values[-2::-1]): # self.midpoint_values[-1::-1]
            if self.arrow_value <= val:
                alpha = self.fade_alpha
                hatch = self.fade_hatch
            else:
                alpha = 1
                hatch = None

            # Wedges
            self.patches.append(Wedge(self.center, self.radius, *ang, width=self.width_ratio*self.radius,
                                      facecolor=c, edgecolor=self.arc_edgecolor, lw=self.patch_lw, alpha=alpha, hatch=hatch))
            # Wedges with just an edgecolor (alpha edgecolor issues)
            self.patches.append(Wedge(self.center, self.radius, *ang, width=self.width_ratio*self.radius, facecolor='None', edgecolor=self.arc_edgecolor, lw=patch_lw))

        [self.ax.add_patch(p) for p in self.patches]

        if draw_labels:
            for angle, label in zip(self.annotation_angles, self.labels[-1::-1]):
                if rotate_labels:
                    radius_factor = 0.625
                    if angle < 90:
                        adj = 90
                    else:
                        adj = -90
                else:
                    radius_factor = 0.65
                    if (angle < 0) | (angle > 180):
                        adj = 180
                    else:
                        adj = 0

                if type(label) == int:
                    if label[-2:] == '.0':
                        label = label[:-2]

                self.ax.text(self.center[0] + radius_factor * self.radius * np.cos(np.radians(angle)),
                             self.center[1] + radius_factor * self.radius * np.sin(np.radians(angle)),
                             label, horizontalalignment='center', verticalalignment='center', fontsize=label_fontsize,
                             fontweight='bold', color=self.label_fontcolor, rotation=rotate(angle) + adj,
                             bbox={'facecolor': self.arc_edgecolor, 'ec': 'None', 'pad': 0},
                             zorder=10)

        self.set_arrow_angle()

        self.arrow = self.ax.arrow(*self.center,
                                   .825 * self.radius * np.cos(np.radians(self.arrow_angle)),
                                   .825 * self.radius * np.sin(np.radians(self.arrow_angle)),
                                   width=self.radius/20, head_width=self.radius/10, head_length=self.radius/15,
                                   fc=self.ax.get_facecolor(), ec=self.label_fontcolor, zorder=9, lw=2)

        self.ax.add_patch(Circle(self.center, radius=self.radius/20, facecolor=self.ax.get_facecolor(), edgecolor=self.label_fontcolor, lw=2.5, zorder=10))

        self.set_annotation_text()

        # Bottom Annotation
        self.annotation = self.ax.text(self.center[0], self.center[1] - self.annotation_offset * self.radius, self.annotation_text, horizontalalignment='center',
                                       verticalalignment='center', fontsize=self.annotation_fontsize, fontweight='bold', color=self.annotation_fontcolor,
                                       bbox={'facecolor': self.annotation_facecolor, 'edgecolor': self.annotation_edgecolor, 'pad': self.annotation_pad},
                                       zorder=11, visible=False)

        if draw_annotation:
            self.annotation.set_visible(True)

        # Title Annotation
        if title is not None:

            self.title_annotation = self.ax.text(self.center[0], self.center[1] + self.title_offset * self.radius, self.title, horizontalalignment='center',
                                                 verticalalignment='center', fontsize=self.title_fontsize, fontweight='bold', color=self.title_fontcolor,
                                                 bbox={'facecolor': self.title_facecolor, 'edgecolor': self.title_edgecolor, 'pad': self.title_pad},
                                                 zorder=11)

    def set_annotation_text(self):
        if self.annotation_text is None:
            self.annotation_text = f'{self.value}{self.unit}'

    def set_arrow_angle(self):
        if self.snap_to_pos:
            self.arrow_angle = self.midpoints[-1::-1][(self.arrow_index - len(self.colors))]
        else:
            self.deg_range = self.end_angle - self.start_angle
            self.val_range = self.end_value - self.start_value
            self.arrow_angle = self.end_angle - (self.value - self.start_value) / self.val_range * self.deg_range

    def _rotate(self, arr, theta):
        """
        rotates a 2D vector by `theta` degrees in radians counterclockwise.
        """
        # Rotation Matrix R
        R = [[np.cos(theta), -np.sin(theta)], 
             [np.sin(theta),  np.cos(theta)]]

        return np.matmul(R, arr.T).T

    def update_wedges(self):
        for bool_, patch, in zip(self.edge_values < self.value,
                                 self.patches[-2::-2]):
            if bool_:
                patch.set_alpha(1)
                patch.set_hatch('')
            else:
                patch.set_alpha(self.fade_alpha)
                patch.set_hatch(self.fade_hatch)

    def update_arrow_position(self, value):

        self.value = value
        self.arrow_index = np.argmin(abs(self.midpoint_values - self.value))
        self.arrow_value = self.midpoint_values[self.arrow_index]

        old_angle = self.arrow_angle
        self.set_arrow_angle()

        rotation_degrees = self.arrow_angle - old_angle

        self.arrow.set_xy(self._rotate(self.arrow.get_xy(), np.deg2rad(rotation_degrees)))
        self.annotation.set_text(f'{self.value}{self.unit}')
        self.update_wedges()