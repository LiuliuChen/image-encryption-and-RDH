import encryptor
import data_hiding
import cv2
import numpy as np
import common


pic = cv2.imread('data/lena.bmp', 0)
block_size = [(3, 3), (4, 4), (16, 16), (32, 32)]
for i in range(5):
    block_size.extend(block_size)
for size in block_size:
    # encrypt image
    encryption_key = list((np.random.permutation(128)))
    permutation_key = list((np.random.permutation(128)))
    print('encyption key:', common.list_key2string(encryption_key))
    print('permutation key:', common.list_key2string(permutation_key))
    encypted_img = encryptor.image_encryption(pic, encryption_key, permutation_key, size)

    # embed data
    embedding_key = list((np.random.permutation(128)))
    print('embedding key:', common.list_key2string(embedding_key))
    msg = 'plane-walker aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    embedded_img = data_hiding.data_embedding(encypted_img, size, embedding_key, msg)

    cv2.imwrite('result/lena_encrypted.bmp', embedded_img)

    # extract data
    extracted_img, data, max_embedded_bits = data_hiding.data_extracting(embedded_img, embedding_key, size)
    print('extracted msg: ', data)

    # decrypt image
    decrypted_img = encryptor.image_decrption(embedded_img, encryption_key, permutation_key, size=size)
    decrypted_img = decrypted_img[0:pic.shape[0], 0:pic.shape[1]]

    cv2.imwrite('result/lena_decryted.bmp', decrypted_img)


    cv2.namedWindow('input', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('input', decrypted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # calculate PSNR
    psnr = common.get_psnr(pic, decrypted_img)
    print(size, psnr)

    psnr = common.get_psnr(embedded_img, extracted_img)
    print('aaa', psnr)

    with open('result/lena_psnr.txt', 'a') as f:
        f.write(str(psnr))
        f.write('\n')

    # calculate EC
    # print('max', max_embedded_bits)
    ec = max_embedded_bits / (pic.shape[0]*pic.shape[1])
    print('ec', ec)
    with open('result/lena_ec.txt', 'a') as f:
        f.write(str(ec))
        f.write('\n')

common.draw_ec_psnr('result/lena_ec.txt', 'result/lena_psnr.txt', 'lena')

