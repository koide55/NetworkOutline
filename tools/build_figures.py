#!/usr/bin/env python3
"""図をすべて描き出す。

    python3 tools/build_figures.py            # 全部
    python3 tools/build_figures.py 06         # 第6回だけ

fig-co-*.svg はコンピュータシステム通論（CompOutline）の図を複製したもの。ここでは描かない。
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'figs'))

MODULES = ['net01', 'net02', 'net04', 'net05', 'net06', 'net07', 'net08']


def main():
    want = sys.argv[1:]
    figs = {}
    for m in MODULES:
        figs.update(importlib.import_module(m).FIGURES)
    os.makedirs(os.path.join(ROOT, 'figures'), exist_ok=True)
    n = 0
    for key, fn in sorted(figs.items()):
        if want and key.split('-')[0] not in want:
            continue
        fn().save(os.path.join(ROOT, 'figures', f'fig-{key}.svg'))
        n += 1
    print(f'{n} 点を figures/ に書き出した')


if __name__ == '__main__':
    main()
