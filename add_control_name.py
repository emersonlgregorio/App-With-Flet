#!/usr/bin/env python3
"""
Script para adicionar método _get_control_name() em todas as classes Control
"""

import os
import re
from pathlib import Path


def add_get_control_name_method(file_path):
    """Adiciona o método _get_control_name() em classes Control"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Encontrar todas as classes que herdam de Control
        pattern = r'class\s+(\w+)\(Control\):'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            class_name = match.group(1)
            
            # Verificar se o método já existe
            method_pattern = rf'def\s+_get_control_name\(self\):'
            if not re.search(method_pattern, content):
                # Encontrar o final da definição da classe __init__
                init_pattern = rf'class\s+{class_name}\(Control\):.*?def\s+__init__\(self[^)]*\):.*?super\(\)\.__init__\(\)'
                init_match = re.search(init_pattern, content, re.DOTALL)
                
                if init_match:
                    # Encontrar o final do método __init__
                    init_end = init_match.end()
                    # Procurar pela próxima linha que não seja indentada ou seja uma nova definição de método
                    lines = content[init_end:].split('\n')
                    insert_pos = init_end
                    
                    for i, line in enumerate(lines):
                        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                            insert_pos = init_end + len('\n'.join(lines[:i]))
                            break
                    
                    # Inserir o método _get_control_name
                    method_code = f"""
    def _get_control_name(self):
        return '{class_name.lower()}'"""
                    
                    content = content[:insert_pos] + method_code + content[insert_pos:]
        
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
    print("🔄 Adicionando método _get_control_name() em classes Control...")
    print("=" * 60)
    
    # Buscar todos os arquivos Python que podem ter classes Control
    python_files = []
    for file_path in Path('.').glob('*.py'):
        if file_path.name not in ['setup_dev.py', 'test_refactoring.py', 'update_usercontrol.py', 'init_db.py', 'fix_imports.py', 'add_control_name.py']:
            python_files.append(file_path)
    
    updated_count = 0
    
    for file_path in python_files:
        if add_get_control_name_method(file_path):
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
