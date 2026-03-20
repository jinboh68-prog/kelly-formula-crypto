# Kelly Formula API - Vercel Serverless
# This is the main entry point for Vercel

def handler(request):
    import json
    from urllib.parse import parse_qs, urlparse
    
    parsed = urlparse(request.url)
    params = parse_qs(parsed.query)
    
    p = float(params.get('p', [None])[0]) if 'p' in params else None
    win = float(params.get('win', [None])[0]) if 'win' in params else None
    loss = float(params.get('loss', [None])[0]) if 'loss' in params else None
    
    payment = {"price": "0.01 USDC", "wallet": "0x24b288c98421d7b447c2d6a6442538d01c5fce22"}
    
    if not all([p, win, loss]):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"msg": "Kelly Formula API", "usage": "/?p=0.55&win=5&loss=3", "payment": payment})
        }
    
    b = win / loss
    kelly = (p * b - (1 - p)) / b
    half_kelly = kelly * 0.5 * 100 if kelly > 0 else 0
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "p": p, "win": win, "loss": loss,
            "kelly": round(half_kelly, 2),
            "payment": payment
        })
    }
