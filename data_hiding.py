import numpy as np
from common import *
from bitarray import bitarray


def data_embedding(img, size, eKey, msg):
    img_gray = np.array(img)

    # divide img
    res = get_subBlocks(img_gray, size)
    x_num, y_num, block_list = res[0], res[1], res[2]

    # note location map
    location = []
    for i in range(len(block_list)):
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                if block_list[i][i_x, i_y] == 1 or block_list[i][i_x, i_y] == 254:
                    location.append(0)
                elif block_list[i][i_x, i_y] == 0:
                    location.append(1)
                    block_list[i][i_x, i_y] = 1
                elif block_list[i][i_x, i_y] == 255:
                    location.append(1)
                    block_list[i][i_x, i_y] = 254

    # no space
    if len(location) == 0:
        return False

    # generate embed key
    embed_key = get_key_sream(eKey, len(eKey) * len(block_list))

    # embed
    msg_bits = str2bit_array(msg).tolist()
    for i in range(len(msg_bits)):
        msg_bits[i] = 1 if msg_bits[i] else 0
    location.extend(msg_bits)
    embed_bits = location
    embed_bits.append(1)

    for i in range(len(block_list)):
        # produce peak pixel
        peak = get_byte_sequence(embed_key[i * len(eKey):(i + 1) * len(eKey)], size[0] * size[1])[0]
        peak_x = peak // size[0]
        peak_y = peak - peak_x * size[0]
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                if i_x == peak_x and i_y == peak_y:
                    continue
                diff_value = block_list[i][i_x, i_y]-block_list[i][peak_x, peak_y]
                if diff_value < -1:
                    block_list[i][i_x, i_y] -= 1
                elif diff_value == -1:
                    if len(embed_bits) > 0:
                        block_list[i][i_x, i_y] -= embed_bits.pop(0)
                elif diff_value == 0:
                    if len(embed_bits) > 0:
                        block_list[i][i_x, i_y] += embed_bits.pop(0)
                elif diff_value > 0:
                    block_list[i][i_x, i_y] += 1

    # combine img
    res_img = combine_img(block_list, x_num, y_num, size)

    return np.uint8(res_img)


def data_extracting(img, eKey, size):

    img_gray = np.array(img)

    # divide img
    res = get_subBlocks(img_gray, size)
    x_num, y_num, block_list = res[0], res[1], res[2]

    # generate embed key
    embed_key = get_key_sream(eKey, len(eKey) * len(block_list))

    # extract msg
    embed_bits = []
    for i in range(len(block_list)):
        # produce peak pixel
        peak = get_byte_sequence(embed_key[i * len(eKey):(i + 1) * len(eKey)], size[0] * size[1])[0]
        peak_x = peak // size[0]
        peak_y = peak - peak_x * size[0]
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                if i_x == peak_x and i_y == peak_y:
                    continue
                diff_value = block_list[i][i_x, i_y] - block_list[i][peak_x, peak_y]
                if diff_value == 0 or diff_value == -1:
                    embed_bits.append(0)
                if diff_value == 1 or diff_value == -2:
                    embed_bits.append(1)
                if diff_value > 0:
                    block_list[i][i_x, i_y] -= 1
                if diff_value < -1:
                    block_list[i][i_x, i_y] += 1

    for i in range(len(block_list)):
        for i_x in range(size[0]):
            for i_y in range(size[1]):
                if block_list[i][i_x, i_y] == 254:
                    temp = embed_bits.pop(0)
                    block_list[i][i_x, i_y] = 255 if temp == 1 else 254
                elif block_list[i][i_x, i_y] == 1:
                    temp = embed_bits.pop(0)
                    block_list[i][i_x, i_y] = 0 if temp == 1 else 1

    while embed_bits.pop() != 1:
        pass

    # combine img
    res_img = combine_img(block_list, x_num, y_num, size)

    return np.uint8(res_img), bit_array2str(bitarray(embed_bits))



