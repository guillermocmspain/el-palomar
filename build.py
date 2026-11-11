"""Generate the static GitHub Pages routes with Python 3."""
from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parent
NAV = [('', 'Inicio'), ('productos', 'Productos'), ('historia', 'Historia'), ('contacto', 'Contacto')]
SIZES = [('S', 'menos de 53 g', 'Pequeño'), ('M', '53 a menos de 63 g', 'Mediano'), ('L', '63 a menos de 73 g', 'Grande'), ('XL', '73 g o más', 'Muy grande')]

def page(route, title, description, content):
    prefix = '../' * len(route.split('/')) if route else './'
    def link(slug):
        return prefix + (slug + '/' if slug else '')
    navigation = ''.join(f'<a href="{link(slug)}"'+(' aria-current="page"' if slug==route else '')+f'>{label}</a>' for slug,label in NAV)
    body_class = 'home' if not route else 'inside'
    css = (ROOT/'style.css').read_text(encoding='utf-8').replace("url('assets/", f"url('{prefix}assets/")
    document = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f5ed">
<noscript><style>.scroll-scene{{height:auto}}.sticky{{position:relative}}.sticky>.intro,.pause{{display:none}}.home .top{{position:sticky;left:auto;transform:none;visibility:visible}}.scrolled .center{{visibility:visible}}</style></noscript><title>{title} · El Palomar</title><meta name="description" content="{escape(description)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><style>{css}</style><script defer src="{prefix}app.js?v=pradera3"></script></head>
<body class="{body_class}"><a class="skip" href="#principal">Saltar al contenido</a><header class="top"><a class="word" href="{prefix}">El Palomar</a><nav aria-label="Principal">{navigation}</nav></header>
<main id="principal">{content.replace('@/',prefix)}</main>
<footer><div><a class="word" href="{prefix}">El Palomar</a><p>Huevos camperos de Martín Miguel, Segovia.</p></div><nav aria-label="Pie de página">{navigation}</nav></footer></body></html>'''
    folder = ROOT / route
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'index.html').write_text(document, encoding='utf-8')

def catalog(exclude=None):
    cards=[]
    for i,(size,weight,kind) in enumerate(SIZES):
        if size == exclude:
            continue
        slug=size.lower()
        cards.append(f'''<a class="egg" href="@/productos/{slug}/"><span class="shelf"><img width="224" height="280" style="--size:{62+12*i}%" loading="lazy" src="@/assets/cascaron-{slug}.avif" data-turn="@/assets/cascaron-{slug}-giro.webp" alt=""></span><span class="eggname">Calibre {size}<span aria-hidden="true">↗</span></span><span>{kind} · {weight}</span></a>''')
    return '<div class="eggs">'+''.join(cards)+'</div>'

story='''<section class="story"><div class="portrait"><img width="375" height="750" loading="lazy" src="@/assets/cobriza.avif" data-motion="@/assets/cobriza-viva.webp" alt="Gallina de plumaje cobrizo de El Palomar"><button type="button" class="motion-control" aria-label="Pausar la gallina">Ⅱ</button></div><div><p class="kicker">Nuestra historia</p><h2>Todo empieza en <em>Martín Miguel.</em></h2><p>En este pueblo de Segovia nace El Palomar. El proyecto recupera una forma cercana de producir huevos, con el cuidado diario de las gallinas en el centro.</p><a class="button" href="@/historia/">Conocer la historia <span>↗</span></a></div></section>'''
formats='''<section class="formats"><h2>Dos formas de llevarlos.</h2><div><h3>Caja de docena</h3><p>Doce huevos en una huevera.</p></div><div><h3>Formato 6 + 6</h3><p>Dos medias docenas en un estuche dividido.</p></div><p class="note">Trabajamos con todos los calibres. El envasado se ajusta al peso mínimo indicado en el estuche para la docena o la media docena.</p></section>'''
intro='''<section class="intro" id="proyecto"><p class="kicker">El proyecto</p><h2>Del campo <em>a la mesa.</em></h2><p>En El Palomar criamos gallinas camperas en Martín Miguel, Segovia. Cuidamos su alimentación y su entorno a lo largo de todo el ciclo de cría.</p></section>'''
hero='''<div class="scroll-scene"><section class="sticky"><div class="landscape"><picture><source media="(max-aspect-ratio: 3/4)" srcset="@/assets/campo-vertical.avif"><img fetchpriority="high" width="880" height="495" src="@/assets/campo.avif" alt=""></picture><div class="shade"></div></div>
<div class="bird-stage"><img class="pair" width="720" height="716" srcset="@/assets/pareja-compacta.avif 440w, @/assets/pareja.avif 720w" sizes="(max-width: 600px) 88vw, 53vh" src="@/assets/pareja.avif" data-motion="@/assets/pareja-viva.webp" alt="Dos gallinas camperas de El Palomar">INTRO</div>
<div class="hero-copy"><p class="place">Martín Miguel <span> / </span> Segovia</p><h1>Huevos <em>camperos.</em></h1></div>
<nav class="center" aria-label="Portada"><a href="@/productos/">Productos</a><a class="brand" href="@/" aria-label="El Palomar, inicio"><img src="@/assets/marca.webp" width="340" height="58" alt="El Palomar"></a><a href="@/historia/">Historia</a></nav>
<button class="pause" type="button" aria-label="Pausar movimiento">Ⅱ</button><a class="down" href="#presentacion" aria-label="Descubrir el proyecto">↓</a></section><span id="presentacion"></span></div>'''
page('', 'Huevos camperos de Martín Miguel', 'Descubre El Palomar, su historia y su catálogo de huevos camperos en cuatro calibres.', hero.replace('INTRO',intro)+'<section class="collection"><p class="kicker">Nuestros productos</p><h2>Cuatro <em>calibres.</em></h2><p>Del más pequeño al más grande. Elige un huevo para ver su peso y sus formatos.</p>'+catalog()+'</section>'+story)
page('productos','Productos','Catálogo de huevos camperos S, M, L y XL con pesos y formatos de envasado.','<section class="collection"><p class="kicker">El catálogo</p><h1>Nuestros <em>huevos.</em></h1><p>Cuatro calibres, ordenados por peso. Elige el tuyo para ver su ficha.</p>'+catalog()+'</section>'+formats)
for size, weight, kind in SIZES:
    slug=size.lower()
    page('productos/'+slug,'Huevo campero calibre '+size, f'Huevo campero {kind.lower()}, calibre {size}, de {weight}. Consulta sus formatos.',f'''<article class="detail"><div class="sample"><img width="224" height="280" src="@/assets/cascaron-{slug}.avif" data-turn="@/assets/cascaron-{slug}-giro.webp" alt="Huevo campero calibre {size}"></div><div><a href="@/productos/">← Todos los productos</a><p class="kicker">Huevo campero · {kind}</p><h1>Calibre <em>{size}.</em></h1><p class="weight">{weight.capitalize()} por huevo</p><p>Disponible en caja de docena y en formato de 6 + 6. Consulta la disponibilidad directamente con la granja.</p><a class="button" href="@/contacto/">Consultar a la granja ↗</a></div></article>'''+formats+'<section class="related"><h2>Otros <em>calibres.</em></h2>'+catalog(size)+'</section>')
page('historia','Nuestra historia','Conoce el origen de El Palomar y su forma de criar gallinas en Martín Miguel, Segovia.',story.replace('<h2>','<h1>').replace('</h2>','</h1>').replace('<a class="button" href="@/historia/">Conocer la historia <span>↗</span></a>','<p>La granja se ocupa de todo el ciclo de cría. Desde la alimentación hasta el espacio en el que viven las aves, cada etapa forma parte del trabajo que hay detrás de una docena.</p><a class="button" href="@/productos/">Ver los huevos ↗</a>'))
page('contacto','Contacto','Contacta con Granja El Palomar en Martín Miguel para consultar calibres, formatos y disponibilidad.','''<section class="contact"><div><p class="kicker">Contacto</p><h1>Habla con <em>la granja.</em></h1><p>Escríbenos para consultar calibres, formatos o disponibilidad.</p><a class="email" href="mailto:info@granjaelpalomar.es">info@granjaelpalomar.es ↗</a><address>Calle Mingolobo, 23<br>40130 Martín Miguel, Segovia</address></div><img src="@/assets/campo.webp" width="880" height="495" alt="Paisaje de campo"></section>''')
