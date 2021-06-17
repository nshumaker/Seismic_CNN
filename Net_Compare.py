# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:55:39 2021

@author: niven
"""

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import Model
from keras.models import load_model
from keras.backend import clear_session
from keras.utils.vis_utils import plot_model

import matplotlib.pyplot as plt
from numpy import expand_dims

# %%
# Import helper functions from utils folder
from src.definitions import ROOT_DIR
from src.data.utils import plot_image_compare, gen_feature_map, L2_norm, Filter_Activation_Sort
# %%
#Model weights and structure as VGG19 (may take a while to download)

model_dir = ROOT_DIR/'src/data/Unet_grayscale_True_pad_False_size_128.h5'
model = load_model(model_dir)
model.summary()

# %%
plot_model(model, to_file='salt_plot.png', show_shapes=True, show_layer_names=True)

# %%
model_dir = ROOT_DIR/'../PetSegmentation/oxford_segmentation.h5'
model = load_model(model_dir)
# %%
plot_model(model, to_file='oxford_pet_plot.png', show_shapes=True, show_layer_names=True)

# %%
