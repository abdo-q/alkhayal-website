from pathlib import Path
import json

ROOT=Path(__file__).parent

# Remove the gallery from all navigation/footer references and replace it with useful pages.
for p in ROOT.glob('*.html'):
    text=p.read_text(encoding='utf-8')
    text=text.replace('<a class="" href="gallery.html">المعرض</a>','<a class="" href="faq.html">الأسئلة الشائعة</a><a class="" href="process.html">كيف نعمل</a>')
    text=text.replace('<a class="active" href="gallery.html">المعرض</a>','<a class="" href="faq.html">الأسئلة الشائعة</a><a class="" href="process.html">كيف نعمل</a>')
    text=text.replace('<a href="gallery.html">معرض الصور</a>','<a href="faq.html">الأسئلة الشائعة</a><a href="process.html">كيف نعمل</a>')
    text=text.replace('gallery.html','faq.html')
    text=text.replace('استعرض كل الصور','اقرأ الأسئلة الشائعة')
    p.write_text(text,encoding='utf-8')

# Add article jump buttons and a longer guide section.
articles=ROOT/'articles.html'
text=articles.read_text(encoding='utf-8')
if 'article-jump-buttons' not in text:
    buttons='''<nav class="article-jump-buttons" aria-label="اختيار المقال"><a href="#moving">نقل الأثاث</a><a href="#maintenance">الصيانة</a><a href="#cleaning">التنظيف</a><a href="#ac">التكييف</a><a href="#gas">أفران الغاز</a><a href="#moving-cost">التكلفة</a><a href="#home-checklist">فحص المنزل</a></nav>'''
    text=text.replace('<section class="section article-list">',buttons+'<section class="section article-list">',1)
if 'article-more-help' not in text:
    more='''<section id="article-more-help" class="section article-more-help"><p class="eyebrow">دليل سريع</p><h2>كيف تستخدم هذه المقالات؟</h2><div class="guide-grid"><div><span>01</span><h3>اختر الموضوع</h3><p>ابدأ بالمقال الأقرب للخدمة التي تحتاجها، ثم استخدم الروابط داخل المقال للانتقال إلى الخدمة أو المقال المرتبط.</p></div><div><span>02</span><h3>جهّز التفاصيل</h3><p>دوّن المكان والموعد ووصف المشكلة أو كمية الأثاث. المعلومات الواضحة تجعل التواصل أسرع.</p></div><div><span>03</span><h3>تواصل معنا</h3><p>عندما تتضح الصورة، انتقل إلى <a href="contact.html">صفحة التواصل</a> أو راجع <a href="services.html">كل الخدمات</a>.</p></div></div></section>'''
    text=text.replace('<section class="contact">',more+'<section class="contact">',1)
articles.write_text(text,encoding='utf-8')

# Make core pages longer with useful, connected content.
additions={
'about.html':'''<section class="section about-extra"><p class="eyebrow">ما الذي نقدمه؟</p><h2>تجربة أوضح من أول زيارة</h2><div class="guide-grid"><div><span>01</span><h3>نفهم الاحتياج</h3><p>نبدأ بنوع الخدمة والموقع والموعد والتفاصيل التي تؤثر في التنفيذ، بدل تقديم إجابة عامة لا تناسب المكان.</p></div><div><span>02</span><h3>نرتب الخطوات</h3><p>نربطك بالمقال المناسب، ثم بصفحة الخدمة والتواصل حتى تعرف ما الذي تجهزه قبل الطلب.</p></div><div><span>03</span><h3>نبقى قريبين</h3><p>يمكنك الوصول إلى <a href="services.html">الخدمات</a> أو <a href="articles.html">المقالات</a> أو <a href="contact.html">التواصل</a> من أي صفحة.</p></div></div></section>''',
'services.html':'''<section class="section services-extra"><p class="eyebrow">اختيار الخدمة</p><h2>كيف تعرف القسم المناسب؟</h2><p>للنقل ابدأ بمعلومات الأثاث والمداخل. للصيانة اذكر العلامات ووقت ظهورها. للتكييف راقب التبريد والتسربات. لأفران الغاز قدّم وصفًا آمنًا للرائحة أو اللهب دون لمس التوصيلات. وللنظافة حدد الغرف والمساحة والموعد.</p><p>يمكنك قراءة <a href="articles.html">مقالاتنا الإرشادية</a>، ثم الانتقال إلى <a href="contact.html">صفحة التواصل</a> لإرسال التفاصيل.</p></section>''',
'contact.html':'''<section class="section contact-extra"><p class="eyebrow">قبل الإرسال</p><h2>رسالة قصيرة تساعدنا</h2><p>اكتب: نوع الخدمة، المدينة أو المنطقة، الموعد المفضل، وصف مختصر، وأي صورة أو ملاحظة مهمة. إذا كان الطلب متعلقًا بالغاز أو الكهرباء، لا تحاول إصلاح الخلل قبل التواصل مع مختص.</p><div class="quick-links"><a class="button light" href="articles.html">راجع المقالات أولًا</a><a class="button light" href="faq.html">شاهد الأسئلة الشائعة</a><a class="button light" href="process.html">تعرّف على طريقة العمل</a></div></section>'''
}
for fn,block in additions.items():
    p=ROOT/fn; t=p.read_text(encoding='utf-8')
    if 'about-extra' not in t and 'services-extra' not in t and 'contact-extra' not in t:
        t=t.replace('</main>',block+'</main>',1)
        p.write_text(t,encoding='utf-8')

