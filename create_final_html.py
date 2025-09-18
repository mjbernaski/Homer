#!/usr/bin/env python3
import html
import re
import json
import os

def create_odyssey_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Load statistics if available
    stats = {}
    if os.path.exists('odyssey_stats.json'):
        with open('odyssey_stats.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Odyssey by Homer</title>
    <style>
        :root {
            --primary: #2c3e50;
            --accent: #3498db;
            --gold: #f39c12;
            --text: #34495e;
            --bg-light: #ecf0f1;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif;
            line-height: 1.7;
            color: var(--text);
            background: linear-gradient(to bottom, #1e3c72, #2a5298);
            min-height: 100vh;
        }

        .ocean-bg {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                linear-gradient(180deg, rgba(30,60,114,0.9) 0%, rgba(42,82,152,0.9) 100%),
                url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.05" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,128C672,107,768,85,864,90.7C960,96,1056,128,1152,133.3C1248,139,1344,117,1392,106.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
            background-size: cover;
            z-index: -1;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 50px rgba(0,0,0,0.3);
            position: relative;
        }

        header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 80px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '⚓';
            position: absolute;
            font-size: 300px;
            opacity: 0.05;
            top: -50px;
            left: -50px;
            transform: rotate(-15deg);
        }

        header::after {
            content: '🏛️';
            position: absolute;
            font-size: 300px;
            opacity: 0.05;
            bottom: -50px;
            right: -50px;
            transform: rotate(15deg);
        }

        h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            font-weight: normal;
            letter-spacing: 3px;
            position: relative;
            z-index: 1;
        }

        .subtitle {
            font-size: 1.5em;
            opacity: 0.95;
            font-style: italic;
            position: relative;
            z-index: 1;
        }

        .translator {
            margin-top: 10px;
            font-size: 1.2em;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        nav {
            background: var(--primary);
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        nav select {
            padding: 10px 20px;
            font-size: 1.1em;
            border: none;
            border-radius: 5px;
            background: white;
            color: var(--primary);
            cursor: pointer;
            font-family: inherit;
            margin-right: 20px;
        }

        nav button {
            padding: 10px 20px;
            font-size: 1.1em;
            border: none;
            border-radius: 5px;
            background: var(--gold);
            color: white;
            cursor: pointer;
            font-family: inherit;
            margin-left: 10px;
        }

        nav button:hover {
            background: #e67e22;
        }

        .content {
            padding: 60px;
            background: white;
            min-height: 500px;
        }

        .book-header {
            color: var(--accent);
            font-size: 2.5em;
            margin: 60px 0 30px 0;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--gold);
            font-weight: normal;
            page-break-before: always;
        }

        .book-header:first-child {
            margin-top: 0;
        }

        .chapter-subtitle {
            color: var(--primary);
            font-size: 1.3em;
            font-weight: bold;
            margin: 30px 0 20px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        p {
            margin-bottom: 1.5em;
            text-align: justify;
            text-indent: 2em;
        }

        p:first-of-type {
            text-indent: 0;
        }

        .book-section > p:first-child::first-letter {
            font-size: 5em;
            float: left;
            line-height: 0.8;
            margin: 0.1em 0.05em 0 0;
            color: var(--gold);
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .footnote {
            font-size: 0.9em;
            color: #7f8c8d;
            padding: 15px;
            margin: 20px 0;
            background: var(--bg-light);
            border-left: 4px solid var(--accent);
            font-style: italic;
        }

        .statistics {
            background: linear-gradient(135deg, var(--bg-light) 0%, #d5dbdb 100%);
            padding: 40px;
            margin: 40px 0;
            border-radius: 15px;
            border: 1px solid #bdc3c7;
            display: none;
        }

        .statistics.active {
            display: block;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }

        .stat-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .stat-section h4 {
            color: var(--primary);
            margin-bottom: 15px;
            font-size: 1.2em;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 5px;
        }

        .stat-list {
            list-style: none;
            padding: 0;
        }

        .stat-list li {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #ecf0f1;
        }

        .stat-list li:last-child {
            border-bottom: none;
        }

        .stat-number {
            color: var(--accent);
            font-weight: bold;
        }

        .basic-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .basic-stat {
            text-align: center;
            padding: 15px;
            background: var(--accent);
            color: white;
            border-radius: 8px;
        }

        .basic-stat .number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }

        .basic-stat .label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        footer {
            background: var(--primary);
            color: white;
            text-align: center;
            padding: 40px;
            font-size: 0.9em;
        }

        footer a {
            color: var(--gold);
            text-decoration: none;
        }

        .scroll-progress {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: var(--gold);
            z-index: 200;
            transition: width 0.2s;
        }

        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--accent);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: none;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            font-size: 1.5em;
            transition: all 0.3s;
            z-index: 1000;
        }

        .back-to-top:hover {
            transform: translateY(-5px);
            background: var(--primary);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2.5em;
            }

            .content {
                padding: 30px;
            }

            .book-header {
                font-size: 2em;
            }
        }

        @media print {
            .ocean-bg {
                display: none;
            }

            nav, .back-to-top, .scroll-progress {
                display: none;
            }

            .container {
                box-shadow: none;
            }

            .book-header {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>
    <div class="ocean-bg"></div>
    <div class="scroll-progress" id="scrollProgress"></div>

    <div class="container">
        <header>
            <h1>The Odyssey</h1>
            <div class="subtitle">An Epic Poem</div>
            <div class="translator">by Homer • Translated by Samuel Butler</div>
        </header>

        <nav>
            <select id="bookSelector" onchange="jumpToBook()">
                <option value="">Navigate to Book...</option>
"""

    # Find all books and add to navigation
    book_pattern = re.compile(r'^BOOK ([IVXLCDM]+)$')
    books_found = []

    for line in lines:
        match = book_pattern.match(line.strip())
        if match:
            book_num = match.group(1)
            books_found.append(book_num)
            html_content += f'                <option value="book-{book_num}">{book_num}</option>\n'

    html_content += """            </select>
            <button onclick="toggleStats()">📊 View Statistics</button>
        </nav>

        <div class="content">
"""

    current_book = None
    in_book = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Escape HTML characters
        line = html.escape(line)

        # Check for BOOK header
        match = book_pattern.match(line)
        if match:
            if current_book:
                html_content += '</div>\n'
            book_num = match.group(1)
            html_content += f'<div class="book-section" id="book-{book_num}">\n'
            html_content += f'<h2 class="book-header">Book {book_num}</h2>\n'
            current_book = book_num
            in_book = True
            continue

        # Check for chapter subtitle (all caps, multi-word)
        if (line.isupper() and
            len(line.split()) > 2 and
            not line.startswith('BOOK') and
            len(line) < 100):
            html_content += f'<div class="chapter-subtitle">{line}</div>\n'
            continue

        # Check for footnotes
        if line.startswith('[') and line.endswith(']'):
            html_content += f'<div class="footnote">{line}</div>\n'
            continue

        # Regular paragraph - add superscript formatting for footnote numbers
        # Convert standalone numbers to superscript (e.g., "text.14 more text" -> "text.<sup>14</sup> more text")
        formatted_line = re.sub(r'\.(\d+)\s', r'.<sup>\1</sup> ', line)

        html_content += f'<p>{formatted_line}</p>\n'

    if current_book:
        html_content += '</div>\n'

    # Add statistics section if stats are available
    if stats:
        html_content += f"""
        </div>

        <div class="statistics" id="statisticsSection">
            <h3 style="color: var(--primary); margin-bottom: 30px; text-align: center; font-size: 2em;">📊 Text Analysis & Statistics</h3>

            <div class="basic-stats">
                <div class="basic-stat">
                    <span class="number">{stats.get('total_words', 0):,}</span>
                    <span class="label">Total Words</span>
                </div>
                <div class="basic-stat">
                    <span class="number">{stats.get('unique_words', 0):,}</span>
                    <span class="label">Unique Words</span>
                </div>
                <div class="basic-stat">
                    <span class="number">{stats.get('total_sentences', 0):,}</span>
                    <span class="label">Sentences</span>
                </div>
                <div class="basic-stat">
                    <span class="number">{stats.get('total_books', 0)}</span>
                    <span class="label">Books</span>
                </div>
                <div class="basic-stat">
                    <span class="number">{stats.get('avg_word_length', 0):.1f}</span>
                    <span class="label">Avg Word Length</span>
                </div>
                <div class="basic-stat">
                    <span class="number">{stats.get('avg_words_per_sentence', 0):.1f}</span>
                    <span class="label">Words/Sentence</span>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-section">
                    <h4>Most Common Words (Non-Stop Words)</h4>
                    <ul class="stat-list">"""

        # Add top 25 most common words
        for word, count in stats.get('most_common_words', [])[:25]:
            html_content += f'                        <li><span>{word.title()}</span> <span class="stat-number">{count}</span></li>\n'

        html_content += """                    </ul>
                </div>

                <div class="stat-section">
                    <h4>Character Mentions</h4>
                    <ul class="stat-list">"""

        # Add character mentions
        for name, count in stats.get('character_mentions', [])[:15]:
            html_content += f'                        <li><span>{name.title()}</span> <span class="stat-number">{count}</span></li>\n'

        html_content += """                    </ul>
                </div>

                <div class="stat-section">
                    <h4>Longest Words</h4>
                    <ul class="stat-list">"""

        # Add longest words
        for word in stats.get('longest_words', [])[:15]:
            html_content += f'                        <li><span>{word.title()}</span> <span class="stat-number">{len(word)} letters</span></li>\n'

        html_content += """                    </ul>
                </div>

                <div class="stat-section">
                    <h4>Most Common Stop Words</h4>
                    <ul class="stat-list">"""

        # Add stop words
        for word, count in stats.get('most_common_stop_words', [])[:15]:
            html_content += f'                        <li><span>{word.title()}</span> <span class="stat-number">{count}</span></li>\n'

        html_content += """                    </ul>
                </div>
            </div>
        </div>

        <footer>
            <p>Homer's Odyssey • Translated by Samuel Butler</p>
            <p>This edition from <a href="https://www.gutenberg.org">Project Gutenberg</a></p>
        </footer>
    </div>

    <div class="back-to-top" onclick="scrollToTop()" id="backToTop">↑</div>"""
    else:
        html_content += """
        </div>

        <footer>
            <p>Homer's Odyssey • Translated by Samuel Butler</p>
            <p>This edition from <a href="https://www.gutenberg.org">Project Gutenberg</a></p>
        </footer>
    </div>

    <div class="back-to-top" onclick="scrollToTop()" id="backToTop">↑</div>"""

    html_content += """

    <script>
        function jumpToBook() {
            const selector = document.getElementById('bookSelector');
            const bookId = selector.value;
            if (bookId) {
                document.getElementById(bookId).scrollIntoView({ behavior: 'smooth' });
                selector.value = '';
            }
        }

        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function toggleStats() {
            const statsSection = document.getElementById('statisticsSection');
            if (statsSection) {
                statsSection.classList.toggle('active');
                if (statsSection.classList.contains('active')) {
                    statsSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
        }

        // Show/hide back to top button
        window.addEventListener('scroll', () => {
            const backToTop = document.getElementById('backToTop');
            const scrollProgress = document.getElementById('scrollProgress');

            if (window.scrollY > 300) {
                backToTop.style.display = 'flex';
            } else {
                backToTop.style.display = 'none';
            }

            // Update scroll progress bar
            const winHeight = window.innerHeight;
            const docHeight = document.documentElement.scrollHeight;
            const scrolled = window.scrollY;
            const scrollPercent = (scrolled / (docHeight - winHeight)) * 100;
            scrollProgress.style.width = scrollPercent + '%';
        });

        // Initialize
        document.getElementById('backToTop').style.display = 'none';
    </script>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML page created: {output_file}")

if __name__ == "__main__":
    create_odyssey_html("odyssey_formatted.txt", "odyssey_final.html")