# Folleto para bares de València — notas de diseño

Tres archivos listos para imprimir mañana:

| Archivo | Qué es | Dónde |
|---|---|---|
| `folleto-A5-con-sangre.pdf` | El folleto, 2 caras, 148×210 mm + 3 mm de sangrado | Copistería (pídeles "A5, doble cara, 170 g") |
| `A4-2-por-hoja.pdf` | Dos folletos por A4 horizontal, con línea de corte. Página 1 = caras A, página 2 = dorsos | Tu impresora de casa |
| `cartel-A4.pdf` | Cartel A4 para la barra o el escaparate | Copistería, 250-300 g |

---

## 1. Cómo imprimirlo (2 minutos)

**En copistería** (lo más rápido y queda mejor): llévate `folleto-A5-con-sangre.pdf` y di
*"A5, doble cara, papel mate de 170 g, a tamaño real"*. Unas 40 copias salen por 8-12 €.
El sangrado ya está incluido, así que no tienen que tocar nada.

**En casa** (para tener 2 folletos hoy mismo): abre `A4-2-por-hoja.pdf`, imprime la página 1,
dale la vuelta al papel e imprime la página 2. **Marca "tamaño real / 100 %", no "ajustar al papel".**
Luego corta por la línea de puntos con regla y cúter. La impresora dejará 4-5 mm de blanco en los
bordes: recórtalos y queda limpio.

**Ajustes que sí importan:**
- Calidad: **alta o "óptima"**, nunca borrador (el grano del papel y la foto se pierden).
- Escala: **100 %**.
- Papel: mate, nunca brillo. El brillo convierte el crema en un charco de luz.

---

## 2. Qué es humano y qué es máquina, decisión por decisión

Me pediste que se notara que lo hiciste tú. Esto es exactamente lo que separa este folleto de
lo que habría salido de un generador:

| Decisión | Por qué se lee como humano | Lo que habría hecho una IA |
|---|---|---|
| **Dos tintas** (negro cálido + rojo teja sobre crema) | Es una limitación de imprenta real: quien imprime barato trabaja con dos tintas | Degradado azul-violeta, "moderno", imposible de imprimir barato |
| **La foto en semitono, con grano y trama** | Parece pasada por una fotocopiadora o una riso, no renderizada | Foto nítida y perfecta, con fondo desenfocado artificial |
| **El azulejo del baño convertido en textura clara** | La foto se salvó en vez de disimularse: no hay fondo falso | Habría puesto un fondo de oficina generado (y cantaría) |
| **Subrayado que se pasa del final y no es recto** | Nadie dibuja una línea perfecta a mano | Sublínea perfecta, equidistante, del ancho exacto del texto |
| **Los tres ticks dibujados a mano alzada** | Cada uno es distinto: tamaño, ángulo y grosor varían | Icono de check idéntico repetido tres veces, en verde |
| **El precio "490 → 290" escrito con letras desalineadas** | Es rotulador, con las letras del 290 torcidas medio grado cada una | Número en tipografía perfecta, con un badge circular de "oferta" |
| **La tarjeta de precio girada 3,2°** | Está pegada, no colocada en una rejilla | Todo perfectamente alineado a la cuadrícula |
| **El sello "HECHO A MANO EN PATRAIX" girado y pegado sobre la foto** | Los sellos se estampan torcidos, y encima de la foto | Ningún sello: un badge vectorial con sombra suave |
| **Cierre en cuerpo pequeño y con letras irregulares** ("Si has llegado hasta aquí leyendo…") | Parece tecleado en el último momento, que es justo lo que es | Una frase de cierre centrada, grande y vacía ("¿Hablamos?") |
| **Texto que dice cosas incómodas** (la oferta solo para los dos primeros, la mitad al entregar) | Un humano negocia; una máquina no se compromete | "Contáctanos para más información" |
| **Cero iconos, cero sombras, cero degradados** | Solo tipografía, trama y dos tintas | Iconitos de línea, tarjetas con sombra y esquinas de 16 px |
| **La grapa del contenido: números concretos** (290 €, 39 €/mes, 5-7 días, mitad y mitad) | Un autónomo que necesita el trabajo se moja | Precios "a consultar" y plazos "según proyecto" |

