#!/usr/bin/env python3
"""
Script para compilar archivos LaTeX y generar PDFs
Uso: python compile_latex.py [archivo.tex]
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from colorama import init, Fore, Style
import click

# Inicializar colorama para colores en terminal
init(autoreset=True)

def check_latex_installation():
    """Verificar si LaTeX está instalado en el sistema"""
    try:
        # Verificar si pdflatex está disponible
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ LaTeX (pdflatex) está instalado{Style.RESET_ALL}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Verificar si latexmk está disponible
        result = subprocess.run(['latexmk', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ LaTeX (latexmk) está instalado{Style.RESET_ALL}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"{Fore.RED}✗ LaTeX no está instalado{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Por favor instala LaTeX en tu sistema:{Style.RESET_ALL}")
    print("  Ubuntu/Debian: sudo apt-get install texlive-full")
    print("  CentOS/RHEL: sudo yum install texlive-scheme-full")
    print("  macOS: brew install --cask mactex")
    print("  Windows: Descarga MiKTeX desde https://miktex.org/")
    return False

def check_moderncv():
    """Verificar si el paquete moderncv está disponible"""
    try:
        # Crear un archivo temporal para verificar moderncv
        test_content = r"""
\documentclass{moderncv}
\begin{document}
\makecvtitle
\end{document}
"""
        test_file = Path("test_moderncv.tex")
        test_file.write_text(test_content)
        
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', str(test_file)], 
                              capture_output=True, text=True, timeout=30)
        
        # Limpiar archivos temporales
        for ext in ['.tex', '.aux', '.log', '.pdf']:
            test_file.with_suffix(ext).unlink(missing_ok=True)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Paquete moderncv está disponible{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✗ Paquete moderncv no está disponible{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Instalando moderncv...{Style.RESET_ALL}")
            install_moderncv()
            return True
            
    except Exception as e:
        print(f"{Fore.RED}Error verificando moderncv: {e}{Style.RESET_ALL}")
        return False

def install_moderncv():
    """Instalar el paquete moderncv si no está disponible"""
    try:
        # Crear directorio para paquetes locales si no existe
        local_texmf = Path.home() / "texmf" / "tex" / "latex"
        local_texmf.mkdir(parents=True, exist_ok=True)
        
        # Descargar moderncv desde CTAN
        moderncv_url = "https://mirrors.ctan.org/macros/latex/contrib/moderncv.zip"
        print(f"{Fore.YELLOW}Descargando moderncv...{Style.RESET_ALL}")
        
        # Usar curl o wget para descargar
        if shutil.which('curl'):
            subprocess.run(['curl', '-L', '-o', 'moderncv.zip', moderncv_url], check=True)
        elif shutil.which('wget'):
            subprocess.run(['wget', '-O', 'moderncv.zip', moderncv_url], check=True)
        else:
            print(f"{Fore.RED}No se encontró curl o wget para descargar moderncv{Style.RESET_ALL}")
            return False
        
        # Extraer y mover a la ubicación correcta
        if shutil.which('unzip'):
            subprocess.run(['unzip', '-q', 'moderncv.zip'], check=True)
            moderncv_dir = local_texmf / "moderncv"
            if moderncv_dir.exists():
                shutil.rmtree(moderncv_dir)
            shutil.move('moderncv', str(moderncv_dir))
            
            # Limpiar archivo zip
            Path('moderncv.zip').unlink()
            
            print(f"{Fore.GREEN}✓ moderncv instalado exitosamente{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}No se encontró unzip para extraer moderncv{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}Error instalando moderncv: {e}{Style.RESET_ALL}")
        return False

def compile_latex_file(tex_file_path):
    """Compilar un archivo LaTeX y generar PDF"""
    tex_file = Path(tex_file_path)
    
    if not tex_file.exists():
        print(f"{Fore.RED}Error: El archivo {tex_file} no existe{Style.RESET_ALL}")
        return False
    
    if tex_file.suffix.lower() != '.tex':
        print(f"{Fore.RED}Error: El archivo debe tener extensión .tex{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.CYAN}Compilando {tex_file}...{Style.RESET_ALL}")
    
    try:
        # Cambiar al directorio del archivo LaTeX
        original_dir = Path.cwd()
        os.chdir(tex_file.parent)
        
        # Intentar compilar con latexmk primero (más robusto)
        if shutil.which('latexmk'):
            cmd = ['latexmk', '-pdf', '-interaction=nonstopmode', tex_file.name]
        else:
            cmd = ['pdflatex', '-interaction=nonstopmode', tex_file.name]
        
        print(f"{Fore.YELLOW}Ejecutando: {' '.join(cmd)}{Style.RESET_ALL}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # Volver al directorio original
        os.chdir(original_dir)
        
        if result.returncode == 0:
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists():
                print(f"{Fore.GREEN}✓ PDF generado exitosamente: {pdf_file}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}✗ No se pudo generar el PDF{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED}✗ Error durante la compilación{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Log de errores:{Style.RESET_ALL}")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}✗ Timeout durante la compilación{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error inesperado: {e}{Style.RESET_ALL}")
        return False

@click.command()
@click.argument('tex_file', type=click.Path(exists=True), required=False)
def main(tex_file):
    """Compilar archivo LaTeX a PDF"""
    print(f"{Fore.CYAN}=== Compilador de LaTeX a PDF ==={Style.RESET_ALL}")
    
    # Verificar instalación de LaTeX
    if not check_latex_installation():
        sys.exit(1)
    
    # Verificar paquete moderncv
    if not check_moderncv():
        print(f"{Fore.YELLOW}Advertencia: moderncv no está disponible{Style.RESET_ALL}")
    
    # Si no se especifica archivo, buscar en el directorio resume
    if not tex_file:
        resume_dir = Path("resume")
        if resume_dir.exists():
            tex_files = list(resume_dir.glob("*.tex"))
            if tex_files:
                tex_file = str(tex_files[0])
                print(f"{Fore.YELLOW}Usando archivo encontrado: {tex_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No se encontraron archivos .tex en el directorio resume{Style.RESET_ALL}")
                sys.exit(1)
        else:
            print(f"{Fore.RED}No se especificó archivo y no existe el directorio resume{Style.RESET_ALL}")
            sys.exit(1)
    
    # Compilar el archivo
    success = compile_latex_file(tex_file)
    
    if success:
        print(f"{Fore.GREEN}¡Compilación completada exitosamente!{Style.RESET_ALL}")
        sys.exit(0)
    else:
        print(f"{Fore.RED}La compilación falló{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
