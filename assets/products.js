const API_BASE_URL = window.__API_BASE_URL__ || "http://localhost:8080";

const state = {
  products: [],
  rendered: 0,
  batch: 6,
  isRendering: false,
  currentPaymentId: null,
  currentProduct: null,
  pollTimer: null,
};

const randomId = () => {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
};

const grid = document.getElementById("product-grid");
const template = document.getElementById("product-card-template");
const loadingIndicator = document.querySelector("[data-loading]");

const checkoutModal = document.querySelector("[data-checkout]");
const checkoutTitle = checkoutModal?.querySelector("[data-checkout-title]");
const checkoutNote = checkoutModal?.querySelector("[data-checkout-note]");
const checkoutPrice = checkoutModal?.querySelector("[data-checkout-price]");
const checkoutLifetime = checkoutModal?.querySelector("[data-checkout-lifetime]");
const checkoutLoading = checkoutModal?.querySelector("[data-checkout-loading]");
const checkoutContent = checkoutModal?.querySelector("[data-checkout-content]");
const pixCodeField = checkoutModal?.querySelector("[data-pix-code]");
const pixQr = checkoutModal?.querySelector("[data-pix-qr]");
const statusLabel = checkoutModal?.querySelector("[data-payment-status]");
const secretWrap = checkoutModal?.querySelector("[data-secret]");
const secretLink = checkoutModal?.querySelector("[data-secret-link]");

const createMediaElement = (product) => {
  if (product.media_type === "video" && product.media_src) {
    const video = document.createElement("video");
    video.src = product.media_src;
    video.poster = product.media_poster || "";
    video.muted = true;
    video.loop = true;
    video.autoplay = true;
    video.playsInline = true;
    video.className = "product-card__video";
    video.setAttribute("aria-label", product.title);
    return video;
  }

  const img = document.createElement("img");
  img.src = product.media_src || "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=900&q=80";
  img.alt = product.title;
  img.loading = "lazy";
  img.className = "product-card__media";
  return img;
};

const buildBenefits = (listEl, benefits) => {
  listEl.innerHTML = "";
  (benefits || []).forEach((benefit) => {
    const item = document.createElement("li");
    item.textContent = benefit;
    listEl.appendChild(item);
  });
};

// Botão "Ver mais" agora navega para produto.html (implementado no renderBatch)

const renderBatch = (count = state.batch) => {
  if (!grid || !template || state.isRendering || !state.products.length) return;
  state.isRendering = true;
  loadingIndicator?.removeAttribute("hidden");

  window.setTimeout(() => {
    for (let i = 0; i < count; i += 1) {
      const product = state.products[state.rendered % state.products.length];
      const node = template.content.cloneNode(true);

      const mediaWrap = node.querySelector("[data-media]");
      mediaWrap?.replaceChildren(createMediaElement(product));

      node.querySelector("[data-category]").textContent = product.category || "Premium";
      const titleLink = node.querySelector("[data-product-title]");
      titleLink.textContent = product.title;
      titleLink.href = "#";
      node.querySelector("[data-description]").textContent = product.description;
      node.querySelector("[data-lifetime]").textContent = product.lifetime_text || "Acesso vitalício incluído";
      node.querySelector("[data-price]").textContent = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: product.currency || "BRL",
      }).format(product.price);

      buildBenefits(node.querySelector("[data-benefits]"), product.benefits);
      node.querySelector("[data-note]").textContent = product.note || "Liberação imediata";

      const cta = node.querySelector("[data-cta]");
      cta.textContent = "Ver mais";
      cta.dataset.productId = product.product_id;
      // Navega para a página estática do produto (ou dinâmica como fallback)
      cta.addEventListener("click", () => {
        // Tenta página estática primeiro, depois dinâmica
        const staticPage = `produto-${product.product_id}.html`;
        // Usa página estática se existir, senão usa dinâmica
        window.location.href = staticPage;
      });

      grid.appendChild(node);
      state.rendered += 1;
    }

    loadingIndicator?.setAttribute("hidden", "");
    state.isRendering = false;
  }, 150);
};

const handleScroll = () => {
  if (state.isRendering) return;
  const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 200;
  if (nearBottom) {
    renderBatch();
  }
};

const showModal = () => {
  checkoutModal?.removeAttribute("hidden");
};

const hideModal = () => {
  checkoutModal?.setAttribute("hidden", "");
  secretWrap?.setAttribute("hidden", "");
  if (statusLabel) statusLabel.textContent = "Aguardando pagamento...";
  if (pixCodeField) pixCodeField.value = "";
  if (pixQr) pixQr.removeAttribute("src");
  state.currentPaymentId = null;
  state.currentProduct = null;
  checkoutContent?.setAttribute("hidden", "");
  checkoutLoading?.removeAttribute("hidden");
  if (state.pollTimer) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
  }
};

const updateStatus = (text) => {
  if (statusLabel) statusLabel.textContent = text;
};

