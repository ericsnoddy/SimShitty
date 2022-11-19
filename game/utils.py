# reqs
import pygame as pg

def draw_text(win, pos, text, size, color):
    font = pg.font.Font(None, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(topleft = pos)
    win.blit(text_surf, text_rect)