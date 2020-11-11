import colors as col
import pygame as pg
import pygame_gui as pgui
import pygame_gui.windows.ui_file_dialog as fdl
import math


window_width = 800
window_height = 800

LOADEVENT = pg.USEREVENT + 1
SAVEEVENT = pg.USEREVENT + 2


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

class InterfaceManager:
    """
    class that manages the GUI and provides user input to the program
    using get_speed method and is_running variable
    """
    def __init__(self, screen):
        self.screen = screen
        # this variable tells whether the simulation is running right now
        self.is_running = False

        self.manager = pgui.UIManager((window_width, window_height))

        self.init_buttons()
        self.init_slider()

        self.init_time_label()

        self.loadDialog = None
        self.saveDialog = None


    def init_buttons(self):
        buttonRect = pg.Rect(0, 0, 90, 40)

        self.startButton = self.init_button_bottomleft(buttonRect, ( 10, -10), 'Start')
        self.loadButton  = self.init_button_bottomleft(buttonRect, (110, -10), 'Load')
        self.saveButton  = self.init_button_bottomleft(buttonRect, (210, -10), 'Save')

    def init_button_bottomleft(self, rect, pos, text):
        """
        inits button in such a way that it is placed relative to the bottom left corner
        """
        buttonRect = rect.copy()
        buttonRect.bottomleft = pos
        return pgui.elements.UIButton(relative_rect=buttonRect, 
                                      text=text, manager=self.manager,
                                      anchors={'left': 'left',
                                               'right': 'left',
                                               'top': 'bottom',
                                               'bottom': 'bottom'})

    def init_slider(self):
        """
        initiates speed slider and spee display label
        """
        anchors = {'left': 'right',
                   'right': 'right',
                   'top': 'bottom',
                   'bottom': 'bottom'}
        value_range = (1, 100)
        sliderRect = pg.Rect(0, 0, 200, 40)
        sliderRect.bottomright = (-10, -10)

        self.speedSlider = pgui.elements.UIHorizontalSlider(sliderRect, start_value=1,value_range=value_range,
                                                            manager=self.manager, anchors=anchors)

        labelRect = pg.Rect((0, 0, 100, 40))
        labelRect.bottomright = (-220, -10)

        self.speedLabel = pgui.elements.UILabel(labelRect, "speed: 1", manager=self.manager, anchors=anchors)

    def init_time_label(self):
        labelRect = pg.Rect((0, 0, 200, 40))
        labelRect.topleft = (10, 10)

        self.timeLabel = pgui.elements.UILabel(labelRect, "elapsed time: 0s", manager=self.manager)


    def disable_buttons(self):
        self.startButton.disable()
        self.saveButton.disable()
        self.loadButton.disable()
        
    def enable_buttons(self):
        self.startButton.enable()
        self.saveButton.enable()
        self.loadButton.enable()

    
    def process_event(self, event):
        self.manager.process_events(event)

        if event.type == pg.USEREVENT:    
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.startButton:
                    self.toggle_simulation()
                elif event.ui_element == self.loadButton:
                    self.stop_simulation()
                    self.loadDialog = self.open_file_dialog("Load configuration file", True)
                elif event.ui_element == self.saveButton:
                    self.stop_simulation()
                    self.saveDialog = self.open_file_dialog("Save configuration to file", False)    
            if event.user_type == pgui.UI_WINDOW_CLOSE:
                self.enable_buttons()
                if event.ui_element == self.loadDialog:
                    self.loadDialog = None
                elif event.ui_element == self.saveDialog:
                    self.saveDialog = None
            if event.user_type == pgui.UI_FILE_DIALOG_PATH_PICKED:
                self.enable_buttons()
                if event.ui_element == self.loadDialog:
                    pg.event.post(pg.event.Event(LOADEVENT, {'file': event.text}))
                elif event.ui_element == self.saveDialog:
                    pg.event.post(pg.event.Event(SAVEEVENT, {'file': event.text}))

        if event.type == LOADEVENT:
            self.displayed_time = 0


    def stop_simulation(self):
        self.is_running = False
        self.startButton.set_text('Start')

    def start_simulation(self):
        self.is_running = True
        self.startButton.set_text('Stop')

    def toggle_simulation(self):
        if self.is_running:
            self.stop_simulation()
        else:
            self.start_simulation()


    def get_speed(self):
        return self.speedSlider.get_current_value()

    def update_displayed_speed(self):
        self.speedLabel.set_text("speed: " + str(self.get_speed()))
    
    def update_displayed_time(self, time):
        self.timeLabel.set_text("elapsed time: " + str(truncate(time, 1)) + "s")

    def update(self, time_delta, physical_time):
        self.update_displayed_speed()
        self.update_displayed_time(physical_time)
        self.manager.update(time_delta)
        self.manager.draw_ui(self.screen)
    
    def open_file_dialog(self, window_title, allow_existing_only):
        """
        opens a file dialog; call with allow_existing_only = True when you need to load an existing file
        """
        self.stop_simulation()
        self.disable_buttons()

        return fdl.UIFileDialog(pg.Rect(160, 50, 440, 500), self.manager,
                                    window_title=window_title,
                                    initial_file_path='.',
                                    allow_existing_files_only=allow_existing_only)
        

if __name__ == "__main__":
    print("This module is not for direct call!")
