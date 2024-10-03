import os
import io
import json
import math
import pygame
import pygame_gui
import re

from math import floor
from typing import Optional, Tuple, List, Union, Dict
from pygame_gui import PackageResource
from pygame_gui.core import UIWindowStack, ObjectID
from pygame_gui.core.gui_type_hints import RectLike
from pygame_gui.core.interfaces import (
    IUIElementInterface,
    IUIManagerInterface,
    IUITooltipInterface,
)
from pygame_gui.core.resource_loaders import IResourceLoader
from pygame_gui.elements import UITooltip

from manager import MANAGER

screen_scale = 1

# classes copied from clangen scripts.game_structure.ui_manager

class UIManager(pygame_gui.UIManager):
    def __init__(
        self,
        window_resolution: Tuple[int, int],
        offset: Tuple[int, int] = None,
        screen_scale: float = 1,
        theme_path: Optional[
            Union[str, os.PathLike, io.StringIO, PackageResource, dict]
        ] = None,
        enable_live_theme_updates: bool = True,
        resource_loader: Optional[IResourceLoader] = None,
        starting_language: str = "en",
        translation_directory_paths: Optional[List[str]] = None,
    ):
        super().__init__(
            window_resolution,
            theme_path,
            enable_live_theme_updates,
            resource_loader,
            starting_language,
            translation_directory_paths,
        )
        self.offset = offset
        self.screen_scale = screen_scale

        self.root_container.kill()
        self.root_container = None
        self.root_container = UIManagerContainer(
            pygame.Rect((0, 0), self.window_resolution),
            self,
            starting_height=1,
            container=None,
            parent_element=None,
            object_id="#root_container",
            screen_scale=screen_scale,
        )
        self.root_container.set_focus_set(None)
        self.root_container.set_position(offset)

        self.ui_window_stack = None
        self.ui_window_stack = UIWindowStack(
            self.window_resolution, self.root_container
        )

    def create_tool_tip(
        self,
        text: str,
        position: Tuple[int, int],
        hover_distance: Tuple[int, int],
        parent_element: IUIElementInterface,
        object_id: ObjectID,
        *,
        wrap_width: Optional[int] = None,
        text_kwargs: Optional[Dict[str, str]] = None
    ) -> IUITooltipInterface:
        """
        Creates a tool tip ands returns it. Have hidden this away in the manager, so we can call it
        from other UI elements and create tool tips without creating cyclical import problems.

        :param text: The tool tips text, can utilise the HTML subset used in all UITextBoxes.
        :param position: The screen position to create the tool tip for.
        :param hover_distance: The distance we should hover away from our target position.
        :param parent_element: The UIElement that spawned this tool tip.
        :param object_id: the object_id of the tooltip.
        :param wrap_width: an optional width for the tool tip, will overwrite any value from the theme file.
        :param text_kwargs: a dictionary of variable arguments to pass to the translated string
                            useful when you have multiple translations that need variables inserted
                            in the middle.

        :return: A tool tip placed somewhere on the screen.
        """
        tool_tip = UITooltip(
            text,
            hover_distance,
            self,
            text_kwargs=text_kwargs,
            parent_element=parent_element,
            object_id=object_id,
            wrap_width=wrap_width,
        )
        tool_tip.find_valid_position(pygame.math.Vector2(position[0], position[1]))
        return tool_tip

    def set_offset(self, offset: Tuple[int, int]):
        """
        Sets the screen offset.

        :param offset: the offset to set
        """
        self.offset = offset
        self.root_container.set_position(offset)
        self.ui_window_stack.root_container.set_position(offset)


class UIManagerContainer(pygame_gui.core.UIContainer):
    """For exclusive use by the UIManager to ensure we blit backgrounds to the right place"""

    def __init__(
        self,
        relative_rect: RectLike,
        manager: IUIManagerInterface,
        starting_height: int,
        container,
        parent_element,
        object_id,
        screen_scale: float,
    ):
        super().__init__(
            relative_rect,
            manager,
            starting_height=starting_height,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
        )
        self.screen_scale = screen_scale

# functions copied directly from clangen scripts.game_structure.screen_settings or scripts.ui.generate_screen_scale_json

def determine_screen_scale(x, y):
    global screen_scale, screen_x, screen_y, offset, game_screen_size
    # this means screen scales in multiples of 200 x 175 which has a reasonable tradeoff for crunch
    scalex = x // 200
    scaley = y // 175
    screen_scale = min(scalex, scaley) / 4
    screen_x = 800 * screen_scale
    screen_y = 700 * screen_scale

    offset = (
        floor((x - screen_x) / 2),
        floor((y - screen_y) / 2),
    )
    game_screen_size = (screen_x, screen_y)

def _multiply_numbers_in_string(s, multiplier):
    # Function to replace matched number with the floored multiplied value
    def replace(match):
        number = float(match.group())
        multiplied = math.floor(number * multiplier)
        return str(multiplied)

    # Use regex to find all numbers in the string
    return re.sub(r"(?<![#0x])(?<![#0X])-?\b\d+\.?\d*\b", replace, s)

def _multiply_numbers(data, multiplier):
    if isinstance(data, dict):
        result = {}
        blacklist = ["prototype", "line_spacing", "colours"]
        for key, value in data.items():
            if key in blacklist:
                result[key] = value
            else:
                result[key] = _multiply_numbers(value, multiplier)
        return result
    elif isinstance(data, list):
        return [_multiply_numbers(element, multiplier) for element in data]
    elif isinstance(data, str):
        return _multiply_numbers_in_string(data, multiplier)
    return data

def generate_screen_scale(input_file, output_file, multiplier):
    with open(input_file, "r") as readfile:
        data = json.load(readfile)

    modified_data = _multiply_numbers(data, multiplier)

    if not os.path.exists(output_file):
        from pathlib import Path

        p = Path(output_file)
        os.makedirs(p.parent)
    with open(os.path.abspath(output_file), "w") as writefile:
        json.dump(modified_data, writefile, indent=4)


def load_manager(res: Tuple[int, int], screen_offset: Tuple[int, int], scale: float):
    global MANAGER
    if MANAGER is not None:
        MANAGER = None
    
    # initialize pygame_gui manager, and load themes
    manager = UIManager(
        res,
        screen_offset,
        scale,
        None,
        enable_live_theme_updates=False,
    )
    manager.add_font_paths(
        font_name="notosans",
        regular_path="fonts/NotoSans-Medium.ttf",
        bold_path="fonts/NotoSans-ExtraBold.ttf",
        italic_path="fonts/NotoSans-MediumItalic.ttf",
        bold_italic_path="fonts/NotoSans-ExtraBoldItalic.ttf",
    )
    manager.add_font_paths(
        font_name="clangen", regular_path="fonts/clangen.ttf"
    )

    generate_screen_scale(
        "theme/master_screen_scale.json",
        "theme/generated/screen_scale.json",
        screen_scale,
    )

    manager.get_theme().load_theme("theme/generated/screen_scale.json")
    # manager.get_theme().load_theme("theme/themes/dark.json")

    return manager
