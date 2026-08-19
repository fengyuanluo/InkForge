"""Public novel ranking research services."""

from app.novel_research.service import (
    SUPPORTED_SITES,
    discover_rankings,
    list_ranked_novels,
    read_novel_opening,
)

__all__ = [
    "SUPPORTED_SITES",
    "discover_rankings",
    "list_ranked_novels",
    "read_novel_opening",
]