# New longer pages.
common_head='''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="style.css"><link rel="manifest" href="site.webmanifest"><link rel="icon" href="logo.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="logo.svg">'''
meta_faq='''<title>الأسئلة الشائعة | شركة الخيال</title><meta name="description" content="إجابات شركة الخيال عن نقل الأثاث والصيانة والنظافة والتكييف وصيانة أفران الغاز."><meta name="keywords" content="أسئلة شائعة خدمات منزلية, نقل أثاث, صيانة منزلية, تنظيف, تكييف, أفران الغاز">'''
meta_process='''<title>كيف نعمل | شركة الخيال</title><meta name="description" content="تعرف على خطوات طلب خدمة منزلية من شركة الخيال من وصف الاحتياج حتى التواصل وترتيب الموعد."><meta name="keywords" content="طريقة طلب خدمة منزلية, شركة الخيال, نقل أثاث, صيانة, تنظيف منازل">'''
faq_body='''<section class="page-hero"><p class="eyebrow">مساعدة قبل التواصل</p><h1>الأسئلة الشائعة</h1><p>إجابات سريعة تساعدك على اختيار الخدمة وتجهيز المعلومات المناسبة.</p></section><section class="section faq-long"><details open><summary>ما الخدمات التي تقدمها شركة الخيال؟</summary><p>نقدم معلومات وخدمات مرتبطة بنقل الأثاث، الصيانة المنزلية، صيانة التكييف، صيانة أفران الغاز، وخدمات النظافة. ابدأ من <a href="services.html">صفحة الخدمات</a>.</p></details><details><summary>ما المعلومات المطلوبة عند التواصل؟</summary><p>نوع الخدمة، المنطقة، الموعد، وصف مختصر للمطلوب، وأي قيود في المكان. تساعدك <a href="articles.html">المقالات</a> على تجهيز التفاصيل.</p></details><details><summary>ماذا أفعل عند رائحة الغاز؟</summary><p>أغلق مصدر الغاز إن كان ذلك آمنًا، افتح التهوية، لا تشعل مفاتيح أو لهبًا، وابتعد عن مصدر الخطر. راجع <a href="gas-ovens.html">صفحة صيانة أفران الغاز</a> ولا تفك التوصيلات بنفسك.</p></details><details><summary>هل يمكن الاستفسار قبل الموعد؟</summary><p>نعم. استخدم <a href="contact.html">صفحة التواصل</a> لشرح احتياجك قبل ترتيب الخطوة التالية.</p></details><details><summary>أين أجد نصائح التنظيف والتكييف؟</summary><p>ستجدها في <a href="articles.html#cleaning">مقال التنظيف</a> و<a href="articles.html#ac">مقال التكييف</a>، مع روابط إلى صفحات الخدمات.</p></details></section><section class="section faq-next"><h2>لم تجد إجابتك؟</h2><p>انتقل إلى <a href="process.html">كيف نعمل</a> أو تواصل معنا مباشرة.</p><a class="button" href="contact.html">تواصل معنا</a></section>'''
process_body='''<section class="page-hero"><p class="eyebrow">خطوات بسيطة</p><h1>كيف نعمل؟</h1><p>نحوّل تفاصيل الطلب إلى خطوات مفهومة تساعدك على الاستعداد والتواصل.</p></section><section class="section process-grid"><div><span>01</span><h2>صف احتياجك</h2><p>حدد الخدمة، المنطقة، الموعد، وأهم التفاصيل. كلما كان الوصف أوضح كان اختيار الخطوة التالية أسهل.</p><a href="contact.html">صف احتياجك ←</a></div><div><span>02</span><h2>راجع الإرشادات</h2><p>استخدم <a href="articles.html">المقالات</a> لمعرفة ما الذي تجهزه قبل نقل الأثاث أو الصيانة أو التنظيف.</p><a href="articles.html">اقرأ المقالات ←</a></div><div><span>03</span><h2>اختر الخدمة</h2><p>انتقل إلى صفحة الخدمة المرتبطة: <a href="gas-ovens.html">أفران الغاز</a>، <a href="cleaning.html">النظافة</a>، أو غيرها.</p><a href="services.html">كل الخدمات ←</a></div><div><span>04</span><h2>تواصل مباشرة</h2><p>استخدم الهاتف أو واتساب من <a href="contact.html">صفحة التواصل</a> لترتيب المعلومات والموعد.</p><a href="contact.html">تواصل معنا ←</a></div></section><section class="section process-note"><h2>نحن نؤمن بالوضوح</h2><p>لا تحتاج إلى حفظ كل الخطوات. ابدأ من <a href="index.html">الرئيسية</a>، واستخدم الروابط الموجودة في كل صفحة للوصول إلى المعلومة التالية.</p></section>'''
# Get shared header/footer/floating from an existing page.
source=(ROOT/'services.html').read_text(encoding='utf-8')
header=source[source.find('<header>'):source.find('</header>')+9]
footer=source[source.find('<footer>'):source.find('</footer>')+9]
floating=source[source.find('<div class="floating-contact"'):source.find('</div></body></html>')+6]
for fn,meta,body,active in [('faq.html',meta_faq,faq_body,'faq.html'),('process.html',meta_process,process_body,'process.html')]:
    html=common_head+meta+'</head><body class="site-shell"><div class="site-background-art" aria-hidden="true"><img class="art-1" src="assets/gallery-24.png" alt=""><img class="art-2" src="assets/gallery-25.png" alt=""><img class="art-3" src="assets/gallery-26.png" alt=""><img class="art-4" src="assets/gallery-27.jpg" alt=""><img class="art-5" src="assets/gallery-28.jpg" alt=""><img class="art-6" src="assets/gallery-29.jpg" alt=""></div>'+header+'<main>'+body+'</main>'+footer+floating+'</body></html>'
    # mark the matching nav item active
    html=html.replace(f'<a class="" href="{active}">',f'<a class="active" href="{active}">')
    (ROOT/fn).write_text(html,encoding='utf-8')

