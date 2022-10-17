#!/usr/bin/env python

from argparse import ArgumentParser
import numpy as np


def crawl(fl):
    subs = []
    with open(fl) as fhandle:
        for _, line in enumerate(fhandle):
            if not (_ % 1e6):
                print(_)

            vals = line.split("\t")
            try:
                sub = vals[3].split('.')[0]
                if 'sub' in sub:
                    subs += [sub.strip('"')]
            except:
                continue
            del sub

    subs = list(np.unique(subs))
    print("N subs: {0}".format(len(subs)))
    return subs


def main():
    parser = ArgumentParser()
    parser.add_argument('data_manifest')
    parser.add_argument('output')

    args = parser.parse_args()
    infl = args.data_manifest
    oufl = args.output

    sublist = crawl(infl)
    with open(oufl, 'w') as fhandle:
        [fhandle.write("{0}\n".format(s))
         for s in sublist]


if __name__ == "__main__":
    main()

