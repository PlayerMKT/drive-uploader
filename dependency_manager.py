#!/usr/bin/env python3
"""
Gerenciador de Dependências Python
Analisa e instala dependências de múltiplos arquivos requirements.txt
"""

import os
import subprocess
import sys
import glob
from pathlib import Path

def find_requirements_files():
    """Encontra todos os arquivos requirements.txt no projeto"""
    print("🔍 Procurando arquivos requirements.txt...")
    
    req_files = []
    
    # Padrões para buscar
    patterns = [
        'requirements*.txt',
        '**/requirements*.txt',
        '.codespace-config/requirements_*.txt'
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        req_files.extend(files)
    
    # Remover duplicatas e ordenar
    req_files = sorted(list(set(req_files)))
    
    print(f"📄 Encontrados {len(req_files)} arquivos:")
    for f in req_files:
        size = os.path.getsize(f) if os.path.exists(f) else 0
        print(f"  - {f} ({size} bytes)")
    
    return req_files

def analyze_requirements_file(filepath):
    """Analisa um arquivo requirements.txt"""
    packages = []
    
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    packages.append({
                        'line': line,
                        'file': filepath,
                        'line_num': line_num
                    })
    except Exception as e:
        print(f"⚠️ Erro ao ler {filepath}: {e}")
    
    return packages

def consolidate_all_requirements():
    """Consolida todos os requirements encontrados"""
    print("\n🔄 Consolidando requirements...")
    
    req_files = find_requirements_files()
    all_packages = {}
    
    for req_file in req_files:
        if os.path.exists(req_file):
            packages = analyze_requirements_file(req_file)
            print(f"📦 {req_file}: {len(packages)} pacotes")
            
            for pkg in packages:
                pkg_name = pkg['line'].split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                all_packages[pkg_name] = pkg['line']
    
    # Criar arquivo consolidado
    consolidated_file = '.codespace-config/requirements-consolidated.txt'
    os.makedirs('.codespace-config', exist_ok=True)
    
    with open(consolidated_file, 'w') as f:
        f.write("# Arquivo consolidado de requirements\n")
        f.write("# Gerado automaticamente pelo dependency_manager.py\n")
        f.write(f"# Total de pacotes únicos: {len(all_packages)}\n\n")
        
        for pkg_name in sorted(all_packages.keys()):
            f.write(f"{all_packages[pkg_name]}\n")
    
    print(f"✅ Arquivo consolidado criado: {consolidated_file}")
    print(f"📊 Total de pacotes únicos: {len(all_packages)}")
    
    return consolidated_file, all_packages

def install_requirements(req_file):
    """Instala requirements de um arquivo"""
    print(f"\n📦 Instalando dependências de {req_file}...")
    
    try:
        cmd = [sys.executable, '-m', 'pip', 'install', '-r', req_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Instalação de {req_file} concluída!")
            return True
        else:
            print(f"❌ Erro na instalação de {req_file}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao executar instalação: {e}")
        return False

def check_installed_packages():
    """Verifica quais pacotes estão instalados"""
    print("\n🔍 Verificando pacotes instalados...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=freeze'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            installed = result.stdout.strip().split('\n')
            print(f"📊 Total de pacotes instalados: {len(installed)}")
            return installed
        else:
            print("❌ Erro ao verificar pacotes instalados")
            return []
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def main():
    """Função principal"""
    print("🐍 Gerenciador de Dependências Python")
    print("=" * 50)
    
    # 1. Encontrar e consolidar requirements
    consolidated_file, all_packages = consolidate_all_requirements()
    
    # 2. Mostrar opções
    print("\n" + "=" * 50)
    print("Opções disponíveis:")
    print("1. Instalar arquivo consolidado")
    print("2. Instalar arquivos individuais")
    print("3. Verificar pacotes instalados")
    print("4. Sair")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    if choice == '1':
        if os.path.exists(consolidated_file):
            install_requirements(consolidated_file)
        else:
            print("❌ Arquivo consolidado não encontrado")
    
    elif choice == '2':
        req_files = find_requirements_files()
        for req_file in req_files:
            if os.path.exists(req_file):
                install_requirements(req_file)
    
    elif choice == '3':
        check_installed_packages()
    
    elif choice == '4':
        print("👋 Saindo...")
        return
    
    else:
        print("❌ Opção inválida")
    
    # Verificação final
    print("\n" + "=" * 50)
    print("📋 RESUMO FINAL:")
    print(f"Arquivo consolidado: {consolidated_file}")
    print(f"Pacotes únicos encontrados: {len(all_packages)}")
    
    if os.path.exists(consolidated_file):
        print(f"Tamanho do arquivo consolidado: {os.path.getsize(consolidated_file)} bytes")
    
    print("\n💡 Para instalar tudo automaticamente:")
    print(f"pip install -r {consolidated_file}")

if __name__ == "__main__":
    main()
