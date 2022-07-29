import numpy as np
from numba import njit
import pygame as pg
import math
from settings import *

@njit(fastmath=True)
def raycasting(player_pos, player_angle, player_height, player_tilt, delta_angle, color_arr, height_arr, width, height, fov_height, fov, ray_length, scale_height, result):
    result[:] = np.array([0, 0, 0])
    heights_buffer = np.full(width, height)
    # find the angle of the first ray
    ray_angle = player_angle - fov_height
    for n_ray in range(width):
        first_contact = False
        for step_along in range(1, ray_length):
            x = int(math.cos(ray_angle) * step_along + player_pos[0])
            if 0 < x < width:
                y = int(math.sin(ray_angle) * step_along + player_pos[1])
                if 0 < y < height:
                    # eliminate fish eye effect
                    step_along *= math.cos(player_angle - fov - ray_angle)

                    # calculate height(the further we are the smaller it gets)
                    curr_height = int((player_height - height_arr[x][y]) / step_along * scale_height + player_tilt)

                    # remove excessive lines
                    if not first_contact:
                        heights_buffer[n_ray] = min(curr_height, heights_buffer[n_ray])
                        first_contact = True
                    # dealing with mirroring
                    curr_height = max(0, curr_height)
                    # draw vertical line
                    if curr_height < heights_buffer[n_ray]:
                        for y_line in range(curr_height, heights_buffer[n_ray]):
                            result[n_ray][y_line] = color_arr[x][y]
                        heights_buffer[n_ray] = curr_height
        ray_angle += delta_angle
    return result


class Engine:
    def __init__(self, image_arr, image_height_arr, player, game):
        self.fov = math.pi / 3
        self.fov_height = math.pi / 2
        self.delta_angle = self.fov / WIDTH
        self.ray_dist = int(max(len(image_height_arr[0]), len(image_height_arr)) * 1.5)
        self.scale_height = HEIGHT
        self.color_arr = np.array(image_arr)
        self.height_arr = np.array(image_height_arr)
        self.result = np.full((WIDTH,  HEIGHT, 3), np.array([0, 0, 0]))
        self.player = player
        self.game = game

    def update(self):
        self.result = raycasting(self.player.pos, self.player.angle, self.player.height, self.player.tilt, self.delta_angle, self.color_arr, self.height_arr,WIDTH, HEIGHT, self.fov_height, self.fov, self.ray_dist,
                                 self.scale_height, self.result)
    def draw(self, screen):
        screen.blit(pg.surfarray.make_surface(self.result), (0, 0))