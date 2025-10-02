#!/usr/bin/env python3
"""
Script para corrigir rapidamente os métodos build() restantes
"""

import os
import re
from pathlib import Path


def fix_build_methods(file_path):
    """Corrige métodos build() em classes Container"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrões comuns para corrigir
        patterns = [
            # Padrão: return content
            (r'(\s+)return content\s*$', r'\1# Configurar o Container diretamente\n\1self.content = content'),
            # Padrão: return customers_content
            (r'(\s+)return (\w+_content)\s*$', r'\1# Configurar o Container diretamente\n\1self.content = \2'),
            # Padrão: return users_content
            (r'(\s+)return (\w+_content)\s*$', r'\1# Configurar o Container diretamente\n\1self.content = \2'),
            # Padrão: return products_content
            (r'(\s+)return (\w+_content)\s*$', r'\1# Configurar o Container diretamente\n\1self.content = \2'),
            # Padrão: return sales_content
            (r'(\s+)return (\w+_content)\s*$', r'\1# Configurar o Container diretamente\n\1self.content = \2'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
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
    print("🔄 Corrigindo métodos build() restantes...")
    print("=" * 60)
    
    # Arquivos principais que precisam de correção
    main_files = [
        'Users.py',
        'Products.py', 
        'Sales.py',
        'RegisterCustomer.py',
        'RegisterProducts.py',
        'RegisterSales.py',
        'CategoryBrand.py',
        'CreateFirstAdmin.py',
        'SelectCustomer.py',
        'SelectProduct.py'
    ]
    
    updated_count = 0
    
    for file_name in main_files:
        file_path = Path(file_name)
        if file_path.exists():
            if fix_build_methods(file_path):
                updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {updated_count} arquivos atualizados")
    
    if updated_count > 0:
        print("🎉 Correção de métodos build() concluída!")
        print("💡 Agora você pode executar: python main.py")
    else:
        print("ℹ️  Nenhum arquivo precisou ser atualizado")


if __name__ == "__main__":
    main()
