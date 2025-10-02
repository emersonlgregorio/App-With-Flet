#!/usr/bin/env python3
"""
Script para atualizar UserControl para Control na nova versão do Flet
"""

import os
import re
from pathlib import Path


def update_file(file_path):
    """Atualiza um arquivo substituindo UserControl por Control"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir UserControl por Control
        updated_content = content.replace('UserControl', 'Control')
        
        # Substituir imports
        updated_content = re.sub(
            r'from flet import \([^)]*UserControl[^)]*\)',
            lambda m: m.group(0).replace('UserControl', 'Control'),
            updated_content
        )
        
        # Se houve mudanças, salvar o arquivo
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
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
    print("🔄 Atualizando UserControl para Control...")
    print("=" * 50)
    
    # Lista de arquivos que usam UserControl
    files_to_update = [
        'Login.py',
        'draft.py', 
        'Users.py',
        'SideMenu.py',
        'Sales.py',
        'RegisterSales.py',
        'RegisterProducts.py',
        'RegisterCustomer.py',
        'Products.py',
        'Notification.py',
        'Home.py',
        'Customers.py',
        'Appbar.py'
    ]
    
    updated_count = 0
    
    for file_name in files_to_update:
        file_path = Path(file_name)
        if file_path.exists():
            if update_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {file_name}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {updated_count} arquivos atualizados")
    
    if updated_count > 0:
        print("🎉 Atualização concluída!")
        print("💡 Agora você pode executar: python main.py")
    else:
        print("ℹ️  Nenhum arquivo precisou ser atualizado")


if __name__ == "__main__":
    main()
