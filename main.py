#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pygame-ce",
#   "python-i18n",
#   "pygame-gui"
# ]
# ///

import pygame
import asyncio
from pygame_gui.core.utility import get_default_manager

from debug_menu import debugConsole
from screen import load_manager
from manager import MANAGER

pygame.init()

window = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()
if MANAGER is None:
    MANAGER = load_manager(res=(800, 700), screen_offset=(0, 0), scale=1)

debug_console = debugConsole(pygame.rect.Rect(0, 0, 800, 700), MANAGER)

async def main():
    while True:
        window.fill((255, 255, 255))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
