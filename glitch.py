from PIL import Image
import numpy as np

def generate_glitch(width=250, height=122):
    arr = np.random.choice([0, 255], (height, width)).astype('uint8')
    return Image.fromarray(arr, 'L').convert('1')
