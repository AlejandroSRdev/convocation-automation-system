from app.application.rendering.dtos import ConvocationRenderDTO


def render_header(dto: ConvocationRenderDTO) -> list[str]:
    return [
        f"*{dto.home_team} vs {dto.away_team}*",
        f"Jornada {dto.matchday} — {dto.competition_type}",
    ]
