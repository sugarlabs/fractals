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
import math


class Simulator:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        self.sidebar = pygame.Surface((0.3 * self.screen.get_width(), self.screen.get_height()))
        self.sidebar_rect = self.sidebar.get_rect(topleft=(0, 0))
        self.renderer = pygame.Surface((0.7 * self.screen.get_width(), self.screen.get_height()))
        self.renderer_rect = self.renderer.get_rect(topleft=(0.3 * self.screen.get_width(), 0))

        self.fractals = {
            "snowflake": {
                "sentence": "F++F++F++",
                "rules": {
                    "F": "F-F++F-F"
                },
                "params": {
                    "angle": 60,
                    "length": 1,
                    "iterations": 0,
                    "initial angle": 180
                }
            },

            "test": {
                "sentence": "F-F-F+F+FX++F-F-F+F+FX--F-F-F+F+FX",
                "rules": {
                    "X" : "F-F-F+F+FX++F-F-F+F+FX--F-F-F+F+FX",
                    "F": ""
                },
                "params": {
                    "angle": 60,
                    "length": 1,
                    "iterations": 0,
                    "initial angle": 0
                }
            },

            "levy curve": {
                "sentence": "F++F++F++F",
                "rules": {
                    "F": "-F++F-"
                },
                "params": {
                    "angle": 45,
                    "length": 1,
                    "iterations": 0,
                    "initial angle": 0
                }
            },

            "serpinski triangle": {
                "sentence": "F-G-G",
                "rules": {
                    "F": "F-G+F+G-F",
                    "G": "GG"
                },
                "params": {
                    "angle": 120,
                    "length": 1,
                    "iterations": 0,
                    "initial angle": 0
                }
            },

            "plant": {
                "sentence": "F-[[X]+X]+F[+FX]-X",
                "rules": {
                    "X": "F-[[X]+X]+F[+FX]-X",
                    "F": "FF"
                },
                "params": {
                    "angle": 25,
                    "length": 1,
                    "iterations": 0,
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
            "peano curve": {
                "sentence": "A",
                "rules": {
                    "A": "-BF+AFA+FB-",
                    "B": "+AF-BFB-FA+",
                    "C": ""
                },
                "params" : {
                    "angle": 90,
                    "length": 1,
                    "iterations": 1,
                    "initial angle": 0
                }
            }
        }

        self.fractal_index = -1
        self.fractal_list = [key for key in self.fractals.keys()]

        self.fractal = self.fractals[self.fractal_list[self.fractal_index]]
        self.default_angle = self.fractal["params"]["angle"]
        self.fractal_zoom = 0
        self.inc_angle = False
        self.draw_fractal()
    
    def generate(self, sentence, rules, iterations):
        start_string = sentence
        end_string = start_string
        for _ in range(iterations):
            end_string = "".join(rules[char] if char in rules else char for char in start_string)
            start_string = end_string
        return end_string

    def get_orig_and_scale(self, sentence, angle, length, initial_angle):
        left, top, right, bottom = 0, 0, 0, 0
        stack = []
        turtle = {
            "pos": (0, 0),
            "angle": initial_angle
        }
        for cmd in sentence:   
            if cmd == "+":
                turtle["angle"] += angle
            elif cmd == "-":
                turtle["angle"] -= angle
            elif cmd == "[":
                stack.append((turtle["pos"], turtle["angle"]))
            elif cmd == "]":
                turtle["pos"], turtle["angle"] = stack.pop()
            else:
                x, y = turtle["pos"]
                rad = math.radians(turtle["angle"])
                new_x = x + math.cos(rad) * length
                new_y = y + math.sin(rad) * length
                turtle["pos"] = (new_x, new_y)

                left = min(new_x, left)
                top = min(new_y, top)
                right = max(new_x, right)
                bottom = max(new_y, bottom)
        
        sw, sh = self.renderer.get_width() * 0.9, self.renderer.get_height() * 0.9
        x_scale = sw / (right - left)
        y_scale = sh / (bottom - top)
        scale = min(x_scale, y_scale)
        originate = (-left * scale, -top * scale)

        return originate, scale, pygame.Surface(((scale * (right - left)) + 1, (scale * (bottom - top)) + 1))

    def draw_fractal(self):
        self.renderer.fill("black")
        stack = []
        params = self.fractal["params"]
        length = params["length"]
        angle = params["angle"]
        iterations = params["iterations"]
        sentence = self.generate(self.fractal["sentence"], self.fractal["rules"], iterations)
        orig, scale, surf = self.get_orig_and_scale(sentence, angle, length, params["initial angle"])
        length *= scale
        surf_rect = surf.get_rect(center=(self.renderer.get_width()/2, self.renderer.get_height()/2))
        turtle = {
            "pos": orig,
            "angle": params["initial angle"]
        }

        color = 0
        dcolor = 255 / len(sentence)
        for cmd in sentence:   
            if cmd == "+":
                turtle["angle"] += angle
            elif cmd == "-":
                turtle["angle"] -= angle
            elif cmd == "[":
                stack.append((turtle["pos"], turtle["angle"]))
            elif cmd == "]":
                turtle["pos"], turtle["angle"] = stack.pop()
            else:
                x, y = turtle["pos"]
                rad = math.radians(turtle["angle"])
                new_x = x + math.cos(rad) * length
                new_y = y + math.sin(rad) * length
                pygame.draw.line(surf, (255 - color, color, 125 + color / 2), (x, y), (new_x, new_y), 1)
                turtle["pos"] = (new_x, new_y)
            color += dcolor

        self.renderer.blit(surf, surf_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.renderer_rect.collidepoint(pygame.mouse.get_pos()):
                self.fractal["params"]["iterations"] += 1
                self.fractal["params"]["angle"] = self.default_angle
                self.inc_angle = False
                self.draw_fractal()
            else:
                self.fractal["params"]["iterations"] = 0
                self.fractal["params"]["angle"] = self.default_angle
                self.inc_angle = False
                self.fractal_index += 1
                self.fractal_index %= len(self.fractal_list)
                self.fractal = self.fractals[self.fractal_list[self.fractal_index]]
                self.default_angle = self.fractal["params"]["angle"]
                self.draw_fractal()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.inc_angle = not self.inc_angle

    def render(self):
        self.screen.fill("black")
        self.sidebarbar.fill((10, 10, 10))
        self.screen.blit(self.sidebar, self.sidebar_rect)

        self.screen.blit(self.renderer, self.renderer_rect)

    def run(self):
        if self.inc_angle:
            self.fractal['params']['angle'] += 0.4
        self.draw_fractal()
        self.render()
