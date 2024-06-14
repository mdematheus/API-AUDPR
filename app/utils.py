import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd

def read_barcode(image_path):
    image = cv2.imread(image_path)
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        return barcode_data
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}

def parse_excel(filepath):
    df = pd.read_excel(filepath)
    return df
