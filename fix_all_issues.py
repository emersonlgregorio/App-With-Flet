#!/usr/bin/env python3
"""
Script para corrigir todos os métodos connect() e problemas de Container
"""

import os
import re
from pathlib import Path


def fix_connect_methods(file_path):
    """Remove chamadas para mydb.connect() que não existem mais"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remover linhas que contêm mydb.connect()
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Pular linhas que contêm mydb.connect()
            if 'mydb.connect()' in line:
                print(f"  Removendo: {line.strip()}")
                continue
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Se houve mudanças, salvar o arquivo
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Atualizado: {file_path}")
            return True
        else:
            print(f"⏭️  Sem mudanças: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao atualizar {file_path}: {e}")
        return False


def fix_container_build_methods(file_path):
    """Corrige classes Container removendo método build() desnecessário"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Verificar se o arquivo tem classes que herdam de Container e método build()
        if 'class ' in content and '(Container):' in content and 'def build(self):' in content:
            print(f"⚠️  Arquivo {file_path} precisa de correção manual de Container")
            return False
        
        return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar {file_path}: {e}")
        return False


def main():
    """Função principal"""
    print("🔄 Corrigindo métodos connect() em todos os arquivos...")
    print("=" * 60)
    
    # Buscar todos os arquivos Python que podem ter problemas
    python_files = []
    for file_path in Path('.').glob('*.py'):
        if file_path.name not in ['setup_dev.py', 'test_refactoring.py', 'update_usercontrol.py', 'init_db.py', 'fix_imports.py', 'add_control_name.py', 'replace_control.py', 'fix_container.py', 'fix_all_issues.py']:
            python_files.append(file_path)
    
    updated_count = 0
    
    for file_path in python_files:
        if fix_connect_methods(file_path):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {updated_count} arquivos atualizados")
    
    if updated_count > 0:
        print("🎉 Correção de métodos connect() concluída!")
        print("💡 Agora você pode executar: python main.py")
    else:
        print("ℹ️  Nenhum arquivo precisou ser atualizado")


if __name__ == "__main__":
    main()
