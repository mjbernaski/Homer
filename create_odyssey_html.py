#!/usr/bin/env python3
import html
import re

def create_html_page(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Odyssey by Homer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><path d="M0 50 Q 25 25, 50 50 T 100 50" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none"/></svg>');
            opacity: 0.3;
        }

        h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            letter-spacing: 2px;
            position: relative;
        }

        .subtitle {
            font-size: 1.3em;
            opacity: 0.9;
            font-style: italic;
            position: relative;
        }

        .content {
            padding: 40px;
            position: relative;
        }

        .content::before {
            content: '📜';
            font-size: 200px;
            position: absolute;
            top: 20px;
            right: 20px;
            opacity: 0.05;
            transform: rotate(-15deg);
        }

        .book-info {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }

        .book-info h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.8em;
        }

        .text-content {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            font-size: 1.1em;
            position: relative;
            z-index: 1;
        }

        .text-content p {
            margin-bottom: 1.2em;
            text-align: justify;
        }

        .text-content p:first-child::first-letter {
            font-size: 4em;
            float: left;
            line-height: 0.8;
            margin: 0.1em 0.1em 0 0;
            color: #667eea;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(102, 126, 234, 0.3);
        }

        .chapter-marker {
            color: #764ba2;
            font-weight: bold;
            font-size: 1.3em;
            margin: 2em 0 1em 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
            display: block;
        }

        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            font-size: 0.9em;
        }

        footer a {
            color: #667eea;
            text-decoration: none;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2.5em;
            }

            .content {
                padding: 20px;
            }

            .text-content {
                padding: 20px;
                font-size: 1em;
            }
        }

        .scroll-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s, box-shadow 0.3s;
            z-index: 1000;
        }

        .scroll-to-top:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>The Odyssey</h1>
            <div class="subtitle">by Homer • Translated by Samuel Butler</div>
        </header>

        <div class="content">
            <div class="book-info">
                <h2>About This Edition</h2>
                <p>A Project Gutenberg eBook - One of the greatest epic poems of ancient Greece, telling the story of Odysseus's ten-year journey home after the Trojan War.</p>
            </div>

            <div class="text-content">
"""

    is_first_content_line = True
    in_book_section = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        line = html.escape(line)

        if "BOOK" in line.upper() and len(line) < 50:
            html_content += f'<span class="chapter-marker">{line}</span>\n'
            in_book_section = True
            is_first_content_line = True
        elif "Project Gutenberg" in line or "Title:" in line or "Author:" in line or "Translator:" in line:
            if not in_book_section:
                html_content += f'<p>{line}</p>\n'
        else:
            if is_first_content_line and in_book_section:
                html_content += f'<p>{line}</p>\n'
                is_first_content_line = False
            else:
                html_content += f'<p>{line}</p>\n'

    html_content += """
            </div>
        </div>

        <footer>
            <p>This eBook is for the use of anyone anywhere in the United States and most other parts of the world at no cost.</p>
            <p>Source: <a href="https://www.gutenberg.org">Project Gutenberg</a></p>
        </footer>
    </div>

    <div class="scroll-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
        ↑
    </div>

    <script>
        const scrollButton = document.querySelector('.scroll-to-top');

        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollButton.style.display = 'flex';
            } else {
                scrollButton.style.display = 'none';
            }
        });

        scrollButton.style.display = 'none';
    </script>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML page created successfully: {output_file}")

if __name__ == "__main__":
    create_html_page("Odyssey_formatted.txt", "odyssey.html")