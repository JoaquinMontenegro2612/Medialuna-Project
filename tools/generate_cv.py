#!/usr/bin/env python3
"""Genera el CV maestro ATS-safe de Joaquín Montenegro (una columna, sin tablas ni cajas)."""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ACCENT = RGBColor(0x1F, 0x4E, 0x45)
GREY = RGBColor(0x55, 0x5F, 0x66)
DARK = RGBColor(0x1A, 0x1A, 0x1A)

doc = Document()

# --- página y estilos base ---
sec = doc.sections[0]
sec.top_margin = Cm(1.5)
sec.bottom_margin = Cm(1.5)
sec.left_margin = Cm(1.8)
sec.right_margin = Cm(1.8)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)
style.font.color.rgb = DARK
style.paragraph_format.space_after = Pt(3)
style.paragraph_format.space_before = Pt(0)
style.paragraph_format.line_spacing = 1.06
rpr = style.element.get_or_add_rPr()
rf = rpr.find(qn("w:rFonts"))
if rf is None:
    rf = OxmlElement("w:rFonts")
    rpr.append(rf)
rf.set(qn("w:eastAsia"), "Calibri")

RIGHT = Cm(17.4)  # ancho útil ~17,4 cm


def para(space_before=0, space_after=3, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    return p


def run(p, text, size=10, bold=False, italic=False, color=DARK, caps=False, spacing=None):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    r.font.name = "Calibri"
    if caps:
        r.font.all_caps = True
    if spacing:
        rpr = r._element.get_or_add_rPr()
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:val"), str(spacing))
        rpr.append(sp)
    return r


def bottom_border(p, color="1F4E45", size=6):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)


def section_title(text):
    p = para(space_before=11, space_after=5)
    run(p, text, size=10.5, bold=True, color=ACCENT, caps=True, spacing=30)
    bottom_border(p)


def job(title, company, dates, location=None):
    p = para(space_before=7, space_after=0)
    p.paragraph_format.tab_stops.add_tab_stop(RIGHT, WD_TAB_ALIGNMENT.RIGHT)
    run(p, title, size=10.5, bold=True)
    run(p, "  |  ", size=10, color=GREY)
    run(p, company, size=10, color=ACCENT, bold=True)
    run(p, "\t" + dates, size=9, color=GREY)


def sub(text):
    p = para(space_before=0, space_after=2)
    run(p, text, size=9, italic=True, color=GREY)


def bullet(text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    pf = p.paragraph_format
    pf.left_indent = Cm(0.55)
    pf.first_line_indent = Cm(-0.35)
    pf.space_before = Pt(0)
    pf.space_after = Pt(1.5)
    pf.line_spacing = 1.03
    if bold_lead:
        run(p, bold_lead, size=10, bold=True)
    run(p, text, size=10)
    return p


# ---------- CABECERA ----------
p = para(space_after=0)
run(p, "JOAQUÍN MONTENEGRO", size=22, bold=True, color=ACCENT, spacing=20)

p = para(space_before=1, space_after=3)
run(p, "Consultor Power Platform & Dynamics 365 · Desarrollo Web (React) · QA", size=11, bold=True, color=DARK)

p = para(space_after=2)
run(p, "Valencia, España (100 % remoto o híbrido)  ·  +34 601 580 269  ·  joaquinmontenegro2612@gmail.com", size=9, color=GREY)
p = para(space_after=2)
run(p, "linkedin.com/in/joaquin-montenegro  ·  github.com/tu-usuario  ·  Disponibilidad inmediata  ·  Permiso B", size=9, color=GREY)
bottom_border(p, size=4)

# ---------- PERFIL ----------
section_title("Perfil profesional")
p = para()
run(p,
    "Desarrollador y consultor con más de dos años de experiencia técnica en consultoría y producto, con año y medio "
    "centrado en Microsoft Power Platform y Dynamics 365, y base de frontend (React/JavaScript) y QA. Perfil híbrido capaz de hablar con el negocio y "
    "de ejecutar la parte técnica: traduzco procesos reales (presupuestos, compras, stock, atención al cliente) "
    "en soluciones que la gente usa de verdad. Aporto además experiencia de gestión de negocio propio, lo que "
    "me permite entender el coste y el impacto de cada automatización antes de construirla.", size=10)

# ---------- EXPERIENCIA ----------
section_title("Experiencia profesional")

job("Desarrollador Dynamics 365 / Power Platform", "Tigloo", "ene. 2024 – dic. 2024")
sub("Consultoría tecnológica · Desarrollo e implantación de soluciones de negocio")
bullet("Personalicé entidades, formularios, flujos de trabajo y procesos de negocio en Dynamics 365 para adaptar el CRM a los procesos reales de cada cliente.")
bullet("Automaticé procesos internos con Power Automate y construí apps de negocio con Power Apps, eliminando tareas manuales en los equipos de ventas y operaciones.")
bullet("Desarrollé integraciones entre Dynamics 365 y otros sistemas empresariales mediante Power Automate y Azure Integration Services.")
bullet("Traduje requisitos funcionales en soluciones técnicas junto a equipos multidisciplinares, con pruebas unitarias, de integración y documentación del diseño.")

job("Desarrollador React JS / QA Engineer", "Create Ape", "jun. 2022 – abr. 2023")
sub("Producto digital · Doble rol: desarrollo frontend y aseguramiento de calidad")
bullet("Desarrollé el frontend de aplicaciones con React, JavaScript, Vite, Chakra UI y Material UI, con Firebase como backend.")
bullet("Como QA Engineer ejecuté pruebas funcionales, de backend y móviles (iOS/Android), diseñando y ejecutando casos de prueba en Jira y TestLodge.")
bullet("Gestioné despliegues y configuración de entornos con Azure DevOps, Bitbucket y Git.")

job("Desarrollador Dynamics CRM", "Softtek", "dic. 2020 – jun. 2021")
sub("Consultoría TI · Desarrollo y personalización de CRM")
bullet("Desarrollé plugins en .NET Framework (C#) con el SDK de Dynamics CRM y personalicé formularios con JavaScript sobre Dynamics CRM 2016/365 on-premise.")
bullet("Trabajé con Visual Studio, XRM ToolBox, GitHub y Azure DevOps bajo metodología ágil Scrum.")

job("Socio y encargado", "Cafetería Medialuna", "oct. 2024 – dic. 2025")
sub("Negocio propio · Compaginado con mi última etapa como desarrollador")
bullet("Fundé y gestioné el local: operación diaria, atención al cliente, caja y administración, compras y relación con proveedores, control de stock y supervisión de personal.")
bullet("Diseñé cartas y procesos de trabajo, formé al equipo y ejecuté acciones de marketing para captar clientes.")
bullet("Aprendizaje directo de gestión de costes y márgenes, trato con clientes difíciles y toma de decisiones con dinero propio en juego.")

job("Reformista (escape rooms)", "Experiencity SL", "ene. 2026 – oct. 2026")
sub("Construcción y reformas · Plazos cerrados ligados a la apertura de cada sala")
bullet("Ejecuté trabajos de albañilería, pladur, yeso, pintura, alicatado y reparaciones generales, con responsabilidad sobre acabados y cumplimiento de plazos.")
bullet("Coordiné materiales, pedidos y orden de la obra, interpretando indicaciones y resolviendo imprevistos en obra.")

# ---------- APTITUDES ----------
section_title("Aptitudes técnicas")

def skill_line(label, value):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.55)
    pf.first_line_indent = Cm(-0.55)
    pf.space_before = Pt(0)
    pf.space_after = Pt(2)
    run(p, label, size=10, bold=True)
    run(p, value, size=10)

