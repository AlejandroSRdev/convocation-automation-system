from app.application.rendering.dtos import ConvocationRenderDTO


def render_match_info(dto: ConvocationRenderDTO) -> list[str]:
    date_str = dto.match_date.strftime("%d/%m/%Y")
    day_str = dto.match_date.strftime("%A")
    match_time_str = dto.match_time.strftime("%H:%M")
    return [
        f"🗓️ {day_str} {date_str}",
        f"⏰ Partido: {match_time_str}h",
        f"🕤 Convocatoria: {dto.convocation_time}h",
        f"🏟️ {dto.location}",
    ]
