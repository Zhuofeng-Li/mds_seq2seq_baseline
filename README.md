<!---
Copyright 2020 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

## Summarization

This directory contains examples for finetuning and evaluating **seq2seq-based transformers** on multi-document summarization  tasks.

### Supported seq2seq MDS Architectures

- `BartForConditionalGeneration`
- `FSMTForConditionalGeneration` (translation only)
- `MBartForConditionalGeneration`
- `MarianMTModel`
- `PegasusForConditionalGeneration`
- `T5ForConditionalGeneration`
- `MT5ForConditionalGeneration`

### Dataset 
https://huggingface.co/datasets/ZhuofengLi/MDS

### With Trainer

Please refer to `train_baseline.sh`.

Only T5 models `google-t5/t5-small`, `google-t5/t5-base`, `google-t5/t5-large`, `google-t5/t5-3b` and `google-t5/t5-11b` must use an additional argument: `--source_prefix "summarize: "`.

### Tutorial
1. First check the [summarization codes from huggingface](https://github.com/huggingface/transformers/blob/main/examples/pytorch/summarization/run_summarization.py)

