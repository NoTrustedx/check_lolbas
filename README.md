# check_lolbas
Herramienta en Python para verificar rápidamente si una lista de binarios de Windows están documentados como LOLBins en el proyecto [LOLBAS](https://lolbas-project.github.io/).
Aquí tienes un `README.md` listo para subir a tu repositorio de GitHub. Está orientado a un público técnico y pensado para tu presentación en conferencias como BSidesPerú:

---

```markdown
# 🔍 check_lolbas.py

**check_lolbas.py** es una herramienta en Python para verificar rápidamente si una lista de binarios de Windows (por ejemplo, `*.exe`) están documentados como LOLBins en el proyecto [LOLBAS](https://lolbas-project.github.io/).

Este script fue desarrollado como parte del proyecto de investigación **LOLBins Shadow Warfare**, presentado en conferencias de ciberseguridad como BSides.

## 🚀 Características

- Verifica binarios contra el sitio oficial de LOLBAS.
- Soporta procesamiento concurrente para acelerar el análisis.
- Clasifica los binarios en:
  - 🟥 Encontrados en LOLBAS
  - 🟦 No encontrados (potencial para investigación)
- Identifica falsos negativos conocidos por verificación cruzada.
- Guarda los resultados en archivos `.txt`.

## 📁 Estructura del Proyecto

```

├── check\_lolbas.py
├── Only\_binaries.txt           # Lista de binarios a verificar (uno por línea)
├── found\_in\_lolbas.txt         # Binarios encontrados con sus URLs
├── not\_found\_in\_lolbas.txt     # Binarios no encontrados

````

## 🛠️ Requisitos

- Python 3.8+
- Librerías:

```bash
pip install requests beautifulsoup4 colorama
````

## 📄 Uso

1. Crea un archivo `Only_binaries.txt` con una lista de binarios, por ejemplo:

```
cmd.exe
calc.exe
bitsadmin.exe
```

2. Ejecuta el script:

```bash
python check_lolbas.py
```

3. El script generará:

* `found_in_lolbas.txt`: listado de binarios encontrados con su URL al sitio LOLBAS.
* `not_found_in_lolbas.txt`: listado de binarios no documentados en LOLBAS (útiles para investigar posibles nuevos LOLBins).

## ⚠️ Notas

* El script utiliza scraping básico. Si el diseño del sitio LOLBAS cambia, puede requerir ajustes.
* La detección de falsos negativos ayuda a evitar confusiones con binarios conocidos como `wmic.exe`, `msbuild.exe`, etc.

## 🧪 Ejemplo de salida

```
=== Verificador de Binarios en LOLBAS ===

Verificando 15 binarios en LOLBAS Project...

=== Resultados ===

Binarios ENCONTRADOS en LOLBAS (5):
- bitsadmin.exe (https://lolbas-project.github.io/lolbas/Binaries/Bitsadmin/)

Binarios NO encontrados en LOLBAS (10):
- mytool.exe
- customrunner.exe

¡Advertencia! Los siguientes binarios conocidos aparecen como no encontrados:
- wmic.exe (verificar manualmente: https://lolbas-project.github.io/#wmic)
```

## 📚 Créditos

Este script fue creado por **Erick O.** como parte de una investigación sobre binarios olvidados utilizados en operaciones ofensivas y persistencia post-explotación. Más detalles en la charla **"LOLBins Shadow Warfare"**.

## 📄 Licencia

MIT License

```

---

¿Deseas que te genere también el `requirements.txt` o un `setup.py` para distribuirlo como paquete?
```
