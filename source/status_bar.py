"""
Draw a status bar
"""
import arcade

from themes.current_theme import colors


def draw_status_bar(center_x, center_y, width, height, current_value, max_value):
    """ Draw a status bar """
    arcade.draw_rectangle_filled(
        center_x, center_y, width, height, colors["status_bar_background"]
    )
    status_width = (current_value / max_value) * width
    arcade.draw_rectangle_filled(
        center_x - (width / 2 - status_width / 2),
        center_y,
        status_width,
        height,
        colors["status_bar_foreground"],
    )
