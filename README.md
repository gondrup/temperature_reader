# Temperature Reader

Takes a webcam image of my cheap chinese temperature monitor and gets the current temperature by recognising the digits on the screen.

**NOTE: This is a work in progress and is not complete.**

## Requirements

 * Python 3 or 2.7
 * ImageMagick
 * [Color Math Python library](https://pypi.python.org/pypi/colormath/)
 * [PIL/Pillow Python library](https://pillow.readthedocs.io/en/latest/)

```bash
sudo apt update
sudo apt upgrade

sudo apt install imagemagick

pip install colormath

sudo apt install libjpeg-dev
pip install pillow
```

## Process

![Chinese Temperature Monitor](https://raw.githubusercontent.com/gondrup/temperature_reader/master/test_images/auto_2018-01-29_141232.jpg "Chinese Temperature Monitor")

1. Find latest image and process it (imageprocess.py)
	- Find and load latest image from webcam (similar to the example image)
	- Use screen module to find the screen coordinates in the image
	- Use ImageMagick to fix the perspective and crop the image based on the coordinates found

2. Read the temperature from the processed image
	- Load processed/cropped image
	- Use segment definitions to detect temperature

# Running Tests

Run all tests with this command from the project directory:

```bash
python -m unittest discover -s tests
```

# Supporting Spreadsheet

Some coordinate calculations can be found on the [Google Sheet](https://docs.google.com/spreadsheets/d/14z58qDwLv3IFIqYmGrKh-dDi_LGai2fQFcGIiLmRNcQ/edit)