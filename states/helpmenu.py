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

from components.title import Title
from components.button import Button
from utils import Utils

content = """\
Fractals are patterns that exhibit self-similarity at various \
scales and levels of magnification.

Available Fractals - Snowflake, Dragon Curve, Levy Curve, \
Serpinski Triangle, Plant Fractal, Tree Fractal and Peano Curve.

For visualising the fractals, you can use the sliders present \
in sidebar. Effect of each slider and widget is as follows -
1 Fractal Iterator - Click on left and right buttons to change \
between different fractals.
2 Angle - The angle at which next iteration pattern forms.
3 Thickness - Thickness of the lines used for visualisation.
4 Depth - Number of iterations upto which the fractal would \
generate.
5 Initial Angle - The angle at which first iteration forms. \
Change this to set the overall orientation of the fractal.
"""


class HelpMenu:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.logo = Title(sw / 2, 60)

        self.home_button = Button(0, 0, "./assets/home-button.png")
        self.home_button.image = pygame.transform.scale_by(
            self.home_button.image, 1.5
        )
        self.home_button.rect = self.home_button.image.get_rect(
            center=(sw / 2 - 220, 80)
        )

        self.help_surf = pygame.Surface((sw - 20, sh - 110))
        pygame.draw.rect(
            self.help_surf, "white",
            pygame.Rect(
                5,
                5,
                self.help_surf.get_width() - 10,
                self.help_surf.get_height() - 10
            ),
            2
        )
        self.help_rect = self.help_surf.get_rect(topleft=(10, 110))

        self.font, self.line_height = Utils.get_font_and_line_height(
            self.screen
        )
        Utils.render_multiple_lines(
            content,
            self.help_surf,
            30, (30, 30), "white",
            self.font, self.line_height
        )

    def render(self):
        self.screen.fill("black")
        self.screen.blit(self.logo.image, self.logo.rect)
        self.screen.blit(self.home_button.image, self.home_button.rect)
        self.screen.blit(self.help_surf, self.help_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.home_button.check_press():
                self.gameStateManager.set_state("main-menu")

    def run(self):
        self.logo.update()
        self.home_button.update()
        self.render()
