"""
Kelly Formula API - x402付费版本
收款钱包: 0x24b288c98421d7b447c2d6a6442538d01c5fce22 (Base)
价格: 0.01 USDC/次
"""

import json
from datetime import datetime
from typing import Optional
from fastapi import FastAPI

PAYMENT_INFO = {
    "price": "0.01 USDC",
    "wallet": "0x24b288c98421d7b447c2d6a6442538d01c5fce22",
    "chain": "Base (eip155:8453)"
}


def kelly_position(p: float, b: float, fraction: float = 0.5) -> float:
    """计算凯利仓位"""
    if p <= 0.5 or b <= 0:
        return 0.0
    f_star = (p * b - (1 - p)) / b
    if f_star < 0:
        return 0.0
    return f_star * fraction


def calculate_trade(p: float, win_pct: float, loss_pct: float, 
                   fraction: float = 0.5) -> dict:
    """完整交易计算"""
    b = win_pct / loss_pct if loss_pct > 0 else 0
    
    full_kelly = kelly_position(p, b, 1.0)
    half_kelly = kelly_position(p, b, 0.5)
    quarter_kelly = kelly_position(p, b, 0.25)
    
    edge = p * win_pct - (1 - p) * loss_pct
    
    return {
        "inputs": {
            "win_probability": p,
            "win_pct": win_pct,
            "loss_pct": loss_pct,
            "fraction": fraction
        },
        "kelly": {
            "full_kelly_pct": round(full_kelly * 100, 2),
            "half_kelly_pct": round(half_kelly * 100, 2),
            "quarter_kelly_pct": round(quarter_kelly * 100, 2)
        },
        "net_edge": {
            "edge_pct": round(edge, 2),
        },
        "recommendation": {
            "position_pct": round(half_kelly * 100, 2),
            "reason": "Half-Kelly recommended for balanced risk"
        },
        "payment": PAYMENT_INFO
    }


app = FastAPI(title="Kelly Formula API", version="1.0.0")


@app.get("/")
@app.get("/calculate")
async def calculate(
    p: float = None,
    win: float = None,
    loss: float = None,
    fraction: float = 0.5
):
    """凯利公式计算"""
    if p is None or win is None or loss is None:
        return {
            "success": True,
            "message": "Kelly Formula API",
            "usage": "/calculate?p=0.55&win=5&loss=3&fraction=0.5",
            "payment": PAYMENT_INFO
        }
    
    return {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "result": calculate_trade(p, win, loss, fraction)
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
