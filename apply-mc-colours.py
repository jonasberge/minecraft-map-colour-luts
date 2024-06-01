from clut.clut.clut import CLUT
from PIL import Image

APPLY_LUT = 'Agfa Vista 200.png'
TO_IMAGE = 'zenith-shader-lut.png'
TARGET_FILE = 'zenith-shader-lut-agfa-vista-200.png'

clut = CLUT(APPLY_LUT)
im_out = clut(TO_IMAGE)
im_out = Image.fromarray(im_out)
im_out.save(TARGET_FILE)
