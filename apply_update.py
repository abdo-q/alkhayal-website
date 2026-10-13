from pathlib import Path
import requests, re, shutil, json
from urllib.parse import urlparse

ROOT = Path(__file__).parent
ASSETS = ROOT/'assets'; ASSETS.mkdir(exist_ok=True)
new_images = [
 ('https://i.ibb.co/LdYsKBWd/92223568324.png','gallery-24.png'),
 ('https://i.ibb.co/pBNL4vbg/Gente.png','gallery-25.png'),
 ('https://i.ibb.co/s9xKFMW1/1.png','gallery-26.png'),
 ('https://i.ibb.co/d4xGsxLS/image.jpg','gallery-27.jpg'),
 ('https://i.ibb.co/WNC9k3Wh/Fundo-azul-da-aguarela-Vetor-Gr-tis.jpg','gallery-28.jpg'),
 ('https://i.ibb.co/wN3TPzSj/743023638586932333.jpg','gallery-29.jpg'),
]
for url, name in new_images:
    r=requests.get(url, timeout=60); r.raise_for_status(); (ASSETS/name).write_bytes(r.content)
shutil.copy2('/home/ubuntu/upload/bffb9ec3-8392-4185-835d-c38ac837ac4f(1).mp4', ASSETS/'customer-video.mp4')

# Add the full Soft Spotlight composition as a reusable site background and decorative image layer.
css = ROOT/'style.css'
s = css.read_text(encoding='utf-8')
s += '''\n\n/* Soft Spotlight background inspired by Opensource UI's public component. The central demo text is intentionally omitted. */
body.site-shell{position:relative;isolation:isolate;background:#e8e6e1;background-image:none;overflow-x:hidden}
body.site-shell:before{content:"";position:fixed;inset:0;z-index:-4;pointer-events:none;background:radial-gradient(circle at 50% 18%,#fff 0%,#f7f6f3 38%,#e8e6e1 72%,#d6d3ce 100%)}
body.site-shell:after{content:"";position:fixed;inset:0;z-index:-3;pointer-events:none;background-image:radial-gradient(circle at 50% 0%,rgba(255,255,255,.9) 0%,transparent 52%),radial-gradient(circle at center,transparent 48%,rgba(41,37,36,.12) 100%),radial-gradient(circle at center,#000 1px,transparent 1px);background-size:auto,auto,4px 4px;background-position:center,center,center;opacity:1}
.site-background-art{position:fixed;inset:0;z-index:-2;overflow:hidden;pointer-events:none}
.site-background-art img{position:absolute;display:block;object-fit:cover;border:7px solid rgba(255,255,255,.78);box-shadow:0 20px 45px rgba(41,37,36,.18);opacity:.72;filter:saturate(.86) contrast(.96)}
.site-background-art .art-1{width:170px;height:150px;top:9%;right:4%;transform:rotate(8deg)}
.site-background-art .art-2{width:210px;height:155px;top:38%;left:-45px;transform:rotate(-9deg)}
.site-background-art .art-3{width:160px;height:180px;top:70%;right:3%;transform:rotate(-7deg)}
.site-background-art .art-4{width:190px;height:135px;top:83%;left:12%;transform:rotate(11deg)}
.site-background-art .art-5{width:150px;height:170px;top:21%;left:7%;transform:rotate(-13deg)}
.site-background-art .art-6{width:200px;height:150px;top:56%;right:11%;transform:rotate(5deg)}
body.site-shell header,body.site-shell main,body.site-shell footer{position:relative;z-index:1}
body.site-shell .hero,body.site-shell .split-band{background:rgba(247,246,243,.46)}
body.site-shell .section{background:rgba(251,250,247,.24)}
body.site-shell.content-art .page-hero{background:linear-gradient(135deg,rgba(18,59,74,.95),rgba(9,24,31,.92)),url("assets/gallery-28.jpg") center/cover}
body.site-shell.content-art .article-list{background:rgba(255,255,255,.55);border-radius:28px}
body.site-shell.cleaning-art .page-hero{background:linear-gradient(135deg,rgba(18,59,74,.9),rgba(7,19,25,.88)),url("assets/gallery-27.jpg") center/cover}
body.site-shell.cleaning-art .section{background:rgba(255,255,255,.56);border-radius:28px}
.contact{background-color:#050505;background-image:radial-gradient(#fff 1px,transparent 1px);background-size:18px 18px}
@media(max-width:760px){.site-background-art img{opacity:.35}.site-background-art .art-1{right:-50px}.site-background-art .art-5{left:-45px}.site-background-art .art-6{right:-50px}}
'''
css.write_text(s, encoding='utf-8')

