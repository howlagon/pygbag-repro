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

pygame.init()

window = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((800, 700))

pause_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 275), (100, 50)),
    text='Pause',
    manager=manager
)

paused = False

status = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((350, 325), (100, 50)),
    text='Status: ?',
    manager=manager
)

async def main():
    while True:
        delta = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pause_button:
                        global paused
                        paused = not paused
                        pause_button.set_text('Resume' if paused else 'Pause')
                        if paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
            manager.process_events(event)
        manager.update(delta)
        window.fill((255, 255, 255))
        manager.draw_ui(window)
        status.set_text(f'Busy: {pygame.mixer.music.get_busy()}')
        if not pygame.mixer.music.get_busy() and not paused:
            pygame.mixer.music.load('Menu_Ambiance.ogg')
            pygame.mixer.music.play()
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
