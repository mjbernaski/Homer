#!/usr/bin/env python3

def extract_odyssey_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if line.strip() == "BOOK I" and start_line is None:
            start_line = i

        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_line = i
            break

    if start_line is None or end_line is None:
        print("Could not find proper boundaries")
        return

    odyssey_content = lines[start_line:end_line]

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in odyssey_content:
            f.write(line)

    print(f"Extracted Odyssey text from line {start_line} to line {end_line}")
    print(f"Output saved to {output_file}")
    print(f"Original file: {len(lines)} lines")
    print(f"Cleaned file: {len(odyssey_content)} lines")

if __name__ == "__main__":
    extract_odyssey_text("raw_Odyssey.txt", "odyssey_clean.txt")