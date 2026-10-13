from pathlib import Path
import re

ROOT=Path(__file__).parent
services=ROOT/'services.html'; articles=ROOT/'articles.html'
s=services.read_text(encoding='utf-8'); a=articles.read_text(encoding='utf-8')

def main_of(t):
    return t[t.index('<main>'):t.index('</main>')+7]
def replace_main(t, main):
    return t[:t.index('<main>')] + main + t[t.index('</main>')+7:]

old_services_main=main_of(s)
old_articles_main=main_of(a)
# Swap the page bodies: services.html becomes the long articles page, articles.html becomes the services page.
s=replace_main(s, old_articles_main)
a=replace_main(a, old_services_main)

# Swap every internal destination so the renamed pages remain semantically connected.
for p in ROOT.glob('*.html'):
    t=p.read_text(encoding='utf-8')
    t=t.replace('___ARTICLES___','articles.html').replace('___SERVICES___','services.html')
    t=t.replace('articles.html','___ARTICLES___').replace('services.html','___SERVICES___')
    t=t.replace('___ARTICLES___','services.html').replace('___SERVICES___','articles.html')
    p.write_text(t,encoding='utf-8')
# Reload swapped files after the global link swap.
s=services.read_text(encoding='utf-8'); a=articles.read_text(encoding='utf-8')

# Update visible names, active states, and page metadata.
def rename_meta(t, old_title, new_title, old_desc, new_desc):
    t=t.replace(old_title,new_title).replace(old_desc,new_desc)
    t=t.replace('<a class="active" href="services.html">خدماتنا</a>','<a class="" href="services.html">مقالات</a>')
    t=t.replace('<a class="active" href="articles.html">المقالات</a>','<a class="active" href="articles.html">خدماتنا</a>')
    t=t.replace('<a class="" href="services.html">خدماتنا</a>','<a class="active" href="services.html">مقالات</a>')
    t=t.replace('<a class="" href="articles.html">المقالات</a>','<a class="active" href="articles.html">خدماتنا</a>')
    return t
s=rename_meta(s,'مقالات ونصائح الخدمات المنزلية | شركة الخيال','مقالات ونصائح طويلة | شركة الخيال','مقالات شركة الخيال عن نقل الأثاث والصيانة المنزلية والتكييف وصيانة أفران الغاز والتنظيف','مقالات وأدلة شركة الخيال الطويلة عن نقل الأثاث والصيانة والتكييف وأفران الغاز والتنظيف.')
a=rename_meta(a,'خدمات شركة الخيال | نقل وصيانة ونظافة','خدماتنا | شركة الخيال للخدمات المنزلية','استكشف خدمات شركة الخيال في نقل الأثاث والصيانة المنزلية والتكييف والنظافة، مع تفاصيل عملية وروابط مباشرة للتواصل.','استكشف خدمات شركة الخيال في نقل الأثاث والصيانة والتكييف وأفران الغاز والنظافة مع روابط مباشرة للتواصل.')
# Swap the hero labels that came from the original page bodies.
s=s.replace('خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك','مركز المقالات</p><h1>مقالات وأدلة تساعدك في منزلك')
a=a.replace('مركز المعرفة</p><h1>مقالات ونصائح للخدمات المنزلية','خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك')
# The old services page is now the article page; make its bottom call-to-action article-focused.
s=s.replace('هل لديك سؤال مختلف؟','هل تريد اختيار الخدمة المناسبة؟').replace('أرسل تفاصيل احتياجك وسنساعدك على تحديد الخطوة التالية.','اقرأ المقال المرتبط أولًا، ثم انتقل إلى صفحة الخدمة أو التواصل عند جاهزيتك.')
# The old article page is now services; add a very long service guide before its closing contact section.
if 'service-deep-dive' not in a:
    deep='''<section class="section service-deep-dive"><p class="eyebrow">دليل الخدمات بالتفصيل</p><h2>اختر الخدمة حسب احتياج منزلك</h2><div class="deep-service"><h3>نقل الأثاث والعفش</h3><p>ابدأ بجرد الغرف والقطع الكبيرة، ودوّن المداخل والسلالم والمصعد والمسافة بين الموقعين. تغليف القطع الحساسة، كتابة محتوى الصناديق، وترتيب الصناديق الأساسية يجعل يوم النقل أكثر هدوءًا.</p><p>بعد تحديد التفاصيل، راجع <a href="moving.html">صفحة نقل الأثاث</a> ثم اقرأ <a href="services.html#moving">مقال الاستعداد للنقل</a> وانتقل إلى <a href="contact.html">التواصل</a>.</p></div><div class="deep-service"><h3>الصيانة المنزلية</h3><p>صف العلامات ومتى بدأت، ولا تلمس التوصيلات عند وجود شرر أو رائحة احتراق أو تسرب قرب الكهرباء. جهّز رقم الجهاز أو صورة من مسافة آمنة، واترك مساحة مناسبة للفحص.</p><p>راجع <a href="maintenance.html">صفحة الصيانة</a> و<a href="services.html#maintenance">مقال متى تستدعي فنيًا</a> لمعرفة الخطوة الأكثر أمانًا.</p></div><div class="deep-service"><h3>صيانة التكييف وأفران الغاز</h3><p>نظافة الفلاتر ومراقبة التسربات والأصوات تساعد في اكتشاف مشاكل التكييف مبكرًا. أما رائحة الغاز أو اللهب غير المنتظم فتحتاج إلى إغلاق المصدر إن كان ذلك آمنًا وطلب فني مختص دون تفكيك التوصيلات.</p><p>اقرأ <a href="air-conditioning.html">صيانة التكييف</a> و<a href="gas-ovens.html">صيانة أفران الغاز</a>، ثم أرسل التفاصيل من <a href="contact.html">صفحة التواصل</a>.</p></div><div class="deep-service"><h3>خدمات النظافة</h3><p>قسّم المساحة إلى مناطق، ابدأ من الأعلى إلى الأسفل، واستخدم أدوات منفصلة للمطبخ والحمام. لا تخلط المنظفات واحفظها بعيدًا عن الأطفال. يمكن بناء جدول أسبوعي أو طلب مساعدة لمساحة كبيرة.</p><p>تعرّف على <a href="cleaning.html">خدمات النظافة</a> ثم راجع <a href="services.html#cleaning">مقال خطة التنظيف الأسبوعية</a>.</p></div><div class="deep-service"><h3>ثلاث خطوات قبل أي طلب</h3><ol><li>حدد الخدمة والمكان والموعد التقريبي.</li><li>اكتب وصفًا مختصرًا وأرفق ملاحظة أو صورة إن كانت مناسبة.</li><li>راجع <a href="faq.html">الأسئلة الشائعة</a> و<a href="process.html">كيف نعمل</a> ثم تواصل معنا.</li></ol></div></section>'''
    a=a.replace('<section class="contact">',deep+'<section class="contact">',1)
