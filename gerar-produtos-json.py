#!/usr/bin/env python3
"""Gera arquivo JSON estático com produtos para GitHub Pages"""
import json
import sys
from pathlib import Path

# Adiciona o diretório bot ao path
sys.path.insert(0, str(Path(__file__).parent / "bot"))

from storage import store

def main():
    output_file = Path("products.json")
    
    products = store.list_products()
    
    # Converte produtos para formato JSON simples
    products_data = []
    for product in products:
        products_data.append({
            "product_id": product.product_id,
            "title": product.title,
            "price": product.price,
            "currency": product.currency,
            "description": product.description,
            "media_type": product.media_type,
            "media_src": product.media_src,
            "media_poster": product.media_poster,
            "benefits": product.benefits,
            "note": product.note,
            "lifetime_text": product.lifetime_text,
            "category": product.category,
        })
    
    # Escreve o arquivo JSON
    output_file.write_text(
        json.dumps(products_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    print(f"[OK] Arquivo products.json gerado com {len(products_data)} produto(s)")
    print(f"     Salvo em: {output_file.absolute()}")

if __name__ == "__main__":
    main()

