# Image Steganography

## Hide messages in plain sight with steganography.

This python script manipulates pixel color values to hide any ascii message 'inside' an image.

## Requirements

Requires Python 2.7 and the pillow library

Currently only works with PNG format

## Usage

Help:
```
python image_steg.py -h
```

Encoding:
```
python image_steg.py -e <original_image_path> -o <output_path> -m <message>

or

echo <message> | python image_steg.py -e <original_image_path> -o <output_path>
```

Decoding:
```
decoding: python image_steg.py -d <encoded_image_path>
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

or 

echo 'Hello, world!' | python image_steg.py -e ./images/input_image.png -o ./images/output_image.png
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
python image_steg.py -d ./images/output_image.png
```

Output
```
Hello, world!
```

