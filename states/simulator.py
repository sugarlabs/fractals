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

from components.slider import Slider
from components.button import Button
from components.fractaliterator import FractalIterator


class Simulator:
    def __init__(self, game):
        self.screen = game.screen
        self.gameStateManager = game.gameStateManager
        self.game = game

        self.sidebar = pygame.Surface((214, self.screen.get_height()))
        self.sidebar_rect = self.sidebar.get_rect(topleft=(0, 0))
        self.renderer = pygame.Surface((self.screen.get_width() - 214, self.screen.get_height()))
        self.renderer_rect = self.renderer.get_rect(topleft=(214, 0))

        self.populate_sidebar()
        self.change_fractal()
    
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
        angle = self.angle_slider.val
        iterations = self.depth_slider.val
        thickness = self.thickness_slider.val
        sentence = self.generate(self.fractal["sentence"], self.fractal["rules"], iterations)
        orig, scale, surf = self.get_orig_and_scale(sentence, angle, length, self.initial_angle_slider.val)
        length *= scale
        surf_rect = surf.get_rect(center=(self.renderer.get_width()/2, self.renderer.get_height()/2))
        turtle = {
            "pos": orig,
            "angle": self.initial_angle_slider.val
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
                pygame.draw.line(surf, (255 - color, color, 125 + color / 2), (x, y), (new_x, new_y), thickness)
                turtle["pos"] = (new_x, new_y)
            color += dcolor

        self.renderer.blit(surf, surf_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for slider in self.sliders:
                slider.handle_press()
            if self.sim_button.check_press():
                self.draw_fractal()
            if self.fractal_iterator.handle_press():
                self.change_fractal()
            if self.home_button.check_press():
                self.gameStateManager.set_state("main-menu")
        elif pygame.mouse.get_pressed()[0]:
            for slider in self.sliders:
                slider.update_slider_pos()
    
    def change_fractal(self):
        self.fractal = self.fractal_iterator.get_curr_fractal()
        self.angle_slider.val = self.fractal["params"]["angle"]
        self.angle_slider.recalibrate_slider_pos()

        self.depth_slider.val = self.fractal["params"]["iterations"]
        self.depth_slider.recalibrate_slider_pos()

        self.thickness_slider.val = 1
        self.thickness_slider.recalibrate_slider_pos()
        
        self.initial_angle_slider.val = self.fractal["params"]["initial angle"]
        self.initial_angle_slider.recalibrate_slider_pos()

        self.renderer.fill("black")

    def render(self):
        self.screen.fill("black")
        self.sidebar.fill((10, 10, 10))
        self.screen.blit(self.sidebar, self.sidebar_rect)
        self.fractal_iterator.draw(self.screen)
        for slider in self.sliders:
            slider.draw(self.screen)
        self.screen.blit(self.sim_button.image, self.sim_button.rect)
        self.screen.blit(self.home_button.image, self.home_button.rect)
        self.screen.blit(self.renderer, self.renderer_rect)
    
    def populate_sidebar(self):
        self.fractal_iterator = FractalIterator(105, 30)
        self.angle_slider = Slider(105, 90, 60, 10, "ANGLE", 180, -180)
        self.thickness_slider = Slider(105, 150, 2, 1, "THICKNESS", 5, 1)
        self.depth_slider = Slider(105, 210, 7, 1, "DEPTH", 8, 1)
        self.initial_angle_slider = Slider(105, 270, 0, 10, "INITIAL ANGLE", 180, -180)
        self.sliders = [self.angle_slider, self.thickness_slider, self.depth_slider, self.initial_angle_slider]
        self.sim_button = Button(105, 330, "./assets/simulate-button.png")
        self.home_button = Button(165, 330, "./assets/home-button.png")

    def run(self):
        self.render()
