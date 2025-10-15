# Compilador de LaTeX para CV

Este proyecto contiene un script de Python para compilar archivos LaTeX y generar PDFs, específicamente diseñado para compilar el CV de Jesús Herrera Ledón.

## 📋 Requisitos Previos

### 1. Instalar LaTeX

Antes de usar este script, necesitas tener LaTeX instalado en tu sistema:

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install texlive-full latexmk
```

#### CentOS/RHEL:
```bash
sudo yum install texlive-scheme-full
```

#### macOS:
```bash
brew install --cask mactex
```

#### Windows:
Descarga e instala MiKTeX desde [https://miktex.org/](https://miktex.org/)

### 2. Verificar instalación
```bash
pdflatex --version
latexmk --version
```

## 🐍 Configuración del Entorno Python

### 1. Crear entorno virtual (recomendado)
```bash
# Crear entorno virtual
python3 -m venv latex_env

# Activar entorno virtual
# En Linux/macOS:
source latex_env/bin/activate
# En Windows:
latex_env\Scripts\activate
```

### 2. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

## 🚀 Uso del Script

### Compilar automáticamente
El script buscará automáticamente archivos `.tex` en el directorio `resume/`:

```bash
python compile_latex.py
```

### Compilar archivo específico
```bash
python compile_latex.py resume/jesus_Herrera_Ledon.tex
```

### Verificar dependencias
El script verificará automáticamente:
- ✅ Instalación de LaTeX (pdflatex o latexmk)
- ✅ Paquete moderncv (lo instalará automáticamente si falta)

## 📁 Estructura del Proyecto

```
PersonalWebPage/
├── resume/
│   ├── jesus_Herrera_Ledon.tex    # Archivo LaTeX del CV
│   └── Jesus_Herrera_Ledon.pdf    # PDF generado
├── compile_latex.py               # Script de compilación
├── requirements.txt               # Dependencias de Python
└── README.md                      # Este archivo
```

## 🔧 Características del Script

- **Verificación automática**: Comprueba que LaTeX esté instalado
- **Instalación automática**: Descarga e instala el paquete `moderncv` si falta
- **Manejo de errores**: Muestra errores detallados si la compilación falla
- **Colores en terminal**: Interfaz colorida para mejor experiencia
- **Timeout protection**: Evita que el script se cuelgue
- **Limpieza automática**: Elimina archivos temporales de prueba

## 🐛 Solución de Problemas

### Error: "LaTeX no está instalado"
1. Instala LaTeX siguiendo las instrucciones de arriba
2. Verifica la instalación con `pdflatex --version`

### Error: "moderncv no está disponible"
El script intentará instalarlo automáticamente. Si falla:
1. Instala manualmente: `sudo apt-get install texlive-latex-extra`
2. O descarga desde CTAN: https://ctan.org/pkg/moderncv

### Error durante la compilación
1. Revisa el log de errores que muestra el script
2. Verifica que el archivo `.tex` no tenga errores de sintaxis
3. Asegúrate de que todos los paquetes necesarios estén instalados

### Error de permisos
```bash
chmod +x compile_latex.py
```

## 📝 Archivos Generados

Después de una compilación exitosa, encontrarás:
- `resume/jesus_Herrera_Ledon.pdf` - El CV en formato PDF
- Archivos temporales (`.aux`, `.log`, `.out`) que se pueden eliminar

## 🔄 Recompilación Futura

Para recompilar el CV en el futuro:

1. **Activar el entorno virtual** (si usaste uno):
   ```bash
   source latex_env/bin/activate
   ```

2. **Ejecutar el script**:
   ```bash
   python compile_latex.py
   ```

3. **O compilar directamente con LaTeX**:
   ```bash
   cd resume
   pdflatex jesus_Herrera_Ledon.tex
   ```

## 📦 Dependencias de Python

- `latexmk`: Para compilación robusta de LaTeX
- `pathlib2`: Manejo de rutas de archivos
- `colorama`: Colores en terminal
- `click`: Interfaz de línea de comandos
- `pyyaml`: Manejo de configuraciones

## 🤝 Contribuciones

Si encuentras problemas o quieres mejorar el script:
1. Revisa los logs de error
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el archivo LaTeX sea válido

## 📄 Licencia

Este proyecto es de uso personal para la compilación del CV de Jesús Herrera Ledón.
