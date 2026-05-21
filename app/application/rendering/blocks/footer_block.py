from app.application.rendering.dtos import ConvocationRenderDTO


def render_footer(dto: ConvocationRenderDTO) -> list[str]:
    return [
        "Si alguien no puede asistir, colocar ❌ al lado de su nombre. Con antelación y buenos hábitos.",
        "",
        "🐾 *CB Panteres Vallès*",
    ]
