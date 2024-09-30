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

import math
import pygame

font_l = pygame.font.Font("./fonts/m04b.ttf", 20)
font_m = pygame.font.Font("./fonts/m04b.ttf", 16)
font_s = pygame.font.Font("./fonts/m04b.ttf", 10)

class Utils:
    @staticmethod
    def render_multiple_lines(text, surface, right_margin, pos, color, font, line_height=5):
        rect = surface.get_rect()
        bound = rect.right - right_margin
        x, y = pos
        space = font.size(' ')[0]

        words = [line.split() for line in text.split('\n')]
        for line in words:
            for word in line:
                word_surf = font.render(word, False, color)
                word_width, word_height = word_surf.get_size()
                if x + word_width > bound:
                    x = pos[0]
                    y += word_height + line_height - 2

                surface.blit(word_surf, (x, y))
                x += word_width + space

            x = pos[0]
            y += word_height + line_height
    
    @staticmethod
    def get_font_and_line_height(screen):
        sw = screen.get_width()
        if sw > 1500:
            return font_l, 15
        elif sw > 1000:
            return font_m, 10
        else:
            return font_s, 5
