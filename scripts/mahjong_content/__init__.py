"""Structured bilingual content for the Mahjong AI article set.

Each article is a dict with paired ``[zh, en]`` values so the site's
``data-zh``/``data-en`` language toggle keeps Chinese first and English in
parallel. See ``generate_mahjong_articles.py`` for the renderer.
"""

from __future__ import annotations

# Category key → (label_zh, label_en). Order here drives the hub page order.
CATEGORIES = {
    "rules": ("规则入门", "Rules & Basics"),
    "variants": ("地方玩法", "Regional Variants"),
    "scoring": ("番种与算分", "Scoring & Hands"),
    "strategy": ("策略技巧", "Strategy & Tactics"),
    "shapes": ("牌型与听牌", "Hand Shapes & Waits"),
    "riichi": ("立直麻将", "Riichi Mahjong"),
    "culture": ("麻将文化", "Culture & History"),
    "ai": ("AI 与麻将", "AI & Mahjong"),
    "comp": ("竞技与赛事", "Competition & Play"),
    "beginner": ("新手指南", "Beginner Guides"),
}

# Shared app copy reused across every article page.
APP = {
    "cta_top_zh": "麻将 AI 智能助手，实时分析牌局，帮你提升技术与胜率。支持 iPhone 与 iPad。",
    "cta_top_en": "AI-powered mahjong assistant that analyzes your hand in real time. Level up on iPhone and iPad.",
    "cta_bottom_zh": "免费下载 Mahjong AI，让每一局麻将都成为有效的训练。",
    "cta_bottom_en": "Download Mahjong AI for free and make every game a real training session.",
    "features": [
        ("<strong>实时牌局分析：</strong>即时给出当前手牌的最优出牌方向，不再凭感觉盲打。",
         "<strong>Real-time hand analysis:</strong> shows the optimal discard direction for your hand instantly."),
        ("<strong>多种玩法支持：</strong>覆盖国标、广东、四川等主流玩法，满足不同地区玩家。",
         "<strong>Multiple rulesets:</strong> covers standard Chinese, Cantonese, Sichuan and more regional variants."),
        ("<strong>危险牌提示：</strong>依据对手舍牌智能提示高风险牌，降低点炮概率。",
         "<strong>Danger-tile warnings:</strong> flags risky discards from opponents' patterns to cut how often you deal in."),
        ("<strong>简洁易用：</strong>界面符合 Apple 设计规范，支持深色模式，专注打牌不打扰。",
         "<strong>Clean and simple:</strong> Apple-style interface with dark mode support that stays out of your way."),
    ],
}


def _load() -> list[dict]:
    from . import (  # noqa: WPS433 (intentional late import to keep parts tidy)
        part1_beginner,
        part2_rules,
        part3_variants,
        part4_scoring,
        part5_strategy,
        part6_related,
    )

    articles: list[dict] = []
    for module in (
        part1_beginner,
        part2_rules,
        part3_variants,
        part4_scoring,
        part5_strategy,
        part6_related,
    ):
        articles.extend(module.ARTICLES)
    return articles


ALL_ARTICLES: list[dict] = _load()
