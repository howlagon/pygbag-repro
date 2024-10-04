import pygame_gui
import pygame

class debugConsole(pygame_gui.windows.UIConsoleWindow):
    def __init__(self, rect, manager):
        super().__init__(
            rect,
            manager,
            window_title="Debug Console",
            object_id="#debug_console",
            visible=0,
        )

        # Force it to print help txt
        ev = pygame.event.Event(
            pygame_gui.UI_CONSOLE_COMMAND_ENTERED, {"command": "help"}
        )
        self.process_event(ev)