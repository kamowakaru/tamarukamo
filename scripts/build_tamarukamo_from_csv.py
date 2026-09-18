from pathlib import Path
import csv
import json
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = Path('/workspace/scratch/aa484b8d857f/tamarukamo-article-management-draft(2).csv')
CONTENT = ROOT / 'content' / 'articles'

CATEGORIES = [
    {'slug': 'saving', 'name': '節約', 'icon': '🧾', 'description': '固定費・食費・光熱費など'},
    {'slug': 'household-budget', 'name': '家計管理', 'icon': '📒', 'description': '家計簿・貯金・生活費など'},
    {'slug': 'income-up', 'name': '収入アップ', 'icon': '📈', 'description': '転職・副業・働き方など'},
    {'slug': 'nisa-investment', 'name': 'NISA・投資信託', 'icon': '📊', 'description': 'NISA・投資信託・商品比較'},
    {'slug': 'asset-building', 'name': '資産形成', 'icon': '🌱', 'description': '長期投資・FIRE・取り崩し'},
    {'slug': 'money-basics', 'name': 'お金の基礎', 'icon': '💰', 'description': '税金・社会保険・金利など'},
    {'slug': 'life-plan', 'name': 'ライフプラン', 'icon': '🏠', 'description': '住宅・教育費・老後など'},
]

TAGS = [
    {'slug': 'saving', 'name': '節約'},
    {'slug': 'household-budget', 'name': '家計管理'},
    {'slug': 'income-up', 'name': '収入アップ'},
    {'slug': 'nisa', 'name': 'NISA'},
    {'slug': 'investment-trust', 'name': '投資信託'},
    {'slug': 'asset-building', 'name': '資産形成'},
    {'slug': 'money-basics', 'name': 'お金の基礎'},
    {'slug': 'life-plan', 'name': 'ライフプラン'},
]

CATEGORY_SLUGS = {x['name']: x['slug'] for x in CATEGORIES}
CATEGORY_TAGS = {
    '節約': ['saving'],
    '家計管理': ['household-budget'],
    '収入アップ': ['income-up'],
    'NISA・投資信託': ['nisa', 'investment-trust'],
    '資産形成': ['asset-building'],
    'お金の基礎': ['money-basics'],
    'ライフプラン': ['life-plan'],
}


def q(value):
    return str(value).replace('\\', '\\\\').replace('"', '\\"')


with SOURCE_CSV.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit('CSVに記事がありません')

required = {'No.', 'カテゴリ', 'グループ', '種別', 'タイトル', '公開済', 'アフィ候補'}
if set(rows[0]) != required:
    raise SystemExit(f'CSV列が一致しません: {list(rows[0])}')

numbers = [r['No.'].strip() for r in rows]
if len(numbers) != len(set(numbers)):
    raise SystemExit('管理番号が重複しています')
if any(not re.fullmatch(r'\d+(?:_\d+)*', no) for no in numbers):
    raise SystemExit('不正な管理番号があります')
if any(r['カテゴリ'] not in CATEGORY_SLUGS for r in rows):
    raise SystemExit('未登録カテゴリがあります')

parents = {r['No.']: r for r in rows if r['種別'] == '親'}
for row in rows:
    root = row['No.'].split('_', 1)[0]
    if root not in parents:
        raise SystemExit(f'{row["No."]}: 親記事 {root} がありません')

children = {}
for row in rows:
    root = row['No.'].split('_', 1)[0]
    if row['No.'] != root:
        children.setdefault(root, []).append(row)

# Publication master used by generate_site.py. All CSV titles are shown now,
# while their article bodies remain explicit placeholders for later rewriting.
management = ROOT / 'data' / 'article-management.csv'
management.parent.mkdir(parents=True, exist_ok=True)
with management.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    for row in rows:
        out = dict(row)
        out['公開済'] = '済'
        writer.writerow(out)

