#!/usr/bin/env python3

def add_newlines_after_commas(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    modified_content = content.replace(',', ',\n')

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_content)

    print(f"Successfully processed {input_file}")
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    input_filename = "raw_Odyssey.txt"
    output_filename = "Odyssey_formatted.txt"

    add_newlines_after_commas(input_filename, output_filename)