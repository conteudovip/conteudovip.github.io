document.addEventListener("DOMContentLoaded", () => {
  const flows = document.querySelectorAll("[data-pix-flow]");

  flows.forEach((section) => {
    const generateBtn = section.querySelector("[data-generate]");
    const copyBtn = section.querySelector("[data-copy]");
    const confirmBtn = section.querySelector("[data-confirm]");
    const codeField = section.querySelector("[data-pix-code]");
    const resultEl = section.querySelector("[data-pix-result]");
    const secretWrap = section.querySelector("[data-secret-wrap]");
    const secretLink = section.querySelector("[data-secret-link]");

    if (!generateBtn || !codeField) {
      return;
    }

    const productName = section.dataset.product || "Produto VIP";
    const amount = section.dataset.amount || "0,00";
    const secretUrl = section.dataset.secretUrl || "#";

    const buildPixCode = () => {
      const timestamp = Date.now().toString(16).toUpperCase();
      const randomPart = Math.random().toString(36).substring(2, 10).toUpperCase();
      return `PIX|${productName}|${amount}|${timestamp}${randomPart}`;
    };

    const setResult = (message, state = "info") => {
      if (!resultEl) return;
      resultEl.textContent = message;
      resultEl.dataset.state = state;
    };

    generateBtn.addEventListener("click", () => {
      codeField.value = buildPixCode();
      setResult("Código Pix gerado. Copie, pague no seu banco e confirme aqui.", "ready");
      section.classList.add("pix-flow--generated");
    });

    copyBtn?.addEventListener("click", async () => {
      if (!codeField.value) {
        setResult("Gere o Pix antes de copiar.", "error");
        return;
      }

      try {
        await navigator.clipboard.writeText(codeField.value);
        setResult('Código copiado! Finalize o pagamento e clique em "Já paguei".', "ready");
      } catch (err) {
        codeField.select();
        setResult("Copie manualmente usando CTRL+C / CMD+C.", "info");
      }
    });

    confirmBtn?.addEventListener("click", () => {
      if (!codeField.value) {
        setResult("Gere e pague o Pix antes de confirmar.", "error");
        return;
      }

      confirmBtn.disabled = true;
      setResult("Validando pagamento Pix...", "loading");

      setTimeout(() => {
        setResult("Pix confirmado! Seu link exclusivo está liberado.", "success");
        confirmBtn.disabled = false;
        if (secretWrap) {
          secretWrap.hidden = false;
        }
        if (secretLink) {
          secretLink.href = secretUrl;
        }
      }, 1600);
    });
  });
});

