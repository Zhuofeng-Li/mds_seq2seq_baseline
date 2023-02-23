import re
import os
import logging
import pickle
import argparse

import numpy as np
import pandas as pd

from tqdm import tqdm


def make_summarization_csv(args):
    logging.info('Making csv files for summarization...')
    logging.info("Columns={'reference': literature review title <s> chapter title <s> abstract of cited paper 1 <s> BIB001 </s> literature review title <s> chapter title <s> abstract of cited paper 2 <s> BIB002 </s> ..., 'target': literature review chapter}")
    section_df = pd.read_pickle(os.path.join(args.dataset_path, 'split_survey_df.pkl'))

    dataset_df = section_df[section_df['n_bibs'].apply(lambda n_bibs: n_bibs > 1)]  # Remove sections with less than two citations

    dataset_df = dataset_df.rename(columns={'text': 'target'})
    dataset_df = dataset_df.rename(columns={'bib_cinting_sentences': 'bib_citing_sentences'})  # 

    dataset_df['reference'] = dataset_df[['bib_abstracts', 'section', 'title']].apply(lambda bib_abstracts: ' '.join(['</s> {} <s> {} <s> {} <s> BIB{}'.format(bib_abstracts[2], bib_abstracts[1], abstract, bib) for bib, abstract in bib_abstracts[0].items()]), axis=1)
    if args.for_qfid:
        dataset_df['reference'] = dataset_df['title'] + ' <s> ' + dataset_df['section'] + ' ' + dataset_df['reference']
    else:
        dataset_df['reference'] = dataset_df['reference'].apply(lambda s: s[5:])

    split_df = dataset_df['split']
    dataset_df = dataset_df[['reference', 'target']]

    train_df = dataset_df[split_df == 'train']
    val_df = dataset_df[split_df == 'val']
    test_df = dataset_df[split_df == 'test']

    train_df.to_csv(os.path.join(args.dataset_path, 'train.csv'))
    val_df.to_csv(os.path.join(args.dataset_path, 'val.csv'))
    test_df.to_csv(os.path.join(args.dataset_path, 'test.csv'))
    logging.info('Done!')


def anonymize_bib(args):
    logging.info('Converting BIB identifiers...')
    for split in ["val", "test", "train"]:
        df = pd.read_csv(os.path.join(args.dataset_path, '{}.csv'.format(split)))
        bar = tqdm(total=len(df))
        for row in df.itertuples():
            cnt = 1
            bib_dict = {}
            for i in range(len(row.reference)):
                if row.reference[i:i+7] == "<s> BIB":
                    bib_dict[row.reference[i+7:].split(" ")[0]] = cnt
                    cnt += 1
            ref = row.reference
            tgt = row.target
            for key, value in bib_dict.items():
                ref = re.sub("BIB{}".format(key), "BIB{:0>3}".format(value), ref)
                tgt = re.sub("BIB{}".format(key), "BIB{:0>3}".format(value), tgt)
            df.at[row.Index, "reference"] = ref
            df.at[row.Index, "target"] = tgt
            bar.update(1)
        print("Saving...")
        df.to_csv(os.path.join(args.dataset_path, '{}.csv'.format(split)))


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-dataset_path', help='Path to the generated dataset')
    parser.add_argument('--for_qfid', action='store_true', help='Add if you train QFiD on the generated csv files')
    args = parser.parse_args()

    make_summarization_csv(args)
    anonymize_bib(args)