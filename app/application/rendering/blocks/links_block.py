from app.application.rendering.dtos import ConvocationRenderDTO

_STATS_URL = "https://www.fcbs.cat/campionat/2026/b_sub14/stats/bar.htm"
_ROSTER_URL = "https://www.fcbs.cat/wp/wp-content/uploads/2026/04/Roster_Ct.Catalunya_Valles_Sub14_Beisbol_28.04.2026.pdf"
_CALENDAR_URL = "https://www.fcbs.cat/campionat/2026/b_sub14/res.php"
_33INSPIRER = "https://33inspirer.com"


def render_links(dto: ConvocationRenderDTO) -> list[str]:
    return [
        "🔗 *Enlaces operacionales:*",
        f"📊 Estadísticas: {_STATS_URL}",
        f"📋 Plantilla: {_ROSTER_URL}",
        f"📅 Calendario: {_CALENDAR_URL}",
        f"⚡ 33inspirer: {_33INSPIRER}",
    ]
