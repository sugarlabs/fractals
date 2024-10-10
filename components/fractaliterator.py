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

font_s = pygame.font.Font("./fonts/m04b.ttf", 8)
font_l = pygame.font.Font("./fonts/m04b.ttf", 12)


class FractalIterator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.bg = pygame.image.load("./assets/fractal-title-bg.png")
        self.bg_rect = self.bg.get_rect(topleft=(0, 0))
        self.image = pygame.Surface(self.bg.get_size())
        self.rect = self.image.get_rect(center=(x, y))
        self.left_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 18, 5, 7)
        self.right_rect = pygame.Rect(
            self.rect.x + 190, self.rect.y + 18, 5, 7
        )

        self.fractals = {
            "snowflake": {
                "sentence": "F++F++F++",
                "rules": {
                    "F": "F-F++F-F"
                },
                "params": {
                    "angle": 60,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 180
                }
            },

            "dragon": {
                "sentence": "X",
                "rules": {
                    "X": "F-F-F+F+FX++F-F-F+F+FX--F-F-F+F+FX",
                    "F": ""
                },
                "params": {
                    "angle": 60,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 0
                }
            },

            "levy": {
                "sentence": "F++F++F++F",
                "rules": {
                    "F": "-F++F-"
                },
                "params": {
                    "angle": 45,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 0
                }
            },

            "serpinski": {
                "sentence": "F-G-G",
                "rules": {
                    "F": "F-G+F+G-F",
                    "G": "GG"
                },
                "params": {
                    "angle": 120,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 0
                }
            },

            "plant": {
                "sentence": "X",
                "rules": {
                    "X": "F-[[X]+X]+F[+FX]-X",
                    "F": "FF"
                },
                "params": {
                    "angle": 25,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": -90
                }
            },
            "binary tree": {
                "sentence": "F",
                "rules": {
                    "F": "G[-GFFF][+FFFG]",
                    "G": "GG"
                },
                "params": {
                    "angle": 30,
                    "length": 0.29,
                    "iterations": 1,
                    "initial angle": -90
                }
            },
            "peano": {
                "sentence": "A",
                "rules": {
                    "A": "-BF+AFA+FB-",
                    "B": "+AF-BFB-FA+",
                    "C": ""
                },
                "params": {
                    "angle": 90,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 0
                }
            }
        }

        self.index = 0
        self.fractal_list = [key for key in self.fractals.keys()]
        self.update_text()

    def get_curr_fractal(self):
        return self.fractals[self.fractal_list[self.index]]

    def handle_press(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.left_rect.collidepoint(mouse_pos):
            self.index -= 1
            if self.index < 0:
                self.index = len(self.fractal_list) - 1
            self.update_text()
            return True
        elif self.right_rect.collidepoint(mouse_pos):
            self.index += 1
            if self.index >= len(self.fractal_list):
                self.index = 0
            self.update_text()
            return True
        return False

    def update_text(self):
        self.text = font_l.render(
            self.fractal_list[self.index], False, "black"
        )
        self.text_rect = self.text.get_rect(
            center=(self.rect.width / 2, self.rect.height / 2)
        )

    def draw(self, screen):
        self.image.fill("black")
        self.image.blit(self.bg, self.bg_rect)
        self.image.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)

    def update(self):
        pass
