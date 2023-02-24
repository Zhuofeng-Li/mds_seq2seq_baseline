# SciReviewGen
**This is the official dataset repository for `SciReviewGen: A Large-scale Dataset for Automatic Literature Review Generation` in ACL 2023.**

## Dataset
- split_survey_df: The split version of SciReviewGen, which aims to generate literature review **chapters**
- original_survey_df: The original version of SciReviewGen, which aims to generate **the entire text** of literature reviews
- summarization_csv: CSV files suitable for summarization task

### Data format
#### split_survey_df & original_survey_df
- Row: 
  - literature review chapter or the entire text of literature review
- Column:
  - paper_id: paper_id used in S2ORC
  - title: title of the literature review
  - abstract: abstract of the literature review
  - section: chapter title
  - text: body text of literature review chapter or literature review paper
  - n_bibs: number of the cited papers that can be used as inputs
  - n_nonbibs: number of the cited papers that cannot be used as inputs
  - bib_titles: titles of the cited papers
  - bib_abstracts: abstracts of the cited papers
  - bib_citing_sentences: citing sentences that cite the cited papers

#### summarization_csv
- Row: 
  - literature review chapter
- Column:
  - reference: `literature review title <s> chapter title <s> abstract of cited paper 1 <s> BIB001 </s> literature review title <s> chapter title <s> abstract of cited paper 2 <s> BIB002 </s> ...`
  - target: literature review chapter


## How to create SciReviewGen from S2ORC

### 0. Environment
- Python 3.9
- Run the following script to install required packages
```
pip install -r requirements.txt
```

### 1. Preprocessing
- Download [S2ORC](https://github.com/allenai/s2orc) (We use the version released on **2020-07-05**, which contains papers up until 2020-04-14)
- Run the following command:
```
git clone https://github.com/tetsu9923/SciReviewGen.git
cd SciReviewGen
python json_to_df.py \
  -s2orc_path <Path to the S2ORC full dataset directory (Typically ".../s2orc/full/20200705v1/full")> \
  -dataset_path <Path to the generated dataset> \
  --field <Optional: the field of the literature reviews (mag_field_of_study in S2ORC, default="Computer Science")>
```
The metadata and pdf parses of the candidates for the literature reviews and the cited papers are stored in *dataset_path* (in the form of pandas dataframe).

### 2. Construct SciReviewGen
- Run the following command:
```
python make_section_df.py \
  -dataset_path <Path to the generated dataset> \
  --version <Optional: the version of SciReviewGen ("split" or "original", default="split")>
```
The SciReviewGen dataset (**split_survey_df.pkl** or **original_survey_df.pkl**) is stored in *dataset_path* (in the form of pandas dataframe).
`filtered_dict.pkl` give the list of literature reviews filtered by the [SciBERT](https://arxiv.org/abs/1903.10676)-based classifier (Section 3.2).

### 3. Construct csv data for summarization
- Run the following command:
```
python make_summarization_csv.py \
  -dataset_path <Path to the generated dataset> 
```
The csv files for summarization (**train.csv**, **val.csv**, and **test.csv**) are stored in *dataset_path*.
If you train QFiD on the generated csv files, add `--for_qfid` argument as below.
```
python make_summarization_csv.py \
  -dataset_path <Path to the generated dataset> \
  --for_qfid
```


## Additional resources
### SciBERT-based literature review classifier
We trained the [SciBERT](https://arxiv.org/abs/1903.10676)-based literature review classifier.
The model weight is available here.

### Query-weighted Fusion-in-Decoder (QFiD)
We proposed Query-weighted Fusion-in-Decoder (QFiD) that explicitly considers the relevance of each input document to the queries.
You can train QFiD on SciReviewGen csv data.
- Modify qfid/run.sh (CUDA_VISIBLE_DEVICES, csv file path, and outpput_dir)
- Run the following command:
```
cd qfid
./run.sh
```
