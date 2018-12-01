import sys
import math
import getopt
from PIL import Image

max_bits = 9
algo_key = 1

def prime_check(n):
    n = abs(int(n))
    if n < 2:
        return False
    if n == 2:
        return True
    if not n & 1:
        return False
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False
    return True

def find_nearest_prime(n):
    while n < 255:
        if prime_check(n):
            return n
        else:
            n += 1
    while n > 0:
        if prime_check(n):
            return n
        else:
            n -= 1
    return 83

def chunk(input_string):
    final_arr = []
    for i in xrange(0, len(input_string), 3):
        sub_arr = []
        sub_arr.append(input_string[i])
        if len(input_string) > i+1:
            sub_arr.append(input_string[i+1])
        if len(input_string) > i+2:
            sub_arr.append(input_string[i+2])
        final_arr.append(sub_arr)
    
    return final_arr

def unchunk(input_arr):
    output_string = ''
    for i in xrange(0, len(input_arr)):
        for j in xrange(0, len(input_arr[i])):
            output_string = output_string + input_arr[i][j]
    return output_string

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

def check_all_vals_for_prime(vals):
    limit = 3
    for x in range(0, limit):
        if not prime_check(vals[x]):
            return False
    return True

def find_non_prime(odd, n):
    if odd:
        compare = 0
    else:
        compare = 1
    while n > 0:
        if n % 2 != compare and not prime_check(n):
            return n
        else:
            n -= 1
    while n < 255:
        if n % 2 != compare and not prime_check(n):
            return n
        else:
            n += 1

def encode_image(image_name, output_image, message):
    encoded_message = string_to_bin(message)
    chunk_arr = chunk(encoded_message)
    input_image = Image.open(image_name)
    pixels = input_image.load()
    x_size = input_image.size[0]
    y_size = input_image.size[1]
    max_msg_size = ((x_size * y_size * 3)) - 1
    y_chunk = -1
    final_idex = len(chunk_arr) - 1

    if max_msg_size <= len(encoded_message):
        print 'ERROR: image too small'
        print 'image size:',[x_size, y_size]
        print 'max bits: ', max_msg_size
        print 'current message size:', len(encoded_message)
        return False
    else:
        print 'image size:',[x_size, y_size]
        print 'max bits: ', max_msg_size
        print 'current message size:', len(encoded_message)

    if len(chunk_arr[final_idex]) < 3:
        for x in range(0, 3 - len(chunk_arr[final_idex])):
            chunk_arr[final_idex].append('2')
    else:
        chunk_arr.append(['2', '2', '2'])

    for x in range(0, len(chunk_arr)):
        current_x = x % x_size
        if current_x == 0:
            y_chunk += 1
        current_y = y_chunk
        for y in range(0, len(chunk_arr[x])):
            current_char = chunk_arr[x][y]
            new_val = -1
            val_arr = []
            if current_char == '1':
                if pixels[current_x, current_y][y] == 255:
                    new_val = pixels[current_x, current_y][y] - 1
                else:
                    if pixels[current_x, current_y][y] % 2 != 0:
                        new_val = find_non_prime(False, pixels[current_x, current_y][y] + 1)
                    else:
                        new_val = find_non_prime(False,pixels[current_x, current_y][y])
            elif current_char == '2':
                new_val = find_nearest_prime(pixels[current_x, current_y][y])        
            else:
                if pixels[current_x, current_y][y] == 255:
                    new_val = pixels[current_x, current_y][y]
                else:
                    if pixels[current_x, current_y][y] % 2 == 0:
                       new_val = find_non_prime(True, pixels[current_x, current_y][y])
                    else:
                        new_val = find_non_prime(True, pixels[current_x, current_y][y])
                
            for z in range(0, len(pixels[current_x, current_y])):
                if z == y:
                    val_arr.append(new_val)
                else:
                    val_arr.append(pixels[current_x, current_y][z])
            if len(val_arr) == 4:
                new_tuple = (val_arr[0], val_arr[1], val_arr[2], val_arr[3])
            else:
                new_tuple = (val_arr[0], val_arr[1], val_arr[2])
            pixels[current_x, current_y] = new_tuple

    input_image.save(output_image)
    return True

def decode_image(encoded_image_name):
    encoded_message = ''
    encoded_image = Image.open(encoded_image_name)
    encoded_pixels = encoded_image.load()
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    max_msg_size = ((x_size * y_size * 3))

    y_chunk = -1

    for x in range(0, max_msg_size):
        current_x = x % x_size
        if current_x == 0:
            y_chunk += 1
        current_y = y_chunk
        if check_all_vals_for_prime(encoded_pixels[current_x, current_y]):
            return encoded_message
        for z in range(0, 3):
            try:
                if encoded_pixels[current_x, current_y][z] % 2 == 0:
                    encoded_message = encoded_message + '1'
                else:
                    encoded_message = encoded_message + '0'
            except:
                return False
                
    return False

def help():
    print
    print 'image steganography'
    print 'encoding: python image_steg.py -e <original_image_path> -o <output_path> -m <message> '
    print 'encoding: echo <message> | python image_steg.py -e <original_image_path> -o <output_path>'
    print 'decoding: python image_steg.py -d <encoded_image_path>'
    print
    sys.exit(0)

def main():
    encode_mode = False
    decode_flag = False
    input_file_path = ''
    output_file_path = ''
    decode_file_path = ''
    message = ''

    if not len(sys.argv[1:]):
        help()
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'he:o:m:d:',
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
        else:
            assert False, 'invalid parameter'
    
    if encode_mode and not len(message):
        for line in sys.stdin:
            message = message + line
    
    if decode_flag and encode_mode:
        print 'invalid parameters'
        help()
    elif encode_mode and (not len(message) or not len(output_file_path)):
        print 'invalid parameters'
        help()
    
    if encode_mode:
        print 'encoding image with your message'
        sucess = encode_image(input_file_path, output_file_path, message)
        if sucess:
            print 'encoding complete'
        else:
            print 'encoding failed'        
    elif decode_flag:
        decoded_message = decode_image(decode_file_path)
        if decoded_message:
            print bin_to_string(decoded_message)
        else:
            print 'decoding failed'
    else:
        print 'invalid parameters'
        help()

main()
