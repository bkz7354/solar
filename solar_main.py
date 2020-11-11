#!/usr/bin/env python3

import pygame as pg
import colors as col
import solar_vis as vis
import solar_model as physics
import solar_input as file_io

def main():
    pg.init()

    screen = pg.display.set_mode((vis.window_width, vis.window_height))
    GUI_manager = vis.InterfaceManager(screen)
    model = physics.Model([])

    clock = pg.time.Clock()
    quit_flag = False

    while not quit_flag:
        time_delta = clock.tick(60)/1000.0

        if GUI_manager.is_running:
            model.update(time_delta*GUI_manager.get_speed())

        screen.fill(col.black)
        GUI_manager.update(time_delta, model.time)
        for event in pg.event.get():
            GUI_manager.process_event(event)
            if event.type == pg.QUIT:
                quit_flag = True
            elif event.type == vis.LOADEVENT:
                model = physics.Model(file_io.load_from_file(event.file))
            elif event.type == vis.SAVEEVENT:
                file_io.save_to_file(model.get_objects(), event.file)
                
        
        pg.display.update()


if __name__ == "__main__":
    main()
