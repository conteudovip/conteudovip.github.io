const endpoint =
  process.env.SYNCPAY_AUTH_URL || "https://syncpay.apidog.io/api/partner/v1/auth-token";

const clientId =
  process.env.SYNCPAY_CLIENT_ID || "e7c08cb5-e1a9-429f-87a2-261a376a23b9";
const clientSecret =
  process.env.SYNCPAY_CLIENT_SECRET || "9cb25cd3-8e7c-45fd-b04f-ddf96d5feaed";

async function generateToken() {
  if (!clientId || !clientSecret) {
    console.error("SYNCPAY_CLIENT_ID e SYNCPAY_CLIENT_SECRET são obrigatórios.");
    process.exit(1);
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
      }),
    });

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`Request failed: ${response.status} - ${errorBody}`);
    }

    const data = await response.json();
    console.log("Token gerado com sucesso:");
    console.log(JSON.stringify(data, null, 2));
  } catch (error) {
    console.error("Erro ao gerar token:", error.message);
    process.exit(1);
  }
}

generateToken();

