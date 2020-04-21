import glob
import numpy as np
from PIL import Image, ImageSequence
Image.MAX_IMAGE_PIXELS = None
gif_list = []
image_list = []
for filename in glob.glob('input/*.*'):
    img = Image.open(filename)
    if img.format == 'GIF':
        size = np.array(
            [np.array(frame.copy().convert('RGBA').getdata(), dtype=np.uint8).reshape(frame.size[1], frame.size[0], 4)
             for frame in ImageSequence.Iterator(img)])
        yk = len(size[0]) * 2
        gn = len(size[0][0]) * 2
        gif_list.append(np.array(
            [np.array(frame.copy().convert('RGBA').resize((gn, yk), Image.LANCZOS).getdata(), dtype=np.uint8).reshape(
                yk, gn, 4)
                for frame in ImageSequence.Iterator(img)]))
    else:
        size = [np.array(img.convert('RGBA'))]
        image_list.append(
            np.array(img.convert('RGBA').resize((len(size[0][0]) * 2, len(size[0]) * 2), Image.LANCZOS), dtype=np.uint8))

a = 0
for x in image_list:
    img = Image.fromarray(x)
    img.save('output/image' + str(a) + '.png')
    a += 1
a = 0
for x in gif_list:
    img = []
    for i in range(len(x)):
        img.append(Image.fromarray(x[i]))
    img[0].save('output/gif' + str(a) + '.gif', save_all=True, append_images=img[1:], loop=0, duration=40)
    a += 1
