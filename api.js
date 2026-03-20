export default {
  async fetch(request) {
    const url = new URL(request.url);
    const params = url.searchParams;
    
    const p = parseFloat(params.get('p'));
    const win = parseFloat(params.get('win'));
    const loss = parseFloat(params.get('loss'));
    
    const payment = {
      price: "0.01 USDC",
      wallet: "0x24b288c98421d7b447c2d6a6442538d01c5fce22",
      chain: "Base"
    };
    
    if (!p || !win || !loss) {
      return new Response(JSON.stringify({
        message: "Kelly Formula API",
        usage: "/?p=0.55&win=5&loss=3",
        payment
      }), { headers: { "Content-Type": "application/json" } });
    }
    
    const b = win / loss;
    const fStar = (p * b - (1 - p)) / b;
    const halfKelly = fStar > 0 ? fStar * 0.5 * 100 : 0;
    
    return new Response(JSON.stringify({
      success: true,
      inputs: { p, win, loss },
      kelly: { half_kelly_pct: halfKelly.toFixed(2) },
      payment
    }), { headers: { "Content-Type": "application/json" } });
  }
};