skill_line("Microsoft Power Platform:  ", "Power Apps, Power Automate, Power Platform environments, integraciones con Azure Integration Services.")
skill_line("Dynamics 365 / CRM:  ", "Personalización de entidades y formularios, flujos de trabajo, procesos de negocio, plugins .NET/C#, JavaScript, SDK de CRM.")
skill_line("Desarrollo web:  ", "React.js, JavaScript, Vite, Chakra UI, Material UI, Firebase, HTML5, CSS3.")
skill_line("QA y pruebas:  ", "Pruebas funcionales, de backend y móviles (iOS/Android), diseño y ejecución de casos de prueba, depuración, Jira, TestLodge.")
skill_line("Herramientas y metodologías:  ", "Git, GitHub, Bitbucket, Azure DevOps, Visual Studio, XRM ToolBox, Scrum.")
skill_line("Negocio y cliente:  ", "Atención al cliente, gestión de equipos, compras y proveedores, control de stock, presupuestos, coordinación de obra.")

# ---------- PROYECTOS ----------
section_title("Proyectos")
bullet(" —  Aplicación de negocio que permite crear un presupuesto desde el móvil, generar el PDF con logo e IVA y enviarlo al cliente automáticamente, con seguimiento. Power Apps + Power Automate (demo y vídeo disponibles).", bold_lead="PresupuestoPro")
bullet(" —  Desarrollo frontend con React, JavaScript y Firebase, con pruebas funcionales y de regresión previas a la entrega.", bold_lead="Aplicación web (React)")

# ---------- FORMACIÓN ----------
section_title("Formación")
job("Máster en Desarrollo Web", "AIP Barcelona", "2021 – 2022")
job("Desarrollo Web y Programación", "Coderhouse", "completado")
job("Bachillerato orientado en Ciencias Sociales", "Buenos Aires, Argentina", "2018")

# ---------- IDIOMAS Y OTROS ----------
section_title("Idiomas y otros datos")
p = para(space_after=2)
run(p, "Español: ", size=10, bold=True)
run(p, "nativo  ·  ", size=10)
run(p, "Inglés: ", size=10, bold=True)
run(p, "intermedio B1-B2 (trabajo y documentación técnica).", size=10)
p = para(space_after=2)
run(p, "Otros: ", size=10, bold=True)
run(p, "permiso de conducir B y vehículo propio · certificado de manipulación de alimentos · disponibilidad inmediata, "
       "incluidos turnos y fines de semana · acostumbrado a trabajo remoto y a coordinación por videollamada.", size=10)

doc.save("cv/CV-Joaquin-Montenegro-Remoto.docx")
print("ok")