art_html='''<div class="site-background-art" aria-hidden="true"><img class="art-1" src="assets/gallery-24.png" alt=""><img class="art-2" src="assets/gallery-25.png" alt=""><img class="art-3" src="assets/gallery-26.png" alt=""><img class="art-4" src="assets/gallery-27.jpg" alt=""><img class="art-5" src="assets/gallery-28.jpg" alt=""><img class="art-6" src="assets/gallery-29.jpg" alt=""></div>'''
for p in ROOT.glob('*.html'):
    text=p.read_text(encoding='utf-8')
    cls='site-shell'
    if p.name=='articles.html': cls+=' content-art'
    if p.name=='cleaning.html': cls+=' cleaning-art'
    text=text.replace('<body>', f'<body class="{cls}">', 1)
    text=text.replace(f'<body class="{cls}">{art_html}', f'<body class="{cls}">{art_html}', 1) if art_html not in text else text
    if art_html not in text:
        text=text.replace(f'<body class="{cls}">', f'<body class="{cls}">{art_html}', 1)
    text=text.replace('<link rel="stylesheet" href="style.css"><link rel="manifest" href="site.webmanifest">', '<link rel="stylesheet" href="style.css"><link rel="manifest" href="site.webmanifest"><link rel="icon" href="logo.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="logo.svg">')
    text=text.replace('assets/intro.mp4','assets/customer-video.mp4')
    text=text.replace('لمحات من خدمات شركة الخيال','صيانة أفران الغاز')
    text=text.replace('فيديو تعريفي قصير من صور الموقع. أرسل لنا رابط الفيديو الرسمي لاحقًا لاستبداله به.','شاهد الفيديو التعريفي المرفق وتعرّف على طريقة عرض خدمات شركة الخيال.')
    # Add a gas-oven service card to the existing service card groups once per page.
    if p.name in ('index.html','services.html') and 'gas-ovens.html' not in text:
        marker='</div></section>'
        card='<article class="service-card"><img class="service-image" src="assets/gallery-24.png" alt="صيانة أفران الغاز" loading="lazy"><div class="card-body"><p class="card-kicker">خدمة منزلية</p><h3>صيانة أفران الغاز</h3><p>فحص وتنظيف ومعالجة الملاحظات الشائعة في أفران الغاز مع أولوية السلامة.</p><a class="icon-link" href="gas-ovens.html">تفاصيل الخدمة <span>←</span></a></div></article>'
        # target first service grid closing in each page
        pos=text.find(marker, text.find('service-cards'))
        if pos!=-1: text=text[:pos]+card+text[pos:]
    text=text.replace('نقل الأثاث، الصيانة المنزلية، صيانة التكييف، وخدمات النظافة','نقل الأثاث، الصيانة المنزلية، صيانة التكييف، صيانة أفران الغاز، وخدمات النظافة')
    p.write_text(text,encoding='utf-8')

