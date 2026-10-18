from playwright.sync_api import sync_playwright


URL = "https://gestiondocumental.epn.edu.ec/login.php"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("Abriendo Quipux...")

    page.goto(URL)

    print()
    print("=" * 50)
    print("QUIPUX")
    print("=" * 50)
    print("Inicia sesión normalmente.")
    print("Cuando ya veas TU BANDEJA de Quipux,")
    print("regresa aquí y presiona ENTER.")
    print("=" * 50)

    input("ENTER cuando estés dentro: ")

    # -------------------------------------------------
    # INTERFAZ PRINCIPAL
    # -------------------------------------------------

    print("\nEntrando a la interfaz principal...")

    page.goto(
        "https://gestiondocumental.epn.edu.ec/index_frames.php"
    )

    page.wait_for_timeout(2000)

    # -------------------------------------------------
    # MENÚ
    # -------------------------------------------------

    menu_frame = None

    for frame in page.frames:

        if frame.name == "lieftFrame":

            menu_frame = frame
            break

    if not menu_frame:

        print("❌ No se encontró lieftFrame")

        input("ENTER para cerrar...")

        browser.close()

        exit()

    print("✅ lieftFrame encontrado")

    # -------------------------------------------------
    # BÚSQUEDA AVANZADA
    # -------------------------------------------------

    menu_frame.get_by_text(
        "Búsqueda Avanzada",
        exact=True
    ).click()

    page.wait_for_timeout(1500)

    # -------------------------------------------------
    # FRAME DE BÚSQUEDA
    # -------------------------------------------------

    search_frame = None

    for frame in page.frames:

        if (
            frame.name == "mainFrame"
            and "busquedaN" in frame.url
        ):

            search_frame = frame
            break

    if not search_frame:

        print("❌ No se encontró formulario de búsqueda")

        input("ENTER para cerrar...")

        browser.close()

        exit()

    print("✅ Formulario de búsqueda encontrado")

    # -------------------------------------------------
    # TEXTO
    # -------------------------------------------------

    search_frame.locator(
        "#txt_texto"
    ).fill("Convocatoria")

    # -------------------------------------------------
    # TIPO = MEMORANDO
    # -------------------------------------------------

    search_frame.locator(
        "#txt_tipo_documento"
    ).select_option("3")

    # -------------------------------------------------
    # ESTADO = TODOS
    # -------------------------------------------------

    search_frame.locator(
        "#txt_estado"
    ).select_option("999")

    # -------------------------------------------------
    # ÁREA = CONSEJO
    # -------------------------------------------------

    print("Configurando área...")

    search_frame.locator(
        "#img_depe_cambiar"
    ).click()

    page.wait_for_timeout(500)

    search_frame.locator(
        "#slc_depe_combo"
    ).select_option("130") #130

    page.wait_for_timeout(800)

    print(
        "Área seleccionada:",
        search_frame.locator(
            "#span_depe_nombre"
        ).inner_text()
    )

    print(
        "Código área:",
        search_frame.locator(
            "#txt_depe_codi"
        ).input_value()
    )

    # -------------------------------------------------
    # USUARIO = TODOS
    # -------------------------------------------------

    print("Configurando usuario...")

    search_frame.locator(
        "#img_usua_cambiar"
    ).click()

    page.wait_for_timeout(500)

    search_frame.locator(
        "#slc_usua_combo"
    ).select_option("0")

    page.wait_for_timeout(800)

    print(
        "Usuario seleccionado:",
        search_frame.locator(
            "#span_usua_nombre"
        ).inner_text()
    )

    print(
        "Código usuario:",
        search_frame.locator(
            "#txt_usua_codi"
        ).input_value()
    )

    # -------------------------------------------------
    # FIRMA = TODOS
    # -------------------------------------------------

    search_frame.locator(
        "#txt_sino_firma"
    ).select_option("2")

    # -------------------------------------------------
    # FECHAS
    # -------------------------------------------------

    fecha_desde = search_frame.locator(
        "#txt_fecha_desde"
    )

    fecha_hasta = search_frame.locator(
        "#txt_fecha_hasta"
    )

    fecha_desde.evaluate(
        "(el) => el.removeAttribute('readonly')"
    )

    fecha_hasta.evaluate(
        "(el) => el.removeAttribute('readonly')"
    )

    fecha_desde.fill(
        "01/01/2023"
    )

    fecha_hasta.fill(
        "31/12/2023"
    )

    # -------------------------------------------------
    # CONFIGURACIÓN
    # -------------------------------------------------

    print()
    print("=" * 50)
    print("CONFIGURACIÓN DE BÚSQUEDA")
    print("=" * 50)

    print(
        "Texto:",
        search_frame.locator(
            "#txt_texto"
        ).input_value()
    )

    print(
        "Tipo:",
        search_frame.locator(
            "#txt_tipo_documento"
        ).input_value()
    )

    print(
        "Estado:",
        search_frame.locator(
            "#txt_estado"
        ).input_value()
    )

    print(
        "Área:",
        search_frame.locator(
            "#txt_depe_codi"
        ).input_value()
    )

    print(
        "Usuario:",
        search_frame.locator(
            "#txt_usua_codi"
        ).input_value()
    )

    print(
        "Fecha desde:",
        fecha_desde.input_value()
    )

    print(
        "Fecha hasta:",
        fecha_hasta.input_value()
    )

    print("=" * 50)

    # -------------------------------------------------
    # BUSCAR
    # -------------------------------------------------

    print("\n🔎 Ejecutando búsqueda...")

    search_frame.locator(
        "#btn_buscar"
    ).click()

    print("✅ Búsqueda ejecutada")

    # -------------------------------------------------
    # ESPERAR RESULTADOS
    # -------------------------------------------------

    # -------------------------------------------------
    # ESPERAR RESULTADOS REALES
    # -------------------------------------------------

    print(
        "\n⏳ Esperando el listado de resultados..."
    )

    print(
        "Esperando a que Quipux genere las filas..."
    )

    resultados_encontrados = False

    for segundo in range(60):

        try:

            tablas = search_frame.locator(
                "table"
            )

            cantidad_tablas = tablas.count()

            for i in range(cantidad_tablas):

                tabla = tablas.nth(i)

                filas = tabla.locator(
                    "tr"
                )

                cantidad_filas = filas.count()

                for j in range(cantidad_filas):

                    fila = filas.nth(j)

                    cantidad_td = fila.locator(
                        "td"
                    ).count()

                    if cantidad_td == 12:

                        resultados_encontrados = True

                        break

                if resultados_encontrados:
                    break

            if resultados_encontrados:
                break

        except Exception:
            pass

        page.wait_for_timeout(1000)

        if segundo % 5 == 0:

            print(
                f"   ⏳ {segundo} segundos..."
            )

    # -------------------------------------------------
    # RESULTADO DE LA ESPERA
    # -------------------------------------------------

    if resultados_encontrados:

        print()
        print(
            "✅ ¡Resultados encontrados!"
        )

        page.wait_for_timeout(1000)

    else:

        print()
        print(
            "⚠️ No aparecieron filas de resultados después de 60 segundos."
        )

        print(
            "Puede que Quipux no haya terminado la búsqueda."
        )




    # # -------------------------------------------------
    # # EXTRAER Y AGRUPAR DOCUMENTOS ÚNICOS
    # # -------------------------------------------------

    # print()
    # print("=" * 60)
    # print("📚 EXTRAYENDO DOCUMENTOS ÚNICOS")
    # print("=" * 60)

    # documentos = {}

    # # -------------------------------------------------
    # # TABLA DE RESULTADOS
    # # -------------------------------------------------

    # tablas = search_frame.locator("table")

    # tabla_resultados = None

    # for i in range(tablas.count()):

    #     tabla = tablas.nth(i)

    #     filas = tabla.locator("tr")

    #     for j in range(filas.count()):

    #         fila = filas.nth(j)

    #         if fila.locator("td").count() == 12:

    #             texto_fila = fila.inner_text().strip()

    #             # Evitamos tomar una tabla que no sea de resultados
    #             if "Memorando" in texto_fila:

    #                 tabla_resultados = tabla

    #                 break

    #     if tabla_resultados:

    #         break

    # if not tabla_resultados:

    #     print("❌ No se encontró la tabla de resultados.")

    #     input(
    #         "\nPresiona ENTER para cerrar..."
    #     )

    #     browser.close()

    #     exit()

    # print("✅ Tabla de resultados encontrada.")

    # # -------------------------------------------------
    # # RECORRER FILAS
    # # -------------------------------------------------

    # filas = tabla_resultados.locator("tr")

    # print(
    #     "Filas totales de la tabla:",
    #     filas.count()
    # )

    # filas_procesadas = 0

    # for j in range(filas.count()):

    #     fila = filas.nth(j)

    #     celdas = fila.locator("td")

    #     # Las filas reales tienen 12 TD
    #     if celdas.count() != 12:
    #         continue







    #     # ------------------------------------------------------------
    #     # Obtener VERRAD desde el enlace de apertura
    #     # ------------------------------------------------------------

    #     verrad = None

    #     try:

    #         celda_apertura = celdas.nth(1)

    #         enlace_apertura = (
    #             celda_apertura
    #             .locator("a")
    #             .first
    #         )

    #         if enlace_apertura.count() > 0:

    #             href_apertura = enlace_apertura.get_attribute(
    #                 "href",
    #                 timeout=3000
    #             )

    #             if href_apertura:

    #                 import re

    #                 coincidencia = re.search(
    #                     r'mostrar_documento\("([^"]+)"',
    #                     href_apertura
    #                 )

    #                 if coincidencia:
    #                     verrad = coincidencia.group(1)

    #     except Exception:
    #         verrad = None


    #     if not verrad:

    #         print(
    #             f"⚠️ Documento {numero}: "
    #             "no se encontró verrad."
    #         )





    #     try:

    #         datos = []

    #         for k in range(12):

    #             datos.append(
    #                 celdas.nth(k).inner_text().strip()
    #             )

    #         # -------------------------------------------------
    #         # COLUMNAS
    #         # -------------------------------------------------

    #         numero = datos[0]

    #         numero = numero.replace(
    #             "→",
    #             ""
    #         ).strip()


    #         if not numero:
    #             continue

    #         fecha = datos[2]

    #         referencia = datos[3]

    #         asunto = datos[4]

    #         usuario = datos[5]

    #         area = datos[6]

    #         de = datos[7]

    #         para = datos[8]

    #         tipo = datos[9]

    #         estado = datos[10]

    #         firma = datos[11]

    #         filas_procesadas += 1

    #         # -------------------------------------------------
    #         # CREAR DOCUMENTO SI NO EXISTE
    #         # -------------------------------------------------

    #         if numero not in documentos:

    #             documentos[numero] = {

    #                 "numero": numero,

    #                 "fecha": fecha,

    #                 "referencia": referencia,

    #                 "asunto": asunto,

    #                 "tipo": tipo,

    #                 "registros": []
    #             }

    #         # -------------------------------------------------
    #         # GUARDAR CADA REGISTRO
    #         # -------------------------------------------------

    #         documentos[numero]["registros"].append({

    #             "usuario": usuario,

    #             "area": area,

    #             "de": de,

    #             "para": para,

    #             "estado": estado,

    #             "firma": firma,

    #             "verrad": verrad
    #         })

    #     except Exception as e:

    #         print(
    #             f"⚠️ Error procesando fila {j}:",
    #             e
    #         )








    # # -------------------------------------------------
    # # MOSTRAR RESUMEN
    # # -------------------------------------------------

    # print()
    # print("=" * 60)
    # print("📊 RESUMEN DE EXTRACCIÓN")
    # print("=" * 60)

    # print(
    #     "Filas procesadas:",
    #     filas_procesadas
    # )

    # print(
    #     "Documentos únicos:",
    #     len(documentos)
    # )

    # # -------------------------------------------------
    # # FILTRAR DOCUMENTOS DEL CONSEJO
    # # -------------------------------------------------

    # documentos_consejo = {}

    # palabras_consejo = [

    #     "SESIÓN DE CONSEJO",

    #     "SESION DE CONSEJO",

    #     "SESIÓN EXTRAORDINARIA DE CONSEJO",

    #     "SESION EXTRAORDINARIA DE CONSEJO",

    #     "REINSTALACIÓN",

    #     "REINSTALACION"
    # ]

    # for numero, documento in documentos.items():

    #     asunto = documento["asunto"].upper()

    #     referencia = documento["referencia"].upper()

    #     encontrado = False

    #     for palabra in palabras_consejo:

    #         if palabra in asunto:

    #             encontrado = True

    #             break

    #     # También revisamos la referencia
    #     if not encontrado:

    #         if "CIIV" in referencia:

    #             encontrado = True

    #     if encontrado:

    #         documentos_consejo[numero] = documento

    # # -------------------------------------------------
    # # MOSTRAR DOCUMENTOS DEL CONSEJO
    # # -------------------------------------------------

    # print()
    # print("=" * 60)
    # print("🏛️ DOCUMENTOS RELACIONADOS CON EL CONSEJO")
    # print("=" * 60)

    # print(
    #     "Total:",
    #     len(documentos_consejo)
    # )

    # for numero, documento in documentos_consejo.items():

    #     print()
    #     print("-" * 60)

    #     print(
    #         "📄",
    #         documento["numero"]
    #     )

    #     print(
    #         "Fecha:",
    #         documento["fecha"]
    #     )

    #     print(
    #         "Referencia:",
    #         documento["referencia"]
    #     )

    #     print(
    #         "Asunto:",
    #         documento["asunto"]
    #     )

    #     print(
    #         "Tipo:",
    #         documento["tipo"]
    #     )

    #     print(
    #         "Registros asociados:",
    #         len(documento["registros"])
    #     )

    #     print(
    #         "Usuarios:"
    #     )

    #     usuarios_mostrados = set()

    #     for registro in documento["registros"]:

    #         usuario = registro["usuario"]

    #         if usuario and usuario not in usuarios_mostrados:

    #             print(
    #                 "   -",
    #                 usuario
    #             )

    #             usuarios_mostrados.add(
    #                 usuario
    #             )

    #     print(
    #         "Estados:"
    #     )

    #     estados_mostrados = set()

    #     for registro in documento["registros"]:

    #         estado = registro["estado"]

    #         if estado and estado not in estados_mostrados:

    #             print(
    #                 "   -",
    #                 estado
    #             )

    #             estados_mostrados.add(
    #                 estado
    #             )

    # # -------------------------------------------------
    # # FIN
    # # -------------------------------------------------

    # print()
    # print("=" * 60)
    # print("✅ EXTRACCIÓN TERMINADA")
    # print("=" * 60)

    # print(
    #     "Documentos únicos encontrados:",
    #     len(documentos)
    # )

    # print(
    #     "Documentos relacionados con Consejo:",
    #     len(documentos_consejo)
    # )


    # # ============================================================
    # # PROCESAR AUTOMÁTICAMENTE LOS DOCUMENTOS DEL CONSEJO
    # # ============================================================

    # for numero_documento, documento_actual in documentos_consejo.items():

    #     print("\n" + "=" * 70)
    #     print(f"📄 PROCESANDO DOCUMENTO: {numero_documento}")
    #     print("=" * 70)

    #     # --------------------------------------------------------
    #     # BUSCAR LA FILA REAL DEL DOCUMENTO
    #     # --------------------------------------------------------

    #     print(f"\n🔎 Buscando fila real para: {numero_documento}")

    #     filas = search_frame.locator("tr")
    #     cantidad_total_filas = filas.count()

    #     fila_doc = None

    #     for i in range(cantidad_total_filas):

    #         fila = filas.nth(i)

    #         try:

    #             celdas = fila.locator("td")
    #             cantidad_td = celdas.count()

    #             # Solo filas reales de resultados
    #             if cantidad_td != 12:
    #                 continue

    #             texto_fila = fila.inner_text().strip()

    #             if numero_documento in texto_fila:

    #                 fila_doc = fila

    #                 print(
    #                     f"✅ Fila real encontrada: {i}"
    #                 )

    #                 break

    #         except Exception:

    #             continue


    #     # --------------------------------------------------------
    #     # SI NO SE ENCUENTRA LA FILA
    #     # --------------------------------------------------------

    #     if fila_doc is None:

    #         print(
    #             f"❌ No se encontró la fila para "
    #             f"{numero_documento}"
    #         )

    #         continue


    #     # --------------------------------------------------------
    #     # OBTENER ENLACE DE APERTURA
    #     # --------------------------------------------------------

    #     celdas = fila_doc.locator("td")

    #     celda_apertura = celdas.nth(1)

    #     enlaces_apertura = celda_apertura.locator("a")

    #     cantidad_enlaces = enlaces_apertura.count()

    #     print(
    #         f"🔗 Enlaces encontrados: "
    #         f"{cantidad_enlaces}"
    #     )


    #     if cantidad_enlaces == 0:

    #         print(
    #             f"❌ No hay enlace de apertura para "
    #             f"{numero_documento}"
    #         )

    #         continue


    #     enlace_apertura = enlaces_apertura.first

    #     href = enlace_apertura.get_attribute(
    #         "href",
    #         timeout=3000
    #     )

    #     print(
    #         "\n✅ ENLACE DE APERTURA ENCONTRADO"
    #     )

    #     print(
    #         "HREF:",
    #         repr(href)
    #     )


    #     # ========================================================
    #     # ABRIR DOCUMENTO
    #     # ========================================================

    #     print(
    #         "\n🖱️ Abriendo documento..."
    #     )

    #     pagina_documento = None

    #     try:

    #         with page.expect_popup(
    #             timeout=5000
    #         ) as popup_info:

    #             enlace_apertura.click()

    #         pagina_documento = popup_info.value

    #         print(
    #             "✅ Documento abierto en nueva ventana/pestaña."
    #         )

    #     except Exception as e:

    #         print(
    #             "⚠️ No se detectó popup."
    #         )

    #         print(
    #             "Detalle:",
    #             e
    #         )

    #         continue


    #     # ========================================================
    #     # ANALIZAR DOCUMENTO
    #     # ========================================================

    #     if pagina_documento is not None:

    #         try:

    #             pagina_documento.wait_for_load_state(
    #                 "domcontentloaded",
    #                 timeout=10000
    #             )

    #         except Exception:

    #             pass

    #         print(
    #             "\n📄 DOCUMENTO ABIERTO"
    #         )

    #         print(
    #             "URL:",
    #             pagina_documento.url
    #         )

    #         print(
    #             "TÍTULO:",
    #             pagina_documento.title()
    #         )






    #     # ================================================================
    #     # ABRIR PESTAÑA ANEXOS
    #     # ================================================================

    #     print("\n📎 Buscando pestaña ANEXOS...")

    #     enlace_anexos = pagina_documento.locator(
    #         'a[onclick*="menu_ver=2"]'
    #     )

    #     cantidad_anexos = enlace_anexos.count()

    #     print(
    #         f"🔗 Enlaces de ANEXOS encontrados: "
    #         f"{cantidad_anexos}"
    #     )


    #     if cantidad_anexos == 0:

    #         print(
    #             "❌ No se encontró el enlace de ANEXOS."
    #         )

    #     else:

    #         print(
    #             "✅ Pestaña ANEXOS encontrada."
    #         )

    #         print(
    #             "\nHTML:"
    #         )

    #         print(
    #             enlace_anexos.first.evaluate(
    #                 "(el) => el.outerHTML"
    #             )
    #         )


    #         # ------------------------------------------------------------
    #         # Clic en ANEXOS
    #         # ------------------------------------------------------------

    #         print(
    #             "\n🖱️ Haciendo clic en ANEXOS..."
    #         )

    #         enlace_anexos.first.click()

    #         pagina_documento.wait_for_timeout(
    #             1500
    #         )


    #         print(
    #             "✅ Clic realizado."
    #         )

    #         print(
    #             "\n📍 URL actual:"
    #         )

    #         print(
    #             pagina_documento.url
    #         )

    #         # ================================================================
    #         # EXTRAER ANEXOS DESCARGABLES
    #         # ================================================================

    #         print("\n📎 EXTRAYENDO ANEXOS DESCARGABLES...")

    #         # filas_anexos = pagina_documento.locator(
    #         #     'tr[id^="tr_anexo_"]'
    #         # )


    #         filas_anexos = pagina_documento.locator(
    #             'tr[id^="tr_anexo_"]:not([id^="tr_anexo_detalle_"])'
    #         )


    #         cantidad_anexos = filas_anexos.count()

    #         print(
    #             f"📦 Filas de anexos encontradas: {cantidad_anexos}"
    #         )


    #         anexos = []


    #         for i in range(cantidad_anexos):

    #             fila_anexo = filas_anexos.nth(i)

    #             try:

    #                 # --------------------------------------------------------
    #                 # ID de la fila
    #                 # --------------------------------------------------------

    #                 id_fila = fila_anexo.get_attribute("id")

    #                 # Ejemplo:
    #                 # tr_anexo_20220001301113642270_00001

    #                 anex_codigo = id_fila.replace(
    #                     "tr_anexo_",
    #                     ""
    #                 )


    #                 # --------------------------------------------------------
    #                 # Nombre del archivo
    #                 # --------------------------------------------------------

    #                 nombre_elemento = fila_anexo.locator(
    #                     "td.listado2 b"
    #                 ).first

    #                 nombre_archivo = (
    #                     nombre_elemento
    #                     .inner_text()
    #                     .strip()
    #                 )


    #                 # --------------------------------------------------------
    #                 # Botón verde de descarga
    #                 # --------------------------------------------------------

    #                 boton_descarga = fila_anexo.locator(
    #                     'img[title="Descargar Archivo"]'
    #                 ).first

    #                 existe_boton = (
    #                     boton_descarga.count() > 0
    #                 )


    #                 # --------------------------------------------------------
    #                 # ONCLICK
    #                 # --------------------------------------------------------

    #                 if existe_boton:

    #                     onclick_descarga = (
    #                         boton_descarga
    #                         .get_attribute("onclick")
    #                     )

    #                 else:

    #                     onclick_descarga = None


    #                 # --------------------------------------------------------
    #                 # Mostrar resultado
    #                 # --------------------------------------------------------

    #                 print(
    #                     f"\n📄 ANEXO #{i + 1}"
    #                 )

    #                 print(
    #                     "   ID:",
    #                     id_fila
    #                 )

    #                 print(
    #                     "   Código:",
    #                     anex_codigo
    #                 )

    #                 print(
    #                     "   Archivo:",
    #                     nombre_archivo
    #                 )

    #                 print(
    #                     "   Botón descarga:",
    #                     "✅" if existe_boton else "❌"
    #                 )

    #                 print(
    #                     "   ONCLICK:",
    #                     onclick_descarga
    #                 )


    #                 anexos.append(
    #                     {
    #                         "codigo": anex_codigo,
    #                         "nombre": nombre_archivo,
    #                         "onclick": onclick_descarga
    #                     }
    #                 )


    #             except Exception as e:

    #                 print(
    #                     f"⚠️ Error procesando anexo {i}:",
    #                     e
    #                 )


    

    #         # ================================================================
    #         # DESCARGAR TODOS LOS ANEXOS
    #         # ================================================================

    #         import os

    #         carpeta_descargas = (
    #             r"C:\Users\Admin\Documents\docsapp"
    #             r"\Descargas_Quipux"
    #             r"\2022"
    #             r"\EPN-CIIV-2022-0321-M"
    #         )

    #         os.makedirs(
    #             carpeta_descargas,
    #             exist_ok=True
    #         )

    #         print("\n" + "=" * 70)
    #         print("📥 DESCARGANDO ANEXOS")
    #         print("=" * 70)

    #         cantidad_anexos = filas_anexos.count()

    #         print(
    #             f"📦 Anexos encontrados: {cantidad_anexos}"
    #         )

    #         descargas_exitosas = 0
    #         descargas_fallidas = 0


    #         for i in range(cantidad_anexos):

    #             fila_anexo = filas_anexos.nth(i)

    #             try:

    #                 # --------------------------------------------------------
    #                 # Código del anexo
    #                 # --------------------------------------------------------

    #                 id_fila = fila_anexo.get_attribute(
    #                     "id"
    #                 )

    #                 anex_codigo = id_fila.replace(
    #                     "tr_anexo_",
    #                     ""
    #                 )


    #                 # --------------------------------------------------------
    #                 # Nombre del archivo
    #                 # --------------------------------------------------------

    #                 nombre_elemento = fila_anexo.locator(
    #                     "td.listado2 b"
    #                 ).first

    #                 nombre_archivo = (
    #                     nombre_elemento
    #                     .inner_text(timeout=5000)
    #                     .strip()
    #                 )


    #                 # --------------------------------------------------------
    #                 # Botón verde
    #                 # --------------------------------------------------------

    #                 boton_descarga = fila_anexo.locator(
    #                     'img[title="Descargar Archivo"]'
    #                 ).first


    #                 if boton_descarga.count() == 0:

    #                     print(
    #                         f"\n❌ [{i + 1}/{cantidad_anexos}] "
    #                         f"No hay botón de descarga:"
    #                     )

    #                     print(
    #                         nombre_archivo
    #                     )

    #                     descargas_fallidas += 1

    #                     continue


    #                 # --------------------------------------------------------
    #                 # Ruta final
    #                 # --------------------------------------------------------

    #                 ruta_final = os.path.join(
    #                     carpeta_descargas,
    #                     nombre_archivo
    #                 )


    #                 print(
    #                     f"\n📥 [{i + 1}/{cantidad_anexos}]"
    #                 )

    #                 print(
    #                     "   Archivo:",
    #                     nombre_archivo
    #                 )

    #                 print(
    #                     "   Código:",
    #                     anex_codigo
    #                 )


    #                 # --------------------------------------------------------
    #                 # Si ya existe, no volver a descargar
    #                 # --------------------------------------------------------

    #                 if os.path.exists(ruta_final):

    #                     print(
    #                         "   ⏭️ Ya existe. Se omite."
    #                     )

    #                     descargas_exitosas += 1

    #                     continue


    #                 # --------------------------------------------------------
    #                 # Descargar
    #                 # --------------------------------------------------------

    #                 with pagina_documento.expect_download(
    #                     timeout=15000
    #                 ) as descarga_info:

    #                     boton_descarga.click()

    #                 descarga = descarga_info.value


    #                 # --------------------------------------------------------
    #                 # Guardar con nombre original
    #                 # --------------------------------------------------------

    #                 descarga.save_as(
    #                     ruta_final
    #                 )


    #                 print(
    #                     "   ✅ Guardado:"
    #                 )

    #                 print(
    #                     "   ",
    #                     ruta_final
    #                 )

    #                 descargas_exitosas += 1


    #             except Exception as e:

    #                 print(
    #                     f"\n❌ [{i + 1}/{cantidad_anexos}] "
    #                     f"ERROR:"
    #                 )

    #                 print(
    #                     repr(e)
    #                 )

    #                 descargas_fallidas += 1


    #         # ================================================================
    #         # RESUMEN
    #         # ================================================================

    #         print(
    #             "\n" + "=" * 70
    #         )

    #         print(
    #             "📊 RESUMEN DE DESCARGA"
    #         )

    #         print(
    #             "=" * 70
    #         )

    #         print(
    #             "Total de anexos:",
    #             cantidad_anexos
    #         )

    #         print(
    #             "✅ Exitosos:",
    #             descargas_exitosas
    #         )

    #         print(
    #             "❌ Fallidos:",
    #             descargas_fallidas
    #         )

    #         print(
    #             "📁 Carpeta:",
    #             carpeta_descargas
    #         )






    #         # ================================================================
    #         # RESUMEN
    #         # ================================================================

    #         print(
    #             "\n" + "=" * 70
    #         )

    #         print(
    #             "📊 RESUMEN DE ANEXOS"
    #         )

    #         print(
    #             "=" * 70
    #         )

    #         print(
    #             f"Total encontrados: {len(anexos)}"
    #         )


    #         for i, anexo in enumerate(
    #             anexos,
    #             start=1
    #         ):

    #             print(
    #                 f"{i}. {anexo['nombre']}"
    #             )

    #             print(
    #                 f"   Código: {anexo['codigo']}"
    #             )

    #             print(
    #                 f"   Descarga: "
    #                 f"{'✅' if anexo['onclick'] else '❌'}"
    #             )


    # else:

    #     print(
    #         "\n❌ No se pudo abrir el documento."
    #     )


    # ============================================================
    # PROCESAR TODAS LAS PÁGINAS DE RESULTADOS
    # ============================================================

    print()
    print("=" * 70)
    print("📚 INICIANDO PROCESAMIENTO DE TODAS LAS PÁGINAS")
    print("=" * 70)

    # ------------------------------------------------------------
    # DOCUMENTOS ACUMULADOS
    # ------------------------------------------------------------

    documentos = {}

    # Para evitar procesar dos veces el mismo documento
    documentos_procesados = set()

    # Palabras para identificar documentos relacionados
    # con Consejo
    palabras_consejo = [
        "SESIÓN DE CONSEJO",
        "SESION DE CONSEJO",
        "SESIÓN EXTRAORDINARIA DE CONSEJO",
        "SESION EXTRAORDINARIA DE CONSEJO",
        "REINSTALACIÓN",
        "REINSTALACION"
    ]

    numero_pagina = 1

    # ============================================================
    # BUCLE PRINCIPAL DE PÁGINAS
    # ============================================================

    while True:

        print()
        print("=" * 70)
        print(f"📄 PROCESANDO PÁGINA {numero_pagina}")
        print("=" * 70)

        # --------------------------------------------------------
        # ESPERAR A QUE APAREZCA LA TABLA DE RESULTADOS
        # --------------------------------------------------------

        print("⏳ Esperando resultados de la página...")

        tabla_resultados = None

        for segundo in range(30):

            try:

                tablas = search_frame.locator("table")

                for i in range(tablas.count()):

                    tabla = tablas.nth(i)

                    filas_temp = tabla.locator("tr")

                    for j in range(filas_temp.count()):

                        fila_temp = filas_temp.nth(j)

                        if fila_temp.locator("td").count() == 12:

                            tabla_resultados = tabla
                            break

                    if tabla_resultados:
                        break

                if tabla_resultados:
                    break

            except Exception:
                pass

            page.wait_for_timeout(500)

        # --------------------------------------------------------
        # SI NO SE ENCUENTRA LA TABLA
        # --------------------------------------------------------

        if not tabla_resultados:

            print(
                f"❌ No se encontró la tabla en la página "
                f"{numero_pagina}."
            )

            break

        print("✅ Tabla de resultados encontrada.")

        # --------------------------------------------------------
        # FILAS DE LA PÁGINA ACTUAL
        # --------------------------------------------------------

        filas = tabla_resultados.locator("tr")

        cantidad_filas = filas.count()

        print(
            f"📋 Filas encontradas: {cantidad_filas}"
        )

        filas_procesadas = 0
        documentos_pagina = set()

        # ========================================================
        # RECORRER CADA FILA DE LA PÁGINA
        # ========================================================

        for j in range(cantidad_filas):

            fila = filas.nth(j)

            try:

                celdas = fila.locator("td")

                # Las filas reales tienen 12 TD
                if celdas.count() != 12:
                    continue

                # ------------------------------------------------
                # EXTRAER DATOS
                # ------------------------------------------------

                datos = []

                for k in range(12):

                    datos.append(
                        celdas.nth(k).inner_text().strip()
                    )

                numero = datos[0]

                numero = numero.replace(
                    "→",
                    ""
                ).strip()

                if not numero:
                    continue

                fecha = datos[2]
                referencia = datos[3]
                asunto = datos[4]
                usuario = datos[5]
                area = datos[6]
                de = datos[7]
                para = datos[8]
                tipo = datos[9]
                estado = datos[10]
                firma = datos[11]

                # ------------------------------------------------
                # OBTENER VERRAD
                # ------------------------------------------------

                verrad = None

                try:

                    celda_apertura = celdas.nth(1)

                    enlace_apertura = (
                        celda_apertura
                        .locator("a")
                        .first
                    )

                    if enlace_apertura.count() > 0:

                        href_apertura = (
                            enlace_apertura
                            .get_attribute(
                                "href",
                                timeout=3000
                            )
                        )

                        if href_apertura:

                            import re

                            coincidencia = re.search(
                                r'mostrar_documento\("([^"]+)"',
                                href_apertura
                            )

                            if coincidencia:

                                verrad = (
                                    coincidencia.group(1)
                                )

                except Exception:

                    verrad = None

                if not verrad:

                    print(
                        f"⚠️ {numero}: "
                        "no se encontró verrad."
                    )

                # ------------------------------------------------
                # GUARDAR DOCUMENTO
                # ------------------------------------------------

                if numero not in documentos:

                    documentos[numero] = {

                        "numero": numero,

                        "fecha": fecha,

                        "referencia": referencia,

                        "asunto": asunto,

                        "tipo": tipo,

                        "registros": []
                    }

                documentos[numero]["registros"].append({

                    "usuario": usuario,

                    "area": area,

                    "de": de,

                    "para": para,

                    "estado": estado,

                    "firma": firma,

                    "verrad": verrad
                })

                filas_procesadas += 1

                documentos_pagina.add(numero)

                # =================================================
                # DETERMINAR SI ES DOCUMENTO DEL CONSEJO
                # =================================================

                asunto_mayus = asunto.upper()
                referencia_mayus = referencia.upper()

                es_consejo = False

                for palabra in palabras_consejo:

                    if palabra in asunto_mayus:

                        es_consejo = True
                        break

                if not es_consejo:

                    if "CIIV" in referencia_mayus:

                        es_consejo = True

                # ------------------------------------------------
                # SI NO ES DEL CONSEJO → SIGUIENTE FILA
                # ------------------------------------------------

                if not es_consejo:

                    continue

                print()
                print("-" * 70)
                print(
                    f"🏛️ DOCUMENTO DEL CONSEJO: {numero}"
                )
                print("-" * 70)

                # ------------------------------------------------
                # EVITAR DUPLICADOS
                # ------------------------------------------------

                clave_proceso = verrad

                if not clave_proceso:

                    clave_proceso = numero

                if clave_proceso in documentos_procesados:

                    print(
                        "⏭️ Este documento ya fue procesado."
                    )

                    continue

                documentos_procesados.add(
                    clave_proceso
                )

                # =================================================
                # OBTENER ENLACE DIRECTAMENTE DE ESTA FILA
                # =================================================

                enlaces_apertura = (
                    celdas
                    .nth(1)
                    .locator("a")
                )

                cantidad_enlaces = (
                    enlaces_apertura.count()
                )

                print(
                    f"🔗 Enlaces encontrados: "
                    f"{cantidad_enlaces}"
                )

                if cantidad_enlaces == 0:

                    print(
                        f"❌ No hay enlace de apertura "
                        f"para {numero}"
                    )

                    continue

                enlace_apertura = (
                    enlaces_apertura.first
                )

                href = enlace_apertura.get_attribute(
                    "href",
                    timeout=3000
                )

                print(
                    "✅ Enlace encontrado:"
                )

                print(
                    "   ",
                    repr(href)
                )

                # =================================================
                # ABRIR DOCUMENTO
                # =================================================

                print(
                    "\n🖱️ Abriendo documento..."
                )

                pagina_documento = None

                try:

                    with page.expect_popup(
                        timeout=5000
                    ) as popup_info:

                        enlace_apertura.click()

                    pagina_documento = (
                        popup_info.value
                    )

                    print(
                        "✅ Documento abierto "
                        "en nueva ventana/pestaña."
                    )

                except Exception as e:

                    print(
                        "⚠️ No se detectó popup."
                    )

                    print(
                        "Detalle:",
                        e
                    )

                    continue

                # =================================================
                # ANALIZAR DOCUMENTO
                # =================================================

                try:

                    try:

                        pagina_documento.wait_for_load_state(
                            "domcontentloaded",
                            timeout=10000
                        )

                    except Exception:

                        pass

                    print(
                        "\n📄 DOCUMENTO ABIERTO"
                    )

                    print(
                        "URL:",
                        pagina_documento.url
                    )

                    print(
                        "TÍTULO:",
                        pagina_documento.title()
                    )

                    # =================================================
                    # BUSCAR ANEXOS
                    # =================================================

                    print(
                        "\n📎 Buscando pestaña ANEXOS..."
                    )

                    enlace_anexos = (
                        pagina_documento.locator(
                            'a[onclick*="menu_ver=2"]'
                        )
                    )

                    cantidad_anexos = (
                        enlace_anexos.count()
                    )

                    print(
                        "🔗 Enlaces de ANEXOS encontrados:",
                        cantidad_anexos
                    )

                    # -------------------------------------------------
                    # SI NO TIENE ANEXOS
                    # -------------------------------------------------

                    if cantidad_anexos == 0:

                        print(
                            "ℹ️ Este documento no tiene "
                            "pestaña de ANEXOS."
                        )

                    else:

                        print(
                            "✅ Pestaña ANEXOS encontrada."
                        )

                        # ------------------------------------------------
                        # CLIC EN ANEXOS
                        # ------------------------------------------------

                        enlace_anexos.first.click()

                        pagina_documento.wait_for_timeout(
                            1500
                        )

                        print(
                            "✅ Pestaña ANEXOS abierta."
                        )

                        # =================================================
                        # EXTRAER ANEXOS
                        # =================================================

                        filas_anexos = (
                            pagina_documento.locator(
                                'tr[id^="tr_anexo_"]:not([id^="tr_anexo_detalle_"])'
                            )
                        )

                        cantidad_anexos = (
                            filas_anexos.count()
                        )

                        print(
                            f"📦 Filas de anexos encontradas: "
                            f"{cantidad_anexos}"
                        )

                        anexos = []

                        # ------------------------------------------------
                        # LEER ANEXOS
                        # ------------------------------------------------

                        for i in range(
                            cantidad_anexos
                        ):

                            fila_anexo = (
                                filas_anexos.nth(i)
                            )

                            try:

                                id_fila = (
                                    fila_anexo
                                    .get_attribute("id")
                                )

                                anex_codigo = (
                                    id_fila
                                    .replace(
                                        "tr_anexo_",
                                        ""
                                    )
                                )

                                nombre_elemento = (
                                    fila_anexo
                                    .locator(
                                        "td.listado2 b"
                                    )
                                    .first
                                )

                                nombre_archivo = (
                                    nombre_elemento
                                    .inner_text()
                                    .strip()
                                )

                                boton_descarga = (
                                    fila_anexo
                                    .locator(
                                        'img[title="Descargar Archivo"]'
                                    )
                                    .first
                                )

                                existe_boton = (
                                    boton_descarga.count()
                                    > 0
                                )

                                if existe_boton:

                                    onclick_descarga = (
                                        boton_descarga
                                        .get_attribute(
                                            "onclick"
                                        )
                                    )

                                else:

                                    onclick_descarga = None

                                print()
                                print(
                                    f"📄 ANEXO #{i + 1}"
                                )

                                print(
                                    "   Archivo:",
                                    nombre_archivo
                                )

                                print(
                                    "   Código:",
                                    anex_codigo
                                )

                                print(
                                    "   Descarga:",
                                    "✅"
                                    if existe_boton
                                    else "❌"
                                )

                                anexos.append({

                                    "codigo":
                                        anex_codigo,

                                    "nombre":
                                        nombre_archivo,

                                    "onclick":
                                        onclick_descarga
                                })

                            except Exception as e:

                                print(
                                    f"⚠️ Error procesando "
                                    f"anexo {i}:",
                                    e
                                )

                        # =================================================
                        # DESCARGAR ANEXOS
                        # =================================================

                        import os

                        carpeta_descargas = (
                            os.path.join(
                                r"C:\Users\Admin\Documents\docsapp",
                                "Descargas_Quipux",
                                "2023",
                                numero
                            )
                        )

                        os.makedirs(
                            carpeta_descargas,
                            exist_ok=True
                        )

                        print()
                        print(
                            "=" * 70
                        )

                        print(
                            "📥 DESCARGANDO ANEXOS"
                        )

                        print(
                            "=" * 70
                        )

                        descargas_exitosas = 0
                        descargas_fallidas = 0

                        # ------------------------------------------------
                        # DESCARGAR CADA ANEXO
                        # ------------------------------------------------

                        for i in range(
                            cantidad_anexos
                        ):

                            fila_anexo = (
                                filas_anexos.nth(i)
                            )

                            try:

                                id_fila = (
                                    fila_anexo
                                    .get_attribute(
                                        "id"
                                    )
                                )

                                anex_codigo = (
                                    id_fila
                                    .replace(
                                        "tr_anexo_",
                                        ""
                                    )
                                )

                                nombre_elemento = (
                                    fila_anexo
                                    .locator(
                                        "td.listado2 b"
                                    )
                                    .first
                                )

                                nombre_archivo = (
                                    nombre_elemento
                                    .inner_text(
                                        timeout=5000
                                    )
                                    .strip()
                                )

                                boton_descarga = (
                                    fila_anexo
                                    .locator(
                                        'img[title="Descargar Archivo"]'
                                    )
                                    .first
                                )

                                if (
                                    boton_descarga.count()
                                    == 0
                                ):

                                    print(
                                        f"\n❌ [{i + 1}/"
                                        f"{cantidad_anexos}] "
                                        "No hay botón de descarga:"
                                    )

                                    print(
                                        "   ",
                                        nombre_archivo
                                    )

                                    descargas_fallidas += 1

                                    continue

                                ruta_final = (
                                    os.path.join(
                                        carpeta_descargas,
                                        nombre_archivo
                                    )
                                )

                                print(
                                    f"\n📥 [{i + 1}/"
                                    f"{cantidad_anexos}]"
                                )

                                print(
                                    "   Archivo:",
                                    nombre_archivo
                                )

                                print(
                                    "   Código:",
                                    anex_codigo
                                )

                                # ----------------------------------------
                                # SI YA EXISTE
                                # ----------------------------------------

                                if os.path.exists(
                                    ruta_final
                                ):

                                    print(
                                        "   ⏭️ Ya existe. "
                                        "Se omite."
                                    )

                                    descargas_exitosas += 1

                                    continue

                                # ----------------------------------------
                                # DESCARGAR
                                # ----------------------------------------

                                with (
                                    pagina_documento
                                    .expect_download(
                                        timeout=15000
                                    )
                                ) as descarga_info:

                                    boton_descarga.click()

                                descarga = (
                                    descarga_info.value
                                )

                                descarga.save_as(
                                    ruta_final
                                )

                                print(
                                    "   ✅ Guardado:"
                                )

                                print(
                                    "   ",
                                    ruta_final
                                )

                                descargas_exitosas += 1

                            except Exception as e:

                                print(
                                    f"\n❌ [{i + 1}/"
                                    f"{cantidad_anexos}] "
                                    "ERROR:"
                                )

                                print(
                                    repr(e)
                                )

                                descargas_fallidas += 1

                        # ------------------------------------------------
                        # RESUMEN DE DESCARGA
                        # ------------------------------------------------

                        print()
                        print(
                            "=" * 70
                        )

                        print(
                            "📊 RESUMEN DE DESCARGA"
                        )

                        print(
                            "=" * 70
                        )

                        print(
                            "Total de anexos:",
                            cantidad_anexos
                        )

                        print(
                            "✅ Exitosos:",
                            descargas_exitosas
                        )

                        print(
                            "❌ Fallidos:",
                            descargas_fallidas
                        )

                        print(
                            "📁 Carpeta:",
                            carpeta_descargas
                        )

                except Exception as e:

                    print()
                    print(
                        f"❌ Error procesando "
                        f"el documento {numero}:"
                    )

                    print(
                        repr(e)
                    )

                finally:

                    # =================================================
                    # CERRAR POPUP
                    # =================================================

                    try:

                        if (
                            pagina_documento
                            and not pagina_documento.is_closed()
                        ):

                            pagina_documento.close()

                            print(
                                "🔒 Documento cerrado."
                            )

                    except Exception:

                        pass

            except Exception as e:

                print(
                    f"⚠️ Error procesando fila {j}:",
                    e
                )

        # ========================================================
        # RESUMEN DE LA PÁGINA
        # ========================================================

        print()
        print("=" * 70)
        print(
            f"📊 RESUMEN PÁGINA {numero_pagina}"
        )
        print("=" * 70)

        print(
            "Filas procesadas:",
            filas_procesadas
        )

        print(
            "Documentos encontrados:",
            len(documentos_pagina)
        )

        print(
            "Documentos procesados acumulados:",
            len(documentos_procesados)
        )

        # ========================================================
        # BUSCAR SIGUIENTE PÁGINA
        # ========================================================

        print()
        print(
            "🔎 Buscando siguiente página..."
        )

        enlaces_paginacion = search_frame.locator(
            'a[href*="paginador_reload_div"][href*="adodb_next_page="]'
        )

        enlace_siguiente = None

        cantidad_enlaces = (
            enlaces_paginacion.count()
        )

        print(
            "Enlaces de paginación encontrados:",
            cantidad_enlaces
        )

        for i in range(
            cantidad_enlaces
        ):

            enlace = (
                enlaces_paginacion.nth(i)
            )

            try:

                texto = (
                    enlace
                    .inner_text()
                    .strip()
                )

                if texto == ">>":

                    enlace_siguiente = enlace

                    break

            except Exception:

                continue

        # ========================================================
        # NO HAY MÁS PÁGINAS
        # ========================================================

        if enlace_siguiente is None:

            print()
            print(
                "✅ No hay más páginas."
            )

            break

        # ========================================================
        # PASAR A SIGUIENTE PÁGINA
        # ========================================================

        print()
        print(
            "➡️ Pasando a la siguiente página..."
        )

        try:

            enlace_siguiente.click()

        except Exception as e:

            print(
                "❌ Error al pasar a la siguiente página:"
            )

            print(
                repr(e)
            )

            break

        numero_pagina += 1

        # --------------------------------------------------------
        # DAR TIEMPO A QUIPUX PARA ACTUALIZAR
        # --------------------------------------------------------

        page.wait_for_timeout(
            1500
        )

    # ============================================================
    # RESUMEN FINAL
    # ============================================================

    print()
    print("=" * 70)
    print("🏁 PROCESAMIENTO DE TODAS LAS PÁGINAS TERMINADO")
    print("=" * 70)

    print(
        "Páginas procesadas:",
        numero_pagina
    )

    print(
        "Documentos únicos acumulados:",
        len(documentos)
    )

    print(
        "Documentos procesados:",
        len(documentos_procesados)
    )

    # ============================================================
    # DOCUMENTOS DEL CONSEJO ENCONTRADOS
    # ============================================================

    documentos_consejo = {}

    for numero, documento in documentos.items():

        asunto = documento["asunto"].upper()

        referencia = documento["referencia"].upper()

        encontrado = False

        for palabra in palabras_consejo:

            if palabra in asunto:

                encontrado = True
                break

        if not encontrado:

            if "CIIV" in referencia:

                encontrado = True

        if encontrado:

            documentos_consejo[numero] = documento

    print()
    print("=" * 70)
    print("🏛️ DOCUMENTOS RELACIONADOS CON EL CONSEJO")
    print("=" * 70)

    print(
        "Total:",
        len(documentos_consejo)
    )

    for numero, documento in documentos_consejo.items():

        print()
        print("-" * 70)

        print(
            "📄",
            documento["numero"]
        )

        print(
            "Fecha:",
            documento["fecha"]
        )

        print(
            "Referencia:",
            documento["referencia"]
        )

        print(
            "Asunto:",
            documento["asunto"]
        )

        print(
            "Registros asociados:",
            len(documento["registros"])
        )

    print()
    print("=" * 70)
    print("✅ EXTRACCIÓN TERMINADA")
    print("=" * 70)




    # ============================================================
    # FIN DEL DIAGNÓSTICO
    # ============================================================

    print("\n")
    print("=" * 70)
    print("⏸️ DIAGNÓSTICO TERMINADO")
    print("=" * 70)

    input(
        "\n👉 Presiona ENTER para cerrar..."
    )

    browser.close()