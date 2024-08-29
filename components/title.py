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


class Title(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.logo_img = pygame.image.load("./assets/logo.png")
        self.logo_img_rect = self.logo_img.get_rect(topleft=(0, 0))
        self.image = pygame.Surface(self.logo_img.get_size())
        self.rect = self.image.get_rect(center=(x, y))

        self.black_rects = []
        n = len("fractals")
        for i in range(n):
            new_rect = pygame.Rect(self.rect.left + (i * 45), self.rect.top + 42, 45, 42)
            self.black_rects.append(new_rect)

    def update(self):
        self.image.fill("black")
        self.image.blit(self.logo_img, self.logo_img_rect)
        mouse_pos = pygame.mouse.get_pos()
        for rect in self.black_rects:
            draw_rect = pygame.Rect(rect.left - self.rect.left, rect.top - self.rect.top - 42, 45, 42)
            if rect.collidepoint(mouse_pos):
                draw_rect.top += 42
            
            pygame.draw.rect(self.image, "black", draw_rect)
