"""Gera páginas HTML estáticas para produtos"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Dict

from config import settings
from storage import Product


def escape_html(text: str) -> str:
    """Escapa caracteres especiais para HTML"""
    if not text:
        return ""
    return html.escape(str(text))


def generate_product_page(product: Product, output_dir: Path) -> Path:
    """Gera uma página HTML estática para um produto"""
    
    # Define o nome do arquivo
    filename = f"produto-{product.product_id}.html"
    output_path = output_dir / filename
    
    # Template HTML
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{product.title} · Telegram Secrets</title>
    <meta name="description" content="{escape_html(product.description[:150])}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="./styles.css" />
    <script>
      // Comunicação totalmente via bot - sem API
      const TELEGRAM_BOT_USERNAME = "{escape_html(settings.telegram_bot_username)}";
    </script>
  </head>
  <body class="product-page">
    <header class="sub-header">
      <a class="sub-header__back" href="index.html#produtos">← Voltar para os produtos</a>
      <div class="logo">
        <div class="logo__badge">TS</div>
        <div class="logo__text">
          <span>Telegram Secrets</span>
          <small>VIPs</small>
        </div>
      </div>
    </header>

    <main>
      <section class="product-hero">
        <span class="product-hero__tag">{escape_html(product.category or "Premium")}</span>
        <h1>{escape_html(product.title)}</h1>
        <p class="product-hero__lead">{escape_html(product.description)}</p>
        <div class="product-hero__meta">
          <span>{format_price(product.price, product.currency)}</span>
          <span>{escape_html(product.lifetime_text or "Acesso vitalício incluído")}</span>
        </div>
      </section>

      <section class="product-details">
        <article>
          <h2>Detalhes do Produto</h2>
          {generate_media_html(product)}
          <p>{escape_html(product.description)}</p>
          {generate_benefits_html(product)}
        </article>
      </section>

      <section class="product-pix" id="pix-section">
        <div class="product-pix__header">
          <h2>💳 Pagamento via Pix</h2>
          <p class="badge badge--hot">Pagamento seguro e anônimo</p>
        </div>

        <div id="pix-generate" class="product-pix__generate">
          <button class="primary-cta" id="btn-generate-pix" type="button">
            Gerar Código Pix
          </button>
          <p class="product-pix__note">{escape_html(product.note or "Liberação imediata")}</p>
        </div>

        <div id="pix-loading" class="product-pix__loading" hidden>
          <span></span>
          <p>Gerando código Pix...</p>
        </div>

        <div id="pix-content" class="product-pix__content" hidden>
          <div class="product-pix__price">
            <strong id="pix-price"></strong>
            <small id="pix-lifetime"></small>
          </div>

          <label for="pix-code">Código Pix (copia e cola)</label>
          <textarea id="pix-code" readonly></textarea>

          <div class="product-pix__actions">
            <button type="button" class="primary-cta" id="btn-copy-pix">Copiar código</button>
            <button type="button" class="secondary-cta" id="btn-regenerate-pix">Gerar novamente</button>
          </div>

          <div class="product-pix__qr">
            <img id="pix-qr" alt="QR Code Pix" />
          </div>

          <div class="product-pix__status" id="pix-status">
            Aguardando pagamento Pix...
          </div>

          <div class="product-pix__link-waiting" id="pix-link-waiting">
            <p>🔒 Seu link aparecerá aqui quando o pagamento for concluído</p>
          </div>

          <div class="product-pix__secret" id="pix-secret" hidden>
            <p>✅ Pagamento confirmado! Acesso liberado:</p>
            <a id="secret-link" target="_blank" rel="noopener noreferrer" class="primary-cta">
              Abrir conteúdo premium
            </a>
          </div>
        </div>
      </section>
    </main>

    <script>
      const API_BASE_URL = window.__API_BASE_URL__ || "http://localhost:8080";
      const PRODUCT_ID = "{product.product_id}";
      const PRODUCT_DATA = {json.dumps({
        "product_id": product.product_id,
        "title": product.title,
        "price": product.price,
        "currency": product.currency,
        "description": product.description,
        "secret_link": product.secret_link,
        "lifetime_text": product.lifetime_text,
        "note": product.note,
      }, ensure_ascii=False)};

      const state = {{
        product: PRODUCT_DATA,
        paymentId: null,
        pollTimer: null,
      }};

      const pixLoading = document.getElementById("pix-loading");
      const pixGenerate = document.getElementById("pix-generate");
      const pixContent = document.getElementById("pix-content");
      const btnGeneratePix = document.getElementById("btn-generate-pix");
      const btnCopyPix = document.getElementById("btn-copy-pix");
      const btnRegeneratePix = document.getElementById("btn-regenerate-pix");
      const pixCodeField = document.getElementById("pix-code");
      const pixQr = document.getElementById("pix-qr");
      const pixStatus = document.getElementById("pix-status");
      const pixLinkWaiting = document.getElementById("pix-link-waiting");
      const pixSecret = document.getElementById("pix-secret");
      const secretLink = document.getElementById("secret-link");

      async function generatePix() {{
        console.log("=== INÍCIO generatePix() ===");
        console.log("PRODUCT_ID:", PRODUCT_ID);
        console.log("API_BASE_URL:", API_BASE_URL);
        
        // Verifica elementos
        console.log("Verificando elementos DOM:");
        console.log("  pixLoading:", pixLoading ? "OK" : "FALTANDO");
        console.log("  pixGenerate:", pixGenerate ? "OK" : "FALTANDO");
        console.log("  pixContent:", pixContent ? "OK" : "FALTANDO");
        console.log("  btnGeneratePix:", btnGeneratePix ? "OK" : "FALTANDO");
        console.log("  pixCodeField:", pixCodeField ? "OK" : "FALTANDO");
        console.log("  pixQr:", pixQr ? "OK" : "FALTANDO");
        console.log("  pixStatus:", pixStatus ? "OK" : "FALTANDO");
        
        if (!pixLoading || !pixGenerate || !pixContent) {{
          console.error("❌ ERRO: Elementos PIX não encontrados!");
          console.error("pixLoading:", pixLoading);
          console.error("pixGenerate:", pixGenerate);
          console.error("pixContent:", pixContent);
          return;
        }}
        
        console.log("✅ Todos os elementos encontrados. Iniciando geração...");
        
        // Mostra loading
        console.log("Mostrando loading...");
        pixLoading.removeAttribute("hidden");
        pixLoading.style.display = "block";
        console.log("  pixLoading.display:", pixLoading.style.display);
        
        // Esconde botão gerar
        console.log("Escondendo botão gerar...");
        pixGenerate.setAttribute("hidden", "");
        pixGenerate.style.display = "none";
        console.log("  pixGenerate.display:", pixGenerate.style.display);
        
        // Esconde conteúdo (será mostrado depois)
        console.log("Escondendo conteúdo inicialmente...");
        pixContent.setAttribute("hidden", "");
        pixContent.style.display = "none";
        console.log("  pixContent.display:", pixContent.style.display);
        
        if (pixStatus) {{
          pixStatus.textContent = "Gerando código Pix seguro...";
          console.log("Status atualizado para: Gerando código Pix seguro...");
        }}

        try {{
          const requestBody = {{
            product_id: PRODUCT_ID,
            customer_ref: crypto.randomUUID ? crypto.randomUUID() : `${{Date.now()}}-${{Math.random()}}`,
          }};
          
          console.log("📤 Enviando requisição para API:");
          console.log("  URL:", `${{API_BASE_URL}}/checkout`);
          console.log("  Body:", JSON.stringify(requestBody, null, 2));
          
          const response = await fetch(`${{API_BASE_URL}}/checkout`, {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify(requestBody),
          }});

          console.log("📥 Resposta recebida:");
          console.log("  Status:", response.status);
          console.log("  OK:", response.ok);
          console.log("  Headers:", Object.fromEntries(response.headers.entries()));

          if (!response.ok) {{
            const errorText = await response.text();
            console.error("❌ ERRO na resposta da API:");
            console.error("  Status:", response.status);
            console.error("  Erro:", errorText);
            throw new Error(errorText);
          }}

          const data = await response.json();
          console.log("✅ Dados recebidos da API:");
          console.log("  payment_id:", data.payment_id);
          console.log("  pix_code:", data.pix_code ? `${{data.pix_code.substring(0, 50)}}...` : "FALTANDO");
          console.log("  qr_base64:", data.qr_base64 ? `${{data.qr_base64.substring(0, 50)}}...` : "FALTANDO");
          console.log("  Dados completos:", JSON.stringify(data, null, 2));
          
          state.paymentId = data.payment_id;
          console.log("  state.paymentId definido:", state.paymentId);

          // Preenche código Pix
          console.log("📝 Preenchendo código Pix...");
          if (pixCodeField) {{
            pixCodeField.value = data.pix_code || "";
            console.log("  ✅ Código Pix preenchido:", data.pix_code ? `SIM (${{data.pix_code.length}} caracteres)` : "NÃO");
            console.log("  pixCodeField.value:", pixCodeField.value ? `${{pixCodeField.value.substring(0, 30)}}...` : "VAZIO");
          }} else {{
            console.error("  ❌ pixCodeField não encontrado!");
          }}
          
          // Preenche QR Code
          console.log("🖼️ Preenchendo QR Code...");
          if (data.qr_base64 && pixQr) {{
            console.log("  QR Code disponível, tamanho:", data.qr_base64.length, "caracteres");
            
            // Remove prefixo "data:image/png;base64," se já existir
            let base64Data = data.qr_base64;
            if (base64Data.startsWith("data:image")) {{
              // Já tem o prefixo, usa direto
              pixQr.src = base64Data;
            }} else {{
              // Adiciona o prefixo
              pixQr.src = `data:image/png;base64,${{base64Data}}`;
            }}
            
            pixQr.style.display = "block";
            pixQr.style.visibility = "visible";
            pixQr.style.width = "100%";
            pixQr.style.maxWidth = "250px";
            pixQr.style.height = "auto";
            pixQr.style.margin = "0 auto";
            
            console.log("  ✅ QR Code definido");
            console.log("  pixQr.src (primeiros 100 chars):", pixQr.src.substring(0, 100) + "...");
            console.log("  pixQr.style.display:", pixQr.style.display);
            console.log("  pixQr.style.visibility:", pixQr.style.visibility);
            console.log("  pixQr.offsetWidth:", pixQr.offsetWidth);
            console.log("  pixQr.offsetHeight:", pixQr.offsetHeight);
            
            // Força reload da imagem
            pixQr.onload = () => {{
              console.log("  ✅ QR Code imagem carregada com sucesso!");
            }};
            pixQr.onerror = (e) => {{
              console.error("  ❌ Erro ao carregar QR Code:", e);
            }};
          }} else {{
            console.warn("  ⚠️ QR Code não recebido da API");
            console.warn("    data.qr_base64:", data.qr_base64 ? `EXISTE (${{data.qr_base64.length}} chars)` : "FALTANDO");
            console.warn("    pixQr:", pixQr ? "EXISTE" : "FALTANDO");
            if (pixQr) {{
              pixQr.style.display = "none";
            }}
          }}
          
          // Preenche preço
          console.log("💰 Preenchendo preço...");
          const priceEl = document.getElementById("pix-price");
          if (priceEl) {{
            const formattedPrice = new Intl.NumberFormat("pt-BR", {{
              style: "currency",
              currency: PRODUCT_DATA.currency || "BRL",
            }}).format(PRODUCT_DATA.price);
            priceEl.textContent = formattedPrice;
            console.log("  ✅ Preço preenchido:", formattedPrice);
            console.log("  priceEl.textContent:", priceEl.textContent);
          }} else {{
            console.error("  ❌ Elemento pix-price não encontrado!");
          }}
          
          // Preenche lifetime
          console.log("⏰ Preenchendo lifetime...");
          const lifetimeEl = document.getElementById("pix-lifetime");
          if (lifetimeEl) {{
            lifetimeEl.textContent = PRODUCT_DATA.lifetime_text || "Acesso vitalício incluído";
            console.log("  ✅ Lifetime preenchido:", lifetimeEl.textContent);
          }} else {{
            console.error("  ❌ Elemento pix-lifetime não encontrado!");
          }}

          // Esconde loading e mostra conteúdo
          console.log("🎨 Atualizando visibilidade dos elementos...");
          
          if (pixLoading) {{
            pixLoading.setAttribute("hidden", "");
            pixLoading.style.display = "none";
            console.log("  ✅ Loading escondido");
          }} else {{
            console.error("  ❌ pixLoading não encontrado!");
          }}
          
          if (pixContent) {{
            console.log("  Mostrando pixContent...");
            console.log("    Antes - hasAttribute('hidden'):", pixContent.hasAttribute("hidden"));
            console.log("    Antes - style.display:", pixContent.style.display);
            console.log("    Antes - computed display:", window.getComputedStyle(pixContent).display);
            
            pixContent.removeAttribute("hidden");
            pixContent.style.display = "flex"; // Usa flex do CSS
            pixContent.style.visibility = "visible";
            pixContent.style.opacity = "1";
            
            console.log("    Depois - hasAttribute('hidden'):", pixContent.hasAttribute("hidden"));
            console.log("    Depois - style.display:", pixContent.style.display);
            console.log("    Depois - computed display:", window.getComputedStyle(pixContent).display);
            console.log("    Depois - style.visibility:", pixContent.style.visibility);
            console.log("    Depois - style.opacity:", pixContent.style.opacity);
            console.log("  ✅ pixContent mostrado");
          }} else {{
            console.error("  ❌ pixContent não encontrado!");
          }}
          
          if (pixStatus) {{
            pixStatus.textContent = "Aguardando pagamento Pix...";
            console.log("  ✅ Status atualizado");
          }} else {{
            console.error("  ❌ pixStatus não encontrado!");
          }}
          
          if (pixLinkWaiting) {{
            pixLinkWaiting.style.display = "block";
            pixLinkWaiting.style.visibility = "visible";
            console.log("  ✅ Link waiting mostrado");
          }} else {{
            console.warn("  ⚠️ pixLinkWaiting não encontrado!");
          }}
          
          if (pixSecret) {{
            pixSecret.setAttribute("hidden", "");
            pixSecret.style.display = "none";
            console.log("  ✅ Secret escondido");
          }} else {{
            console.warn("  ⚠️ pixSecret não encontrado!");
          }}
          
          console.log("=== RESUMO FINAL ===");
          console.log("✅ PIX gerado com sucesso!");
          console.log("Dados:", data);
          console.log("Estado do pixContent:", {{
            elemento: pixContent ? "EXISTE" : "FALTANDO",
            hasHidden: pixContent ? pixContent.hasAttribute("hidden") : "N/A",
            styleDisplay: pixContent ? pixContent.style.display : "N/A",
            computedDisplay: pixContent ? window.getComputedStyle(pixContent).display : "N/A",
            offsetHeight: pixContent ? pixContent.offsetHeight : "N/A",
            offsetWidth: pixContent ? pixContent.offsetWidth : "N/A"
          }});
          console.log("Elementos preenchidos:", {{
            pixCodeField: pixCodeField && pixCodeField.value ? "SIM" : "NÃO",
            pixQr: pixQr && pixQr.src ? "SIM" : "NÃO",
            priceEl: document.getElementById("pix-price")?.textContent ? "SIM" : "NÃO",
            lifetimeEl: document.getElementById("pix-lifetime")?.textContent ? "SIM" : "NÃO"
          }});
          console.log("=== FIM generatePix() ===");

          startPolling();
        }} catch (error) {{
          console.error("=== ERRO ao gerar Pix ===");
          console.error("Erro:", error);
          console.error("Mensagem:", error.message);
          console.error("Stack:", error.stack);
          console.error("========================");
          
          if (pixLoading) {{
            pixLoading.setAttribute("hidden", "");
            pixLoading.style.display = "none";
            console.log("Loading escondido após erro");
          }}
          if (pixGenerate) {{
            pixGenerate.removeAttribute("hidden");
            pixGenerate.style.display = "block";
            console.log("Botão gerar mostrado após erro");
          }}
          if (pixStatus) {{
            pixStatus.textContent = "Erro ao gerar Pix. Tente novamente.";
            console.log("Status atualizado com erro");
          }}
        }}
      }}

      function pollPayment() {{
        if (!state.paymentId) return;
        fetch(`${{API_BASE_URL}}/payments/${{state.paymentId}}`)
          .then(res => res.json())
          .then(data => {{
            if (data.status === "paid") {{
              if (pixStatus) pixStatus.textContent = "✅ Pagamento confirmado! Acesso liberado!";
              if (pixLinkWaiting) pixLinkWaiting.style.display = "none";
              if (data.secret_link && secretLink) {{
                secretLink.href = data.secret_link;
                secretLink.textContent = "Abrir conteúdo premium";
                if (pixSecret) {{
                  pixSecret.removeAttribute("hidden");
                  pixSecret.style.display = "block";
                }}
              }}
              if (state.pollTimer) {{
                clearInterval(state.pollTimer);
                state.pollTimer = null;
              }}
            }}
          }})
          .catch(() => {{}});
      }}

      function startPolling() {{
        if (state.pollTimer) clearInterval(state.pollTimer);
        state.pollTimer = setInterval(pollPayment, 4000);
      }}

      // Garante que o DOM está carregado
      if (document.readyState === "loading") {{
        document.addEventListener("DOMContentLoaded", initPix);
      }} else {{
        initPix();
      }}
      
      function initPix() {{
        console.log("=== INICIALIZANDO PIX ===");
        console.log("PRODUCT_ID:", PRODUCT_ID);
        console.log("PRODUCT_DATA:", PRODUCT_DATA);
        console.log("API_BASE_URL:", API_BASE_URL);
        
        console.log("Verificando elementos DOM:");
        console.log("  btnGeneratePix:", btnGeneratePix);
        console.log("  pixContent:", pixContent);
        console.log("  pixLoading:", pixLoading);
        console.log("  pixGenerate:", pixGenerate);
        console.log("  pixCodeField:", pixCodeField);
        console.log("  pixQr:", pixQr);
        console.log("  pixStatus:", pixStatus);
        
        if (btnGeneratePix) {{
          btnGeneratePix.addEventListener("click", (e) => {{
            console.log("🖱️ CLIQUE NO BOTÃO GERAR PIX DETECTADO!");
            console.log("Event:", e);
            generatePix();
          }});
          console.log("✅ Evento de click anexado ao botão Gerar Pix");
        }} else {{
          console.error("❌ Botão Gerar Pix não encontrado!");
          console.error("Tentando encontrar manualmente...");
          const manualBtn = document.getElementById("btn-generate-pix");
          console.error("  document.getElementById('btn-generate-pix'):", manualBtn);
        }}
        
        if (btnRegeneratePix) {{
          btnRegeneratePix.addEventListener("click", generatePix);
        }}
        
        if (btnCopyPix) {{
          btnCopyPix.addEventListener("click", async () => {{
            if (!pixCodeField || !pixCodeField.value) return;
            try {{
              await navigator.clipboard.writeText(pixCodeField.value);
              if (pixStatus) pixStatus.textContent = "Código copiado! Finalize o pagamento no app do banco.";
            }} catch (error) {{
              pixCodeField.select();
              if (pixStatus) pixStatus.textContent = "Copie manualmente usando CTRL+C";
            }}
          }});
        }}
      }}
    </script>
  </body>
</html>"""
    
    # Escreve o arquivo com encoding UTF-8 e BOM para garantir compatibilidade
    output_path.write_text(html_template, encoding="utf-8-sig")
    return output_path


