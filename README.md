# Quipux Archiver

Quipux Archiver es un script de automatización diseñado para facilitar la recopilación y organización de documentación institucional consultada en Quipux.

El programa utiliza Playwright para interactuar con la interfaz web, realizar búsquedas avanzadas, recorrer los resultados paginados, abrir documentos y descargar sus anexos.

La autenticación se realiza manualmente por parte del usuario.

## Objetivos

- Automatizar búsquedas documentales repetitivas.
- Facilitar la identificación de memorandos relacionados con una temática.
- Recorrer los resultados de búsqueda por páginas.
- Consultar los anexos disponibles en cada documento.
- Descargar los archivos y organizarlos en carpetas por documento.
- Evitar la descarga de archivos que ya existen localmente.
- Mostrar resúmenes del procesamiento y de las descargas realizadas.

## Tecnologías

- Python 3
- Playwright
- Chromium
- Git y GitHub para el control de versiones

## Funcionamiento general

1. El programa abre la página de acceso a Quipux.
2. El usuario inicia sesión manualmente.
3. El programa accede a la interfaz principal y abre la búsqueda avanzada.
4. Se configuran los criterios de búsqueda: texto, tipo documental, fechas, área, usuario y estado.
5. Se ejecuta la búsqueda.
6. Se recorren las páginas de resultados.
7. Se identifican los documentos de interés mediante los criterios configurados.
8. Se abre cada documento en una ventana emergente.
9. Se consulta la sección de anexos.
10. Se descargan los archivos disponibles en la carpeta correspondiente al documento.
11. Se omiten los archivos que ya existen en la ruta de destino.
12. Se muestran resúmenes por documento y por página, y se finaliza el proceso cuando no hay más páginas.

## Configuración de búsqueda

Los criterios de búsqueda se encuentran definidos en el script y pueden modificarse según el período y la documentación que se necesite recopilar.

Ejemplo de configuración utilizada durante las pruebas:

| Parámetro | Valor de ejemplo |
|---|---|
| Texto de búsqueda | `Convocatoria` |
| Tipo documental | Memorando |
| Código de tipo documental | `3` |
| Área | Todas las áreas |
| Código de todas las áreas | `0` |
| Usuario | Todos los usuarios |
| Código de todos los usuarios | `0` |
| Período | Año configurado en el script |

Los códigos corresponden a las opciones identificadas en la interfaz de Quipux utilizada durante las pruebas. Deben verificarse si la aplicación cambia.

## Requisitos previos

- Tener Python instalado.
- Contar con acceso autorizado a Quipux.
- Tener instalada una versión compatible de Playwright.
- Disponer de acceso al navegador Chromium utilizado por Playwright.
- Contar con permisos para consultar los documentos y descargar sus anexos.

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd quipux-archiver
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Si Playwright requiere instalar Chromium:

```bash
playwright install chromium
```

## Ejecución

Ejecutar el script:

```bash
python quipux_bot.py
```

Cuando se abra la página de acceso, el usuario debe iniciar sesión manualmente y continuar cuando el programa lo solicite.

La ejecución depende de que la sesión institucional sea válida y de que la interfaz de Quipux mantenga los elementos con los que interactúa el script.

## Organización de las descargas

Los archivos se guardan en directorios organizados por año y número de documento.

Ejemplo de estructura:

```text
Descargas_Quipux/
└── 2023/
    └── EPN-CIIV-2023-0001-M/
        ├── anexo_1.pdf
        └── anexo_2.xlsx
```

La ruta base y el año deben revisarse en la configuración del script antes de ejecutar una búsqueda para otro período.

Los nombres de los archivos descargados dependen de los nombres que Quipux presenta para sus anexos.

## Consideraciones y limitaciones

- El usuario debe autenticarse manualmente.
- La ejecución depende de la disponibilidad de Quipux y de su estructura HTML.
- Los cambios en los selectores, ventanas emergentes o controles de paginación pueden requerir ajustes.
- No todos los documentos necesariamente tienen anexos.
- Los archivos existentes en la ruta de destino se omiten para evitar descargas repetidas.
- La clasificación de documentos relevantes depende de los criterios implementados en el script.
- Antes de procesar períodos extensos, se recomienda realizar una prueba con un rango de fechas pequeño y verificar los resultados.

## Seguridad y uso responsable

Este proyecto está destinado a la consulta y recopilación documental mediante acceso autorizado.

El script no debe utilizarse para firmar, enviar, reasignar, modificar o eliminar documentos.

No se deben publicar en el repositorio:

- Contraseñas o credenciales institucionales.
- Cookies, tokens o datos de sesión.
- Documentos institucionales descargados.
- Archivos de configuración con datos personales o rutas privadas innecesarias.
- Registros que expongan información documental confidencial.

Antes de publicar el repositorio, se debe comprobar que el código y el historial de Git no contengan información sensible.

## Estado del proyecto

Versión inicial funcional en proceso de documentación.

La versión actual automatiza la búsqueda, navegación por páginas y descarga de anexos. Las mejoras futuras deberán documentarse y probarse antes de incorporarse a la versión estable.

## Mejoras futuras

- Centralizar los parámetros de búsqueda en un archivo de configuración.
- Registrar resultados y errores en un archivo de log.
- Generar un inventario CSV de documentos y anexos.
- Mejorar la recuperación ante errores de carga o navegación.
- Consolidar la deduplicación de documentos mediante el identificador `verrad`.
- Incorporar pruebas con distintos períodos y criterios de búsqueda.
- Separar la configuración, la navegación, la descarga y los reportes en módulos independientes.