# Apply a page class to make the renamed articles page border-free.
s=s.replace('<body class="site-shell content-art">','<body class="site-shell content-art articles-renamed">')
a=a.replace('<body class="site-shell">','<body class="site-shell services-renamed">',1)
services.write_text(s,encoding='utf-8'); articles.write_text(a,encoding='utf-8')

# Restore the original neutral dotted site background while retaining floating background images.
css=ROOT/'style.css'; c=css.read_text(encoding='utf-8')
c += '''\n\n/* Restore the original neutral dotted canvas; keep the floating background images. */
body.site-shell{background:#f7f7f5;background-image:radial-gradient(#182c4b0c .8px,transparent .8px);background-size:18px 18px}
body.site-shell:before,body.site-shell:after{display:none}
.articles-renamed .section,.articles-renamed .long-article,.articles-renamed .article-related,.articles-renamed .article-next{border:0!important;box-shadow:none}
.articles-renamed .article-list,.articles-renamed .article-next{background:transparent}
.services-renamed .section,.services-renamed .cards article,.services-renamed .faq details{border:0;box-shadow:none}
.service-deep-dive{max-width:920px}.deep-service{padding:28px 0;border-bottom:1px solid #dce2dc}.deep-service:last-child{border-bottom:0}.deep-service h3{font-size:25px;color:var(--brand);margin:0 0 8px}.deep-service p{max-width:800px}.deep-service li{margin:8px 0;color:var(--muted)}
'''
css.write_text(c,encoding='utf-8')

# Update route titles for the swapped labels.
routes=ROOT/'manus-routes.json'; r=routes.read_text(encoding='utf-8').replace('"/services.html","title":"الخدمات"','"/services.html","title":"المقالات"').replace('"/articles.html","title":"المقالات"','"/articles.html","title":"خدماتنا"'); routes.write_text(r,encoding='utf-8')
sitemap=ROOT/'sitemap.xml'; st=sitemap.read_text(encoding='utf-8'); sitemap.write_text(st,encoding='utf-8')
print('swapped page identities, expanded services content, restored original background')
