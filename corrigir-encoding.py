#!/usr/bin/env python3
"""Corrige o encoding do arquivo products.json"""
import json
from pathlib import Path

def main():
    # Tenta diferentes caminhos possíveis
    possible_paths = [
        Path("bot/data/products.json"),
        Path("bot/products.json"),
    ]
    
    products_file = None
    for path in possible_paths:
        if path.exists():
            products_file = path
            break
    
    if not products_file:
        print("Erro: products.json não encontrado em nenhum dos caminhos:")
        for p in possible_paths:
            print(f"  - {p}")
        return
    
    # Tenta ler com diferentes encodings
    content = None
    for encoding in ["latin-1", "cp1252", "utf-8"]:
        try:
            content = products_file.read_text(encoding=encoding)
            print(f"Lido com encoding: {encoding}")
            break
        except:
            continue
    
    if not content:
        print("Erro: não foi possível ler o arquivo")
        return
    
    # Parse JSON
    try:
        data = json.loads(content)
    except Exception as e:
        print(f"Erro ao parsear JSON: {e}")
        return
    
    # Reescreve com UTF-8
    products_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    print("OK: Arquivo products.json corrigido com encoding UTF-8!")
    print(f"   {len(data)} produto(s) processado(s)")

if __name__ == "__main__":
    main()

