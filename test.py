#!/usr/bin/env python

import tesseract

api = tesseract.TessBaseAPI()
api.Init(".", "letsgodigital", tesseract.OEM_DEFAULT)
api.SetVariable("tessedit_char_whitelist", "-+.,E1234567890")
api.SetPageSegMode(tesseract.PSM_AUTO)
api.SetVariable("debug_file", "/dev/null")
