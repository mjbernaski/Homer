# Homer's Odyssey Text Processing

A collection of Python scripts to process and format Homer's Odyssey from Project Gutenberg into beautifully formatted HTML.

## Overview

This project takes the raw text of Homer's Odyssey from Project Gutenberg and transforms it through several stages:
1. Extracts pure Odyssey content (removing Gutenberg headers/footers)
2. Formats the text for better readability
3. Generates an elegant HTML version with navigation

## Files

### Source Files
- `raw_Odyssey.txt` - Original text from Project Gutenberg
- `odyssey_clean.txt` - Odyssey text with Gutenberg matter removed
- `odyssey_formatted.txt` - Nicely formatted version with proper paragraph structure
- `Odyssey_formatted.txt` - Version with newlines after commas

### Python Scripts
- `extract_odyssey_only.py` - Removes Project Gutenberg front/end matter
- `format_odyssey_nicely.py` - Improves text formatting and readability
- `add_newlines_after_commas.py` - Adds newlines after each comma
- `create_final_html.py` - Generates the final styled HTML version
- `create_odyssey_html.py` - Alternative HTML generator

### Output Files
- `odyssey_final.html` - Final formatted HTML with ocean theme and navigation
- `odyssey.html` - Alternative HTML version with purple theme

## Features

The HTML version includes:
- Ocean-themed design with blue gradients
- Book-by-book navigation dropdown
- Scroll progress indicator
- Smooth scrolling and back-to-top button
- Elegant typography with drop caps
- Responsive design for mobile devices
- Print-friendly CSS

## Usage

To recreate the formatted versions:

```bash
# Extract clean Odyssey text
python3 extract_odyssey_only.py

# Format the text nicely
python3 format_odyssey_nicely.py

# Generate HTML
python3 create_final_html.py

# Open in browser
open odyssey_final.html
```

## Source

Original text from [Project Gutenberg](https://www.gutenberg.org)
Translation by Samuel Butler