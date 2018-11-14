# Image Steganography

### Hide messages in plain sight with steganography.

This python script manipulates pixel color values to hide any ascii message 'inside' an image. To decode the message the decoder will need the original image as a key and the encoded image to reveal the message.

### Requirements

Requires Python 2.7 and the pillow library

### Usage

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