def format_price(price: float, currency: str = "BRL") -> str:
    """Formata o preço"""
    return f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_media_html(product: Product) -> str:
    """Gera HTML para mídia do produto"""
    if product.media_type == "video" and product.media_src:
        poster = f' poster="{product.media_poster}"' if product.media_poster else ""
        return f'<video class="product-media" src="{product.media_src}"{poster} controls></video>'
    elif product.media_src:
        return f'<img class="product-media" src="{product.media_src}" alt="{escape_html(product.title)}" />'
    return ""


def generate_benefits_html(product: Product) -> str:
    """Gera HTML para benefícios"""
    if product.benefits and len(product.benefits) > 0:
        benefits_list = "".join([f"<li>{escape_html(benefit)}</li>" for benefit in product.benefits])
        return f"""
          <div>
            <h3>Benefícios incluídos:</h3>
            <ul class="feature-list">
              {benefits_list}
            </ul>
          </div>
        """
    return ""


def generate_all_pages(products: list[Product], output_dir: Path):
    """Gera páginas para todos os produtos"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated = []
    for product in products:
        try:
            page_path = generate_product_page(product, output_dir)
            generated.append(page_path.name)
        except Exception as e:
            print(f"Erro ao gerar página para {product.product_id}: {e}")
    
    return generated

