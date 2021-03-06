import colors as col
import pygame as pg
import pygame_gui as pgui
import pygame_gui.windows.ui_file_dialog as fdl
import math

window_width = 800
window_height = 800

LOADEVENT = pg.USEREVENT + 1
SAVEEVENT = pg.USEREVENT + 2

default_time_speeds = [
    1, 5, 10, 50, 100, 500, 
    1000, 5000, 10000, 50000, 100000
]

def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class InterfaceManager:
    """
    class that manages the GUI and provides user input to the program
    using get_speed method and is_running variable
    """

    def __init__(self, screen, time_speeds=default_time_speeds):
        self.screen = screen
        # this variable tells whether the simulation is running right now
        self.is_running = False

        self.manager = pgui.UIManager((window_width, window_height))

        self.init_buttons()
        self.init_time_speed(time_speeds)

        self.init_time_label()

        self.loadDialog = None
        self.saveDialog = None

    def init_buttons(self):
        buttonRect = pg.Rect(0, 0, 90, 40)

        self.startButton = self.init_button_bottomleft(buttonRect, (10, -10), 'Start')
        self.loadButton = self.init_button_bottomleft(buttonRect, (110, -10), 'Load')
        self.saveButton = self.init_button_bottomleft(buttonRect, (210, -10), 'Save')

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

    def init_time_speed(self, time_speeds):
        """
        initiates speed slider and spee display label
        """
        anchors = {'left': 'right',
                   'right': 'right',
                   'top': 'bottom',
                   'bottom': 'bottom'}
        self.time_speeds = time_speeds
        self.time_idx = 0
        buttonRect = pg.Rect(0, 0, 30, 40)

        self.speedIncreaseButton = self.init_button_bottomright(buttonRect, (-170, -10), ">")
        self.speedDecreaseButton = self.init_button_bottomright(buttonRect, (-200, -10), "<")

        labelRect = pg.Rect((0, 0, 120, 40))
        labelRect.bottomright = (-10, -10)

        self.speedLabel = pgui.elements.UILabel(labelRect, "speed: " + str(time_speeds[0]), manager=self.manager, anchors=anchors)

    def init_button_bottomright(self, rect, pos, text):
        """
        inits button in such a way that it is placed relative to the bottom right corner
        """
        buttonRect = rect.copy()
        buttonRect.bottomleft = pos
        return pgui.elements.UIButton(relative_rect=buttonRect,
                                      text=text, manager=self.manager,
                                      anchors={'left': 'right',
                                               'right': 'right',
                                               'top': 'bottom',
                                               'bottom': 'bottom'})


    def init_time_label(self):
        labelRect = pg.Rect((0, 0, 300, 40))
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
                elif event.ui_element == self.speedIncreaseButton:
                    self.increase_speed()
                elif event.ui_element == self.speedDecreaseButton:
                    self.decrease_speed()
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

    def increase_speed(self):
        if self.time_idx + 1 < len(self.time_speeds):
            self.time_idx += 1
    
    def decrease_speed(self):
        if self.time_idx > 0:
            self.time_idx -= 1

    def get_speed(self):
        return self.time_speeds[self.time_idx]

    def update_displayed_speed(self):
        self.speedLabel.set_text("speed: " + str(self.get_speed()))

    def get_time_string(self, time):
        res = ""
        minute = 60
        hour = minute*60
        day = hour*24

        if(time >= day):
            res += str(int(time//day)) + "d "
        if(time >= hour):
            res += str(int((time%day)//hour)) + "h "
        if(time >= minute):
            res += str(int((time%hour)//minute)) + "m "
        res += str(truncate(time%minute, 1)) + "s"
        return res

    def update_displayed_time(self, time):
        self.timeLabel.set_text("elapsed time: " + self.get_time_string(time))

    def update(self, time_delta, physical_time):
        self.update_displayed_speed()
        self.update_displayed_time(physical_time)
        self.manager.update(time_delta)
        self.manager.draw_ui(self.screen)

    def open_file_dialog(self, window_title, allow_existing_only):
        """
        opens a file dialog; call with allow_existing_only == True when you need to load an existing file
        """
        self.stop_simulation()
        self.disable_buttons()

        return fdl.UIFileDialog(pg.Rect(160, 50, 440, 500), self.manager,
                                window_title=window_title,
                                initial_file_path='.',
                                allow_existing_files_only=allow_existing_only)

def get_screen_x(scale, x):
    return window_width//2 + int(x*scale)

def get_screen_y(scale, y):
    return window_height//2 - int(y*scale)

def get_screen_coords(scale, coords):
    return [get_screen_x(scale, coords[0]), get_screen_y(scale, coords[1])]

def draw_objects(obj_list, scale_factor, surface):
    screen_scale = scale_factor*min(window_width, window_height)
    for obj in obj_list:
        pg.draw.circle(surface, obj.col, get_screen_coords(screen_scale, obj.coord), obj.rad)
