#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 08:01:30 2020

@author: heiko
"""

import PIL


def get_fname_base(simulation_folder, n_voxel, n_subj, n_repeat, sd,
                   duration, pause, endzeros, use_cor_noise, resolution,
                   sigma_noise, ar_coeff, layer=None, variation=None):
    """ generates the filename base from parameters """
    if layer is None:
        l_text = '/layer%02d'
    else:
        l_text = '/layer%02d' % layer
    if variation:
        fname_base = simulation_folder + l_text \
            + ('/pars_%03d_%02d_%02d_%.3f_%s/' % (
                n_voxel, n_subj, n_repeat, sd, variation)) \
            + ('fmri_%02d_%02d_%03d_%s_%d_%.2f_%.2f/' % (
                duration, pause, endzeros, use_cor_noise, resolution,
                sigma_noise, ar_coeff))
    else:
        fname_base = simulation_folder + l_text \
            + ('/pars_%03d_%02d_%02d_%.3f/' % (
                n_voxel, n_subj, n_repeat, sd)) \
            + ('fmri_%02d_%02d_%03d_%s_%d_%.2f_%.2f/' % (
                duration, pause, endzeros, use_cor_noise, resolution,
                sigma_noise, ar_coeff))
    return fname_base


def get_stimuli_92():
    stimuli = []
    for i_stim in range(92):
        im = PIL.Image.open('96Stimuli/stimulus%d.tif' % (i_stim+1))
        stimuli.append(im)
    return stimuli


def get_stimuli_96():
    stimuli = []
    for i_stim in range(96):
        im = PIL.Image.open('96Stimuli/stimulus%d.tif' % (i_stim+1))
        stimuli.append(im)
    return stimuli
