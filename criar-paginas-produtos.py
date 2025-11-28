#!/usr/bin/env python3
"""Script para criar páginas HTML para todos os produtos existentes"""
import sys
from pathlib import Path

# Adiciona o diretório bot ao path
bot_dir = Path(__file__).parent / "bot"
sys.path.insert(0, str(bot_dir))

# Muda para o diretório bot para importar corretamente
import os
os.chdir(bot_dir)

from storage import store
from page_generator import generate_all_pages

def main():
    print("Gerando paginas para produtos existentes...")
    
    # Busca todos os produtos
    products = store.list_products()
    
    if not products:
        print("Nenhum produto encontrado!")
        return
    
    print(f"Encontrados {len(products)} produto(s)")
    
    # Pasta raiz do projeto
    project_root = Path(__file__).parent
    
    # Gera todas as páginas
    generated = generate_all_pages(products, project_root)
    
    print(f"\n{len(generated)} pagina(s) criada(s):")
    for page in generated:
        print(f"   - {page}")
    
    print(f"\nAcesse: http://localhost:3000/produto-{{id}}.html")

if __name__ == "__main__":
    main()

