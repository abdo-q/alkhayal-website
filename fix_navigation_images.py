from pathlib import Path
import re
ROOT=Path(__file__).parent

# The stable URL mapping is intentional: services.html is the long articles page;
# articles.html is the services page. Only the active state must follow the current file.
for p in ROOT.glob('*.html'):
    t=p.read_text(encoding='utf-8')
    # Clear active only on the two renamed top-level links.
    t=re.sub(r'<a class="active" href="services\.html">', '<a class="" href="services.html">', t)
    t=re.sub(r'<a class="active" href="articles\.html">', '<a class="" href="articles.html">', t)
    if p.name=='services.html':
        t=t.replace('<a class="" href="services.html">مقالات</a>','<a class="active" href="services.html">مقالات</a>',1)
    elif p.name=='articles.html':
        t=t.replace('<a class="" href="articles.html">خدماتنا</a>','<a class="active" href="articles.html">خدماتنا</a>',1)
    p.write_text(t,encoding='utf-8')

css=ROOT/'style.css'; c=css.read_text(encoding='utf-8')
c += '''\n\n/* Final image treatment: preserve the complete image and remove every content/background frame. */
.site-background-art img{border:0!important;box-shadow:none!important;padding:0!important;object-fit:contain!important;background:transparent!important}
.hero-image,.service-image,.split-image,.about-image,.detail-image,.gallery-img,.video-card video{object-fit:contain!important;background:transparent!important;border:0!important}
'''
css.write_text(c,encoding='utf-8')
print('navigation active states and full-image rendering fixed')
