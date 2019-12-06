# -*- coding:utf-8 -*-
import numpy as np
from common import get_subBlocks, get_key_sream, combine_img, get_byte_sequence


def image_encryption(img, encryption_key,permutation_key, size=(8, 8)):

    # preprocess
    img_gray = np.array(img)

    # divide image into sub blocks
    res = get_subBlocks(img_gray, size)
    x_num, y_num, block_list = res[0], res[1], res[2]

    # encryption
    stream_key = get_key_sream(encryption_key, len(block_list))
    for i in range(len(block_list)):
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                block_list[i][i_x, i_y] ^= stream_key[i]  # XOR

    # permutation
    byte_sequence = get_byte_sequence(permutation_key, len(block_list))
    permuted_img = []
    for i in byte_sequence:
        permuted_img.append(block_list[i])

    # combine
    res_img = combine_img(permuted_img, x_num, y_num, size)

    return np.uint8(res_img)


def image_decrption(img, eKey, pKey, size=(8, 8)):

    img_gray = np.array(img)

    # divide image into sub blocks
    res = get_subBlocks(img_gray, size)
    x_num, y_num, block_list = res[0], res[1], res[2]

    # recover order
    byte_sequence = get_byte_sequence(pKey, len(block_list))
    ordered_img = []
    for i in range(len(block_list)):
        ordered_img.append(block_list[byte_sequence.index(i)])

    # decryption
    stream_key = get_key_sream(eKey, len(ordered_img))
    for i in range(len(ordered_img)):
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                ordered_img[i][i_x, i_y] ^= stream_key[i]  # XOR

    # combine
    res_img = combine_img(ordered_img, x_num, y_num, size)

    return np.uint8(res_img)



def get_permutation_key(short_key, size):
    box = list(range(size))
    swap_index = 0
    for index in range(size):
        temp = box[index]
        swap_index = (swap_index + box[index] + short_key[index % len(short_key)]) % size
        box[index] = box[swap_index]
        box[swap_index] = temp
    return box








