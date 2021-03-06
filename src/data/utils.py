

from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

import matplotlib.pyplot as plt

from numpy import expand_dims
from numpy import matmul
from numpy import linalg
from numpy import mean
from numpy import sqrt

import pandas as pd

#generate a figure comparing image 1 in the upper row to image two in the lower row
def plot_image_compare(feature_map1, feature_map2, img1, img2, feature_index, title_name):
    num_features = len(feature_index) #list of filter indexes to plot activations for
    col_subplots = num_features+1
    fignum, ax = plt.subplots(2, col_subplots, figsize=(10, 6.5), facecolor=(0.98,0.97,0.94,1))

    for jx in range(2,col_subplots+1):
        ax = plt.subplot(2, col_subplots, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Seismic 1')
        plt.imshow(img1)
        ax = plt.subplot(2, col_subplots, jx)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Feature'+str(feature_index[jx-2]))
        plt.imshow(feature_map1[0,:,:,feature_index[jx-2] ] )
        
        ax = plt.subplot(2, col_subplots, 1+col_subplots)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Seismic 2')
        plt.imshow(img2)
        ax = plt.subplot(2, col_subplots, col_subplots+jx)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Feature'+str(feature_index[jx-2]))
        plt.imshow(feature_map2[0,:,:,feature_index[jx-2] ] )
    
    featuretitle = title_name+'\n Feature Size= '+str(feature_map1.shape[1]) + ' x '+ str(feature_map1.shape[2])
    fignum.suptitle(featuretitle, fontsize=14)
    #fignum.tight_layout(pad=-.025)
    plt.subplots_adjust(left=.05, right=.995, wspace = 0, hspace=.15)

#forward propagate image through VGG19 network    
def gen_feature_map(model, layer_out, image_in, target_size, color_mode):
    #model = Model(inputs=model.inputs, outputs=model.layers[layer_out].output)
    img = load_img(image_in, target_size=target_size, color_mode=color_mode)
    img = img_to_array(img)
    #expand dimension to represent sample 1 (m=1)
    img = expand_dims(img, axis=0)
    feature_map = model.predict(img)
    return feature_map
#calculate the euclidian distance between filter activations for each feature map
def L2_norm(map1, map2):
    assert map1.shape == map2.shape # should be x by x array
    (m, n_H, n_W) = map1.shape
    map1 = map1.reshape(n_H*n_W, 1)
    map2 = map2.reshape(n_H*n_W, 1)
    var_L2 = linalg.norm(map1-map2)
    return var_L2

#sort mean filter activations low to high and cut off feature maps below a minimal activation threshold   
def Filter_Activation_Sort(map1, map2, activation_cutoff):
    L2_list = []
    activation1 = []
    activation2 = []
    for ix in range(map1.shape[-1]):
        ix_map1 = map1[:,:,:,ix]
        ix_map2 = map2[:,:,:,ix]
        L2_list.append(L2_norm(ix_map1, ix_map2))
        activation1.append(mean(ix_map1))
        activation2.append(mean(ix_map2))
    
    dict_cache = {'L2_norm':L2_list, 'activation1':activation1,'activation2':activation2}
    df_cache = pd.DataFrame(dict_cache).reset_index().rename(columns={'index':'filter_layer'})

    df_cache['norm_activation'] = sqrt(df_cache['activation1']**2 + df_cache['activation2']**2)
    df_cache = df_cache[df_cache.norm_activation > activation_cutoff]
    df_cache['L2_norm_scaled'] = df_cache['L2_norm']/df_cache['norm_activation']
    df_cache.dropna(axis=0, how='any', inplace=True)
    df_cache.sort_values(by='L2_norm_scaled', inplace=True)

    filters_low_dist=df_cache['filter_layer'][0:4].values
    filters_high_dist= df_cache['filter_layer'][-5:-1].values
    return filters_low_dist, filters_high_dist
    