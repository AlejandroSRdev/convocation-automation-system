from app.application.rendering.dtos import ConvocationRenderDTO


def render_staff(dto: ConvocationRenderDTO) -> list[str]:
    if not dto.staff:
        return []
    lines = ["👨‍💼 *Staff Técnico:*"]
    for member in dto.staff:
        lines.append(f"  {member.role}: {member.name}")
    return lines