### Las ocho cosas que delatan a un diseño generado (y que aquí no están)

1. **Emojis en los bullets** (✅ 🚀 💡). Ninguno.
2. **"Soluciones innovadoras que transforman tu negocio".** No hay una sola frase de ese tipo.
3. **Simetría perfecta.** Aquí el precio está torcido, el subrayado se pasa y el sello está ladeado.
4. **Foto de stock.** La foto es tuya, y se nota que es tuya.
5. **Paleta de tres colores "tech"** (morado, azul eléctrico, turquesa). Aquí hay dos tintas de imprenta.
6. **Exceso de texto igual, en bloques del mismo tamaño.** Aquí hay jerarquía agresiva: 24 pt de titular y 4,8 pt de letra pequeña.
7. **"Contáctanos" arriba y abajo, sin datos.** Aquí el móvil está a 13 pt y es lo más grande de la mitad inferior.
8. **Cero fricción, cero opinión.** Aquí hay una frase que filtra ("No hace falta que sepas nada de tecnología") y una que se moja ("contesto yo, no un bot").

---

## 3. La foto: qué le hice exactamente

Trabajé sobre `foto/original/IMG-20260909-WA0008.jpg` (la real, la de la camiseta negra — **no** la
generada con IA, que en un folleto impreso se detecta al instante y además no eres tú).

1. **Recorte 4:5** dejando cabeza y hombros, sin la mano del pulgar que entraba por abajo.
2. **Blanco y negro + contraste fuerte**, hasta que el azulejo del baño queda casi a blanco de papel.
3. **Cuatro niveles de gris** (posterizado): así parece serigrafía o fotocopia, no una foto digital.
4. **Grano** añadido a mano para que la trama no sea limpia y digital.
5. **Marco fino en rojo**, para que la foto pertenezca a la misma impresión de dos tintas.

Resultado: el fondo del baño se disuelve y solo queda tu cara. Nadie va a preguntarse dónde te la
hiciste; van a pensar que la imprimiste.

---

## 4. Tres cosas que tienes que decidir tú antes de imprimir

Te lo dejo escrito, pero son decisiones tuyas, no mías:

1. **La oferta de arranque.** El folleto dice: *"los 2 primeros bares de València: el Bar conectado
   por 290 €, a cambio de una reseña y una foto"*. Es honesto y vende, pero te compromete: si te
   dicen que sí dos bares, tienes que cumplirlo. Si no quieres atarte, cambia la línea por
   *"precio de lanzamiento este mes"* y quita el "2".
2. **La garantía.** Dice *"dos rondas de cambios incluidas. Si algo no funciona, lo arreglo"*. Es
   asumible. Si prefieres no prometer nada, bórralo.
3. **El dato de "5 años detrás de la barra".** Es lo que dice tu CV ("más de 5 años"). Si en una
   conversación te preguntan y son 4, pierdes credibilidad por nada. Pon el número que puedas
   defender con fechas.

---

## 5. Cómo usarlo (esto vale más que el folleto)

No lo repartas por buzoneo. **Entra en el bar, pide algo y déjalo en la barra.**

> *"Buenas. ¿Quién lleva el tema de la carta? … Encantado. Mira, te dejo esto, que soy de Patraix
> y estoy haciendo cartas con QR para bares del barrio. No vengo a venderte nada ahora: míralo cuando
> cierres. Si te interesa, me mandas un mensaje con la palabra CARTA y en un día te enseño cómo
> quedaría la tuya con tus precios y tus fotos. Sin compromiso."*

Tres cosas que funcionan y no están escritas en el folleto:

- **Pide el WhatsApp del dueño, no el del bar.** "¿Me das tu número y te mando un ejemplo?"
- **Si dice "ya tengo web"**, responde: *"perfecto, entonces solo te falta que la carta se pueda
  cambiar sin llamar a nadie. Te enseño eso y decides"*.
- **Vuelve a los 4 días** a los que te dijeron "déjalo, lo miro". El 80 % de los síes llegan en la
  segunda visita, no en la primera.

**Objetivo realista de una tarde:** 12 bares visitados, 5 conversaciones con el dueño, 3 números de
WhatsApp, 1 "mándame el ejemplo". Con eso, la semana que viene tienes el primero.
