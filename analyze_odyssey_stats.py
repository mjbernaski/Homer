#!/usr/bin/env python3
import re
import json
from collections import Counter

def analyze_odyssey_text(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove book headers and chapter subtitles for word analysis
    text_for_analysis = re.sub(r'^BOOK [IVXLCDM]+$', '', text, flags=re.MULTILINE)
    text_for_analysis = re.sub(r'^[A-Z\s—]+$', '', text_for_analysis, flags=re.MULTILINE)

    # Remove footnote markers
    text_for_analysis = re.sub(r'\[\d+[^\]]*\]', '', text_for_analysis)

    # Basic statistics
    stats = {}

    # Character and word counts
    stats['total_characters'] = len(text)
    stats['total_characters_no_spaces'] = len(re.sub(r'\s', '', text))

    # Word analysis
    words = re.findall(r'\b[a-zA-Z]+\b', text_for_analysis.lower())
    stats['total_words'] = len(words)

    # Unique words
    unique_words = set(words)
    stats['unique_words'] = len(unique_words)

    # Average word length
    stats['avg_word_length'] = sum(len(word) for word in words) / len(words) if words else 0

    # Sentences (rough estimate)
    sentences = re.split(r'[.!?]+', text_for_analysis)
    sentences = [s.strip() for s in sentences if s.strip()]
    stats['total_sentences'] = len(sentences)

    # Average words per sentence
    stats['avg_words_per_sentence'] = len(words) / len(sentences) if sentences else 0

    # Paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    stats['total_paragraphs'] = len(paragraphs)

    # Books count
    book_matches = re.findall(r'^BOOK [IVXLCDM]+$', text, flags=re.MULTILINE)
    stats['total_books'] = len(book_matches)

    # Stop words list (common English words)
    stop_words = {
        'the', 'and', 'to', 'of', 'a', 'in', 'that', 'have', 'i', 'it', 'for',
        'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but',
        'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will', 'my', 'one',
        'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
        'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can',
        'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into',
        'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
        'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think',
        'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
        'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
        'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has',
        'had', 'were', 'said', 'each', 'which', 'their', 'said', 'did',
        'get', 'may', 'find', 'use', 'her', 'than', 'call', 'who', 'oil',
        'sit', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come',
        'made', 'may', 'part'
    }

    # Word frequency analysis
    word_freq = Counter(words)

    # Most common words (excluding stop words)
    non_stop_words = [word for word in words if word not in stop_words]
    non_stop_freq = Counter(non_stop_words)
    stats['most_common_words'] = non_stop_freq.most_common(50)

    # Most common stop words (for reference)
    stop_word_freq = {word: count for word, count in word_freq.items() if word in stop_words}
    stats['most_common_stop_words'] = sorted(stop_word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Place names analysis (geographical locations in the Odyssey)
    place_names = {
        'ithaca', 'troy', 'sparta', 'pylos', 'scheria', 'phaeacia', 'crete',
        'egypt', 'cyprus', 'athens', 'argos', 'mycenae', 'tiryns', 'corinth',
        'sicily', 'italy', 'phoenicia', 'libya', 'ethiopia', 'thrace',
        'lemnos', 'lesbos', 'tenedos', 'scyros', 'euboea', 'aegina',
        'salamis', 'megara', 'thebes', 'delphi', 'olympus', 'parnassus',
        'helicon', 'cithaeron', 'pentelicus', 'hymettus', 'laurium',
        'sunium', 'marathon', 'rhamnus', 'decelea', 'aphidna', 'acharnae',
        'colonus', 'aegaleus', 'piraeus', 'phaleron', 'eleusis',
        'dulichium', 'same', 'zacynthus', 'cephalonia', 'leucas',
        'ogygian', 'aeaea', 'laestrygonian', 'cicones', 'lotus',
        'cyclopes', 'hades', 'elysium', 'tartarus', 'styx', 'lethe',
        'acheron', 'cocytus', 'phlegethon', 'oceanus', 'temesa', 'ephyra'
    }

    # Character names analysis (common Greek/epic names)
    character_names = {
        'ulysses', 'odysseus', 'penelope', 'telemachus', 'minerva', 'athena',
        'jupiter', 'jove', 'zeus', 'neptune', 'poseidon', 'apollo', 'mercury',
        'hermes', 'venus', 'aphrodite', 'mars', 'ares', 'diana', 'artemis',
        'antinous', 'eurymachus', 'amphinomus', 'ctesippus', 'eurycleia',
        'eumaeus', 'philoetius', 'melanthius', 'melantho', 'laertes',
        'anticlea', 'nestor', 'menelaus', 'agamemnon', 'helen', 'cassandra',
        'circe', 'calypso', 'nausicaa', 'alcinous', 'arete', 'demodocus'
    }

    # Count place mentions
    place_freq = {}
    for place in place_names:
        count = sum(1 for word in words if word == place)
        if count > 0:
            place_freq[place] = count

    stats['place_mentions'] = sorted(place_freq.items(), key=lambda x: x[1], reverse=True)[:25]

    # Count character mentions
    character_freq = {}
    for name in character_names:
        count = sum(1 for word in words if word == name)
        if count > 0:
            character_freq[name] = count

    stats['character_mentions'] = sorted(character_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Longest words
    stats['longest_words'] = sorted(set(words), key=len, reverse=True)[:20]

    return stats

def save_stats_to_json(stats, output_file):
    # Convert to JSON-serializable format
    json_stats = stats.copy()
    json_stats['avg_word_length'] = round(json_stats['avg_word_length'], 2)
    json_stats['avg_words_per_sentence'] = round(json_stats['avg_words_per_sentence'], 2)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_stats, f, indent=2)

    return json_stats

if __name__ == "__main__":
    stats = analyze_odyssey_text("odyssey_formatted.txt")
    json_stats = save_stats_to_json(stats, "odyssey_stats.json")

    print("Odyssey Text Analysis Complete!")
    print(f"Total words: {stats['total_words']:,}")
    print(f"Unique words: {stats['unique_words']:,}")
    print(f"Total characters: {stats['total_characters']:,}")
    print(f"Total sentences: {stats['total_sentences']:,}")
    print(f"Total paragraphs: {stats['total_paragraphs']:,}")
    print(f"Total books: {stats['total_books']}")
    print(f"Average word length: {stats['avg_word_length']:.2f}")
    print(f"Average words per sentence: {stats['avg_words_per_sentence']:.2f}")
    print("\nTop 10 place mentions:")
    for place, count in stats['place_mentions'][:10]:
        print(f"  {place}: {count}")
    print("\nTop 10 character mentions:")
    for name, count in stats['character_mentions'][:10]:
        print(f"  {name}: {count}")