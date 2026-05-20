from app.application.rendering.dtos import ConvocationRenderDTO


def _format_player_line(number: int | None, name: str, innings: str) -> str:
    if number is not None:
        return f"#{number} {name} ({innings}) ✅"
    return f"{name} ({innings}) ✅"


def render_players(dto: ConvocationRenderDTO) -> list[str]:
    total = len(dto.players) + len(dto.invited_players)
    lines = [f"⚾ *Convocados ({total}):*"]
    for player in dto.players:
        lines.append(_format_player_line(player.number, player.name, player.innings))
    for invited in dto.invited_players:
        lines.append(_format_player_line(invited.number, invited.name, invited.innings))
    return lines
