from app.application.rendering.dtos import ConvocationRenderDTO
from app.application.rendering.blocks.header_block import render_header
from app.application.rendering.blocks.match_info_block import render_match_info
from app.application.rendering.blocks.staff_block import render_staff
from app.application.rendering.blocks.players_block import render_players
from app.application.rendering.blocks.links_block import render_links
from app.application.rendering.blocks.attendance_block import render_attendance
from app.application.rendering.blocks.footer_block import render_footer


class ConvocationRenderer:
    def render(self, dto: ConvocationRenderDTO) -> str:
        sections: list[list[str]] = [
            render_header(dto),
            render_match_info(dto),
            render_staff(dto),
            render_players(dto),
            render_links(dto),
            render_attendance(dto),
            render_footer(dto),
        ]
        lines: list[str] = []
        for section in sections:
            if section:
                if lines:
                    lines.append("")
                lines.extend(section)
        return "\n".join(lines)
