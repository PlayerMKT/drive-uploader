#!/usr/bin/env python3
"""
Interface interativa para seleção de arquivos requirements.txt
Simula a interface mostrada na imagem do usuário
"""

import os
import glob
import subprocess
import sys

class RequirementsSelector:
    def __init__(self):
        self.requirements_files = []
        self.selected_files = []
        
    def find_requirements_files(self):
        """Encontra todos os arquivos requirements.txt no projeto"""
        print("🔍 Procurando arquivos requirements.txt...")
        
        # Padrões de busca
        patterns = [
            "requirements*.txt",
            "*/requirements*.txt", 
            "*/*/requirements*.txt",
            "*/*/*/requirements*.txt"
        ]
        
        all_files = set()
        
        for pattern in patterns:
            files = glob.glob(pattern, recursive=True)
            all_files.update(files)
        
        # Filtrar apenas arquivos que existem e não estão vazios
        self.requirements_files = []
        for file in sorted(all_files):
            if os.path.exists(file) and os.path.getsize(file) > 0:
                self.requirements_files.append(file)
        
        print(f"📋 Encontrados {len(self.requirements_files)} arquivos requirements.txt")
        return self.requirements_files
    
    def display_selection_interface(self):
        """Exibe interface de seleção similar à imagem"""
        print("\n" + "="*60)
        print("🎯 SELETOR DE DEPENDÊNCIAS PARA INSTALAÇÃO")
        print("="*60)
        print("Selecione as dependências a serem instaladas:")
        print()
        
        for i, req_file in enumerate(self.requirements_files, 1):
            # Mostrar tamanho e número de pacotes
            try:
                with open(req_file, 'r') as f:
                    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    package_count = len(lines)
            except:
                package_count = 0
            
            status = "✅" if req_file in self.selected_files else "☐"
            print(f"{status} [{i}] {req_file} ({package_count} pacotes)")
        
        print(f"\n📊 Total selecionado: {len(self.selected_files)} arquivos")
        
    def interactive_selection(self):
        """Interface interativa para seleção"""
        self.find_requirements_files()
        
        if not self.requirements_files:
            print("❌ Nenhum arquivo requirements.txt encontrado!")
            return
        
        while True:
            self.display_selection_interface()
            
            print("\n" + "-"*60)
            print("Opções:")
            print("1-{}: Alternar seleção do arquivo".format(len(self.requirements_files)))
            print("A: Selecionar todos")
            print("N: Deselecionar todos") 
            print("I: Instalar selecionados")
            print("V: Visualizar conteúdo")
            print("Q: Sair")
            print("-"*60)
            
            choice = input("Escolha uma opção: ").strip().upper()
            
            if choice == 'Q':
                print("👋 Saindo...")
                break
            elif choice == 'A':
                self.selected_files = self.requirements_files.copy()
                print("✅ Todos os arquivos selecionados!")
            elif choice == 'N':
                self.selected_files = []
                print("❌ Todos os arquivos desmarcados!")
            elif choice == 'I':
                self.install_selected()
            elif choice == 'V':
                self.view_contents()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.requirements_files):
                    file = self.requirements_files[idx]
                    if file in self.selected_files:
                        self.selected_files.remove(file)
                        print(f"❌ Desmarcado: {file}")
                    else:
                        self.selected_files.append(file)
                        print(f"✅ Marcado: {file}")
                else:
                    print("❌ Número inválido!")
            else:
                print("❌ Opção inválida!")
            
            input("\nPressione Enter para continuar...")
    
    def view_contents(self):
        """Visualiza o conteúdo dos arquivos selecionados"""
        if not self.selected_files:
            print("❌ Nenhum arquivo selecionado!")
            return
        
        print("\n" + "="*60)
        print("📖 CONTEÚDO DOS ARQUIVOS SELECIONADOS")
        print("="*60)
        
        for req_file in self.selected_files:
            print(f"\n📄 {req_file}")
            print("-" * len(req_file))
            try:
                with open(req_file, 'r') as f:
                    content = f.read()
                    if content.strip():
                        print(content)
                    else:
                        print("(arquivo vazio)")
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}")
    
    def install_selected(self):
        """Instala os arquivos selecionados"""
        if not self.selected_files:
            print("❌ Nenhum arquivo selecionado para instalação!")
            return
        
        print("\n" + "="*60)
        print("🚀 INSTALANDO DEPENDÊNCIAS SELECIONADAS")
        print("="*60)
        
        for req_file in self.selected_files:
            print(f"\n📦 Instalando: {req_file}")
            print("-" * (len(req_file) + 13))
            
            try:
                # Instalar usando pip
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", req_file
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Sucesso: {req_file}")
                    if result.stdout:
                        print("📋 Saída:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
                else:
                    print(f"❌ Falha: {req_file}")
                    print("🔍 Erro:", result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr)
                    
            except Exception as e:
                print(f"❌ Erro ao instalar {req_file}: {e}")
        
        print("\n✅ Processo de instalação concluído!")
        
        # Mostrar pacotes instalados
        print("\n📋 Verificando pacotes instalados:")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                print(f"Total de pacotes instalados: {len(lines)-2}")  # -2 para cabeçalho
            else:
                print("❌ Erro ao verificar pacotes")
        except:
            print("❌ Erro ao verificar pacotes")

def main():
    """Função principal"""
    print("🎯 INTERFACE INTERATIVA DE REQUIREMENTS")
    print("Baseada na imagem enviada pelo usuário")
    print("="*60)
    
    selector = RequirementsSelector()
    
    # Verificar se pip está disponível
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
    except:
        print("❌ pip não está disponível!")
        print("Instale o pip primeiro: sudo apt-get install python3-pip")
        return
    
    selector.interactive_selection()

if __name__ == "__main__":
    main()
