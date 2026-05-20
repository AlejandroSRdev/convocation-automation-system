from app.application.rendering.dtos import ConvocationRenderDTO

_STATS_URL = "https://stats.example.com"
_ROSTER_URL = "https://roster.example.com"
_CALENDAR_URL = "https://calendar.example.com"


def render_links(dto: ConvocationRenderDTO) -> list[str]:
    return [
        "🔗 *Enllaços operacionals:*",
        f"📊 Estadístiques: {_STATS_URL}",
        f"📋 Plantilla: {_ROSTER_URL}",
        f"📅 Calendari: {_CALENDAR_URL}",
    ]
