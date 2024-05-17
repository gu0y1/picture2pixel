import numpy as np
import imageio.v2 as imageio
from PIL import Image

def process_image(filename, width, height, r):
    img = imageio.imread(filename)
    img = np.array(Image.fromarray(img).resize((width, height)))

    if img.shape[2] == 4:
        img = img[:, :, :3]

    if r == 0:
        return img

    R_channel = img[:, :, 0]
    G_channel = img[:, :, 1]
    B_channel = img[:, :, 2]

    U_R, S_R, Vt_R = np.linalg.svd(R_channel, full_matrices=False)
    U_G, S_G, Vt_G = np.linalg.svd(G_channel, full_matrices=False)
    U_B, S_B, Vt_B = np.linalg.svd(B_channel, full_matrices=False)

    R_reconstructed = np.dot(U_R[:, :r], np.dot(np.diag(S_R[:r]), Vt_R[:r, :]))
    G_reconstructed = np.dot(U_G[:, :r], np.dot(np.diag(S_G[:r]), Vt_G[:r, :]))
    B_reconstructed = np.dot(U_B[:, :r], np.dot(np.diag(S_B[:r]), Vt_B[:r, :]))

    R_reconstructed = np.clip(R_reconstructed, 0, 255)
    G_reconstructed = np.clip(G_reconstructed, 0, 255)
    B_reconstructed = np.clip(B_reconstructed, 0, 255)

    reconstructed_image = np.zeros(img.shape)
    reconstructed_image[:, :, 0] = R_reconstructed
    reconstructed_image[:, :, 1] = G_reconstructed
    reconstructed_image[:, :, 2] = B_reconstructed

    return np.clip(reconstructed_image, 0, 255).astype(np.uint8)

def apply_floyd_steinberg_dithering(image):
    image = image.astype(np.float64)
    h, w, c = image.shape
    for y in range(h):
        for x in range(w):
            old_pixel = image[y, x].copy()
            new_pixel = np.round(old_pixel / 255 * 31) * (255 / 31)
            image[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            if x + 1 < w:
                image[y, x + 1] += quant_error * 7 / 16
            if x - 1 >= 0 and y + 1 < h:
                image[y + 1, x - 1] += quant_error * 3 / 16
            if y + 1 < h:
                image[y + 1, x] += quant_error * 5 / 16
            if x + 1 < w and y + 1 < h:
                image[y + 1, x + 1] += quant_error * 1 / 16
    return np.clip(image, 0, 255).astype(np.uint8)
