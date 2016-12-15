```
Usage: make_index.py [OPTIONS]

Options:
  --page_offset INTEGER   Page of pdf from which to start the index.  Past all
                          of the preamble.
  --end_page TEXT         final page on which to index contents.
                          Absolute page
                          number.
                          Determined from counting from the very
                          beginning of the pdf
                          (i.e. including TOC, preamble,
                          etc.)
  --tokenizer TEXT        ['alphanum', or 'alpha']
  --ngram_range TEXT      how many words to be used when analyzing phrases.
  --n_entries INTEGER     how many index entries to create
  --input_file TEXT       input pdf
  --output_file TEXT      output text file
  --max_pf FLOAT          maximum page frequency for phrases.  phrases that
                          appear more frequently are discarded
  --min_pf INTEGER        min page frequency for phrases.
  --min_word_len INTEGER
  --help                  Show this message and exit.
```
