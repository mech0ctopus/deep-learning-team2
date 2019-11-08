# -*- coding: utf-8 -*-
"""
Utility functions for working with neural networks.
"""
from keras.models import model_from_json, model_from_yaml
import numpy as np
from os.path import exists
from glob import glob
from PIL import Image
import pickle

def save_model(model,serialize_type,model_name='model'):
    '''Saves model and weights to file.'''
    serialize_type=serialize_type.lower()
    
    if serialize_type=='yaml':
        model_yaml = model.to_yaml()
        with open(model_name+".yaml", "w") as yaml_file:
            yaml_file.write(model_yaml)
    elif serialize_type=='json':
        model_json = model.to_json()
        with open(model_name+".json", "w") as json_file:
            json_file.write(model_json)
    model.save_weights(model_name+".h5")
    
    print(model_name+' & weights saved to disk.')

def load_model(model_filepath,weights_filepath):
    '''Loads model and weights to file.'''
    
    serialize_type=model_filepath.split('.')[-1]
    serialize_type=serialize_type.lower()
    
    file = open(model_filepath, 'r')
    loaded_model = file.read()
    file.close()
    
    if serialize_type=='yaml':
        loaded_model = model_from_yaml(loaded_model)
    elif serialize_type=='json':
        loaded_model=model_from_json(loaded_model)

    loaded_model.load_weights(weights_filepath)
    print("Loaded model from disk")
    return loaded_model

def get_layer_names(model):
    '''Returns list of layer names.'''
    layer_names=[]
    for layer in model.layers:
        layer_names.append(layer.name)
    return layer_names

def generate_pickle_files(X,y,y_names):
    '''Generates pickle file to compress whole dataset.'''
    pickle.dump(X, open("X.p", "wb"))
    pickle.dump(y, open("y.p", "wb"))
    pickle.dump(y, open("y_names.p", "wb"))

def load_pickle_files(X_file, y_file, y_names_file):
    '''Reads data from pickle files'''
    X=pickle.load(open(X_file,'rb'))
    y=pickle.load(open(y_file,'rb'))
    y_names=pickle.load(open(y_names_file,'rb'))

    return X, y, y_names

def read_data(data_folderpath):
    '''Reads full dataset.  Assumes data has been resized.
    Assumes "data_folderpath" contains subfolders corresponding
    to class names and each containing jpg files for class.'''
    X=[]
    y=[]
    y_names={}
    #Append folderpaths if needed
    if data_folderpath.endswith('\\')==False:
        data_folderpath=str(data_folderpath)+ '\\'
    #Collect all foldernames
    foldernames=glob(data_folderpath+'*/')
    #Define classes from foldernames
    for idx,foldername in enumerate(foldernames):
        #Append folder names to classes
        y_names[idx]=(foldername.split('\\')[-2])
        #Build list of xml filenames    
        filelist=glob(foldername+'*')
        for file in filelist:
            #Represent classes as integers
            y.append(idx)
            #Load image
            image=Image.open(file)
            #store as np.array
            X.append(np.array(image))

    X=np.array(X)
    y=np.array(y)

    generate_pickle_files(X,y,y_names)
    return X, y, y_names

if __name__ == '__main__':    
    test=r"G:\Downloads\test"
    read_data(test)