shutil.copy2(SOURCE_CSV, ROOT / 'data' / 'article-management-source.csv')
(ROOT / 'data' / 'categories.json').write_text(json.dumps(CATEGORIES, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'data' / 'tags.json').write_text(json.dumps(TAGS, ensure_ascii=False, indent=2), encoding='utf-8')

tags_dir = ROOT / 'tags'
tags_dir.mkdir(exist_ok=True)
for old in tags_dir.glob('*.html'):
    old.unlink()

CONTENT.mkdir(parents=True, exist_ok=True)
for old in CONTENT.glob('*.md'):
    old.unlink()

for row in rows:
    no = row['No.'].strip()
    title = row['タイトル'].strip()
    category_name = row['カテゴリ'].strip()
    root = no.split('_', 1)[0]
    tags = CATEGORY_TAGS[category_name]
    desc = f'「{title}」について、初心者向けに分かりやすく解説する記事です。'
    point = f'{title}について、実体験と公的情報を確認しながら内容を追加します。'
    fm = [
        '---',
        f'title: "{q(title)}"',
        'date: "2026-09-19"',
        f'article_no: "{no}"',
        f'category: "{CATEGORY_SLUGS[category_name]}"',
        'tags:',
        *[f'  - {tag}' for tag in tags],
        f'description: "{q(desc)}"',
        f'point: "{q(point)}"',
        '---',
        '',
    ]
    body = [
        '## 結論',
        '',
        f'この記事では、**{title}**について解説します。現在、本文を準備中です。',
        '',
    ]
    if no == root:
        body += ['## このグループで分かること', '']
        for child in children.get(root, []):
            body.append(f'[{child["タイトル"]}]({child["No."]}.html)')
            body.append('')
        body += [
            '## 記事本文',
            '',
            '具体的な内容は、体験談・制度の最新情報・確認手順を整理してから追記します。',
            '',
        ]
    else:
        body += [
            '## 記事本文',
            '',
            '具体的な内容は、体験談・制度の最新情報・確認手順を整理してから追記します。',
            '',
            '## 親記事',
            '',
            f'[{parents[root]["タイトル"]}]({root}.html)',
            '',
        ]
    (CONTENT / f'{no}.md').write_text('\n'.join(fm + body), encoding='utf-8')

# Recreate category page shells expected by generate_site.py.
categories_dir = ROOT / 'categories'
categories_dir.mkdir(exist_ok=True)
for old in categories_dir.glob('*.html'):
    old.unlink()
for cat in CATEGORIES:
    page = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{cat['name']} | タマルカモ</title><link rel="stylesheet" href="../assets/css/style.css"></head><body data-root="../"><header class="site-header"><div class="container header-inner"><a class="brand" href="../index.html"><img src="../assets/images/logo-duck.webp" alt=""><span><strong>タマルカモ</strong><small>お金の「わからない」が、貯まるかも。</small></span></a><button class="menu-btn" aria-label="メニュー">☰</button><nav class="nav"><a href="../index.html">ホーム</a><a href="../index.html#categories">カテゴリ</a><a href="../articles.html">記事一覧</a><a href="../about.html">このサイトについて</a></nav></div></header><main><section class="page-hero"><div class="container"><div class="breadcrumb"><a href="../index.html">ホーム</a> › {cat['name']}</div><h1>{cat['name']}</h1><p>{cat['description']}の記事一覧です。</p></div></section><section class="section"><div class="container"><div class="grouped-article-list" data-collection="category"><!-- ARTICLES:START --><!-- ARTICLES:END --></div></div></section></main><footer class="footer"><div class="container footer-inner"><div class="footer-brand"><img src="../assets/images/logo-duck.webp" alt=""><div><strong>タマルカモ</strong><div style="font-size:12px;color:#6c7c91">お金の「わからない」が、貯まるかも。</div></div></div><div class="footer-links"><a href="../index.html">ホーム</a><a href="../articles.html">記事一覧</a><a href="../about.html">このサイトについて</a><a href="../privacy.html">プライバシーポリシー</a></div></div><p class="copyright">© 2026 タマルカモ</p></footer><script src="../assets/js/site.js"></script></body></html>'''
    (categories_dir / f'{cat["slug"]}.html').write_text(page, encoding='utf-8')

print(f'Prepared {len(rows)} dummy articles / {len(parents)} parent groups / {len(CATEGORIES)} categories')
