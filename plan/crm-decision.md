# CRM: qué aprender, qué vender y qué no tocar

Decisión tomada el 5/11/2026, a partir de algo que dijiste tú: *"un CRM conectado con Power Platform
para pymes no lo quiero, no lo sé y no lo puedo implementar rápido. Automatizaciones y webs sí.
Power Apps no."*

Eso no es una debilidad. Es un dato de mercado, y hay que usarlo bien.

---

## 1. La respuesta corta

**No aprendas a construir un CRM. Aprende a implantar y editar uno que ya existe.**

Y hay una segunda parte que casi nadie te dice: **los comercios que quieres vender no compran CRM.**
Un bar, una peluquería o una tienda de barrio no tiene un embudo de ventas; tiene clientes que entran,
pagan y se van. Lo que necesita es ficha de cliente, avisos y reservas. Eso no es un CRM: es una hoja
de cálculo bien conectada.

El CRM de verdad lo compran: clínicas, academias, gimnasios, inmobiliarias, distribuidores,
mayoristas, agencias y cualquier negocio que persiga presupuestos durante semanas. **Ese es tu cliente
de CRM, no el bar de la esquina.**

---

## 2. Por qué construir uno es una mala idea (en números)

Construir un CRM end-to-end es un proyecto de 6 a 12 meses para llegar a algo **peor que lo que ya es
gratis**:

| Lo que harías tú | Lo que ya existe gratis |
|---|---|
| 4-6 meses para contactos, negocios y pipeline | HubSpot CRM, gratis, en 20 minutos |
| 2 meses para facturación y presupuestos | Odoo / Zoho, ya hecho |
| 3 meses para email, plantillas y seguimiento | incluido en cualquiera |
| Soporte eterno de un producto propio con 3 clientes | no lo das |

Con 5 clientes a 39 €/mes son 195 €/mes. Has invertido medio año para facturar lo que vale una tarde
de automatizaciones. **Matemática brutal, y por eso no se hace.**

Donde sí está el dinero: **configurar, migrar datos, conectar y formar.** Eso lo cobras a 490-890 €
por cliente y lo haces en 3-5 días con la misma plantilla. Es el trabajo que nadie quiere hacer porque
no es glamuroso, y es exactamente el que las pymes pagan.

---

## 3. Los tres niveles (y quédate donde estás cómodo)

### Nivel 0 · Lo que ya haces y puedes vender mañana
Web + automatización. Formulario que crea el presupuesto, PDF, envío automático, aviso a los 3 días.
**Nada de Power Apps.** Se hace con web + Make/n8n/Power Automate. Es tu producto actual y funciona.

### Nivel 1 · "CRM de bolsillo" — 3 días de aprendizaje, se vende solo
Un CRM existente, configurado para un negocio concreto. No programas nada: ordenas procesos.

- **Herramienta:** HubSpot (plan gratuito) o Zoho Bigin. Las dos tienen versión gratis suficiente
  para una pyme pequeña.
- **Qué aprendes:** pipeline con las etapas reales del negocio, campos propios, formulario web que
  crea el contacto, importación de Excel, plantillas de email, tareas automáticas, panel con 3 métricas.
- **Qué NO aprendes:** desarrollo de plugins, arquitectura, licencias complejas. No hace falta.
- **Precio del servicio:** **490 €** de implantación + **39 €/mes** de mantenimiento. Con web incluida: **890 €**.
- **Tiempo real por cliente:** 8-14 h la primera vez, 4-6 h las siguientes (misma plantilla).

### Nivel 2 · Odoo — 2-3 semanas, y aquí sí hay mercado en España
Odoo es el ERP/CRM que usan miles de pymes españolas, es open source y **se extiende con Python**, que
no te es ajeno (venías de .NET y JavaScript). Un partner de Odoo en Valencia cobra por implantación y
hay demanda constante de gente que sepa configurarlo.

- **Por qué te conviene:** cubre web + CRM + presupuestos + facturación + stock en una sola
  herramienta. Es el pack completo del comercio, que es justo lo que querías vender.
- **Cuándo:** **solo después** de haber vendido 2 servicios del Nivel 1. Si no has vendido un CRM de
  bolsillo, no vas a vender una implantación de Odoo.
- **Cómo:** instancia community en local o en un VPS barato, montas tu propia cafetería como caso
  (clientes, presupuestos, facturas), y documentas. 20-30 h reales.