# Update route metadata and sitemap.
routes=json.loads((ROOT/'manus-routes.json').read_text(encoding='utf-8'))
for item in [{'path':'/faq.html','title':'الأسئلة الشائعة'},{'path':'/process.html','title':'كيف نعمل'}]:
    if item not in routes['routes']: routes['routes'].append(item)
(ROOT/'manus-routes.json').write_text(json.dumps(routes,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
sitemap=ROOT/'sitemap.xml'; st=sitemap.read_text(encoding='utf-8').replace('<url><loc>https://abdo-q.github.io/alkhayal-website/gallery.html</loc></url>\n','')
for url in ['faq.html','process.html']:
    if f'>{url}</loc>' not in st: st=st.replace('</urlset>',f'<url><loc>https://abdo-q.github.io/alkhayal-website/{url}</loc></url>\n</urlset>')
sitemap.write_text(st,encoding='utf-8')

# Floating buttons: flush with the edge, square tabs, text always visible.
css=ROOT/'style.css'; s=css.read_text(encoding='utf-8')
s += '''\n\n/* Edge-hugging square contact tabs */
.floating-contact{right:0;bottom:22%;gap:8px;align-items:stretch}
.floating-contact a{width:118px;height:54px;min-height:54px;border-radius:12px 0 0 12px;justify-content:flex-start;padding:0 14px;gap:9px}
.floating-contact b{font-size:20px;flex:0 0 auto}.floating-contact span{position:static;opacity:1;background:transparent;padding:0;font-size:12px;font-weight:800;pointer-events:auto;white-space:nowrap}.floating-contact a:hover{transform:translateX(-4px)}
@media(max-width:520px){.floating-contact{bottom:18%;gap:7px}.floating-contact a{width:58px;height:52px;min-height:52px;padding:0;justify-content:center;border-radius:10px 0 0 10px}.floating-contact span{display:none}.floating-contact b{font-size:22px}}
.article-jump-buttons{max-width:var(--max);margin:0 auto;padding:22px 24px 0;display:flex;gap:9px;flex-wrap:wrap}.article-jump-buttons a{background:#fff;border:1px solid #d6ddd6;border-radius:999px;padding:9px 14px;color:var(--brand);font-size:12px;font-weight:800;box-shadow:0 4px 12px #123b4a08}.article-jump-buttons a:hover{background:var(--accent-soft);border-color:var(--accent)}.guide-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}.guide-grid>div{padding:23px;background:rgba(255,255,255,.68);border-radius:18px}.guide-grid span,.process-grid span{color:var(--accent);font-size:22px;font-weight:900}.guide-grid h3{margin:6px 0}.about-extra,.services-extra,.contact-extra{padding-top:28px}.quick-links{display:flex;gap:6px;flex-wrap:wrap}.faq-long{max-width:900px}.faq-long details{background:rgba(255,255,255,.7);border:1px solid #dce1da;border-radius:16px;padding:20px 22px;margin:14px 0}.faq-long summary{cursor:pointer;color:var(--brand);font-weight:900;font-size:17px}.process-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.process-grid>div{padding:28px;background:rgba(255,255,255,.72);border-radius:22px;min-height:220px}.process-grid h2{font-size:25px;margin:7px 0}.process-grid a,.faq-next a{color:var(--brand);font-weight:900}.process-note{padding-top:22px}@media(max-width:700px){.guide-grid,.process-grid{grid-template-columns:1fr}.article-jump-buttons{padding-left:5%;padding-right:5%}}
'''
css.write_text(s,encoding='utf-8')
print('navigation/pages/floating update complete')
