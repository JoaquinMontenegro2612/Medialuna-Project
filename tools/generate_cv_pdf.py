#!/usr/bin/env python3
"""Genera la versión PDF (una columna, ATS-safe) del CV maestro."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

ACCENT = colors.HexColor("#1F4E45")
GREY = colors.HexColor("#5A6570")
DARK = colors.HexColor("#191C1F")
RULE = colors.HexColor("#C9D6D3")

OUT = "cv/CV-Joaquin-Montenegro-Remoto.pdf"
W, H = A4
LM = RM = 16 * mm
TOP = 11 * mm
BOT = 10 * mm
CW = W - LM - RM

base = dict(fontName="Helvetica", fontSize=8.4, leading=10.8, textColor=DARK)

s_name = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=19, leading=21,
                        textColor=ACCENT, spaceAfter=1)
s_role = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=9.2, leading=11.6,
                        textColor=DARK, spaceAfter=3)
s_contact = ParagraphStyle("contact", fontName="Helvetica", fontSize=7.6, leading=9.9,
                           textColor=GREY)
s_head = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8.6, leading=10,
                        textColor=ACCENT, spaceBefore=0, spaceAfter=0)
s_body = ParagraphStyle("body", fontSize=8.3, leading=10.7, textColor=DARK, alignment=TA_JUSTIFY)
s_job = ParagraphStyle("job", fontName="Helvetica-Bold", fontSize=8.8, leading=11.0,
                       textColor=DARK, spaceBefore=0, spaceAfter=0)
s_sub = ParagraphStyle("sub", fontName="Helvetica-Oblique", fontSize=7.5, leading=9.3,
                       textColor=GREY, spaceAfter=1)
s_bul = ParagraphStyle("bul", fontSize=8.3, leading=10.5, textColor=DARK,
                       leftIndent=9, bulletIndent=1.5, spaceBefore=0, spaceAfter=0.8)
s_skill = ParagraphStyle("skill", fontSize=8.3, leading=10.5, textColor=DARK, leftIndent=9,
                         bulletIndent=1.5, spaceAfter=0.9)


def section(title):
    t = Table([[Paragraph(title.upper(), s_head)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.8, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [Spacer(1, 7.5), t, Spacer(1, 3)]


def job(title, company, dates, sub=None):
    left = Paragraph(f'{title} &nbsp;<font color="#1F4E45">|</font>&nbsp; '
                     f'<font color="#1F4E45">{company}</font>', s_job)
    right = Paragraph(f'<font size="7.6" color="#5A6570">{dates}</font>',
                      ParagraphStyle("d", fontName="Helvetica", fontSize=7.6,
                                     leading=9.5, alignment=2))
    t = Table([[left, right]], colWidths=[CW - 34 * mm, 34 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    out = [t]
    if sub:
        out.append(Paragraph(sub, s_sub))
    return out


def bullets(items):
    return [Paragraph(t, s_bul, bulletText="•") for t in items]


story = []
story.append(Paragraph("JOAQUÍN MONTENEGRO", s_name))
story.append(Paragraph("Consultor Power Platform &amp; Dynamics 365 · Desarrollo Web (React) · QA", s_role))
story.append(Paragraph("Valencia, España (100 % remoto o híbrido) &nbsp;·&nbsp; +34 601 580 269 "
                       "&nbsp;·&nbsp; joaquinmontenegro2612@gmail.com", s_contact))
story.append(Paragraph("linkedin.com/in/joaquin-montenegro &nbsp;·&nbsp; github.com/tu-usuario "
                       "&nbsp;·&nbsp; Disponibilidad inmediata &nbsp;·&nbsp; Permiso B", s_contact))

story += section("Perfil profesional")
story.append(Paragraph(
    "Desarrollador y consultor con más de dos años de experiencia técnica en consultoría y producto, con año y medio "
    "centrado en Microsoft Power Platform y Dynamics 365, y base de frontend (React/JavaScript) y QA. Perfil híbrido capaz de hablar con el negocio y "
    "de ejecutar la parte técnica: traduzco procesos reales (presupuestos, compras, stock, atención al cliente) "
    "en soluciones que la gente usa de verdad. Aporto además experiencia de gestión de negocio propio, lo que "
    "me permite entender el coste y el impacto de cada automatización antes de construirla.", s_body))

story += section("Experiencia profesional")

story += job("Desarrollador Dynamics 365 / Power Platform", "Tigloo", "ene. 2024 – dic. 2024",
             "Consultoría tecnológica · Desarrollo e implantación de soluciones de negocio")
story += bullets([
    "Personalicé entidades, formularios, flujos de trabajo y procesos de negocio en Dynamics 365 para adaptar el CRM a los procesos reales de cada cliente.",
    "Automaticé procesos internos con Power Automate y construí apps de negocio con Power Apps, eliminando tareas manuales en los equipos de ventas y operaciones.",
    "Desarrollé integraciones entre Dynamics 365 y otros sistemas empresariales mediante Power Automate y Azure Integration Services.",
])

story += job("Desarrollador React JS / QA Engineer", "Create Ape", "jun. 2022 – abr. 2023",
             "Producto digital · Doble rol: desarrollo frontend y aseguramiento de calidad")
story += bullets([
    "Desarrollé el frontend de aplicaciones con React, JavaScript, Vite, Chakra UI y Material UI, con Firebase como backend.",
    "Como QA Engineer ejecuté pruebas funcionales, de backend y móviles (iOS/Android), diseñando y ejecutando casos de prueba en Jira y TestLodge.",
    "Gestioné despliegues y configuración de entornos con Azure DevOps, Bitbucket y Git.",
])

story += job("Desarrollador Dynamics CRM", "Softtek", "dic. 2020 – jun. 2021",
             "Consultoría TI · Desarrollo y personalización de CRM")
story += bullets([
    "Desarrollé plugins en .NET Framework (C#) con el SDK de Dynamics CRM y personalicé formularios con JavaScript sobre Dynamics CRM 2016/365 on-premise.",
    "Trabajé con Visual Studio, XRM ToolBox, GitHub y Azure DevOps bajo metodología ágil Scrum.",
])

story += job("Socio y encargado", "Cafetería Medialuna", "oct. 2024 – dic. 2025",
             "Negocio propio · Compaginado con mi última etapa como desarrollador")
story += bullets([
    "Fundé y gestioné el local: operación diaria, atención al cliente, caja y administración, compras y relación con proveedores, control de stock y supervisión de personal.",
    "Aprendizaje directo de gestión de costes y márgenes, trato con clientes difíciles y toma de decisiones con dinero propio en juego.",
])

story += job("Reformista (escape rooms)", "Experiencity SL", "ene. 2026 – oct. 2026",
             "Construcción y reformas · Plazos cerrados ligados a la apertura de cada sala")
story += bullets([
    "Ejecuté trabajos de albañilería, pladur, yeso, pintura, alicatado y reparaciones generales, con responsabilidad sobre acabados y cumplimiento de plazos.",
    "Coordiné materiales, pedidos y orden de la obra, interpretando indicaciones y resolviendo imprevistos en obra.",
])

story += section("Aptitudes técnicas")
skills = [
    ("Microsoft Power Platform:", "Power Apps, Power Automate, entornos de Power Platform, integraciones con Azure Integration Services."),
    ("Dynamics 365 / CRM:", "personalización de entidades y formularios, flujos de trabajo, procesos de negocio, plugins .NET/C#, JavaScript, SDK de CRM."),
    ("Desarrollo web:", "React.js, JavaScript, Vite, Chakra UI, Material UI, Firebase, HTML5, CSS3."),
    ("QA y pruebas:", "pruebas funcionales, de backend y móviles (iOS/Android), diseño y ejecución de casos de prueba, depuración, Jira, TestLodge."),
    ("Herramientas y metodologías:", "Git, GitHub, Bitbucket, Azure DevOps, Visual Studio, XRM ToolBox, Scrum."),
    ("Negocio y cliente:", "atención al cliente, gestión de equipos, compras y proveedores, control de stock, presupuestos, coordinación de obra."),
]
for k, v in skills:
    story.append(Paragraph(f"<b>{k}</b> {v}", s_skill, bulletText="•"))

_proj = bullets([
    "<b>PresupuestoPro</b> — aplicación de negocio que permite crear un presupuesto desde el móvil, generar el PDF con logo e IVA y enviarlo al cliente automáticamente, con seguimiento. Power Apps + Power Automate (demo y vídeo disponibles).",
])
story.append(KeepTogether(section("Proyectos") + _proj))

story.append(KeepTogether(section("Formación") +
    job("Máster en Desarrollo Web", "AIP Barcelona", "2021 – 2022") +
    job("Desarrollo Web y Programación", "Coderhouse", "completado") +
    job("Bachillerato en Ciencias Sociales", "Buenos Aires, Argentina", "2018")))

story += section("Idiomas y otros datos")
story.append(Paragraph("<b>Idiomas:</b> español nativo · inglés intermedio B1-B2 (trabajo y documentación técnica). &nbsp;&nbsp;"
                       "<b>Otros:</b> permiso B y vehículo propio · certificado de manipulación de alimentos · "
                       "disponibilidad inmediata, turnos y fines de semana · acostumbrado a trabajo remoto.", s_body))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GREY)
    canvas.drawRightString(W - RM, 8 * mm, f"Joaquín Montenegro · página {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TOP, bottomMargin=BOT, title="CV Joaquín Montenegro",
                      author="Joaquín Montenegro")
frame = Frame(LM, BOT, CW, H - TOP - BOT, id="f", leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
doc.build(story)
print("ok", OUT)
