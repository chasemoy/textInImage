# Chase Moynihan
# CPSC 353
# Project 1 Text In Image
# 10/18/17

from PIL import Image

"""
---------------------------
ENCODING PORTION OF PROJECT
---------------------------
WORK IN PROGRESS
---------------------------
"""
# change pathway for image file
image_to_encode = Image.open("/Users/chasemoynihan/Downloads/Prince_of_Peace.jpg")

width, height = image_to_encode.size                               # get width and height for image size
num_of_pixels = width * height                                     # number of pixels in image
num_of_least_sig_bits = num_of_pixels * 3                          # number of least sig bits in image
max_num_of_bits_in_message = num_of_least_sig_bits - 33            # max number of bits that can be in message
max_num_of_chars_in_message = num_of_least_sig_bits//8             # max number of char's in message

message_to_encode = input("Please enter the message you wish to encode: ")
print("You entered: ", message_to_encode)
message_size_in_bytes = len(message_to_encode)                     # number of characters in message
num_of_bits_to_encode = message_size_in_bytes * 8                  # number of bits to encode in picture
num_of_pixels_to_update_in_image = num_of_bits_to_encode//3
"""
--------------------
function definitions
--------------------
"""

# pixel_access_object = image_copy.load()                          # used to access pixel data

def getlengthbinary(numberofbits):
    return '{0:032b}'.format(numberofbits)


def getmessagebinary(messagetoencode):
    message = ""
    for c in messagetoencode:
        message = message + ('{0:08b}'.format(ord(c)))        # ord for getting the ascii value of the string character
    return message


def encrypt(copy_of_image_temp, message_length_in_binary, message_to_encode_in_binary):
    copy_of_image = copy_of_image_temp.rotate(180)
    rgb_data_image_copy = list(copy_of_image.getdata())
    new_pixel_list = []  # list of new pixel data
    newer_pixel_list = []

    first_counter = 0
    for d in range(0, 11):
        for values in rgb_data_image_copy[d]:                    # was rgb_data_image_copy[i]
            values = '{0:08b}'.format(values)                    # getting rgb value in binary
            temp = message_length_in_binary[first_counter]       # next bit to encode
            new_pixel = values[:6] + temp
            new_pixel_list.append(new_pixel)
        first_counter += 1

    # converting binary into int values for rgb
    rgb_pixel_data_in_decimal = []
    for x in range(0, len(new_pixel_list)):
        int_rgb = int(new_pixel_list[x], 2)
        rgb_pixel_data_in_decimal.append(int_rgb)

    # trying to get message data
    new_counter = 0
    for k in range(12, num_of_pixels_to_update_in_image):
        for values in rgb_data_image_copy[k]:
            values = '{0:08b}'.format(values)
            temp = message_to_encode_in_binary[new_counter]
            newer_pixel = values[:6] + temp
            newer_pixel_list.append(newer_pixel)
            new_counter += 1

    for x in range(12, len(newer_pixel_list)):                   # was len(message_to_encode)
        int_rgb_two = int(newer_pixel_list[x], 2)
        rgb_pixel_data_in_decimal.append(int_rgb_two)

    copy_of_image.putdata(rgb_pixel_data_in_decimal)
    copy_of_image = copy_of_image.rotate(180)
    copy_of_image.save("encryptedimage.png")


if message_size_in_bytes > max_num_of_chars_in_message:
    print("Message is too long.")
else:
    bin_len = getlengthbinary(num_of_bits_to_encode)
    mess_bin = getmessagebinary(message_to_encode)
    encrypt(image_to_encode, bin_len, mess_bin)

"""
------------------
DECODING THE IMAGE
------------------
"""

# im = Image.open("/Users/chasemoynihan/Downloads/testImage.png")
# change pathway for image file
im = Image.open("testImage.png")
im = im.rotate(180)
rgb_data = list(im.getdata())

"""
------------------------
Geting length of message
------------------------
"""

length_in_bits = []
for i in range(11):                                                 # loop through every rgb tuple
    for rgb in rgb_data[i]:                                         # loop through each r g and b value
        rgb = '{0:08b}'.format(rgb)                                 # convert to binary & left pad each val with 0's
        length_in_bits.append(rgb)                                  # add val's to length_info

length_info = length_in_bits[:32]                                   # only use first 32 values

least_significant = ""                                              # used to store least significant bits
for binary in length_info:
    least_significant = least_significant + binary[-1]              # add up least significant bits together

"""
-----------------------------
Extracting message from image
-----------------------------
"""

text_length = int(least_significant, 2)                             # converting length of message into int
print(text_length)
count = 11
message = []
while count < text_length and count < len(rgb_data):                # looping through message and storing least sig bits
    for rgb in rgb_data[count]:
        rgb = '{0:08b}'.format(rgb)                                 # left padding with zero's
        char = rgb[-1]                                              # getting leas significant bit
        message.append(char)
    count += 1

"""
----------------
Decoding message
----------------
"""

# combining least significant bits into 8 bit chunks
combined_bit_data = []
for i in range(0, text_length, 8):
    data_chunk = message[i:i+8]                                     # pushing together 8 bits of data
    combined_bit_data.append(data_chunk)

# combining char's into strings
char_to_string_data = []
for i in range(0, len(combined_bit_data)):
        combined_data = ''.join(combined_bit_data[i])               # combining 8 char's into one string
        char_to_string_data.append(combined_data)

# converting strings into binary
string_to_bin_data = []
for i in range(0, len(char_to_string_data)):
    bin_data = int(char_to_string_data[i], 2)                       # converting string's into binary
    string_to_bin_data.append(bin_data)

# converting int's into char's
decoded_message = ""
for i in range(0, len(string_to_bin_data)):
    character = str(chr(string_to_bin_data[i]))                     # converting binary into ascii values
    decoded_message = decoded_message + character
print(decoded_message)