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
    legal_links = (('aviso-legal', 'Aviso legal'), ('politica-de-privacidad', 'Política de privacidad'), ('politica-de-cookies', 'Política de cookies'))
    legal_nav = ''.join(f'<a href="{link(slug)}">{label}</a>' for slug, label in legal_links)
    banner = f'{prefix}assets/kit-digital.png'
    funding = 'Programa Kit Digital financiado por la Unión Europea – NextGenerationEU. Gobierno de España, Red.es, Plan de Recuperación, Transformación y Resiliencia y Kit Digital.'
    # On narrow screens use regions of the same supplied artwork, preserving its proportions.
    regions = [(395, 0, 390, 26), (0, 46, 252, 66), (265, 46, 348, 66), (630, 46, 151, 66), (785, 46, 181, 66), (968, 46, 212, 66)]
    stacked = ''.join(f'<svg viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" aria-hidden="true"><image href="{banner}" width="1180" height="112"/></svg>' for x,y,w,h in regions)
    body_class = 'home' if not route else 'inside'
    if route.startswith('productos/'):
        body_class += ' product-page'
    css = (ROOT/'style.css').read_text(encoding='utf-8').replace("url('assets/", f"url('{prefix}assets/")
    egg = (ROOT/'assets/coccion.svg').read_text(encoding='utf-8')
    brand = f'<a class="brand-link" href="{prefix}" aria-label="El Palomar, inicio"><img src="{prefix}assets/el-palomar.svg" width="1272" height="759" alt="El Palomar"></a>'
    menu_egg = egg.replace('egg-', 'menu-egg-')
    document = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f5ed">
