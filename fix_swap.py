from pathlib import Path
import re
ROOT=Path(__file__).parent
sp=ROOT/'services.html'; ap=ROOT/'articles.html'
s=sp.read_text(encoding='utf-8'); a=ap.read_text(encoding='utf-8')
def getmain(t): return t[t.index('<main>'):t.index('</main>')+7]
def setmain(t,m): return t[:t.index('<main>')]+m+t[t.index('</main>')+7:]
sm,am=getmain(s),getmain(a)
# Current services page becomes the long articles page; current articles page becomes services.
s=setmain(s,am); a=setmain(a,sm)
# Keep the long service guide on the services-named page (articles.html).
if 'service-deep-dive' not in a:
    deep='''<section class="section service-deep-dive"><p class="eyebrow">دليل الخدمات بالتفصيل</p><h2>اختر الخدمة حسب احتياج منزلك</h2><div class="deep-service"><h3>نقل الأثاث والعفش</h3><p>ابدأ بجرد الغرف والقطع الكبيرة، ودوّن المداخل والسلالم والمصعد والمسافة بين الموقعين. تغليف القطع الحساسة وكتابة محتوى الصناديق يجعل يوم النقل أكثر هدوءًا.</p><p>راجع <a href="moving.html">صفحة نقل الأثاث</a> ثم اقرأ <a href="services.html#moving">مقال الاستعداد للنقل</a> وانتقل إلى <a href="contact.html">التواصل</a>.</p></div><div class="deep-service"><h3>الصيانة المنزلية</h3><p>صف العلامات ومتى بدأت، ولا تلمس التوصيلات عند وجود شرر أو رائحة احتراق أو تسرب قرب الكهرباء. جهّز رقم الجهاز أو صورة من مسافة آمنة واترك مساحة للفحص.</p><p>راجع <a href="maintenance.html">صفحة الصيانة</a> و<a href="services.html#maintenance">مقال متى تستدعي فنيًا</a>.</p></div><div class="deep-service"><h3>صيانة التكييف وأفران الغاز</h3><p>راقب الفلاتر والتسربات والأصوات في التكييف. عند رائحة الغاز أو اللهب غير المنتظم أغلق المصدر إن كان ذلك آمنًا واطلب فنيًا دون تفكيك التوصيلات.</p><p>اقرأ <a href="air-conditioning.html">صيانة التكييف</a> و<a href="gas-ovens.html">صيانة أفران الغاز</a>، ثم أرسل التفاصيل من <a href="contact.html">صفحة التواصل</a>.</p></div><div class="deep-service"><h3>خدمات النظافة</h3><p>قسّم المساحة إلى مناطق، ابدأ من الأعلى إلى الأسفل، واستخدم أدوات منفصلة للمطبخ والحمام. لا تخلط المنظفات واحفظها بعيدًا عن الأطفال.</p><p>تعرّف على <a href="cleaning.html">خدمات النظافة</a> ثم راجع <a href="services.html#cleaning">مقال خطة التنظيف الأسبوعية</a>.</p></div><div class="deep-service"><h3>ثلاث خطوات قبل أي طلب</h3><ol><li>حدد الخدمة والمكان والموعد التقريبي.</li><li>اكتب وصفًا مختصرًا وأرفق ملاحظة مناسبة.</li><li>راجع <a href="faq.html">الأسئلة الشائعة</a> و<a href="process.html">كيف نعمل</a> ثم تواصل معنا.</li></ol></div></section>'''
    a=a.replace('<section class="contact">',deep+'<section class="contact">',1)
# Set body classes for the renamed page styles.
s=re.sub(r'<body class="[^"]*"', '<body class="site-shell content-art articles-renamed"', s, count=1)
a=re.sub(r'<body class="[^"]*"', '<body class="site-shell services-renamed"', a, count=1)
# Normalize navigation labels by destination across the whole site.
for p in ROOT.glob('*.html'):
    t=p.read_text(encoding='utf-8')
    t=re.sub(r'(<a class="[^"]*" href="services\.html">)[^<]*(</a>)',r'\1مقالات\2',t)
    t=re.sub(r'(<a class="[^"]*" href="articles\.html">)[^<]*(</a>)',r'\1خدماتنا\2',t)
    t=re.sub(r'(<a href="services\.html">)[^<]*(</a>)',r'\1مقالات\2',t)
    t=re.sub(r'(<a href="articles\.html">)[^<]*(</a>)',r'\1خدماتنا\2',t)
    p.write_text(t,encoding='utf-8')
# Titles/descriptions and hero text for the two swapped pages.
s=sp.read_text(encoding='utf-8'); a=ap.read_text(encoding='utf-8')
s=s.replace('خدمات شركة الخيال | نقل وصيانة ونظافة','مقالات ونصائح طويلة | شركة الخيال').replace('استكشف خدمات شركة الخيال في نقل الأثاث والصيانة المنزلية والتكييف والنظافة، مع تفاصيل عملية وروابط مباشرة للتواصل.','مقالات وأدلة شركة الخيال الطويلة عن نقل الأثاث والصيانة والتكييف وأفران الغاز والتنظيف.')
s=s.replace('خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك','مركز المقالات</p><h1>مقالات وأدلة تساعدك في منزلك')
a=a.replace('مقالات ونصائح الخدمات المنزلية | شركة الخيال','خدماتنا | شركة الخيال للخدمات المنزلية').replace('مقالات شركة الخيال عن نقل الأثاث والصيانة المنزلية والتكييف وصيانة أفران الغاز والتنظيف، مع نصائح عملية قبل طلب الخدمة.','استكشف خدمات شركة الخيال في نقل الأثاث والصيانة والتكييف وأفران الغاز والنظافة مع روابط مباشرة للتواصل.')
a=a.replace('مركز المعرفة</p><h1>مقالات ونصائح للخدمات المنزلية','خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك')
sp.write_text(s,encoding='utf-8'); ap.write_text(a,encoding='utf-8')
# Route titles.
r=ROOT/'manus-routes.json'; t=r.read_text(encoding='utf-8'); t=t.replace('"/services.html","title":"الخدمات"','"/services.html","title":"المقالات"').replace('"/articles.html","title":"المقالات"','"/articles.html","title":"خدماتنا"'); r.write_text(t,encoding='utf-8')
print('fixed page swap')
