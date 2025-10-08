# -*- coding: utf-8 -*-
"""
Undertale Clone - Browser Version
A pixel-perfect recreation of Undertale using Python and Pygame,
compiled to WebAssembly for browser compatibility.
"""

__version__ = "1.0.0"
__title__ = "Undertale Clone"
__author__ = "code2344"
__license__ = "See LICENSE file"

# Pygbag metadata
__PYGBAG__ = {
    "width": 640,
    "height": 480,
    "title": "Undertale Clone",
    "version": "1.0.0",
    "archive": "undertale-clone",
    # Primary CDN with fallback support
    "cdn": "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/",
    # Fallback CDNs for reliability
    "cdn_fallback": [
        "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/",
        "https://cdnjs.cloudflare.com/ajax/libs/pyodide/0.26.2/",
    ],
}
