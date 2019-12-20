import sys, os, re
from mutagen.mp3 import MP3
import matplotlib.pyplot as plt
import pymorphy2
from nltk.corpus import stopwords

russian_stop_words = stopwords.words('russian')
PRANKS_DIR = sys.argv[-1] if len(sys.argv) > 1 else "/home/dima/Music/prankota"
morph = pymorphy2.MorphAnalyzer()
lengths = []
tokens = {}
for r, d, files in os.walk(PRANKS_DIR):
	for file in files:
		for token_normal_form in [morph.parse(token)[0].normal_form for token in re.split('(\s|-)+',file.split('.')[0].lower()) if not re.match('(\s|-|[0-9])+', token) and token not in russian_stop_words]:
			if token_normal_form in tokens:
				tokens[token_normal_form] += 1
			else:
				tokens[token_normal_form] = 1
		try:
			lengths.append(MP3(f'{PRANKS_DIR}/{file}').info.length)
		except:
			print(f"Invalid file {file}. Skipping...")

pairs = [(token, tokens[token]) for token in tokens.keys()]
pairs = sorted(pairs, key = lambda token: token[1], reverse = True)

with open('word-frequences.txt', 'w') as file:
	file.write(f'{"word":20s}:{"occurred":>10s}\n')
	for pair in pairs[:100]:
		file.write(f'{pair[0]:20s}:{pair[1]:10d}\n')

num_bins = 50
n, bins, patches = plt.hist(list(map(lambda duration_in_seconds: duration_in_seconds/60.0, lengths)), num_bins, facecolor='blue', range=(0, 20))
plt.title("Pranks duration")
plt.xlabel("Duration (min)")
plt.ylabel("Number of pranks")

# print(lengths)

plt.savefig("prank-lengths.png")

# audio = MP3("example.mp3")
# print(audio.info.length)