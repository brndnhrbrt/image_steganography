import math
from PIL import Image

max_bits = 7

def string_to_bin(string):
    bin_string = ''
    for c in string:
        ascii_num = ord(c)
        bin_num = bin(ascii_num)[2:].zfill(max_bits)
        bin_string = bin_string + str(bin_num)
    return bin_string

def bin_to_string(bin_string):
    string_array = [bin_string[i:i+max_bits] for i in range(0, len(bin_string), max_bits)]
    message_string = ''
    for b in string_array:
        msg_val = 0
        for i in range(0, len(b)):
            if b[i] == '1':
                msg_val = msg_val + math.pow(2, max_bits - (i +1))
        message_string = message_string + chr(int(msg_val))
    return message_string

def encode_image(image_path, message):
    encoded_message = string_to_bin(message)
    input_image = Image.open(image_path)
    pixels = input_image.load()
    x_size = input_image.size[0]
    y_size = input_image.size[1]

    if x_size < (len(encoded_message) % 8 + 1):
        print 'image too small'
        return False
    
    if y_size < max_bits:
        print 'image too small'
        return False

    

print 'message: test'
print string_to_bin('test')
print bin_to_string(string_to_bin('test'))