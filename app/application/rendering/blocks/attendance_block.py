from app.application.rendering.dtos import ConvocationRenderDTO


def render_attendance(dto: ConvocationRenderDTO) -> list[str]:
    lines = ["📢 *Instrucciones de asistencia:*"]
    lines.append("Confirmad asistencia por WhatsApp antes de las 20h del viernes, gracias.")
    if dto.manual_notes:
        lines.append("")
        for note in dto.manual_notes:
            lines.append(f"📌 {note}")
    return lines
