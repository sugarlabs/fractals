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


class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, default_val, step, feat_name, max_val, min_val):
        super().__init__()
        self.feat_name = feat_name
        self.val = default_val
        self.step = step
        self.max_val = max_val
        self.min_val = min_val
        self.bg = pygame.image.load("./assets/slider-bg.png")
        self.bg_rect = self.bg.get_rect(topleft=(0, 0))
        self.image = pygame.Surface(self.bg.get_size())
        self.slider_ball_image = pygame.image.load("./assets/slider-ball.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.up_rect = pygame.Rect(self.rect.x + 188, self.rect.y + 26, 6, 4)
        self.down_rect = pygame.Rect(self.rect.x + 188, self.rect.y + 34, 6, 4)
        self.slider_ball_rect = self.slider_ball_image.get_rect(
            topleft=(3, 23)
        )
        self.slider_area_rect = pygame.Rect(
            self.rect.x, self.rect.y + 21, 143, 22
        )
        self.recalibrate_slider_pos()

    def handle_press(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.up_rect.collidepoint(mouse_pos):
            self.val += self.step
            if self.val >= self.max_val:
                self.val = self.max_val
            self.recalibrate_slider_pos()
        elif self.down_rect.collidepoint(mouse_pos):
            self.val -= self.step
            if self.val <= self.min_val:
                self.val = self.min_val
            self.recalibrate_slider_pos()

    def recalibrate_slider_pos(self):
        prop = (self.val - self.min_val) / (self.max_val - self.min_val)
        centerx = self.rect.x + 12 + prop * (134 - 12)
        self.slider_ball_rect.centerx = centerx

    def update_slider_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.slider_area_rect.collidepoint(mouse_pos):
            centerx = mouse_pos[0] - self.rect.x
            centerx = min(centerx, self.rect.x + 134)
            centerx = max(centerx, self.rect.x + 12)
            prop = (centerx - self.rect.x - 12) / (134 - 12)
            self.val = round(
                self.min_val + prop * (self.max_val - self.min_val)
            )
            self.recalibrate_slider_pos()

    def draw(self, screen):
        self.image.fill("black")
        self.image.blit(self.bg, self.bg_rect)
        self.image.blit(self.slider_ball_image, self.slider_ball_rect)
        text = font_s.render("" + (str)(self.val), False, "black")
        text_rect = text.get_rect(midleft=(149, 32))
        self.image.blit(text, text_rect)
        text = font_l.render(self.feat_name, False, "black")
        text_rect = text.get_rect(center=(100, 11))
        self.image.blit(text, text_rect)
        screen.blit(self.image, self.rect)

    def update(self):
        pass
