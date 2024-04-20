import re


def get_paragraphs(text):
    return text.split("\n\n")


def get_sentences(text):
    return text.split(".")


def get_words(text):
    return text.split()


def text_from_sentences(sentences):
    try:
        return f'{".".join(sentences)}.'
    except TypeError as e:
        print(f'Value of the wrong type was passed as function argument. Should be array of strings', e)


def text_from_paragraphs(paragraphs):
    return f'{"\n\n".join(paragraphs)}'


def form_additional_sentence(text):
    last_words = []

    for sentence in get_sentences(text):
        if sentence.split():
            last_words.append(sentence.split()[-1])

    # Form the additional sentence
    return f' {" ".join(last_words).capitalize()}.'


def fix_misspelling_errors(text):
    # Correct misspelling error iz -> is where it is needed
    iz_pattern = re.compile(r"\biz\b", re.IGNORECASE)
    replacement = "is"
    return iz_pattern.sub(replacement, text)


def insert_sentence(text, sentence, paragraph_num):
    # Insert additional sentence at the end of required paragraph
    paragraphs = get_paragraphs(text)
    paragraphs[paragraph_num] += sentence
    return text_from_paragraphs(paragraphs)


def count_whitespaces(text):
    # Calculate number of whitespace characters in final text
    whitespace_pattern = re.compile(r'\s+')
    return len(whitespace_pattern.findall(text))


def normalize_text(text):
    capitalized_paragraphs = []
    for paragraph in get_paragraphs(text.lower()):
        capitalized_sentences = []

        # Capitalize sentences
        for sentence in get_sentences(paragraph):
            if sentence.strip():
                spaces_at_start = len(sentence) - len(sentence.lstrip())
                trimmed_sentence = " " * spaces_at_start + sentence.strip().capitalize()
                capitalized_sentences.append(trimmed_sentence)

        capitalized_paragraph = text_from_sentences(capitalized_sentences)
        capitalized_paragraphs.append(capitalized_paragraph)
    final_text = text_from_paragraphs(capitalized_paragraphs)
    return final_text


if __name__ == '__main__':
    original_text = """
    homEwork:
      tHis iz your homeWork, copy these Text to variable.

      You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH 
    LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

      it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

      last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, 
    but ALL whitespaces. I got 87.

    """
    normalized_text = normalize_text(original_text)
    additional_sentence = form_additional_sentence(normalized_text)
    text_insert_sentence = insert_sentence(normalized_text, additional_sentence, 2)
    result_text = fix_misspelling_errors(text_insert_sentence)
    whitespaces_count = count_whitespaces(result_text)
    print(f'Whitespaces count in final text: {whitespaces_count}')
    print(f'Processed result text: \n {result_text}')

