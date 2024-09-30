#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Fractals
# Copyright (C) 2024 Vaibhav Sangwan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Vaibhav Sangwan    sangwanvaibhav02@gmail.com

from gettext import gettext as _

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pygame
pygame.init()

from gamestatemanager import GameStateManager
from states.simulator import Simulator
from states.mainmenu import MainMenu
from states.helpmenu import HelpMenu

FPS = 30


class Fractals:
    def __init__(self):
        pygame.display.set_caption(_("Fractals"))
        self.clock = pygame.time.Clock()

    def fill_bg(self):
        self.screen.fill("white")

    def run(self):
        self.screen = pygame.display.set_mode((0, 0))

        self.gameStateManager = GameStateManager("main-menu")
        self.states = {}
        self.states["simulator"] = Simulator(self)
        self.states["main-menu"] = MainMenu(self)
        self.states["help-menu"] = HelpMenu(self)

        self.is_running = True
        while self.is_running:
            curr_state = self.states[self.gameStateManager.get_state()]

            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                curr_state.handle_event(event)

            self.fill_bg()
            curr_state.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    g = Fractals()
    g.run()
