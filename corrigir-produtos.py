#!/usr/bin/env python3
"""Corrige os dados dos produtos no JSON"""
import json
from pathlib import Path

# Dados corretos dos produtos
produtos_corretos = {
    "vip-pro": {
        "product_id": "vip-pro",
        "title": "Telegram Vips Pro",
        "price": 497,
        "currency": "BRL",
        "description": "Todos os 37 canais secretos, traduções simultâneas e concierge dedicado.",
        "secret_link": "https://t.me/+vipproaccess",
        "media_type": "image",
        "media_src": "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?auto=format&fit=crop&w=900&q=80",
        "benefits": [
            "37 canais ativos",
            "Concierge 24/7",
            "Alertas prioritários"
        ],
        "note": "Liberação imediata",
        "lifetime_text": "Vitalício para 1 titular",
        "category": "Acesso total"
    },
    "signal-boost": {
        "product_id": "signal-boost",
        "title": "Signal Boost",
        "price": 297,
        "currency": "BRL",
        "description": "Sinais condensados com API e briefing multimídia.",
        "secret_link": "https://t.me/+signalboostvip",
        "media_type": "image",
        "media_src": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=900&q=80",
        "benefits": [
            "API pronta",
            "Até 10 canais",
            "Push instantâneo"
        ],
        "note": "Entrega 24/7",
        "lifetime_text": "Atualizações vitalícias",
        "category": "Operação rápida"
    },
    "consultoria": {
        "product_id": "consultoria",
        "title": "Consultoria 1:1",
        "price": 1997,
        "currency": "BRL",
        "description": "Plano estratégico completo com NDA e relatórios proprietários.",
        "secret_link": "https://t.me/+consultoriaelite",
        "media_type": "video",
        "media_src": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "media_poster": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=900&q=80",
        "benefits": [
            "Framework proprietário",
            "Suporte pós-sessão",
            "Agenda prioritária"
        ],
        "note": "Slots limitados",
        "lifetime_text": "Relatórios vitalícios",
        "category": "Mentoria fechada"
    },
    "produto": {
        "product_id": "produto",
        "title": "Produto",
        "price": 19.99,
        "currency": "BRL",
        "description": "descricao",
        "secret_link": "https://dasdad.sad7",
        "media_type": "image",
        "media_src": "https://api.telegram.org/file/bot8209184510:AAHOw4y0JAQNS5_v86e9CmzO872okkoO9eg/photos/file_0.jpg",
        "media_poster": None,
        "benefits": [],
        "note": "Liberação imediata",
        "lifetime_text": "Acesso vitalício incluído",
        "category": "Premium"
    },
    "dsasdad": {
        "product_id": "dsasdad",
        "title": "dsasdad",
        "price": 19.99,
        "currency": "BRL",
        "description": "dasdasd",
        "secret_link": "sasasda",
        "media_type": "image",
        "media_src": "https://api.telegram.org/file/bot8209184510:AAHOw4y0JAQNS5_v86e9CmzO872okkoO9eg/photos/file_0.jpg",
        "media_poster": None,
        "benefits": [],
        "note": "Liberação imediata",
        "lifetime_text": "Acesso vitalício incluído",
        "category": "Premium"
    }
}

def main():
    products_file = Path("bot/data/products.json")
    
    # Lê o JSON atual
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        try:
            with open(products_file, 'r', encoding='latin-1') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Erro ao ler: {e}")
            return
    
    # Corrige os produtos conhecidos
    for product_id, produto_correto in produtos_corretos.items():
        if product_id in data:
            # Mantém outros campos que possam existir
            data[product_id].update(produto_correto)
            print(f"Corrigido: {product_id}")
    
    # Salva com UTF-8
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nOK: {len(produtos_corretos)} produto(s) corrigido(s)!")

if __name__ == "__main__":
    main()

