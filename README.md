# PDFWatermarker
Easy User Pdf watermark tools based on PyPDF2 and Python3

# Required

::

pip install reportlab
pip install PyPDF2


# Useage

::

usage: python pdf_watermark.py [-h] [--rotate_angle ROTATE_ANGLE]
                               [--font_size FONT_SIZE] [--opacity OPACITY]
                               [--color COLOR]
                               [--watermark_string WATERMARK_STRING]
                               input_file output_file

positional arguments:
  input_file            Input file name
  output_file           Output file name

optional arguments:
  -h, --help            show this help message and exit
  --rotate_angle ROTATE_ANGLE
                        The watermark rotate_angle
  --font_size FONT_SIZE
                        The watermark size
  --opacity OPACITY     The watermark opacity
  --color COLOR         The watermark color:eg. '#000000' or 000000
  --watermark_string WATERMARK_STRING
                        Watermark String


# Notes
if error happened Like this::


File "/usr/local/lib/python3.7/site-packages/PyPDF2/utils.py", line 238, in b_
    r = s.encode('latin-1')
UnicodeEncodeError: 'latin-1' codec can't encode characters in position 8-9: ordinal not in range(256)

You may modify file "/usr/local/lib/python3.7/site-packages/PyPDF2/utils.py" line 238 from ::

r = s.encode('latin-1')

to ::

try:
    r = s.encode('latin-1')
except:
    r = s.encode('utf-8')

