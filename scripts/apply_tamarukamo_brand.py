from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TEXT_EXTS = {'.html', '.py', '.js', '.css', '.md', '.txt', '.yml', '.yaml', '.xml', '.json'}
SKIP = {ROOT / 'scripts' / 'apply_tamarukamo_brand.py'}

for path in ROOT.rglob('*'):
    if not path.is_file() or path in SKIP or path.suffix.lower() not in TEXT_EXTS:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    text = text.replace('https://kamowakaru.github.io/wakarukamo', 'https://kamowakaru.github.io/tamarukamo')
    text = text.replace('ワカルカモ', 'タマルカモ')
    text = text.replace('wakarukamo-point', 'tamarukamo-point')
    text = text.replace('WAKARUKAMO_GA_MEASUREMENT_ID', 'TAMARUKAMO_GA_MEASUREMENT_ID')
    text = text.replace('PC・Web・AIの「わからない」が、わかるかも。', 'お金の「わからない」が、貯まるかも。')
    path.write_text(text, encoding='utf-8')

# Do not carry the existing Wakarukamo AdSense account into a brand-new site.
adsense = re.compile(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=[^"]+"(?:\s+crossorigin="anonymous")?\s*></script>')
for path in ROOT.rglob('*.html'):
    text = adsense.sub('', path.read_text(encoding='utf-8', errors='ignore'))
    path.write_text(text, encoding='utf-8')

index = ROOT / 'index.html'
text = index.read_text(encoding='utf-8')
text = re.sub(r'\s*<!-- Impactアフィリエイト.*?<meta name="impact-site-verification"[^>]*>', '', text, flags=re.S)
text = re.sub(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=[^"]+" crossorigin="anonymous"></script>', '', text)
text = text.replace('＼ これ、どうやる？ ／', '＼ お金、どう貯める？ ／')
text = re.sub(r'<h1>その「わからない」が、<br>\s*<span>わかるかも。</span>\s*</h1>', '<h1>無理なく続けて、<br>\n<span>貯まるかも。</span>\n</h1>', text)
text = text.replace('PC・Web・AIをはじめとしたデジタルの困りごとを、わかりやすく解説するブログです。', '節約・家計管理・NISA・資産形成を、初心者向けにわかりやすく解説するブログです。')
text = text.replace('alt="ノートパソコンを使うカモのマスコット"', 'alt="お金の葉っぱに水をあげるカモのマスコット"')
text = text.replace('「これどうやる？」を、初心者でも追いやすい形でまとめるサイトです。', '「お金をどう整える？」を、初心者でも試しやすい形でまとめるサイトです。')

chips = '''<div class="chips">
<a class="chip" href="categories/saving.html">節約</a>
<a class="chip" href="categories/household-budget.html">家計管理</a>
<a class="chip" href="categories/nisa-investment.html">NISA</a>
<a class="chip" href="categories/asset-building.html">資産形成</a>
</div>'''
text = re.sub(r'<div class="chips">.*?</div>', chips, text, count=1, flags=re.S)

cats = [
 ('saving','🧾','節約','固定費・食費・光熱費など','1'),
 ('household-budget','📒','家計管理','家計簿・貯金・生活費など','6'),
 ('income-up','📈','収入アップ','転職・副業・働き方など','11'),
 ('nisa-investment','📊','NISA・投資信託','NISA・投資信託・商品比較','16'),
 ('asset-building','🌱','資産形成','長期投資・FIRE・取り崩し','21'),
 ('money-basics','💰','お金の基礎','税金・社会保険・金利など','26'),
 ('life-plan','🏠','ライフプラン','住宅・教育費・老後など','31'),
]
cards = []
for slug, icon, name, desc, no in cats:
    cards.append(f'''<div class="category-card-wrap"><a class="category-card" href="categories/{slug}.html">
<span class="icon">{icon}</span><strong>{name}</strong><small>{desc}</small>
</a><div class="category-parent-links"><span>まずはここから</span><a href="articles/{no}.html">{name}の基本を知る</a></div></div>''')
category_section = '''<section class="section" id="categories"><div class="container"><div class="section-title"><h2>カテゴリから探す</h2><a href="articles.html">記事一覧を見る →</a></div><div class="category-grid">''' + ''.join(cards) + '''</div></div></section>'''
text = re.sub(r'<section class="section" id="categories">.*?</section>', category_section, text, count=1, flags=re.S)
index.write_text(text, encoding='utf-8')

about = ROOT / 'about.html'
text = about.read_text(encoding='utf-8')
text = text.replace('PC・Web・AIの「わからない」を、できるだけわかりやすく整理することを目的としたサイトです。', '節約・家計管理・投資など、お金の「わからない」を初心者向けに整理することを目的としたサイトです。')
text = text.replace('企業の情報システム・DX推進・マーケティング業務などを経験。PC・Webサービス・業務自動化など、実際に試して分かったことを初心者向けに解説しています。', '家計管理や節約、資産形成について、自分で調べて試したことを初心者向けに整理しています。')
text = text.replace('個別の記事内容や、PC・Webサービスの操作方法などに関するご質問には回答しておりません。', '個別の記事内容や、投資判断・家計相談などに関するご質問には回答しておりません。')
about.write_text(text, encoding='utf-8')

gen = ROOT / 'scripts' / 'generate_site.py'
text = gen.read_text(encoding='utf-8')
text = re.sub(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=[^"]+" crossorigin="anonymous"></script>', '', text)
text = text.replace('企業の情報システム・DX推進・マーケティング業務などを経験。PC・Webサービス・業務自動化など、実際に試して分かったことを初心者向けに解説しています。', '家計管理や節約、資産形成について、自分で調べて試したことを初心者向けに整理しています。')
gen.write_text(text, encoding='utf-8')

analytics = ROOT / 'assets' / 'js' / 'analytics-config.js'
analytics.write_text("// GA4を利用するときだけ、G-から始まる測定IDを設定してください。\nwindow.TAMARUKAMO_GA_MEASUREMENT_ID = '';\n", encoding='utf-8')

css = ROOT / 'assets' / 'css' / 'style.css'
text = css.read_text(encoding='utf-8')
text = text.replace('--blue:#287be0;--navy:#172944;--text:#203047;--muted:#6c7c91;--line:#e2ebf4;--soft:#f7fbff;--sky:#ddf3ff;--yellow:#fff3a9;', '--blue:#3f9f74;--navy:#173b32;--text:#263a34;--muted:#6b7d76;--line:#dcebe3;--soft:#f7fcf8;--sky:#def4e7;--yellow:#fff0a8;')
text += '''\n/* Tamarukamo money-growth palette */
.hero{background:linear-gradient(180deg,#e4f7ea,#f4fbef 64%,#fff9e9)}
.hero h1{color:#173b32}.hero h1 span{color:#3f9f74}
.hero-art{background:radial-gradient(circle at 77% 83%,#f1cf63 0 15%,transparent 16%),radial-gradient(circle at 52% 84%,#a9d882 0 30%,transparent 31%)}
.chip,.tag-link,.tag-cloud a{background:#e7f6ec;color:#287b58}
.page-hero{background:linear-gradient(180deg,#e9f8ed,#fff)}
.article-main{background:#f7fcf8}.thumb,.parent-thumb{background:#edf7ef}
.category-grid{grid-template-columns:repeat(7,1fr)}
@media(max-width:1100px){.category-grid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:700px){.category-grid{grid-template-columns:repeat(2,1fr)}}
'''
css.write_text(text, encoding='utf-8')

print('Applied Tamarukamo branding and layout')
