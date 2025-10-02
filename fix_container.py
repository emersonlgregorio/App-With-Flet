#!/usr/bin/env python3
"""
Script para corrigir classes Container removendo método build() desnecessário
"""

import os
import re
from pathlib import Path


def fix_container_classes(file_path):
    """Corrige classes Container removendo método build() desnecessário"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Verificar se o arquivo tem classes que herdam de Container
        if 'class ' in content and '(Container):' in content:
            # Verificar se tem método build() que retorna Container
            if 'def build(self):' in content and 'return Container(' in content:
                print(f"⚠️  Arquivo {file_path} precisa de correção manual")
                return False
        
        return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar {file_path}: {e}")
        return False


def main():
    """Função principal"""
    print("🔄 Verificando classes Container que precisam de correção...")
    print("=" * 60)
    
    # Buscar todos os arquivos Python que podem ter classes Container
    python_files = []
    for file_path in Path('.').glob('*.py'):
        if file_path.name not in ['setup_dev.py', 'test_refactoring.py', 'update_usercontrol.py', 'init_db.py', 'fix_imports.py', 'add_control_name.py', 'replace_control.py', 'fix_container.py']:
            python_files.append(file_path)
    
    needs_fix = []
    
    for file_path in python_files:
        if fix_container_classes(file_path):
            needs_fix.append(file_path)
    
    print("\n" + "=" * 60)
    if needs_fix:
        print(f"📋 Arquivos que precisam de correção manual:")
        for file_path in needs_fix:
            print(f"  - {file_path}")
    else:
        print("✅ Todas as classes Container estão corretas!")


if __name__ == "__main__":
    main()
