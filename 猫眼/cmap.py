#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WOFF 字体 OCR 模块
对外只暴露一个函数: build_mapping(woff_path) -> dict
用法:
    from woff_ocr import build_mapping
    mapping = build_mapping("猫眼.woff")
"""

import os
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import ddddocr

FONT_SIZE = 80
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def convert_to_ttf(woff_path, out_path):
    font = TTFont(woff_path)
    font.flavor = None
    if hasattr(font, "flavorData"):
        font.flavorData = None
    font.save(out_path)
    return out_path


def render_glyphs(ttf_path, img_dir):
    os.makedirs(img_dir, exist_ok=True)
    font = TTFont(ttf_path)
    cmap = font.getBestCmap()
    img_font = ImageFont.truetype(ttf_path, FONT_SIZE)

    records = []
    for code in sorted(cmap.keys()):
        if not (0xE000 <= code <= 0xF8FF):
            continue
        ch = chr(code)
        img = Image.new("RGB", (FONT_SIZE + 20, FONT_SIZE + 20), "white")
        ImageDraw.Draw(img).text((10, 10), ch, font=img_font, fill="black")
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            pad = Image.new("RGB", (img.width + 20, img.height + 20), "white")
            pad.paste(img, (10, 10))
            img = pad
        img_path = os.path.join(img_dir, f"U+{code:04X}.png")
        img.save(img_path)
        records.append((code, img_path))
    return records


def ocr_glyphs(records):
    ocr = ddddocr.DdddOcr(show_ad=False)
    mapping = {}
    for code, img_path in records:
        with open(img_path, "rb") as f:
            text = ocr.classification(f.read())
        if text:
            mapping[chr(code)] = text[0]
    return mapping


def build_mapping(woff_path, img_dir=None, verbose=False):
    """
    对外唯一接口
    输入: woff 文件路径
    输出: {'\ue3df': '7', '\ued30': '1', ...}
    """
    if img_dir is None:
        img_dir = os.path.join(BASE_DIR, "glyph_imgs")

    base = os.path.splitext(woff_path)[0]
    ttf_path = base + ".ttf"

    convert_to_ttf(woff_path, ttf_path)
    records = render_glyphs(ttf_path, img_dir)
    mapping = ocr_glyphs(records)

    if verbose:
        print(f"[woff_ocr] 共渲染 {len(records)} 个字形")
        print(f"[woff_ocr] 映射: " +
              ", ".join(f"U+{ord(k):04X}={v}" for k, v in mapping.items()))

    return mapping


def decrypt(text, mapping):
    return "".join(mapping.get(ch, ch) for ch in text)


# 还能独立运行（方便单独调试）
if __name__ == "__main__":
    woff = os.path.join(BASE_DIR, "猫眼.woff")
    m = build_mapping(woff)