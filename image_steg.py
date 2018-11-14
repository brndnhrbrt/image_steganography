import sys
import math
import getopt
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

def encode_image(image_path, output_name, message):
    encoded_message = string_to_bin(message)
    input_image = Image.open(image_path)
    pixels = input_image.load()
    x_size = input_image.size[0]
    y_size = input_image.size[1]

    if x_size < (len(encoded_message) % max_bits + 1):
        print 'image too small'
        return False
    
    if y_size < max_bits:
        print 'image too small'
        return False

    message_array = [encoded_message[i:i+max_bits] for i in range(0, len(encoded_message), max_bits)]
    for x in range(0, len(message_array)):
        for y in range(0, len(message_array[x])):
            current_char = message_array[x][y]
            if current_char == '1':
                new_val = 0
                if pixels[x,y][0] == 255:
                    new_val = pixels[x,y][0] - 1
                else:
                    new_val = pixels[x,y][0] + 1
                new_tuple = (new_val, pixels[x,y][1], pixels[x,y][2], pixels[x,y][3])
                pixels[x,y] = new_tuple
    
    flag_val = 0
    final_x = len(message_array)
    if pixels[final_x,0][0] > 252:
        flag_val = pixels[final_x,0][0] - 3
    else:
        flag_val = pixels[final_x,0][0] + 3

    new_tuple = (flag_val, pixels[final_x,0][1], pixels[final_x,0][2], pixels[final_x,0][3])
    pixels[x,y] = new_tuple
    
    input_image.save(output_name)
    return True

def decode_image(original_image_name, encoded_image_name):
    encoded_message = ''
    original_image = Image.open(original_image_name)
    encoded_image = Image.open(encoded_image_name)
    original_pixels = original_image.load()
    encoded_pixels = encoded_image.load()
    x_size = original_image.size[0]

    if original_image.size != encoded_image.size:
        print 'images are not compatible'
        return False
    
    for x in range(0, x_size):
        if abs(original_pixels[x,0][0] - encoded_pixels[x,0][0]) == 3:
            return encoded_message
        else:
            for y in range(0, max_bits):
                if original_pixels[x,y][0] != encoded_pixels[x,y][0]:
                    encoded_message = encoded_message + '1'
                else:
                    encoded_message = encoded_message + '0'
    return False

def help():
    print 'help'
    sys.exit(0)

def main():
    encode_mode = False
    decode_flag = False
    input_file_path = ''
    output_file_path = ''
    decode_file_path = ''
    key_file_path = ''
    message = ''

    if not len(sys.argv[1:]):
        help()
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'he:o:m:d:k:',
        ['help', 'encode', 'message', 'decode'])
    except getopt.GetoptError as err:
        print str(err)
        help()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
        elif opt in ('-e', '--encode'):
            encode_mode = True
            input_file_path = arg
        elif opt in ('-o', '--output'):
            output_file_path = arg
        elif opt in ('-m', '--message'):
            message = arg
        elif opt in ('-d', '--decode'):
            decode_file_path = arg
            decode_flag = True
        elif opt in ('-k', '--key'):
            key_file_path = arg
        else:
            assert False, 'invalid parameter'
    
    if decode_flag and encode_mode:
        print 'invalid parameters'
        help()
    elif encode_mode and (not len(message) or not len(output_file_path)):
        print 'invalid parameters'
        help()
    
    if encode_mode:
        print 'encoding image with your message'
        encode_image(input_file_path, output_file_path, message)
        print 'complete'
    elif decode_flag and len(key_file_path):
        decoded_message = decode_image(key_file_path, decode_file_path)
        if decoded_message:
            print decoded_message
        else:
            print 'decoding failed'
    else:
        print 'invalid parameters'
        help()

print 'message: test'
print string_to_bin('test')
print bin_to_string(string_to_bin('test'))