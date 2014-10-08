#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lib.tcod import libtcodpy as libtcod
from lib.bass.pybass import *

CONW = 120
CONH = 80

BG_CURRENT_ANIM_NAME = 'anim'
BG_CURRENT_ANIM_CANT = 0
BG_CURRENT_ANIM_VELOC = 0.0

bganim = []
anim_num = 0
anim_pos = 0
anim_acum = 0.0


def load_bg_anim(nombre, cantidad, velocidad):
    global BG_CURRENT_ANIM_NAME
    global BG_CURRENT_ANIM_CANT
    global BG_CURRENT_ANIM_VELOC
    global bganim
    global anim_pos
    global anim_acum
    BG_CURRENT_ANIM_NAME = nombre
    BG_CURRENT_ANIM_CANT = cantidad
    BG_CURRENT_ANIM_VELOC = velocidad
    bganim = []
    anim_pos = 0
    anim_acum = 0.0
    for i in range(0, BG_CURRENT_ANIM_CANT):
        path = os.path.join(b'res',
                            b'animations',
                            BG_CURRENT_ANIM_NAME,
                            b'{:03}.png'.format(i))
        img = libtcod.image_load(path)
        bganim.append(img)


def paint_bg_anim(delta):
    global anim_acum
    global anim_pos
    anim_acum += delta
    libtcod.image_blit_2x(bganim[anim_pos], 0, 0, 0)
    if anim_acum >= BG_CURRENT_ANIM_VELOC:
        anim_acum = 0.0
        # suma y si llega al limite, reinicia
        anim_pos = (anim_pos + 1) % BG_CURRENT_ANIM_CANT
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print(0, 1, 3, "Animacion (fotograma): %d" % anim_pos)


def select_new_bg_anim():
    global anim_num
    if anim_num == 0:
        load_bg_anim(b'rainbow_dancers', 24, .04)
    elif anim_num == 1:
        load_bg_anim(b'walking_cube', 22, .035)
    elif anim_num == 2:
        load_bg_anim(b'saltimbanqui', 76, .05)
    elif anim_num == 3:
        load_bg_anim(b'warp_stars', 15, .02)
    else:
        load_bg_anim(b'alien_world', 27, .045)
    anim_num = (anim_num + 1) % 5  # reiniciamos si llegamos a 5


def mainloop():
    # inicializamos bass
    BASS_Init(-1, 44100, 0, 0, 0)

    # inicializamos libtcod
    libtcod.sys_set_fps(60)
    # screen_w, screen_h = libtcod.sys_get_current_resolution()
    # libtcod.sys_force_fullscreen_resolution(screen_w, screen_h)
    libtcod.console_init_root(CONW,
                              CONH,
                              b'Eliuk Blau: MusicPynda Prototype (Python)')

    #libtcod.console_credits()
    #bgimg = libtcod.image_load(b'bgimg.png')

    # cargamos la animacion inicial
    select_new_bg_anim()

    # cargamos la musica
    musica = BASS_StreamCreateFile(False,
                                   os.path.join(b'res', b'bgmus.ogg'),
                                   0, 0, BASS_SAMPLE_LOOP)
    # iniciamos la musica
    if musica == 0:
        print ('BASS_StreamCreateFile error %s' % get_error_description(BASS_ErrorGetCode()))
    if not BASS_ChannelPlay(musica, True):
        print ('BASS_ChannelPlay error %s' % get_error_description(BASS_ErrorGetCode()))

    # mainloop
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    end_credits = False
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
                                    libtcod.EVENT_MOUSE,
                                    key,
                                    mouse)
        # si se pulsa la tecla de escape, terminamos la demo
        if key.vk == libtcod.KEY_ESCAPE:
            break
        elif key.vk == libtcod.KEY_SPACE:
            select_new_bg_anim()
        #elif key.vk == libtcod.KEY_ENTER:
        #    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # limpiamos la consola
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_clear(0)

        # dibujamos la animacion
        paint_bg_anim(libtcod.sys_get_last_frame_length())

        # dibujamos un texto informativo
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, 1, 1,
                              "Me ejecuto hace %.1f segundos" %
                              libtcod.sys_elapsed_seconds())

        # creditos de libtcod
        if end_credits:
            end_credits = False
            libtcod.console_credits_reset();
        if not end_credits:
            end_credits = libtcod.console_credits_render(103, 73, True)

        # refrescamos la consola
        libtcod.console_flush()

    # terminamos musica y bass
    BASS_ChannelStop(musica)
    BASS_StreamFree(musica)
    BASS_Free()


if __name__ == '__main__':
    mainloop()
