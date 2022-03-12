#!/usr/bin/env python
# coding: utf-8

# Import packages
import numpy as np
import zipfile
import tarfile
import os
from pathlib import Path
import warnings
import pandas as pd
import csv
import seaborn as sns
import sys
import argparse


# set up argument parser
help_message = ('Unpacks HCP zip file, joins the 100 parcellation '
                'resting-state matrix inside this HCP zip and joins it '
                'with the HCP behavioral data. Outputs this joined data, '
                'as well as Train and Test subsets of the data as csv files.')

parser = argparse.ArgumentParser(description=help_message)
parser.add_argument('HCP_zip', help='Path to the HCP netmats zip file '
                    '\(HCP1200_Parcellation_Timeseries_Netmats.zip\) '
                    'which can be downloaded at '
                    'https://db.humanconnectome.org/data/projects/HCP_1200 '
                    'by clicking the link named '
                    '"1003 Subjects, recon r177 + r227, PTN Release" '
                    '(you\'ll need to set up and account and accept their '
                    'data use terms before downloading).')

parser.add_argument('HCP_beh', help='Path to the HCP behavioral data file '
                    '\(behavioral_data.csv\) '
                    'which can be downloaded at '
                    'https://db.humanconnectome.org/data/projects/HCP_1200 '
                    'by clicking the link named '
                    '"Behavioral Data".')
                    
parser.add_argument("output_dir", help='Path to directory to output the joined '
                    'netmat and behavioral data csv files.')
args = parser.parse_args()


# paths set in arguments
HCP_zip = args.HCP_zip
beh_csv = args.HCP_beh
data_dir = args.output_dir

# paths that need to be set
# data_dir = '/mnt/f/portfolio/data/HCPrest'
# HCP_zip = os.path.join(data_dir,'HCP1200_Parcellation_Timeseries_Netmats.zip')
# beh_csv = os.path.join(data_dir,'behavioral_data.csv')

# paths that don't need to be set
mat_dir = os.path.splitext(HCP_zip)[0]
mat_zip = os.path.join(mat_dir,'HCP_PTN1200','netmats_3T_HCP1200_MSMAll_ICAd100_ts2.tar.gz')
netmat_txt = os.path.join(mat_dir,'netmats','3T_HCP1200_MSMAll_d100_ts2','netmats2.txt')
netmatBeh_csv = os.path.join(data_dir,'netmatBeh.csv')
netmatBehTrain_csv =  os.path.join(data_dir,'netmatBehTrain.csv')
netmatBehTest_csv =  os.path.join(data_dir,'netmatBehTest.csv')

# check if inputs exist
if not os.path.isfile(HCP_zip):
    raise Exception(f'{HCP_zip} not found')
if not os.path.isfile(beh_csv):
    raise Exception(f'{beh_csv} not found')

    
# unzip HCP folder, unless already unzipped
if not os.path.isfile(mat_zip):
    with zipfile.ZipFile(HCP_zip, 'r') as zip_file:
        zip_file.extractall(mat_dir)
else:
    warnings.warn(f'File {mat_zip} already exists. Skipping unzipping '
                  f'of {HCP_zip}')

# unzip netmats
if not os.path.isfile(netmat_txt):
    # open file
    file = tarfile.open(mat_zip)
    # extracting file
    file.extractall(mat_dir)
else:
    warnings.warn(f'\n\nFile {netmat_txt} already exists. Skipping unzipping '
                  f'of {mat_zip}')

# read in behavioral file
beh_df = pd.read_csv(beh_csv, index_col=0)

# read in subject numbers from text file that comes with the data
subjectIDs_txt = os.path.join(mat_dir,'HCP_PTN1200','subjectIDs.txt')
with open(subjectIDs_txt, "r") as txtf:
    subjects=[line.strip() for line in txtf]

# read in connectivity data, and join with subject numbers
netmat_df = pd.read_csv(netmat_txt, sep=' ', header=None)
netmat_df.index = np.int64(subjects)
netmat_df.index.rename('Subject', inplace=True)
netmat_df.drop(netmat_df.columns[[0,len(netmat_df.columns)-1]], axis=1, 
               inplace=True)
# dummy code gender
beh_df['Female'] = beh_df['Gender'].map({'M':0,'F':1})

# join brain data with behavioral
df = netmat_df.join(beh_df)
# write df to file
df.to_csv(netmatBeh_csv)

# split data into training and test set
df_test = df.sample(n=150,replace=False,random_state=99)
df_test.to_csv(netmatBehTest_csv)
df_train = pd.concat([df,df_test,df_test]).drop_duplicates(keep=False)
df_train.to_csv(netmatBehTrain_csv)

print(f'\nTraining data output to: {netmatBehTrain_csv}')
print(f'Number of rows in training data {len(df_train)}')

print(f'\nTraining data output to: {netmatBehTest_csv}')
print(f'Number of rows in training data {len(df_test)}')

