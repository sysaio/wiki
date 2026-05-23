import os
import re
import yaml
import markdown
import subprocess
from datetime import datetime

# === KONSTANTY ===
MARKDOWN_DIR = 'markdown'
HTML_DIR = 'navody'
INDEX_FILE = 'index.html'
CATEGORY_ORDER = ['IoT', 'Automatizace', 'Informatika', 'Elektronika', 'Cestování', 'Domácnost', 'Počítače']

# === VYTVOR SLOŽKY PRO HTML ===
os.makedirs(HTML_DIR, exist_ok=True)

# === POMOCNÁ FUNKCE PRO YAML FRONTMATTER ===
def parse_frontmatter(text):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        content = match.group(2)
        return frontmatter, content
    return {}, text

# === ZJISTI DATUM POSLEDNÍ ÚPRAVY ===
def get_git_last_modified_date(file_path):
    try:
        output = subprocess.check_output(['git', 'log', '-1', '--format=%cd', '--', file_path])
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return 'Neznámé'

# === GIT PULL PŘED SPUŠTĚNÍM ===
try:
    subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
    print("✅ Aktualizace z GitHubu proběhla.")
except subprocess.CalledProcessError:
    print("⚠️ Nepodařilo se provést git pull.")

# === ZPRACUJ VŠECHNY .md SOUBORY ===
navody_html = []
for md_file in sorted(os.listdir(MARKDOWN_DIR)):
    if not md_file.endswith('.md'):
        continue

    name = os.path.splitext(md_file)[0]
    md_path = os.path.join(MARKDOWN_DIR, md_file)

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        metadata, text = parse_frontmatter(raw_text)

    title = metadata.get('title', name)
    category = metadata.get('category', 'Nezařazeno')
    tags = metadata.get('tags', [])
    html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    last_modified = get_git_last_modified_date(md_path)

    html_file = f"{name}.html"
    html_path = os.path.join(HTML_DIR, html_file)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{title}</title></head>
<body>
{html}
<p><a href="../index.html">← Zpět na přehled</a></p>
</body>
</html>''')

    navody_html.append({
        'name': name,
        'file': html_file,
        'title': title,
        'category': category,
        'tags': tags,
        'md_link': f'markdown/{name}.md',
        'last_modified': last_modified
    })

# === GENERUJ index.html ===
with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(f'''<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <title>RabuKate Wiki</title>
  <style>
    body {{ font-family: sans-serif; max-width: 1000px; margin: auto; padding: 2em; }}
    input[type="text"] {{ width: 100%; padding: 0.5em; margin-bottom: 1em; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5em; text-align: left; }}
    th {{ background-color: #f0f0f0; }}
    button {{ padding: 0.3em 0.6em; }}
    .category-buttons button.active {{ background-color: #007acc; color: white; }}
    .category-buttons {{ margin-bottom: 1em; }}
    @media (max-width: 600px) {{
      table, thead, tbody, th, td, tr {{ display: block; }}
      td {{ margin-bottom: 1em; }}
    }}
  </style>
</head>
<body>
  <h1>📚 RabuKate Wiki</h1>

  <div class="category-buttons">
    <button data-cat="">Všechny</button>
''')

    for cat in CATEGORY_ORDER:
        f.write(f'    <button data-cat="{cat}">{cat}</button>\n')

    f.write('''
  </div>

  <input type="text" id="search" placeholder="🔍 Hledat...">
  <table>
    <thead>
      <tr>
        <th>Kategorie</th>
        <th>Poslední úprava</th>
        <th>Návod (HTML)</th>
        <th>GitHub (Markdown)</th>
        <th>Tisk</th>
        <th>Zpětná vazba</th>
      </tr>
    </thead>
    <tbody>
''')

    for navod in navody_html:
        f.write(f'''      <tr data-category="{navod['category']}">
        <td>{navod['category']}</td>
        <td>{navod['last_modified']}</td>
        <td><a href="navody/{navod['file']}">{navod['title']}</a></td>
        <td><a href="{navod['md_link']}">{navod['title']}</a></td>
        <td><button onclick="window.print()">🖨️</button></td>
        <td>
          <form onsubmit="alert('Děkujeme za zpětnou vazbu!'); return false;">
            <input type="text" placeholder="Váš názor..." required>
            <button type="submit">Odeslat</button>
          </form>
        </td>
      </tr>\n''')

    f.write('''    </tbody>
  </table>

  <script>
    const searchInput = document.getElementById('search');
    const rows = document.querySelectorAll('tbody tr');
    const categoryButtons = document.querySelectorAll('.category-buttons button');

    searchInput.addEventListener('input', function () {
      const query = this.value.toLowerCase();
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });

    function filterByCategory(cat) {
      rows.forEach(row => {
        const rowCat = row.getAttribute('data-category');
        row.style.display = (!cat || rowCat === cat) ? '' : 'none';
      });
    }

    categoryButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        categoryButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterByCategory(btn.getAttribute('data-cat'));
      });
    });

    categoryButtons[0].classList.add('active');
  </script>
</body>
</html>
''')

# === GIT COMMIT A PUSH ===
try:
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Automatická aktualizace wiki s YAML metadaty'], check=True)
    subprocess.run(['git', 'push'], check=True)
    print("✅ Změny odeslány na GitHub.")
except subprocess.CalledProcessError:
    print("⚠️ Git commit/push selhal – možná nejsou žádné změny.")

