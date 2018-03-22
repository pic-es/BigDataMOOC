#!/usr/bin/python

import os
import sys
import urllib2
import urllib
import argparse
import time
import logging
from StringIO import StringIO
import traceback
import re

from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mimg
import numpy as np
from scipy.stats import norm

try:
    from SciServer.SkyServer import getJpegImgCutout
except:
    getJpegImgCutout = None

IMAGE_PIXSCALE = 0.4
IMAGE_SIZE_PX = 64
IMAGE_WIDTH_PX = IMAGE_SIZE_PX
IMAGE_HEIGHT_PX = IMAGE_SIZE_PX
URL = 'http://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale={scale}&width={width}&height={height}'

FOLDER_NAME = 'images/{scale}/{width}x{height}'
FILE_NAME = 'ra{ra}_dec{dec}.jpg'

SAMPLE_SIZE=100
MAX_TRIES = 3

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        logging.info('%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0))
        return ret
    return wrap

def download_image_bytes(ra, dec, scale=IMAGE_PIXSCALE, width=IMAGE_WIDTH_PX, height=IMAGE_HEIGHT_PX):
    n_tries = 0
    while n_tries < MAX_TRIES:
        try:
            url = URL.format(ra=ra, dec=dec, scale=scale, width=width, height=height)
            response = urllib2.urlopen(url)
        except Exception as e:
            logging.error(''.join(traceback.format_exception(*sys.exc_info())))
            n_tries += 1
            if n_tries < MAX_TRIES:
                logging.info('Going to retry')
            else:
                raise Exception('Number of allowed retries exceeded!')

    return response

def download_image_jpg(ra, dec, file_name=None, scale=IMAGE_PIXSCALE, width=IMAGE_WIDTH_PX, height=IMAGE_HEIGHT_PX):

    whole_file_name = get_whole_file_name(ra, dec, file_name, scale, width, height)
    if os.path.exists(whole_file_name):
        print('file already exists: {}'.format(file_name))
    else:
        url = URL.format(ra=ra, dec=dec, scale=scale, width=width, height=height)
        urllib.urlretrieve(url, whole_file_name)

def image_from_bytes(byte_string):

    #return Image.open(StringIO(byte_string))
    return Image.open(byte_string)


def read_and_subsample_csv(csv_file, sample_size=SAMPLE_SIZE):
    df = pd.read_csv(csv_file, low_memory=False)
    print(df)
    return df.sample(sample_size)

def download_and_resize(ra, dec, file_name, scale, width_or, height_or, width_dest, height_dest):

    whole_file_name = get_whole_file_name(ra, dec, file_name, scale, width_dest, height_dest)
    if os.path.exists(whole_file_name):
        print('file already exists: {}'.format(file_name))
    else:
        b = download_image_bytes(ra, dec, scale, width_or, height_or)
        im = image_from_bytes(b)
        dest_size = width_dest, height_dest
        im_res = im.resize(dest_size, Image.ANTIALIAS)
        im_res.save(whole_file_name, 'JPEG')
    
def get_whole_file_name(ra, dec, file_name=None, scale=IMAGE_PIXSCALE, width=IMAGE_WIDTH_PX, height=IMAGE_HEIGHT_PX):

    folder_name = FOLDER_NAME.format(scale=scale, width=width, height=height)
    if file_name is None:
        file_name = FILE_NAME.format(ra=ra, dec=dec)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    whole_file_name = os.path.join(folder_name, file_name)

    return whole_file_name
    

def create_square_images_from_csv(args):

    csv_file = args.or_csv_file
    n_sample = args.n_sample
    scale = args.scale
    size = args.side

    df = pd.read_csv(csv_file, header=0)
    if not n_sample is None:
        df = df.sample(n_sample)
    width=height=size
    for ind, row in df.iterrows():
        ra = row['ra']
        dec = row['dec']
        file_name = '{}.jpg'.format(row['dr7objid'])
        if size>= 64:
            download_image_jpg(ra, dec, file_name, scale, width, height)
        else:
            download_and_resize(ra, dec, file_name, scale, 64, 64, width, height)


def get_image_array(ra, dec, scale=IMAGE_PIXSCALE, width=IMAGE_WIDTH_PX, height=IMAGE_HEIGHT_PX):

    try:
        if getJpegImgCutout is None:
            b = download_image_bytes(ra, dec, scale, width, height)
            im = mimg.imread(b, format='JPEG')
        else:
            im = getJpegImgCutout(ra, dec, scale=scale, width=width, height=height, dataRelease='DR14')
    except Exception as e:
        error_message = str(e)
        if re.search("Requested \(ra, dec\) is outside the SDSS footprint", error_message):
            im = np.zeros((height, width, 3))
        else:
            raise(e)

    return im

def image_array_to_features(im):
    img_gray = np.dot(im[...,:3], [0.299, 0.587, 0.114])
    features = img_gray.flatten()/255.
    return features

def get_features_from_csv(csv_file, scale=IMAGE_PIXSCALE, size=IMAGE_WIDTH_PX):

    df = pd.read_csv(csv_file, header=0)
    width=height=size
    features = {}
    n_rows = len(df)
    for ind, row in df.iterrows():
        logging.debug('Processing row {}/{}'.format(ind + 1, n_rows))
        ra = row['ra']
        dec = row['dec']
        file_name = '{}.jpg'.format(row['dr7objid'])
        im = get_image_array(ra, dec, scale, width, height)
        features[row['dr7objid']] = image_array_to_features(im)

    return features

def plot_features(features, width, height):

    plt.imshow(features.reshape(height, width), cmap=plt.get_cmap('gist_heat'))
    plt.show()


def write_features_csv(features, csv_file, n_features):

    cols = ['F{}'.format(i) for i in range(n_features)]
    df = pd.DataFrame.from_items(features.items(), columns=cols, orient='index')
    df.to_csv(csv_file, index_label='dr7objid')


def split_csv(csv_file, chunksize):

    df = pd.read_csv(csv_file, header=0)
    
    folder = os.path.dirname(csv_file)
    file_base, file_ext = os.path.splitext(os.path.basename(csv_file))

    final_row = 0
    n_rows = len(df)
    n_digits = int(np.log10(n_rows)) + 1
    while final_row < n_rows:
        rows_text = '_{{:0{}}}to{{:0{}}}'.format(n_digits, n_digits)
        dest_file_name = file_base + rows_text.format(final_row + 1, final_row + chunksize) + file_ext
        whole_dest_file = os.path.join(folder, dest_file_name)
        df.iloc[final_row:final_row + chunksize].to_csv(whole_dest_file)
        final_row += chunksize

@timing
def get_features_from_csv_to_csv(or_csv_file, dest_csv_file=None, scale=IMAGE_PIXSCALE, size=IMAGE_SIZE_PX):

    logging.info('Getting features from file {}'.format(or_csv_file))
    if dest_csv_file is None:
        dest_csv_file = 'F_' + or_csv_file
    if os.path.exists(dest_csv_file):
        logging.warning('File {} already exists'.format(dest_csv_file))
    else:
        features =  get_features_from_csv(or_csv_file, scale, size)
        write_features_csv(features, dest_csv_file, size**2)

@timing
def merge_csvs(or_csv_files_list, dest_csv_file):

    if len(or_csv_files_list) > 0:

        fout = open(dest_csv_file,"a")

        for ind, csv_file in enumerate(or_csv_files_list):

            if not os.path.exists(csv_file):
                logging.warning('File does not exist: {}'.format(csv_file))
                continue

            with open(csv_file) as f:
                if ind != 0:
                    f.next()
                for line in f:
                    fout.write(line)

        fout.close()

    else:
        raise Exception('No origin csv files provided')


def plot_sample_images(csv_file, shape):

    width, height = [int(s) for s in shape]

    df = pd.read_csv(csv_file, index_col=0)
    df_sample = df.sample(width*height)
    fig = plt.figure()
    for i in range(width):
        for j in range(height):
            ind = i*height + j
            ax = fig.add_subplot(width, height, ind + 1)
            ax.imshow(df.iloc[ind].as_matrix().reshape(64, 64), cmap=plt.get_cmap('viridis'), interpolation='none')

    plt.show()

def read_sample_from_csv(csv_file, shape):
    width, height = [int(s) for s in shape]
    df = pd.read_csv(csv_file, index_col=0)
    df_sample = df.sample(width*height)

def plot_images_from_array(arr, shape, image_shape=(64, 64)):
    '''images in rows'''
    width, height = [int(s) for s in shape]
    fig = plt.figure()
    for i in range(width):
        for j in range(height):
            ind = i*height + j
            ax = fig.add_subplot(width, height, ind + 1)
            ax.imshow(arr[ind,:].reshape(*image_shape), cmap=plt.get_cmap('gist_heat'), interpolation='none')
    return fig

def define_arguments():
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # parser for the get_features action
    parser_get_features = subparsers.add_parser('get_features', 
        help='''query the SDSS server and build a csv with the features 
        representing the images of the objects in the input csv file''')
    parser_get_features.add_argument('--or_csv_file', '-o', required=True)
    parser_get_features.add_argument('--dest_csv_file', '-d', required=False)
    parser_get_features.add_argument('--scale', '-sc', required=False, default=IMAGE_PIXSCALE)
    parser_get_features.add_argument('--size', '-sz', required=False, default=IMAGE_SIZE_PX)

    # parser for the merge_csvs action
    parser_merge_csvs = subparsers.add_parser('merge_csvs', help='''Brute force csv files merging''')
    parser_merge_csvs.add_argument('--or_csv_file', '-o', required=True)
    parser_merge_csvs.add_argument('--dest_csv_file', '-d', required=False)

    # parser for the plot_sample action
    parser_plot_sample = subparsers.add_parser('plot_sample_images', 
        help='''plot a random sample of images from a features dataset''')
    parser_plot_sample.add_argument('--or_csv_file', '-o', required=True)
    parser_plot_sample.add_argument('--shape', '-s', required=False, default='3,3')
    
    # parser for getting sample jpegs from SDSS
    parser_get_jpegs = subparsers.add_parser('get_jpegs',
        help='Get sample jpeg images from SDSS')
    parser_get_jpegs.add_argument('--or_csv_file', '-o', required=True,
        help='Csv file containing a set of objects')
    parser_get_jpegs.add_argument('--scale', '-s', required=False, type=float,
        default=IMAGE_PIXSCALE, help='image pixelscale')
    parser_get_jpegs.add_argument('--side', '-d', required=False, type=int,
        default=IMAGE_SIZE_PX, help='size of the image side in pixels')
    parser_get_jpegs.add_argument('--n_sample', '-n', required=False, type=int,
        default=100, help='number of sample images to download')
    parser_get_jpegs.set_defaults(func=create_square_images_from_csv)
    
    parser.add_argument('--loglevel', '-l', required=False, default='INFO')

    return parser


if __name__ == '__main__':

    parser = define_arguments()
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=getattr(logging, args.loglevel))

    args.func(args)

    if hasattr(args, 'get_features'):
        get_features_from_csv_to_csv(args.or_csv_file, args.dest_csv_file, args.scale, args.size)
    elif hasattr(args, 'merge_csvs'):
        merge_csvs(args.or_csv_file.split(','), args.dest_csv_file)
    elif hasattr(args, 'plot_sample_images'):
        plot_sample_images(args.or_csv_file, args.shape.split(','))


            
        
    


