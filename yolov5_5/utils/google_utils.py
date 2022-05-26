# Google utils: https://cloud.google.com/storage/docs/reference/libraries

import os
import platform
import subprocess
import time
from pathlib import Path

import requests
import torch


def gsutil_getsize(url=''):
    # gs://bucket/file size https://cloud.google.com/storage/docs/gsutil/commands/du
    s = subprocess.check_output(f'gsutil du {url}', shell=True).decode('utf-8')
    return eval(s.split(' ')[0]) if len(s) else 0  # bytes


def attempt_download(file, repo='ultralytics/yolov5'):
    model_dict = {'yolov5s.pt': '15HvL10tbrgiEIfu8ZYeg35ya7R4kfZmG',
                  'yolov5m.pt': '1v1Ju8Kk9nKqXKs06_zirrL2sIFafIYzc',
                  'yolov5l.pt': '15faQsp59wAV6FvvZq_8ho5BOPMAAzHmU'
                  }
    file = Path(str(file).strip().replace("'", ''))
    if file.name in model_dict.keys() and not file.exists():
        os.system(f"sh weights/download_weights.sh {model_dict[file.name]} {file}")
    # # Attempt file download if does not exist
    # file = str(file).strip().replace("'", '').lower()
    #
    # models = ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt',
    #           'sdd_yolov5s.pt', 'sdd_yolov5m.pt', 'sdd_yolov5l.pt', 'sdd_yolov5x.pt']  # available models
    # d = {'yolov5s.pt': '1R5T6rIyy3lLwgFXNms8whc-387H0tMQO',
    #      'yolov5m.pt': '1vobuEExpWQVpXExsJ2w-Mbf3HJjWkQJr',
    #      'yolov5l.pt': '1hrlqD1Wdei7UT4OgT785BEk1JwnSvNEV',
    #      'yolov5x.pt': '1mM8aZJlWTxOg7BZJvNUMrTnA2AbeCVzS',
    #      'sdd_yolov5s.pt': '13tTDUQzFO37AVXE2_KAwuVhpZykuDEDt',
    #      'sdd_yolov5m.pt': '1qRJ7oSY2qbcqa1v-0ZnnW_GvVIlqtzoX',
    #      'sdd_yolov5l.pt': '1Z1bS64QxOyqIYkElW_ZoXW8v_JkxuycK',
    #      'sdd_yolov5x.pt': '17XheuE4gyuDY-JDTcOKxTHE5PTDfYlAY'}
    # if file in models and not Path(file).exists():
    #     r = gdrive_download(id=d[file], file=file) if file in d else 1
    #     if r == 0 and Path(file).exists() and os.path.getsize(file) > 1E6:  # check
    #         return
    # try:
    #     response = requests.get(f'https://api.github.com/repos/{repo}/releases/latest').json()  # github api
    #     assets = [x['name'] for x in response['assets']]  # release assets, i.e. ['yolov5s.pt', 'yolov5m.pt', ...]
    #     tag = response['tag_name']  # i.e. 'v1.0'
    # except:  # fallback plan
    #     assets = ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']
    #     tag = subprocess.check_output('git tag', shell=True).decode().split()[-1]
    #
    # name = file.name
    # if name in assets:
    #     msg = f'{file} missing, try downloading from https://github.com/{repo}/releases/'
    #     redundant = False  # second download option
    #     try:  # GitHub
    #         url = f'https://github.com/{repo}/releases/download/{tag}/{name}'
    #         print(f'Downloading {url} to {file}...')
    #         torch.hub.download_url_to_file(url, file)
    #         assert file.exists() and file.stat().st_size > 1E6  # check
    #     except Exception as e:  # GCP
    #         print(f'Download error: {e}')
    #         assert redundant, 'No secondary mirror'
    #         url = f'https://storage.googleapis.com/{repo}/ckpt/{name}'
    #         print(f'Downloading {url} to {file}...')
    #         os.system(f'curl -L {url} -o {file}')  # torch.hub.download_url_to_file(url, weights)
    #     finally:
    #         if not file.exists() or file.stat().st_size < 1E6:  # check
    #             # file.unlink(missing_ok=True)  # remove partial downloads
    #             os.remove(file) if os.path.exists(file) else None  # remove partial downloads
    #             print(f'ERROR: Download failure: {msg}')
    #         print('')
    #         return


def gdrive_download(id='16TiPfZj7htmTyhntwcZyEEAejOUxuT6m', file='tmp.zip'):
    # Downloads a file from Google Drive. from yolov5.utils.google_utils import *; gdrive_download()
    t = time.time()
    file = Path(file)
    cookie = Path('cookie')  # gdrive cookie
    print(f'Downloading https://drive.google.com/uc?export=download&id={id} as {file}... ', end='')
    if file.exists():
        file.unlink()  # remove existing file
    if cookie.exists():
        cookie.unlink()  # remove existing cookie

    # Attempt file download
    out = "NUL" if platform.system() == "Windows" else "/dev/null"
    os.system(f'curl -c ./cookie -s -L "drive.google.com/uc?export=download&id={id}" > {out}')
    if os.path.exists('cookie'):  # large file
        s = f'curl -Lb ./cookie "drive.google.com/uc?export=download&confirm={get_token()}&id={id}" -o {file}'
    else:  # small file
        s = f'curl -s -L -o {file} "drive.google.com/uc?export=download&id={id}"'
    r = os.system(s)  # execute, capture return
    cookie.unlink(missing_ok=True)  # remove existing cookie

    # Error check
    if r != 0:
        file.unlink(missing_ok=True)  # remove partial
        print('Download error ')  # raise Exception('Download error')
        return r

    # Unzip if archive
    if file.suffix == '.zip':
        print('unzipping... ', end='')
        os.system(f'unzip -q {file}')  # unzip
        file.unlink()  # remove zip to free space

    print(f'Done ({time.time() - t:.1f}s)')
    return r


def get_token(cookie="./cookie"):
    with open(cookie) as f:
        for line in f:
            if "download" in line:
                return line.split()[-1]
    return ""

# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     # Uploads a file to a bucket
#     # https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
#
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)
#
#     blob.upload_from_filename(source_file_name)
#
#     print('File {} uploaded to {}.'.format(
#         source_file_name,
#         destination_blob_name))
#
#
# def download_blob(bucket_name, source_blob_name, destination_file_name):
#     # Uploads a blob from a bucket
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)
#
#     blob.download_to_filename(destination_file_name)
#
#     print('Blob {} downloaded to {}.'.format(
#         source_blob_name,
#         destination_file_name))
