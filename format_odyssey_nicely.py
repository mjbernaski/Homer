#!/usr/bin/env python3
import re

def format_odyssey_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    formatted_lines = []
    current_paragraph = []
    in_footnote = False
    consecutive_empty_lines = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this is a footnote (starts with [ and contains ])
        if stripped.startswith('[') and ']' in stripped:
            in_footnote = True

        # Check if this is a BOOK header
        if re.match(r'^BOOK [IVXLCDM]+$', stripped):
            # Flush current paragraph
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                formatted_lines.append('')
                current_paragraph = []

            # Add book header with proper spacing
            if formatted_lines and formatted_lines[-1] != '':
                formatted_lines.append('')
            formatted_lines.append('')
            formatted_lines.append(stripped)
            formatted_lines.append('')
            consecutive_empty_lines = 0
            continue

        # Check if this is a chapter subtitle (all caps, multiple words)
        if (stripped and
            stripped.isupper() and
            len(stripped.split()) > 2 and
            not stripped.startswith('BOOK') and
            len(stripped) < 100):
            # Flush current paragraph
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                formatted_lines.append('')
                current_paragraph = []

            formatted_lines.append(stripped)
            formatted_lines.append('')
            consecutive_empty_lines = 0
            continue

        # Handle empty lines
        if not stripped:
            if current_paragraph:
                # End of paragraph - join lines and add
                formatted_lines.append(' '.join(current_paragraph))
                formatted_lines.append('')
                current_paragraph = []
                consecutive_empty_lines = 1
            else:
                # Multiple empty lines - keep only one
                consecutive_empty_lines += 1
                if consecutive_empty_lines <= 2:
                    continue
        else:
            consecutive_empty_lines = 0

            # Handle footnotes - keep them as separate lines
            if in_footnote:
                if current_paragraph:
                    formatted_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                formatted_lines.append(stripped)
                if stripped.endswith(']'):
                    in_footnote = False
                    formatted_lines.append('')
            else:
                # Regular text - add to current paragraph
                current_paragraph.append(stripped)

    # Don't forget the last paragraph
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))

    # Clean up excessive empty lines at the end
    while formatted_lines and formatted_lines[-1] == '':
        formatted_lines.pop()

    # Join the lines and do final cleanup
    formatted_text = '\n'.join(formatted_lines)

    # Replace multiple spaces with single space
    formatted_text = re.sub(r'  +', ' ', formatted_text)

    # Ensure no more than 2 consecutive newlines
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text)

    # Fix spacing around quotation marks
    formatted_text = re.sub(r'"\s+', '"', formatted_text)
    formatted_text = re.sub(r'\s+"', '"', formatted_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_text)

    print(f"Formatted text saved to {output_file}")
    print(f"Original: {len(lines)} lines")
    print(f"Formatted: {len(formatted_text.splitlines())} lines")

if __name__ == "__main__":
    format_odyssey_text("odyssey_clean.txt", "odyssey_formatted.txt")