#!/usr/bin/env python3
"""
Script para substituir Control por Container nas classes customizadas
"""

import os
import re
from pathlib import Path


def replace_control_with_container(file_path):
    """Substitui Control por Container nas classes customizadas"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Substituir herança de Control por Container
        content = re.sub(
            r'class\s+(\w+)\(Control\):',
            r'class \1(Container):',
            content
        )
        
        # Substituir imports
        content = re.sub(
            r'from flet import \([^)]*Control[^)]*\)',
            lambda m: m.group(0).replace('Control', 'Container'),
            content
        )
        
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


def main():
    """Função principal"""
    print("🔄 Substituindo Control por Container nas classes customizadas...")
    print("=" * 60)
    
    # Buscar todos os arquivos Python que podem ter classes Control
    python_files = []
    for file_path in Path('.').glob('*.py'):
        if file_path.name not in ['setup_dev.py', 'test_refactoring.py', 'update_usercontrol.py', 'init_db.py', 'fix_imports.py', 'add_control_name.py', 'replace_control.py']:
            python_files.append(file_path)
    
    updated_count = 0
    
    for file_path in python_files:
        if replace_control_with_container(file_path):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {updated_count} arquivos atualizados")
    
    if updated_count > 0:
        print("🎉 Atualização concluída!")
        print("💡 Agora você pode executar: python main.py")
    else:
        print("ℹ️  Nenhum arquivo precisou ser atualizado")


if __name__ == "__main__":
    main()
