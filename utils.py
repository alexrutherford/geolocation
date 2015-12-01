# -*- coding: utf-8 -*-
import re

replaceRe=r'(\r|\n|\,|\"|\“|\'|\(|\)|\-|\:|\;|\.|\!|\?|\،|\؛|\{|\}|\[|\}|\\|\n|\r\n|\r|\@|\%|\#|\`|\~|\/|\&)'
replaceRe=re.compile(replaceRe)

def clean(s):
    temp= re.sub(replaceRe,' ',s.lower())
    #print temp
    return temp
