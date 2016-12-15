import click, os, subprocess
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter, defaultdict
import re
import numpy as np

@click.command()
@click.option('--page_offset', default=1,
	help='Page of pdf from which to start the index.  Past all of the preamble.')
@click.option('--end_page',
	help='''final page on which to index contents.
		Absolute page number.
		Determined from counting from the very beginning of the pdf
		(i.e. including TOC, preamble, etc.)''')
@click.option('--tokenizer', default='alphanum', help="['alphanum', or 'alpha']")
@click.option('--ngram_range', default='(1, 2)', help='how many words to be used when analyzing phrases.')
@click.option('--n_entries', default=150, help='how many index entries to create')
@click.option('--input_file', help='input pdf')
@click.option('--output_file', help='output text file')
@click.option('--max_pf', default=0.5, 
	help='maximum page frequency for phrases.  phrases that appear more frequently are discarded')
@click.option('--min_pf', default=2, 
	help='min page frequency for phrases.')
@click.option('--min_word_len', default=3)

def make_index(input_file, output_file, page_offset, tokenizer, ngram_range,
	n_entries, end_page, max_pf, min_pf, min_word_len):

	end_page = int(end_page)
	if tokenizer.lower() != 'alphanum':
		raise NotImplemented('`alphanum` is the only supported tokenizer')

	token_pattern = r'(?u)\b' + r'\w' * min_word_len + r'\w*\b'

	if not os.path.isfile(input_file):
		raise ValueError('invalid input file.')

	ngram_re = r'(\d),\s*(\d)'
	match = re.search(ngram_re, ngram_range)
	if not match:
		raise ValueError('Invalid input for ngram_range')

	ngram_range = map(int, (match.group(1), match.group(2)))

	get_phrases = CountVectorizer(token_pattern=token_pattern, ngram_range=ngram_range, stop_words='english').build_analyzer()

	page_to_text = {}
	phrase_to_page = defaultdict(set)
	command_template = 'pdftotext -f %d -l %d %s -'

	for page_no in range(page_offset, end_page + 1):
		command = command_template % (page_no, page_no, input_file)
		page_text = subprocess.check_output(command, shell=True)
		page_to_text[page_no] = page_text

		index_page_no = page_no - page_offset + 1
		for phrase in get_phrases(page_text):
			phrase_to_page[phrase].add(index_page_no)

	phrase_to_pf = {}
	for phrase, page_nos in phrase_to_page.iteritems():
		pf = (1.0 * len(page_nos)) / len(page_to_text)
		phrase_to_pf[phrase] = pf

	phrases, pf = zip(*phrase_to_pf.iteritems())
	descending_pf_idxs = np.argsort(pf)[::-1]
	filtered_pf_idxs = [x for x in descending_pf_idxs if pf[x] <= max_pf\
				and len(phrase_to_page[phrases[x]]) >= min_pf]
	ordered_phrases = [phrases[i] for i in filtered_pf_idxs]

	phrases_to_keep = ordered_phrases[:n_entries]
	for phrase in sorted(phrases_to_keep):
		page_str = ', '.join(map(str, sorted(phrase_to_page[phrase])))
		print ('%s\t%s' % (phrase, page_str)).encode('utf-8')


if __name__ == '__main__':
	make_index()