# Add dedicated gas oven page.
body='''<section class="page-hero"><p class="eyebrow">خدمات شركة الخيال</p><h1>صيانة أفران الغاز</h1><p>خدمة مخصصة لفحص وتنظيف ومعالجة الملاحظات الشائعة في أفران الغاز، مع التركيز على السلامة قبل أي خطوة.</p></section><section class="section detail-layout"><img class="detail-image" src="assets/gallery-24.png" alt="صيانة أفران الغاز"><div><h2>سلامة مطبخك أولًا</h2><p>إذا ظهرت رائحة غاز أو لهب غير منتظم أو صوت غير معتاد، أغلق مصدر الغاز وابتعد عن إشعال أي مفتاح واستعن بفني مختص. لا تفك صمام الغاز أو التوصيلات بنفسك.</p><ul class="check-list"><li>فحص العلامات الظاهرة ووصف المشكلة</li><li>تنظيف الأجزاء القابلة للتنظيف وفق تعليمات الشركة</li><li>الانتباه للتهوية ومصدر الغاز</li><li>التواصل المباشر عند وجود رائحة أو تسرب</li></ul><a class="button" href="contact.html">اطلب فحصًا</a><a class="button light" href="articles.html#maintenance">اقرأ نصائح السلامة</a></div></section><section class="section related"><h2>قد تهمك أيضًا</h2><p><a href="services.html">كل الخدمات</a> · <a href="cleaning.html">خدمات النظافة</a> · <a href="contact.html">تواصل معنا</a></p></section>'''
head='''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>صيانة أفران الغاز | شركة الخيال</title><meta name="description" content="خدمة صيانة أفران الغاز من شركة الخيال مع نصائح السلامة والفحص والتنظيف والتواصل المباشر."><meta name="keywords" content="صيانة أفران الغاز, تنظيف فرن غاز, فني أفران, خدمات منزلية, شركة الخيال"><meta name="robots" content="index,follow"><link rel="canonical" href="https://abdo-q.github.io/alkhayal-website/gas-ovens.html"><meta property="og:type" content="website"><meta property="og:title" content="صيانة أفران الغاز | شركة الخيال"><meta property="og:description" content="فحص وتنظيف ومعالجة الملاحظات الشائعة في أفران الغاز مع أولوية السلامة."><meta property="og:url" content="https://abdo-q.github.io/alkhayal-website/gas-ovens.html"><meta property="og:image" content="https://abdo-q.github.io/alkhayal-website/assets/gallery-24.png"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="style.css"><link rel="manifest" href="site.webmanifest"><link rel="icon" href="logo.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="logo.svg"></head><body class="site-shell">'''
# Reuse current nav/footer/floating from services page for consistent links.
services= (ROOT/'services.html').read_text(encoding='utf-8')
header=services[services.find('<header>'):services.find('</header>')+9]
footer=services[services.find('<footer>'):services.find('</footer>')+9]
floating=services[services.find('<div class="floating-contact"'):services.find('</div></body></html>')+6]
(ROOT/'gas-ovens.html').write_text(head+art_html+header+'<main>'+body+'</main>'+footer+floating+'</body></html>',encoding='utf-8')

# Add route to manifest and sitemap.
manifest=json.loads((ROOT/'site.webmanifest').read_text(encoding='utf-8'))
manifest['icons']=[{'src':'logo.svg','sizes':'any','type':'image/svg+xml','purpose':'any maskable'}]
(ROOT/'site.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
routes=json.loads((ROOT/'manus-routes.json').read_text(encoding='utf-8'))
routes['routes'].append({'path':'/gas-ovens.html','title':'صيانة أفران الغاز'})
(ROOT/'manus-routes.json').write_text(json.dumps(routes,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
sitemap=ROOT/'sitemap.xml'; st=sitemap.read_text(encoding='utf-8').replace('</urlset>','<url><loc>https://abdo-q.github.io/alkhayal-website/gas-ovens.html</loc></url>\n</urlset>'); sitemap.write_text(st,encoding='utf-8')
print('updated',len(new_images),'images, customer video, spotlight background, gas ovens page')
