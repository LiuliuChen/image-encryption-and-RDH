import numpy as np
from bitarray import bitarray
import math


def str2bit_array(s):
    ret = bitarray(''.join([bin(int('1' + hex(c)[2:], 16))[3:] for c in s.encode('utf-8')]))
    return ret


def bit_array2str(bit):
    return bit.tobytes().decode('utf-8')


def list_key2string(key):
    return "".join(['{:02x}'.format(i) for i in key])


def get_subBlocks(img, size):
    x_num = int(np.ceil(img.shape[0] / size[0]))
    y_num = int(np.ceil(img.shape[1] / size[1]))
    out_img = np.zeros((x_num * size[0], y_num * size[1]), dtype=np.int)
    out_img[0:img.shape[0], 0:img.shape[1]] = img[0:img.shape[0], 0:img.shape[1]]
    block_list = []
    for i in range(x_num):
        for j in range(y_num):
            block_list.append(out_img[i * size[0]:(i + 1) * size[0], j * size[1]:(j + 1) * size[1]])
    return x_num, y_num, block_list


def combine_img(block_list, x_num, y_num, size):
    res_img = np.zeros((x_num * size[0], y_num * size[1]), dtype=np.int)
    for i in range(x_num):
        for j in range(y_num):
            res_img[i * size[0]:(i + 1) * size[0], j * size[1]:(j + 1) * size[1]] = block_list[i * x_num + j]
    return res_img


def get_key_sream(eKey, lens):
    s_box = list(range(256))
    # t = [eKey[x % len(eKey)] for x in range(256)]
    j = 0
    for i in range(256):
        j = (j + s_box[i] + eKey[i % len(eKey)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

    key_stream = []
    i = j = 0
    for s in range(lens):
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        key_stream.append(s_box[t])
    return key_stream


def get_byte_sequence(key, lens):
    byte_sequence = list(range(lens))
    temp = 0
    for i in range(lens):
        temp = (temp + byte_sequence[i] + key[i % len(key)]) % lens
        byte_sequence[i], byte_sequence[temp] = byte_sequence[temp], byte_sequence[i]
    return byte_sequence


def get_psnr(img1, img2):
    mse = np.mean((img1 / 255. - img2 / 255.) ** 2)
    if mse < 1.0e-10:
        return 100
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


def get_ec(img_len, block_size):
    additional_bit = pow(int(img_len / block_size), 2)
    return additional_bit / (img_len * img_len)
