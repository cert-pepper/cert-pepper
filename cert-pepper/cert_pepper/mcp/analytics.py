"""MCP Server 3: analytics — score prediction and weak area reports."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from cert_pepper.db.connection import get_session, init_db

mcp = FastMCP("cert-pepper-analytics")


async def _get_user_id(session) -> int:
    from sqlalchemy import text

    result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
    row = result.fetchone()
    return row[0] if row else 1


@mcp.tool()
async def predict_score() -> str:
    """Calculate predicted exam score and pass probability based on your performance."""
    from cert_pepper.engine.scorer import predict_score as _predict_score

    async with get_session() as db:
        user_id = await _get_user_id(db)
        score = await _predict_score(db, user_id)

    return json.dumps({
        "predicted_score": score.predicted_score,
        "pass_probability": f"{score.pass_probability:.0%}",
        "passing_score": 750,
        "status": "PASS" if score.predicted_score >= 750 else "FAIL",
        "domain_accuracies": {
            "domain_1": f"{score.d1_accuracy:.0%}",
            "domain_2": f"{score.d2_accuracy:.0%}",
            "domain_3": f"{score.d3_accuracy:.0%}",
            "domain_4": f"{score.d4_accuracy:.0%}",
            "domain_5": f"{score.d5_accuracy:.0%}",
        },
        "weighted_accuracy": f"{score.weighted_accuracy:.0%}",
    })


@mcp.tool()
async def get_weak_areas(threshold: float = 0.70) -> str:
    """Get domains below a given accuracy threshold (0.0-1.0)."""
    from cert_pepper.engine.scorer import get_weak_areas as _get_weak_areas

    async with get_session() as db:
        user_id = await _get_user_id(db)
        weak = await _get_weak_areas(db, user_id, threshold=threshold)

    return json.dumps({
        "weak_areas": [
            {
                "domain": w.domain_number,
                "name": w.domain_name,
                "accuracy": f"{w.accuracy_pct:.0%}",
                "weight": f"{w.weight_pct:.0f}%",
                "attempts": w.attempts,
                "priority": round(w.priority_score, 3),
            }
            for w in weak
        ],
        "threshold": f"{threshold:.0%}",
    })


@mcp.tool()
async def get_study_recommendations(days_remaining: int = 10) -> str:
    """Get prioritized study recommendations based on weak areas and days remaining."""
    from cert_pepper.engine.scorer import get_recommendations

    async with get_session() as db:
        user_id = await _get_user_id(db)
        recs = await get_recommendations(db, user_id, days_remaining=days_remaining)

    return json.dumps({
        "days_remaining": days_remaining,
        "recommendations": [
            {
                "domain": r.domain_number,
                "name": r.domain_name,
                "urgency": r.urgency,
                "reason": r.reason,
                "suggested_minutes": r.suggested_minutes,
            }
            for r in recs
        ],
    })


@mcp.tool()
async def get_performance_trend(days: int = 7) -> str:
    """Get accuracy trend per domain over recent sessions."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)
        result = await db.execute(
            text("""
                SELECT date(qa.created_at) as day,
                       d.number as domain_num,
                       COUNT(*) as total,
                       SUM(qa.is_correct) as correct
                FROM question_attempts qa
                JOIN questions q ON q.id = qa.question_id
                JOIN domains d ON d.id = q.domain_id
                WHERE qa.user_id = :uid
                AND qa.created_at >= datetime('now', :days_ago)
                GROUP BY day, domain_num
                ORDER BY day DESC, domain_num
            """),
            {"uid": user_id, "days_ago": f"-{days} days"},
        )
        rows = result.fetchall()

    trend: dict[str, dict] = {}
    for row in rows:
        day, domain_num, total, correct = row
        correct = correct or 0
        if day not in trend:
            trend[day] = {}
        trend[day][f"domain_{domain_num}"] = f"{(correct / total):.0%}" if total > 0 else "—"

    return json.dumps({"days": days, "trend": trend})


@mcp.resource("analytics://dashboard")
async def progress_dashboard() -> str:
    """Full progress report in Markdown."""
    from sqlalchemy import text

    from cert_pepper.engine.scorer import get_weak_areas, predict_score

    async with get_session() as db:
        user_id = await _get_user_id(db)
        score = await predict_score(db, user_id)
        weak = await get_weak_areas(db, user_id)

        result = await db.execute(
            text("SELECT COUNT(*), SUM(is_correct) FROM question_attempts WHERE user_id=:uid"),
            {"uid": user_id},
        )
        row = result.fetchone()
        total = row[0] or 0
        correct = row[1] or 0

    acc = correct / total if total > 0 else 0
    status = "PASS READY" if score.predicted_score >= 750 else "NEEDS WORK"

    report = f"""# cert-pepper Progress Dashboard

## Overview
- **Total Questions**: {total:,}
- **Overall Accuracy**: {acc:.0%}
- **Predicted Score**: {score.predicted_score}/900 ({status})
- **Pass Probability**: {score.pass_probability:.0%}

## Domain Accuracies
| Domain | Accuracy | Weight |
|--------|----------|--------|
| D1: General Security | {score.d1_accuracy:.0%} | 12% |
| D2: Threats & Vulnerabilities | {score.d2_accuracy:.0%} | 22% |
| D3: Security Architecture | {score.d3_accuracy:.0%} | 18% |
| D4: Security Operations | {score.d4_accuracy:.0%} | 28% |
| D5: Program Management | {score.d5_accuracy:.0%} | 20% |

## Weak Areas (below 70%)
{chr(10).join(f"- Domain {w.domain_number}: {w.domain_name} — {w.accuracy_pct:.0%} ({w.attempts} attempts)" for w in weak) or "None — all domains above threshold!"}
"""
    return report


@mcp.resource("analytics://score-history")
async def score_history() -> str:
    """Predicted score over time."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)
        result = await db.execute(
            text("""
                SELECT created_at, predicted_score, pass_probability
                FROM predicted_scores WHERE user_id=:uid
                ORDER BY created_at DESC LIMIT 30
            """),
            {"uid": user_id},
        )
        rows = result.fetchall()

    data = [{"date": str(r[0]), "score": r[1], "pass_prob": f"{r[2]:.0%}"} for r in rows]
    return json.dumps(data)


def serve() -> None:
    """Entry point for the analytics MCP server (stdio transport)."""
    import asyncio

    asyncio.run(init_db())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
