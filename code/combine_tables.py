#!/usr/bin/env python
"""
Example usage:

python combine_tables.py mri_table.csv \
                         -i /data/abcd/Package_1204615/abcd_{lt01,mri01,ra01}.txt \
                         -j interview_date subjectkey interview_age
"""

from argparse import ArgumentParser
import pandas as pd


generic_cols = ['subjectkey', 'interview_date']

def join(df_new, cols, delimiter='\t', bad_rows=1, df_grow=None):
    """
    df_new:    the dataframe to add to the ensemble (or a path to it)
    cols:      the columns to merge the dataframes on
    delimiter: the delimiter of the file; only relevant if a filename is passed
    bad_rows:  the number of starting rows to remove prior to merging (e.g.,
                for field descriptions)
    df_grow:   the dataframe to be growing.
    """
    if isinstance(df_new, str):
        df_new = pd.read_csv(df_new, delimiter=delimiter)
    df_new = df_new.iloc[bad_rows:]

    if df_grow is None:
        return df_new

    df_out = pd.merge(df_grow, df_new, how='inner', on=cols)
    return df_out


def main():
    parser = ArgumentParser(description="Helper utility for joining ABCD data")
    parser.add_argument("outpath",
                        help="Path to store output dataset.")
    parser.add_argument("-i", "--instruments", nargs="+",
                        help="Paths to instruments of interest.")
    parser.add_argument("-j", "--join_on", nargs="+", default=generic_cols,
                        help="List of fields for combining instruments.")
    results = parser.parse_args()

    df_growing = None
    for fl in results.instruments:
        df_growing = join(fl, results.join_on, df_grow=df_growing)
    
    df_growing = df_growing.set_index(results.join_on).reset_index()
    df_growing.to_csv(results.outpath, index=False)


if __name__ == "__main__":
    main()

