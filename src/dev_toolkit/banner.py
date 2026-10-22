from __future__ import annotations

__all__ = ["print_banner", "print_box", "print_divider"]


def print_divider(char: str = "-", length: int = 50) -> str:
    """Generate a horizontal divider line."""
    return char * length


def print_box(text: str, padding: int = 2, border_char: str = "#") -> str:
    """Wrap a block of text inside a styled terminal box."""
    lines = text.splitlines() or [text]
    max_len = max(len(line) for line in lines)
    total_width = max_len + (padding * 2)

    border = border_char * (total_width + 2)
    formatted_lines = [border]

    for line in lines:
        padded_line = line.ljust(max_len)
        spaces = " " * padding
        formatted_lines.append(
            f"{border_char}{spaces}{padded_line}{spaces}{border_char}"
        )

    formatted_lines.append(border)
    return "\n".join(formatted_lines)


def print_banner(title: str, subtitle: str | None = None) -> str:
    """Generate a prominent CLI title banner."""
    divider = "=" * (len(title) + 6)
    banner_text = f"\n{divider}\n   {title.upper()}   \n{divider}"
    if subtitle:
        banner_text += f"\n   {subtitle}\n"
    return banner_text
