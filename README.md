# Image Steganography

Hide images in plain sight with steganography.

Requires Python 2.7 and the pillow library

Encoding:
```
python image_steg.py -e <original_image_path> -o <output_path> -m <message>
```

Decoding:
```
decoding: python image_steg.py -d <encoded_image_path> -o <original_image_path>
```