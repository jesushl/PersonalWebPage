#!/bin/bash

# Script de configuración inicial para el entorno de compilación LaTeX
# Uso: ./setup.sh

set -e  # Salir si hay algún error

echo "🚀 Configurando entorno de compilación LaTeX..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Python 3 está instalado
check_python() {
    print_status "Verificando Python 3..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python 3 encontrado: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 no está instalado"
        print_status "Por favor instala Python 3 antes de continuar"
        return 1
    fi
}

# Verificar si pip está instalado
check_pip() {
    print_status "Verificando pip..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 encontrado"
        return 0
    elif command -v pip &> /dev/null; then
        print_success "pip encontrado"
        return 0
    else
        print_error "pip no está instalado"
        print_status "Instalando pip..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        else
            print_error "No se pudo instalar pip automáticamente"
            return 1
        fi
    fi
}

# Crear entorno virtual
create_venv() {
    print_status "Creando entorno virtual..."
    if [ -d "latex_env" ]; then
        print_warning "El entorno virtual ya existe"
        read -p "¿Quieres recrearlo? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf latex_env
        else
            print_status "Usando entorno virtual existente"
            return 0
        fi
    fi
    
    python3 -m venv latex_env
    print_success "Entorno virtual creado: latex_env"
}

# Activar entorno virtual e instalar dependencias
install_dependencies() {
    print_status "Activando entorno virtual..."
    source latex_env/bin/activate
    
    print_status "Actualizando pip..."
    pip install --upgrade pip
    
    print_status "Instalando dependencias de Python..."
    pip install -r requirements.txt
    
    print_success "Dependencias instaladas correctamente"
}

# Verificar LaTeX
check_latex() {
    print_status "Verificando instalación de LaTeX..."
    
    if command -v pdflatex &> /dev/null; then
        print_success "pdflatex encontrado"
        LATEX_AVAILABLE=true
    elif command -v latexmk &> /dev/null; then
        print_success "latexmk encontrado"
        LATEX_AVAILABLE=true
    else
        print_warning "LaTeX no está instalado"
        print_status "Instalando LaTeX..."
        
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y texlive-full latexmk
        elif command -v yum &> /dev/null; then
            sudo yum install -y texlive-scheme-full
        elif command -v brew &> /dev/null; then
            brew install --cask mactex
        else
            print_error "No se pudo instalar LaTeX automáticamente"
            print_status "Por favor instala LaTeX manualmente:"
            print_status "  Ubuntu/Debian: sudo apt-get install texlive-full"
            print_status "  CentOS/RHEL: sudo yum install texlive-scheme-full"
            print_status "  macOS: brew install --cask mactex"
            print_status "  Windows: Descarga MiKTeX desde https://miktex.org/"
            LATEX_AVAILABLE=false
        fi
    fi
}

# Probar la compilación
test_compilation() {
    if [ "$LATEX_AVAILABLE" = true ]; then
        print_status "Probando la compilación..."
        
        # Activar entorno virtual
        source latex_env/bin/activate
        
        # Ejecutar script de compilación
        if python compile_latex.py --help &> /dev/null; then
            print_success "Script de compilación funciona correctamente"
        else
            print_error "Error al ejecutar el script de compilación"
            return 1
        fi
    else
        print_warning "Saltando prueba de compilación (LaTeX no disponible)"
    fi
}

# Función principal
main() {
    echo "=========================================="
    echo "  Configuración del Entorno LaTeX"
    echo "=========================================="
    echo
    
    # Verificar Python
    if ! check_python; then
        exit 1
    fi
    
    # Verificar pip
    if ! check_pip; then
        exit 1
    fi
    
    # Crear entorno virtual
    create_venv
    
    # Instalar dependencias
    install_dependencies
    
    # Verificar LaTeX
    check_latex
    
    # Probar compilación
    test_compilation
    
    echo
    echo "=========================================="
    print_success "¡Configuración completada!"
    echo "=========================================="
    echo
    echo "Para usar el entorno:"
    echo "1. Activar entorno virtual: source latex_env/bin/activate"
    echo "2. Compilar CV: python compile_latex.py"
    echo "3. Desactivar entorno: deactivate"
    echo
    echo "Para más información, consulta el README.md"
}

# Ejecutar función principal
main "$@"
