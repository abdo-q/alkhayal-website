from pathlib import Path
import re
ROOT=Path(__file__).parent
sp=ROOT/'services.html'; ap=ROOT/'articles.html'
s=sp.read_text(encoding='utf-8'); a=ap.read_text(encoding='utf-8')
def main(t): return t[t.index('<main>'):t.index('</main>')+7]
def setmain(t,m): return t[:t.index('<main>')]+m+t[t.index('</main>')+7:]
sm,am=main(s),main(a)
# Preserve the expanded service guide currently present in the articles page.
deep=''
if 'service-deep-dive' in am:
    start=am.index('<section class="section service-deep-dive">'); end=am.index('</section>',start)+10
    deep=am[start:end]
# Swap bodies.
new_s=am
new_a=sm
# Remove the service guide from the article body before placing that body on services.html.
if deep: new_s=new_s.replace(deep,'')
# Put the service guide on the services-named page.
if deep and 'service-deep-dive' not in new_a:
    new_a=new_a.replace('<section class="contact">',deep+'<section class="contact">',1)
# Correct hero copy after swap.
new_s=new_s.replace('خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك','مركز المقالات</p><h1>مقالات وأدلة تساعدك في منزلك')
new_a=new_a.replace('مركز المقالات</p><h1>مقالات وأدلة تساعدك في منزلك','خدمات شركة الخيال</p><h1>خدمات منزلية تساعدك على إنجاز يومك')
# Set page body classes.
s=re.sub(r'<body class="[^"]*"','<body class="site-shell content-art articles-renamed"',s,count=1)
a=re.sub(r'<body class="[^"]*"','<body class="site-shell services-renamed"',a,count=1)
s=setmain(s,new_s); a=setmain(a,new_a)
sp.write_text(s,encoding='utf-8'); ap.write_text(a,encoding='utf-8')
# Normalize nav labels only (do not swap destinations again).
for p in ROOT.glob('*.html'):
    t=p.read_text(encoding='utf-8')
    t=re.sub(r'(<a class="[^"]*" href="services\.html">)[^<]*(</a>)',r'\1مقالات\2',t)
    t=re.sub(r'(<a class="[^"]*" href="articles\.html">)[^<]*(</a>)',r'\1خدماتنا\2',t)
    t=re.sub(r'(<a href="services\.html">)[^<]*(</a>)',r'\1مقالات\2',t)
    t=re.sub(r'(<a href="articles\.html">)[^<]*(</a>)',r'\1خدماتنا\2',t)
    p.write_text(t,encoding='utf-8')
# Correct titles in the two heads.
s=sp.read_text(encoding='utf-8'); a=ap.read_text(encoding='utf-8')
s=s.replace('خدمات شركة الخيال | نقل وصيانة ونظافة','مقالات ونصائح طويلة | شركة الخيال').replace('استكشف خدمات شركة الخيال في نقل الأثاث والصيانة المنزلية والتكييف والنظافة، مع تفاصيل عملية وروابط مباشرة للتواصل.','مقالات وأدلة شركة الخيال الطويلة عن نقل الأثاث والصيانة والتكييف وأفران الغاز والتنظيف.')
a=a.replace('مقالات ونصائح الخدمات المنزلية | شركة الخيال','خدماتنا | شركة الخيال للخدمات المنزلية').replace('مقالات شركة الخيال عن نقل الأثاث والصيانة المنزلية والتكييف وصيانة أفران الغاز والتنظيف، مع نصائح عملية قبل طلب الخدمة.','استكشف خدمات شركة الخيال في نقل الأثاث والصيانة والتكييف وأفران الغاز والنظافة مع روابط مباشرة للتواصل.')
sp.write_text(s,encoding='utf-8'); ap.write_text(a,encoding='utf-8')
print('final swap complete')
