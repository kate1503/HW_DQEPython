import re
original_text = """
homEwork:
  tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH 
LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, 
but ALL whitespaces. I got 87.

"""

# Correct misspelling error iz -> is where it is needed
iz_pattern = re.compile(r'(?<!”)\biz\b(?!”)', re.IGNORECASE)
replacement = "is"
misspelling_fixed_text = iz_pattern.sub(replacement, original_text)

# Normalize letter cases
normalized_text = misspelling_fixed_text.lower()
paragraphs = normalized_text.split("\n\n")
capitalized_paragraphs = []

# Process paragraphs
for paragraph in paragraphs:
    sentences = paragraph.split(".")
    capitalized_sentences = []

    # Process sentences
    # Capitalize sentences
    for sentence in sentences:
        if sentence.strip():
            spaces_at_start = len(sentence) - len(sentence.lstrip())
            trimmed_sentence = " "*spaces_at_start + sentence.strip().capitalize()
            capitalized_sentences.append(trimmed_sentence)
    capitalized_paragraph = f'{".".join(capitalized_sentences)}.'
    capitalized_paragraphs.append(capitalized_paragraph)


# Create the list of last words in each sentence
last_words = []

for sentence in normalized_text.split("."):
    if sentence.split():
        last_words.append(sentence.split()[-1])

# Form the additional sentence
additional_sentence = f' {" ".join(last_words).capitalize()}.'


# Insert additional sentence at the end of required paragraph
word = "paragraph"
word_index = 0
for index, string in enumerate(capitalized_paragraphs):
    if word in string:
        word_index = index
        capitalized_paragraphs[index] += additional_sentence
        break

final_text = f'{"\n\n".join(capitalized_paragraphs)}'

# Calculate number of whitespace characters in final text
whitespace_pattern = re.compile(r'\s+')
whitespaces_count_final = len(whitespace_pattern.findall(final_text))
whitespace_count_initial = len(whitespace_pattern.findall(original_text))


print(f'Original text: \n {original_text}')
print(f'Fixed text: \n {final_text}')
print(f'Fixed text whitespaces count: {whitespaces_count_final}')
print(f'Initial text whitespaces count: {whitespace_count_initial}')
