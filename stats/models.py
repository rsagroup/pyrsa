#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 07:57:55 2020

@author: heiko
"""

import numpy as np
import tqdm
import nn_simulations as dnn
import pyrsa


def get_models(model_type, fname_base_l, stimuli,
               n_stimuli, n_layer=12, n_sim=1000):
    pat_desc = {'stim': np.arange(n_stimuli)}
    models = []
    for i_layer in tqdm.trange(n_layer):
        if model_type == 'fixed_averagetrue':
            rdm_true_average = 0
            for i in range(n_sim):
                Utrue = np.load(fname_base_l % i_layer
                                + 'Utrue%04d.npy' % i)
                dat_true = [pyrsa.data.Dataset(Utrue[i, :n_stimuli, :])
                            for i in range(Utrue.shape[0])]
                rdm_true = pyrsa.rdm.calc_rdm(dat_true, method='euclidean')
                rdm_mat = rdm_true.get_vectors()
                rdm_mat = rdm_mat / np.sqrt(np.mean(rdm_mat ** 2))
                rdm_true_average = rdm_true_average + np.mean(rdm_mat, 0)
            rdm = rdm_true_average / n_sim
            rdm = pyrsa.rdm.RDMs(rdm, pattern_descriptors=pat_desc)
            model = pyrsa.model.ModelFixed('Layer%02d' % i_layer, rdm)
        elif model_type == 'fixed_full':
            rdm = dnn.get_true_RDM(
                model=dnn.get_default_model(),
                layer=i_layer,
                stimuli=stimuli)
            rdm.pattern_descriptors = pat_desc
            model = pyrsa.model.ModelFixed('Layer%02d' % i_layer, rdm)
        elif model_type == 'select_full':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=False)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelSelect('Layer%02d' % i_layer, rdms)
        elif model_type == 'select_avg':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=True)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelSelect('Layer%02d' % i_layer, rdms)
        elif model_type == 'select_both':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=False)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=True)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelSelect('Layer%02d' % i_layer, rdms)
        elif model_type == 'interpolate_full':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=False)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelInterpolate('Layer%02d' % i_layer, rdms)
        elif model_type == 'interpolate_avg':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=True)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelInterpolate('Layer%02d' % i_layer, rdms)
        elif model_type == 'interpolate_both':
            smoothings = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, np.inf])
            rdms = []
            for i_smooth, smooth in enumerate(smoothings):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smooth,
                    average=True)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            for i_smooth in range(len(smoothings) - 1, -1, -1):
                rdm = dnn.get_true_RDM(
                    model=dnn.get_default_model(),
                    layer=i_layer,
                    stimuli=stimuli,
                    smoothing=smoothings[i_smooth],
                    average=False)
                rdm.pattern_descriptors = pat_desc
                rdms.append(rdm)
            rdms = pyrsa.rdm.concat(rdms)
            model = pyrsa.model.ModelInterpolate('Layer%02d' % i_layer, rdms)
        elif model_type == 'weighted_avgfull':
            rdms = []
            rdm = dnn.get_true_RDM(
                model=dnn.get_default_model(),
                layer=i_layer,
                stimuli=stimuli,
                smoothing=None,
                average=True)
            rdms.append(rdm)
            rdm = dnn.get_true_RDM(
                model=dnn.get_default_model(),
                layer=i_layer,
                stimuli=stimuli,
                smoothing=False,
                average=False)
            rdms.append(rdm)
            rdm = dnn.get_true_RDM(
                model=dnn.get_default_model(),
                layer=i_layer,
                stimuli=stimuli,
                smoothing=np.inf,
                average=False)
            rdms.append(rdm)
            rdm = dnn.get_true_RDM(
                model=dnn.get_default_model(),
                layer=i_layer,
                stimuli=stimuli,
                smoothing=np.inf,
                average=False)
            rdms.append(rdm)
            model = pyrsa.model.ModelWeighted('Layer%02d' % i_layer, rdms)
        models.append(model)
    return models