#!/usr/bin/env python3
"""
Consolidador de arquivos requirements.txt
"""
import os
import glob

def consolidate_requirements():
    """Consolida todos os arquivos requirements encontrados"""
    print("🔍 Consolidando arquivos requirements...")
    
    # Encontrar todos os arquivos requirements
    req_files = glob.glob('.codespace-config/requirements_*.txt')
    req_files.extend(glob.glob('requirements*.txt'))
    
    all_packages = set()
    
    for req_file in req_files:
        if os.path.exists(req_file):
            print(f"📄 Processando: {req_file}")
            try:
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            all_packages.add(line)
            except Exception as e:
                print(f"⚠️ Erro ao processar {req_file}: {e}")
    
    # Criar arquivo consolidado
    consolidated_file = '.codespace-config/requirements-consolidated.txt'
    with open(consolidated_file, 'w') as f:
        f.write("# Arquivo consolidado de requirements\n")
        f.write("# Gerado automaticamente\n\n")
        
        for package in sorted(all_packages):
            f.write(f"{package}\n")
    
    print(f"✅ Arquivo consolidado criado: {consolidated_file}")
    print(f"📊 Total de pacotes únicos: {len(all_packages)}")
    
    return consolidated_file

if __name__ == "__main__":
    consolidate_requirements()
