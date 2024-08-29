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

import pygame

from components.menubutton import MenuButton
from components.title import Title


class MainMenu:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.logo = Title(sw/2, sh/2 - sh/3)

        self.play_button = MenuButton(sw/2, sh/2, "./assets/play-button-active.png", "./assets/play-button-inactive.png")
        self.help_button = MenuButton(sw/2, sh/2 + 100, "./assets/help-button-active.png", "./assets/help-button-inactive.png")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.check_press():
                self.gameStateManager.set_state("simulator")
            if self.help_button.check_press():
                self.gameStateManager.set_state("help-menu")

    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.logo.image, self.logo.rect)
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.help_button.image, self.help_button.rect)

    def run(self):
        self.logo.update()
        self.play_button.update()
        self.help_button.update()
        self.render()