### Nivel -1 · Lo que NO vas a hacer
Construir un CRM propio. Ni con Lovable, ni con Power Apps, ni con Supabase. Ni "una versión simple
para empezar". Es el clásico pozo de 6 meses que te deja sin ingresos y con un producto que nadie pide.

---

## 4. El ejercicio de 3 días (Nivel 1, concreto)

Objetivo: salir con **una demo funcionando y un caso escrito** que puedas enseñar a un cliente y a un
recruiter.

**Día 1 (2 h) — montar el esqueleto**
1. Cuenta gratis en HubSpot. Si no te encaja en 20 minutos, prueba Zoho Bigin y quédate con una.
2. Elige un negocio real que conozcas: tu cafetería, o una de las obras que hiciste.
3. Define **sus** etapas, no las del software. Ejemplo para una clínica: *Consulta recibida → Cita
   dada → Asistió → Presupuesto enviado → Cerrado / Perdido*.
4. Carga 40 contactos reales de tu vida (bares que visitaste, clientes antiguos de reforma, recruiter
   con los que hablaste). Datos reales, no "Juan Pérez".

**Día 2 (3 h) — conectarlo y automatizarlo**
5. Formulario web → crea contacto + negocio en la primera etapa. Esto ya lo sabes hacer.
6. Automatización con Make o n8n (gratis): negocio nuevo → email al dueño + tarea a 3 días + aviso
   por WhatsApp o Telegram.
7. Panel con tres números: cuántos entran, cuántos se cierran, cuánto dinero hay en juego.

**Día 3 (3 h) — empaquetarlo**
8. Escribe el caso en una página: problema del negocio, qué montaste, qué cambió. Sin inventar cifras:
   si no hay resultados, se dice "montado y en uso desde el [fecha]".
9. Graba 2 minutos de pantalla enseñando el flujo. Sin cara si no quieres.
10. Escribe el guion de venta de 30 segundos y la lista de 10 negocios de tu barrio que sí compran CRM
    (clínica, academia, gimnasio, inmobiliaria, distribuidor, taller con muchos presupuestos).

**Coste total: 0 €. Tiempo: 8 horas. Resultado: un servicio vendible y una respuesta sólida en entrevistas.**

---

## 5. Qué cambia en tu discurso profesional

### Lo que dejas de decir
- ❌ "Implemento CRM para pymes con Power Platform."
- ❌ "Desarrollador Power Apps" como titular principal.
- ❌ "Te monto el CRM completo."

### Lo que dices a partir de ahora (verdadero y vendible)
> "Trabajé en proyectos de CRM sobre Dynamics 365 y Power Platform, en equipo y con un alcance
> definido: entidades, formularios, flujos e integraciones. No he liderado una implantación completa y
> no la vendería como tal. Para pymes trabajo con CRMs que ya existen —HubSpot, Odoo— y automatizo
> alrededor: que el presupuesto salga solo, que el aviso llegue a tiempo, que nadie se olvide de un
> cliente."

Esa frase, en una entrevista, vale más que decir "sí" a todo. Un recruiter técnico detecta en dos
preguntas a quien infla, y a partir de ahí deja de escuchar. Tú llegas antes y ganas credibilidad.

### Y en el CV / LinkedIn
- **P1 (consultor Power Platform)** sigue vivo para **empleo**: en una empresa no te piden montar un
  CRM solo, te piden construir piezas dentro de un proyecto. Eso lo has hecho y está probado.
- **"Power Apps"** se queda en tu CV como herramienta que has usado (es verdad, Tigloo), pero **no**
  como servicio que vendes por proyecto cerrado. La diferencia es de alcance, no de honestidad.
- **P2 (automatización)** es el que gana peso con esto. Y es el que más está creciendo en ofertas.

---

## 6. Regla de oro para no volver a meterte en un lío

Antes de aceptar un proyecto, una sola pregunta:

> **¿Puedo entregarlo en menos de 15 horas con herramientas que ya sé usar?**

- **Sí** → cógelo, cobra fijo, entrega.
- **No, pero es aprendizaje que voy a reutilizar 10 veces** → cógelo solo si está pagado o si es demo propia.
- **No, y además cada cliente es distinto** → ni lo toques. Es el tipo de proyecto donde se pierde dinero y
  reputación a la vez.

Un CRM completo a medida para una pyme es siempre el tercer caso.
