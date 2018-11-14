# Image Steganography

## Hide messages in plain sight with steganography.

This python script manipulates pixel color values to hide any ascii message 'inside' an image. To decode the message the decoder will need the original image as a key and the encoded image to reveal the message.

## Requirements

Requires Python 2.7 and the pillow library

## Usage

Help:
```
python image_steg.py -h
```

Encoding:
```
python image_steg.py -e <original_image_path> -o <output_path> -m <message>
```

Decoding:
```
decoding: python image_steg.py -d <encoded_image_path> -o <original_image_path>
```

## Example

Directory Structure

```
image_steg.py
images/
    input_image.png
```

#### Encode
```
python image_steg.py -e ./images/input_image.png -o ./images/output_image.png -m 'Hello, world!'
```

New Directory Structure

```
image_steg.py
images/
    input_image.png
    output_image.png
```

#### Decode
```
python image_steg.py -d ./images/output_image.png -k ./images/input_image.png
```

Output
```
Hello, world!
```

## Errors

To encode a message with _N_ number of characters you must have an image with dimentions greater than or equal to _N_ x 7. If your image does not meet these requirements you will recieve an error.

To decode a message you will need two images with the same width and height. If your images do not meet this requirement you will recieve an error.