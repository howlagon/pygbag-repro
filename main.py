#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pygame-ce",
#   "python-i18n",
#   "pygame-gui"
# ]
# ///

import pygame
import pygame_gui
import asyncio
from pygame_gui.core.utility import get_default_manager

from screen import load_manager
from manager import MANAGER

pygame.init()

MANAGER = load_manager((800, 700), (0, 0), 1)
window = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()

coords_display = pygame_gui.elements.UILabel(
    pygame.Rect((0, 0), (-1, -1)),
    "(0, 0)",
    object_id=None,
)

print(f"{MANAGER=}\n" + f"{get_default_manager()=}\n" + f"{get_default_manager().ui_theme.font_dict.get_default_font()=}")
print(f"{get_default_manager().ui_theme._locale=}")
dmg = get_default_manager()
font = get_default_manager().ui_theme.ele_font_res['label'][get_default_manager().ui_theme._locale]
print(f"\n{font.font_id=}\n" + f"{font.location=}\n" + f"{font.loaded_font=}\n")

async def main():
    while True:
        window.fill((255, 255, 255))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
