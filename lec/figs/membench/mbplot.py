#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def size_name(s):
    "Give a string name to a size in bytes"
    ksize = s/1024
    if ksize >= 1024:
        return "{0}M".format(ksize/1024)
    else:
        return "{0}K".format(ksize)


def line_plots(df):
    """Plot access time vs stride as lines

    Args:
        df: Data frame of CSV output from membench
    """
    for key, grp in df.groupby("size"):
        plt.semilogx(grp['stride'], grp['ns'], label=size_name(key), basex=2)
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel('Stride (bytes)')
    plt.ylabel('Time (ns)')
    return lgd
    

def heat_plot(df, cmap="jet"):
    """Plot access time vs stride as heat map

    Args:
        df: Data frame of CSV output from membench
        cmap: Color map
    """
    df["working"] = df.size / df.stride
    A = np.empty([27,27])
    A[:] = np.NAN
    for idx,row in df.iterrows():
        i = int(row['size']).bit_length()-1
        j = int(row['stride']).bit_length()-1
        A[i,j] = row['ns']
    plt.matshow(A, cmap=plt.get_cmap(cmap))
    plt.xlabel('log2(stride)')
    plt.ylabel('log2(size)')
    plt.xlim([1,27])
    plt.ylim([11,27])
    plt.colorbar(shrink=0.6)


def add_critical_size(level, color='gray'):
    """Add a critical size to the heat map plot

    Args:
        level: log2(marked size)
    """
    level -= 0.5
    plt.plot([1,27], [level,level], color=color, linewidth=3, linestyle='--')


def add_critical_stride(level, color='gray'):
    """Add a critical stride to the heat map plot

    Args:
        level: log2(marked stride)
    """
    level -= 0.5
    plt.plot([level,level], [11,27], color=color, linewidth=3, linestyle='--')


def add_critical_assoc(level, color='gray'):
    """Add a critical stride to the heat map plot

    Args:
        level: log2(associativity)
    """
    level += 0.5
    plt.plot([1,27], [1+level,27+level], color=color,
             linewidth=3, linestyle='--')
    plt.xlim([1,27])
    plt.ylim([11,27])


def main(csv, ext="pdf", cmap="jet"):
    """Plot membench output as line plot and colormap

    Args:
        csv: Base name of CSV file generated by membench
        cmap: Name of color map
    """
    df = pd.read_csv(csv+'.csv')

    plt.figure()
    lgd = line_plots(df)
    plt.savefig(csv+'-line.' + ext,
                bbox_extra_artists=(lgd,), bbox_inches='tight')

    plt.figure()
    heat_plot(df, cmap)
    plt.savefig(csv+'-heat.' + ext, bbox_inches='tight')


if __name__ == "__main__":
    main(*sys.argv[1:])