const pollPayment = () => {
  if (!state.currentPaymentId) return;
  fetch(`${API_BASE_URL}/payments/${state.currentPaymentId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "paid") {
          updateStatus("Pagamento confirmado. Acesso liberado!");
          if (secretLink) {
            secretLink.href = data.secret_link;
            secretLink.textContent = "Abrir conteúdo premium";
          }
          secretWrap?.removeAttribute("hidden");
          if (state.pollTimer) {
            clearInterval(state.pollTimer);
            state.pollTimer = null;
          }
        }
      })
      .catch(() => {});
};

const startPolling = () => {
  if (state.pollTimer) clearInterval(state.pollTimer);
  state.pollTimer = setInterval(pollPayment, 4000);
};

const populateCheckout = (product, checkoutInfo) => {
  checkoutTitle.textContent = product.title;
  checkoutNote.textContent = product.note || "Pagamento seguro e anônimo";
  checkoutPrice.textContent = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: product.currency || "BRL",
  }).format(product.price);
  checkoutLifetime.textContent = product.lifetime_text || "Acesso vitalício incluído";
  pixCodeField.value = checkoutInfo.pix_code;
  if (pixQr && checkoutInfo.qr_base64) {
    pixQr.src = `data:image/png;base64,${checkoutInfo.qr_base64}`;
  }
  checkoutLoading.setAttribute("hidden", "");
  checkoutContent.removeAttribute("hidden");
  updateStatus("Aguardando pagamento Pix...");
};

const requestCheckout = async (product) => {
  checkoutContent?.setAttribute("hidden", "");
  checkoutLoading?.removeAttribute("hidden");
  secretWrap?.setAttribute("hidden", "");
  updateStatus("Gerando Pix seguro...");

  try {
    const response = await fetch(`${API_BASE_URL}/checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: product.product_id, customer_ref: randomId() }),
    });
    if (!response.ok) {
      throw new Error(await response.text());
    }
    const data = await response.json();
    state.currentPaymentId = data.payment_id;
    populateCheckout(product, data);
    startPolling();
  } catch (error) {
    checkoutLoading.setAttribute("hidden", "");
    updateStatus("Não foi possível gerar o Pix. Tente novamente.");
  }
};

const openCheckout = (product) => {
  state.currentProduct = product;
  showModal();
  requestCheckout(product);
};

const attachCheckoutEvents = () => {
  checkoutModal?.querySelectorAll("[data-close]").forEach((el) => {
    el.addEventListener("click", hideModal);
  });

  const copyBtn = checkoutModal?.querySelector("[data-copy]");
  copyBtn?.addEventListener("click", async () => {
    if (!pixCodeField?.value) return;
    try {
      await navigator.clipboard.writeText(pixCodeField.value);
      updateStatus("Código copiado. Finalize no app do banco e aguarde a liberação.");
    } catch (error) {
      updateStatus("Não foi possível copiar automaticamente. Copie manualmente.");
    }
  });

  const regenBtn = checkoutModal?.querySelector("[data-regenerate]");
  regenBtn?.addEventListener("click", () => {
    if (state.currentProduct) {
      requestCheckout(state.currentProduct);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !checkoutModal?.hasAttribute("hidden")) {
      hideModal();
    }
  });
};

const bootstrap = async () => {
  // Verifica se está abrindo via file:// (não funciona por CORS)
  if (window.location.protocol === "file:") {
    const msg = "⚠️ Erro: Não é possível abrir o HTML diretamente (file://).\n\n" +
                "Use um servidor HTTP local:\n" +
                "1. Abra um terminal na pasta do projeto\n" +
                "2. Execute: python -m http.server 3000\n" +
                "3. Acesse: http://localhost:3000\n\n" +
                "OU verifique se o bot está rodando em: " + API_BASE_URL;
    alert(msg);
    if (loadingIndicator) {
      loadingIndicator.querySelector("p").textContent = "Use um servidor HTTP (veja instruções acima)";
      loadingIndicator.querySelector("p").style.color = "#ff4444";
    }
    return;
  }

  try {
    console.log("🔍 Buscando produtos de:", `${API_BASE_URL}/products`);
    
    const response = await fetch(`${API_BASE_URL}/products`);
    
    if (!response.ok) {
      throw new Error(`API retornou erro ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log("✅ Produtos recebidos:", data);
    
    state.products = Array.isArray(data) ? data : [];
    
    if (!state.products.length) {
      const msg = "Nenhum produto encontrado. Adicione produtos usando /addproduct no Telegram.";
      if (loadingIndicator) {
        loadingIndicator.querySelector("p").textContent = msg;
        loadingIndicator.querySelector("p").style.color = "#ffaa00";
      }
      console.warn("⚠️ Catálogo vazio");
      return;
    }
    
    console.log(`✅ ${state.products.length} produto(s) carregado(s) com sucesso!`);
    renderBatch(9);
    window.addEventListener("scroll", handleScroll, { passive: true });
    attachCheckoutEvents();
  } catch (error) {
    console.error("❌ Erro ao carregar produtos:", error);
    const errorMsg = `Erro ao conectar com a API: ${error.message}\n\n` +
                     `Verifique se o bot está rodando e acesse: ${API_BASE_URL}/products`;
    
    if (loadingIndicator) {
      const p = loadingIndicator.querySelector("p");
      if (p) {
        p.textContent = errorMsg;
        p.style.color = "#ff4444";
        p.style.whiteSpace = "pre-line";
      }
    }
    
    // Mostra erro detalhado no console
    alert(`Erro ao carregar produtos!\n\n${errorMsg}\n\nVerifique o console (F12) para mais detalhes.`);
  }
};

if (grid && template) {
  bootstrap();
}

