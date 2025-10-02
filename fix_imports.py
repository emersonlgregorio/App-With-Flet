#!/usr/bin/env python3
"""
Script para corrigir imports do Flet: icons -> Icons e colors -> Colors
"""

import os
import re
from pathlib import Path


def update_file(file_path):
    """Atualiza um arquivo corrigindo imports do Flet"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Substituir imports de icons para Icons
        content = re.sub(
            r'from flet import \([^)]*icons[^)]*\)',
            lambda m: m.group(0).replace('icons', 'Icons'),
            content
        )
        
        # Substituir imports de colors para Colors
        content = re.sub(
            r'from flet import \([^)]*colors[^)]*\)',
            lambda m: m.group(0).replace('colors', 'Colors'),
            content
        )
        
        # Substituir referências diretas
        content = content.replace('Icons.', 'Icons.')
        content = content.replace('Colors.', 'Colors.')
        
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
    print("🔄 Corrigindo imports do Flet (icons -> Icons, colors -> Colors)...")
    print("=" * 60)
    
    # Buscar todos os arquivos Python
    python_files = []
    for file_path in Path('.').glob('*.py'):
        if file_path.name not in ['setup_dev.py', 'test_refactoring.py', 'update_usercontrol.py', 'init_db.py']:
            python_files.append(file_path)
    
    updated_count = 0
    
    for file_path in python_files:
        if update_file(file_path):
            updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {updated_count} arquivos atualizados")
    
    if updated_count > 0:
        print("🎉 Correção concluída!")
        print("💡 Agora você pode executar: python main.py")
    else:
        print("ℹ️  Nenhum arquivo precisou ser atualizado")


if __name__ == "__main__":
    main()
