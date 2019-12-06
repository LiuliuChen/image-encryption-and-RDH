import encryptor
import data_hiding
import cv2
import numpy as np
import common

pic = cv2.imread('lena.bmp')
img_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

# encrypt image
encryption_key = list((np.random.permutation(128)))
permutation_key = list((np.random.permutation(128)))
print('encyption key:', common.list_key2string(encryption_key))
print('permutation key:', common.list_key2string(permutation_key))
encypted_img = encryptor.image_encryption(img_gray, encryption_key, permutation_key, (2, 2))

# embed data
embedding_key = list((np.random.permutation(128)))
print('embedding key:', common.list_key2string(embedding_key))
msg = 'ahahahah'
embedded_img = data_hiding.data_embedding(encypted_img, (2, 2), embedding_key, msg)

# extract data
extracted_img = data_hiding.data_extracting(embedded_img, embedding_key, (2, 2))
print('extracted msg: ', extracted_img[1])

# decrypt image
decrypted_img = encryptor.image_decrption(extracted_img[0], encryption_key, permutation_key, size=(2, 2))

# cv2.namedWindow('input', cv2.WINDOW_AUTOSIZE)
cv2.imshow('input', decrypted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# draw psnr
img_psnr = common.get_psnr(pic, decrypted_img)