<noscript><style>.scroll-scene{{height:auto}}.sticky{{position:relative}}.sticky>.intro,.pause{{display:none}}.home .top{{position:sticky;left:auto;transform:none;visibility:visible}}.scrolled .center{{visibility:visible}}</style></noscript><title>{title} · El Palomar</title><meta name="description" content="{escape(description)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><style>{css}</style><script defer src="{prefix}app.js?v=cabecera"></script></head>
<body class="{body_class}"><a class="skip" href="#principal">Saltar al contenido</a><header class="top">{brand}<nav aria-label="Principal">{navigation}</nav></header>
<button class="burger" type="button" popovertarget="mobile-menu" aria-label="Menú principal" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
<div class="mobile-sheet" id="mobile-menu" popover="auto"><div class="sheet-head"><button type="button" class="sheet-close" autofocus aria-label="Cerrar menú" popovertarget="mobile-menu" popovertargetaction="hide">×</button></div><div class="menu-body">{brand}<nav aria-label="Menú móvil">{navigation}</nav><div class="menu-film">{menu_egg}</div></div></div>
<main id="principal">{content.replace('@/',prefix)}</main>
<footer><div class="footer-main"><div><a class="word" href="{prefix}">El Palomar</a><p>Huevos camperos de Martín Miguel, Segovia.</p></div><nav aria-label="Pie de página">{navigation}</nav></div>
<nav class="legal-links" aria-label="Información legal">{legal_nav}</nav>
<div class="funding"><img width="1180" height="112" loading="lazy" src="{banner}" alt="{funding}"><div class="funding-mobile" role="img" aria-label="{funding}">{stacked}</div></div></footer></body></html>'''
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

def product_walkthrough(heading):
    subheading = "h2" if heading == "h1" else "h3"
    dimensions = {'s': (447, 610), 'm': (445, 610), 'l': (446, 610), 'xl': (446, 610)}
    chapters = []
    links = []
    for index, (size, weight, kind) in enumerate(SIZES):
        slug = size.lower()
        links.append(f'<a href="#calibre-{slug}" aria-label="Ir al calibre {size}">{size}</a>')
        chapters.append(f'''<article class="calibre-chapter" id="calibre-{slug}" style="--proportion:{.76 + .08 * index:.2f}">
          <div class="calibre-frame"><div class="calibre-layout">
            <div class="shell-space"><div class="shell-model"><img loading="lazy" src="@/assets/cascaron-{slug}.avif" data-turn="@/assets/cascaron-{slug}-giro.webp" width="{dimensions[slug][0]}" height="{dimensions[slug][1]}" alt="Huevo campero de calibre {size}"></div></div>
            <div class="calibre-copy"><p class="kicker">Huevo campero · {kind}</p><{subheading} class="calibre-title">Calibre <em>{size}.</em></{subheading}>
            <p class="calibre-weight">{weight.capitalize()} por huevo</p><p>En caja de docena o en estuche de 6 + 6.</p>
            <a class="button" href="@/productos/{slug}/">+ información talla {size} <span aria-hidden="true">↗</span></a></div>
          </div></div></article>''')
    return f'''<section class="walkthrough"><div class="walk-heading"><{heading}>Cuatro <em>calibres.</em></{heading}>
      <nav aria-label="Elegir calibre">{''.join(links)}</nav></div><div class="calibre-run"><div class="pasture" aria-hidden="true"><div class="pasture-next"></div></div>{''.join(chapters)}</div></section>'''

def story_section(full=False):
    heading = 'h1' if full else 'h2'
    portrait = '''<div class="portrait"><img width="370" height="744" loading="lazy" src="@/assets/cobriza.avif" data-motion="@/assets/cobriza-viva.webp" alt="Gallina de plumaje cobrizo de El Palomar"><button type="button" class="motion-control" aria-label="Pausar la gallina">Ⅱ</button></div>'''
    opening = '<p>El Palomar nació en Martín Miguel, un pueblo de Segovia, con la idea de recuperar una forma tradicional de producir huevos camperos y ofrecer un alimento de cercanía.</p>'
    care = '<p>En la granja nos ocupamos de todo el ciclo de cría. Eso nos permite cuidar a las gallinas en cada etapa, desde lo que comen hasta el espacio en el que viven.</p>'
    if full:
        narrative = opening + care + '<p>La última parte de nuestro trabajo se ve al abrir una huevera. Clasificamos los huevos por peso, desde la talla S hasta la XL, y los preparamos en cajas de una docena o en estuches de dos medias docenas.</p>'
        link = '<a class="button" href="@/productos/">Ver los huevos <span aria-hidden="true">↗</span></a>'
    else:
        narrative = opening + care
        link = '<a class="button" href="@/historia/">Leer nuestra historia <span aria-hidden="true">↗</span></a>'
    return f'''<section class="story" aria-labelledby="origen-titulo">{portrait}<div class="story-copy"><p class="kicker">Nuestra historia</p><{heading} id="origen-titulo">Todo empieza en <em>Martín Miguel.</em></{heading}>{narrative}{link}</div></section>'''

formats='''<section class="formats"><h2>Dos formas de llevarlos.</h2><div><h3>Caja de docena</h3><p>Doce huevos en una huevera.</p></div><div><h3>Formato 6 + 6</h3><p>Dos medias docenas en un estuche dividido.</p></div><p class="note">Trabajamos con todos los calibres. El envasado se ajusta al peso mínimo indicado en el estuche para la docena o la media docena.</p></section>'''
intro='''<section class="intro" id="proyecto"><p class="kicker">El proyecto</p><h2>Del campo <em>a la mesa.</em></h2><p>En El Palomar criamos gallinas camperas en Martín Miguel, Segovia. Cuidamos su alimentación y su entorno a lo largo de todo el ciclo de cría.</p></section>'''
hero='''<div class="scroll-scene"><section class="sticky"><div class="landscape"><picture><source media="(max-aspect-ratio: 3/4)" srcset="@/assets/campo-vertical.avif"><img fetchpriority="high" width="880" height="495" src="@/assets/campo.avif" alt=""></picture><div class="shade"></div></div>
<div class="bird-stage"><img class="pair" width="720" height="716" srcset="@/assets/pareja-compacta.avif 440w, @/assets/pareja.avif 720w" sizes="(max-width: 600px) 88vw, 53vh" src="@/assets/pareja.avif" data-motion="@/assets/pareja-viva.webp" alt="Dos gallinas camperas de El Palomar">INTRO</div>
<div class="hero-copy"><p class="place">Martín Miguel <span> / </span> Segovia</p><h1>Huevos <em>camperos.</em></h1></div>
<button class="pause" type="button" aria-label="Pausar movimiento">Ⅱ</button><a class="down" href="#presentacion" aria-label="Descubrir el proyecto">↓</a></section><span id="presentacion"></span></div>'''
page('', 'Huevos camperos de Martín Miguel', 'Descubre El Palomar, su historia y su catálogo de huevos camperos en cuatro calibres.', hero.replace('INTRO',intro)+product_walkthrough('h2')+story_section())
page('productos','Productos','Catálogo de huevos camperos S, M, L y XL con pesos y formatos de envasado.',product_walkthrough('h1')+formats)
for size, weight, kind in SIZES:
    slug=size.lower()
    page('productos/'+slug,'Huevo campero calibre '+size, f'Huevo campero {kind.lower()}, calibre {size}, de {weight}. Consulta sus formatos.',f'''<article class="detail"><div class="sample"><img width="224" height="280" src="@/assets/cascaron-{slug}.avif" data-turn="@/assets/cascaron-{slug}-giro.webp" alt="Huevo campero calibre {size}"><button type="button" class="turn-control">Girar el huevo</button></div><div><a href="@/productos/">← Todos los productos</a><p class="kicker">Huevo campero · {kind}</p><h1>Calibre <em>{size}.</em></h1><p class="weight">{weight.capitalize()} por huevo</p><p>Disponible en caja de docena y en formato de 6 + 6. Consulta la disponibilidad directamente con la granja.</p><a class="button" href="@/contacto/">Consultar a la granja ↗</a></div></article>'''+formats+'<section class="related"><h2>Otros <em>calibres.</em></h2>'+catalog(size)+'</section>')
page('historia','Nuestra historia','Conoce el origen de El Palomar y su forma de criar gallinas en Martín Miguel, Segovia.',story_section(full=True))
page('contacto','Contacto','Contacta con Granja El Palomar en Martín Miguel para consultar calibres, formatos y disponibilidad.','''<section class="contact"><div><p class="kicker">Contacto</p><h1>Habla con <em>la granja.</em></h1><p>Escríbenos para consultar calibres, formatos o disponibilidad.</p><a class="email" href="mailto:info@granjaelpalomar.es">info@granjaelpalomar.es ↗</a><address>Calle Mingolobo, 23<br>40130 Martín Miguel, Segovia</address></div><img src="@/assets/campo.webp" width="880" height="495" alt="Paisaje de campo"></section>''')

legal_pages = [
    ('aviso-legal', 'Aviso legal', 'Titular del catálogo de El Palomar y condiciones de uso de esta web.', """
<h2>Titular y contacto</h2>
<p>El titular de este catálogo es <strong>Granja El Palomar Sociedad Limitada</strong>, con NIF B40280000 y domicilio en calle Mingolobo, 23, 40130 Martín Miguel (Segovia), España. Para comunicarte con la sociedad, escribe a <a href="mailto:info@granjaelpalomar.es">info@granjaelpalomar.es</a>.</p>
<p>Sociedad inscrita en el Registro Mercantil de Segovia, sección 8.ª, hoja SG-7681. Puedes consultar la <a href="https://www.boe.es/borme/dias/2026/03/13/pdfs/BORME-A-2026-50-40.pdf">inscripción publicada en el BORME</a>, acto 130507.</p>
<h2>Uso del catálogo</h2>
<p>El sitio presenta la granja, las características de los huevos y sus formatos. Las imágenes ilustran el catálogo. Puedes consultar la disponibilidad por correo electrónico. El sitio no tramita pedidos ni pagos.</p>
<h2>Contenidos y derechos</h2>
<p>Los textos, diseños y elementos gráficos están protegidos en la medida prevista por la legislación aplicable. Para reutilizarlos fuera de los usos permitidos por ley, solicita autorización al titular de los derechos. Las marcas y emblemas institucionales pertenecen a sus respectivos titulares.</p>
<h2>Consultas e incidencias</h2>
<p>Si detectas información incorrecta o un problema con la web, puedes comunicarlo al correo indicado. Se aplica la legislación española, sin perjuicio de las normas imperativas de protección de consumidores y de la competencia de los tribunales que correspondan por ley.</p>"""),
    ('politica-de-privacidad', 'Política de privacidad', 'Cómo se tratan los datos al visitar el catálogo o contactar con Granja El Palomar.', """
<h2>Quién trata tus datos</h2>
<p>Granja El Palomar Sociedad Limitada, NIF B40280000, es responsable de la atención de las consultas dirigidas a la granja. Puedes contactar en <a href="mailto:info@granjaelpalomar.es">info@granjaelpalomar.es</a> o en calle Mingolobo, 23, 40130 Martín Miguel (Segovia), España.</p>
<h2>Cuando escribes a la granja</h2>
<p>El enlace de contacto abre tu aplicación de correo. Si envías el mensaje, recibimos tu dirección, el nombre que figure en él y la información que decidas incluir. Usamos esos datos para contestarte y dar seguimiento a tu solicitud. Basta con que facilites una dirección de respuesta y el motivo de la consulta.</p>
<p>Cuando solicitas disponibilidad o condiciones con vistas a comprar, el tratamiento se basa en las medidas precontractuales que pides (art. 6.1.b del RGPD). Para las consultas generales, la base es el interés legítimo de la granja en atender las comunicaciones que recibe (art. 6.1.f).</p>
<h2>Alojamiento y destinatarios</h2>
<p>El catálogo se sirve desde GitHub Pages. Al visitarlo, GitHub registra la dirección IP por motivos de seguridad. La información sobre los plazos y las garantías aplicables a sus transferencias internacionales, incluidas las realizadas a Estados Unidos, está disponible en su <a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">declaración de privacidad</a>. Puedes consultar también la <a href="https://docs.github.com/es/pages/getting-started-with-github-pages/what-is-github-pages#data-collection">documentación sobre las visitas a GitHub Pages</a>.</p>
<p>Para entregar y gestionar los mensajes intervienen los proveedores de correo. Los datos también podrán comunicarse a autoridades cuando exista una obligación legal.</p>
<h2>Conservación</h2>
<p>El criterio de conservación de las consultas es el tiempo necesario para atenderlas y completar su seguimiento. Si de una consulta nace una relación comercial, se aplican también los plazos legales de esa relación. Cuando proceda, los datos se conservarán bloqueados durante los plazos de prescripción de posibles responsabilidades.</p>
<h2>Tus derechos</h2>
<p>Puedes solicitar acceso, rectificación, supresión o limitación del tratamiento. Puedes oponerte al tratamiento basado en interés legítimo y solicitar la portabilidad cuando concurran sus requisitos. Escribe al correo o a la dirección postal del responsable indicando qué derecho quieres ejercer. Si existen dudas razonables sobre tu identidad, podremos pedir la información necesaria para verificarla.</p>
<p>También puedes presentar una reclamación ante la <a href="https://www.aepd.es/">Agencia Española de Protección de Datos</a> o ante la autoridad de control competente.</p>"""),
    ('politica-de-cookies', 'Política de cookies', 'Información sobre cookies, almacenamiento del navegador y recursos utilizados por este catálogo.', """
<h2>Qué se guarda al navegar</h2>
<p>Una cookie es un pequeño dato que un sitio guarda en tu navegador y puede recuperar en visitas posteriores. Este catálogo no instala cookies propias ni incorpora herramientas de analítica, publicidad o seguimiento. Tampoco guarda identificadores en el almacenamiento local o de sesión del navegador.</p>
<h2>Imágenes, vídeos y navegación</h2>
<p>Las imágenes y animaciones se cargan desde el propio sitio. El navegador puede guardar copias temporales de los archivos para que las páginas se abran más rápido. El menú y los controles de animación funcionan en la página abierta.</p>
<p>El alojamiento registra direcciones IP por seguridad. Puedes leer más en la <a href="@/politica-de-privacidad/">política de privacidad</a>.</p>
<h2>Control desde tu navegador</h2>
<p>Puedes revisar y eliminar los datos de este sitio desde los ajustes de privacidad del navegador. Si sigues un enlace a otra web, allí se aplicará la política de ese servicio.</p>""")
]
for route, title, description, body in legal_pages:
    page(route, title, description, f'<article class="legal-page"><h1>{title}</h1>{body}</article>')
