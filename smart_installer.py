#!/usr/bin/env python3
"""
Instalador Inteligente de Dependências
Instala dependências Python uma por uma com tratamento de erros
"""

import os
import subprocess
import sys
from pathlib import Path

def install_package(package_line):
    """Instala um pacote individual"""
    package_name = package_line.strip()
    
    if not package_name or package_name.startswith('#'):
        return True
    
    print(f"📦 Instalando: {package_name}")
    
    try:
        cmd = [sys.executable, '-m', 'pip', 'install', package_name]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} instalado com sucesso!")
            return True
        else:
            print(f"❌ Falha ao instalar {package_name}")
            print(f"Erro: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout ao instalar {package_name}")
        return False
    except Exception as e:
        print(f"❌ Erro ao instalar {package_name}: {e}")
        return False

def install_from_consolidated():
    """Instala do arquivo consolidado"""
    consolidated_file = '.codespace-config/requirements-consolidated.txt'
    
    if not os.path.exists(consolidated_file):
        print(f"❌ Arquivo não encontrado: {consolidated_file}")
        return False
    
    print(f"📋 Instalando dependências de {consolidated_file}")
    
    with open(consolidated_file, 'r') as f:
        packages = f.readlines()
    
    successful = 0
    failed = 0
    
    for package_line in packages:
        if install_package(package_line):
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 Resultado: {successful} sucessos, {failed} falhas")
    return failed == 0

def install_essentials():
    """Instala pacotes essenciais primeiro"""
    essentials = [
        'setuptools',
        'wheel',
        'pip --upgrade',
        'requests',
        'python-dotenv',
        'tqdm'
    ]
    
    print("🔧 Instalando pacotes essenciais...")
    
    for package in essentials:
        install_package(package)

def main():
    """Função principal"""
    print("🚀 Instalador Inteligente de Dependências")
    print("=" * 50)
    
    # Primeiro instalar essenciais
    install_essentials()
    
    print("\n" + "=" * 50)
    
    # Instalar do arquivo consolidado
    success = install_from_consolidated()
    
    if success:
        print("🎉 Todas as dependências foram instaladas com sucesso!")
    else:
        print("⚠️ Algumas dependências falharam. Verifique os logs acima.")
    
    # Mostrar pacotes instalados
    print("\n🔍 Verificando instalação...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print(f"📊 Total de pacotes instalados: {len(lines) - 2}")  # -2 for header
        else:
            print("❌ Não foi possível verificar pacotes instalados")
    except Exception as e:
        print(f"❌ Erro ao verificar instalação: {e}")

if __name__ == "__main__":
    main()
