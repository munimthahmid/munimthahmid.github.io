#!/usr/bin/env python3
"""Generate Munim Thahmid's one-page research resume."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "files" / "Munim_Thahmid_Resume.pdf"

PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT = 42
RIGHT = PAGE_WIDTH - 42
CONTENT_WIDTH = RIGHT - LEFT

INK = HexColor("#142724")
MUTED = HexColor("#556762")
GREEN = HexColor("#0F675D")
GREEN_DARK = HexColor("#0B2926")
AMBER = HexColor("#EBA448")
LINE = HexColor("#D5DDD9")
PAPER = HexColor("#FAF9F5")

REGULAR = "DejaVuSans"
BOLD = "DejaVuSans-Bold"


def width(text: str, font: str, size: float) -> float:
    return stringWidth(text, font, size)


def wrap(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and width(candidate, font, size) > max_width:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def draw_link(c: canvas.Canvas, x: float, y: float, label: str, url: str, size: float = 8.2) -> float:
    c.setFillColor(GREEN)
    c.setFont(REGULAR, size)
    c.drawString(x, y, label)
    label_width = width(label, REGULAR, size)
    c.linkURL(url, (x, y - 2, x + label_width, y + size + 1), relative=0)
    return x + label_width


def draw_section(c: canvas.Canvas, y: float, title: str) -> float:
    c.setFillColor(GREEN)
    c.setFont(BOLD, 8.7)
    c.drawString(LEFT, y, title.upper())
    title_width = width(title.upper(), BOLD, 8.7)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(LEFT + title_width + 10, y + 2.5, RIGHT, y + 2.5)
    return y - 16


def draw_entry_header(
    c: canvas.Canvas,
    y: float,
    role: str,
    organization: str,
    date: str,
    location: str = "",
) -> float:
    c.setFillColor(INK)
    c.setFont(BOLD, 9.8)
    c.drawString(LEFT, y, role)
    role_width = width(role, BOLD, 9.8)
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 9.25)
    c.drawString(LEFT + role_width + 6, y, f"| {organization}")
    c.setFillColor(INK)
    c.setFont(BOLD, 8.65)
    c.drawRightString(RIGHT, y, date)
    if location:
        c.setFillColor(MUTED)
        c.setFont(REGULAR, 8.0)
        c.drawRightString(RIGHT, y - 10, location)
        return y - 23
    return y - 14


def draw_bullet(c: canvas.Canvas, y: float, text: str, size: float = 8.8, leading: float = 11.4) -> float:
    bullet_x = LEFT + 3
    text_x = LEFT + 13
    max_width = RIGHT - text_x
    lines = wrap(text, REGULAR, size, max_width)

    c.setFillColor(AMBER)
    c.roundRect(bullet_x, y + 2.1, 3.3, 3.3, 0.8, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(REGULAR, size)
    for index, line in enumerate(lines):
        c.drawString(text_x, y - index * leading, line)
    return y - len(lines) * leading - 1.6


def build_resume(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont(REGULAR, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont(BOLD, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
    c = canvas.Canvas(str(output), pagesize=letter, pageCompression=1)
    c.setTitle("Munim Thahmid - Research Resume")
    c.setAuthor("Munim Thahmid")
    c.setSubject("Formal Methods and Software Systems Research Resume")

    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    # Header
    c.setFillColor(GREEN_DARK)
    c.roundRect(LEFT, PAGE_HEIGHT - 92, 5, 54, 2.5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(BOLD, 24)
    c.drawString(LEFT + 16, PAGE_HEIGHT - 54, "Munim Thahmid")
    c.setFillColor(GREEN)
    c.setFont(BOLD, 8.7)
    c.drawString(LEFT + 17, PAGE_HEIGHT - 69, "FORMAL METHODS  /  SOFTWARE SYSTEMS  /  RESEARCH ENGINEERING")

    x = LEFT + 17
    y = PAGE_HEIGHT - 84
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 8.2)
    c.drawString(x, y, "Dhaka, Bangladesh")
    x += width("Dhaka, Bangladesh", REGULAR, 8.2)
    separator = "  |  "
    c.drawString(x, y, separator)
    x += width(separator, REGULAR, 8.2)
    x = draw_link(c, x, y, "munimthahmid2@gmail.com", "mailto:munimthahmid2@gmail.com")
    c.setFillColor(MUTED)
    c.drawString(x, y, separator)
    x += width(separator, REGULAR, 8.2)
    x = draw_link(c, x, y, "Website", "https://munimthahmid.github.io")
    c.setFillColor(MUTED)
    c.drawString(x, y, separator)
    x += width(separator, REGULAR, 8.2)
    x = draw_link(c, x, y, "LinkedIn", "https://www.linkedin.com/in/munimthahmid/")
    c.setFillColor(MUTED)
    c.drawString(x, y, separator)
    x += width(separator, REGULAR, 8.2)
    draw_link(c, x, y, "GitHub", "https://github.com/munimthahmid")

    y = PAGE_HEIGHT - 112

    # Research focus
    y = draw_section(c, y, "Research focus")
    focus = (
        "Formal methods and dependable software systems, with current work on AI-assisted TLA+ proof "
        "evaluation, scalable TLAPS verification, and reliable agentic-SRE benchmarks."
    )
    c.setFillColor(INK)
    c.setFont(REGULAR, 9.0)
    for line in wrap(focus, REGULAR, 9.0, CONTENT_WIDTH):
        c.drawString(LEFT, y, line)
        y -= 11.5
    y -= 5

    # Education
    y = draw_section(c, y, "Education")
    c.setFillColor(INK)
    c.setFont(BOLD, 9.7)
    c.drawString(LEFT, y, "Bangladesh University of Engineering and Technology (BUET)")
    c.setFont(BOLD, 8.65)
    c.drawRightString(RIGHT, y, "Jan 2022 - May 2026")
    y -= 11.5
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 8.7)
    c.drawString(LEFT, y, "B.Sc. in Computer Science and Engineering")
    c.drawRightString(RIGHT, y, "CGPA: 3.46 / 4.00 | Dhaka, Bangladesh")
    y -= 19

    # Research experience
    y = draw_section(c, y, "Research experience")
    y = draw_entry_header(
        c,
        y,
        "Research Intern",
        "University of Illinois Urbana-Champaign",
        "May 2026 - Present",
        "Remote | Advisor: Prof. Tianyin Xu",
    )
    y = draw_bullet(
        c,
        y,
        "Active contributor to TLAPS-Bench, an evaluation framework for AI-generated TLA+ proofs; authored seven merged pull requests across proof checking and evaluator infrastructure.",
    )
    y = draw_bullet(
        c,
        y,
        "Scaled verification of large proof artifacts through TLAPM fingerprint-cache reuse, fail-fast validation, and parallel sharding at top-level theorem boundaries.",
    )
    y = draw_bullet(
        c,
        y,
        "Improved benchmark validity and resilience with continuation runs, infrastructure-failure retries, result deduplication, and explicit model reasoning controls.",
    )
    y = draw_bullet(
        c,
        y,
        "Built a reproducible SREGym scenario for Kubernetes node conntrack exhaustion, including runtime setup, oracle logic, and analysis of blocked diagnostic-access paths.",
    )
    y -= 4

    y = draw_entry_header(
        c,
        y,
        "Undergraduate Researcher",
        "BUET",
        "2025 - 2026",
        "Supervisor: Dr. Sadia Sharmin",
    )
    y = draw_bullet(
        c,
        y,
        "Led layer-wise probing of Bengali phone-like units across Whisper-small, Whisper-medium, and Whisper-large-v3 under speaker-disjoint evaluation.",
    )
    y = draw_bullet(
        c,
        y,
        "Validated representation trends with XLS-R comparison, ABX discriminability, confidence filtering, duration stratification, and probe ablations; work accepted to INTERSPEECH 2026.",
    )
    y -= 4

    # Engineering experience
    y = draw_section(c, y, "Engineering experience")
    y = draw_entry_header(c, y, "Software Engineer", "Yobo AI", "Oct 2024 - Feb 2026", "Remote | Intern, then part-time")
    y = draw_bullet(
        c,
        y,
        "Built backend systems, testing infrastructure, and production features for AI voice-agent applications over more than one year.",
    )
    y = draw_bullet(
        c,
        y,
        "Developed automated Python testing infrastructure that reduced a regression cycle from roughly eight hours to fifteen minutes.",
    )
    y -= 4

    # Publication
    y = draw_section(c, y, "Selected publication")
    title = "Layer-wise Probing of Whisper's Encoder Representations for Bengali Phone-like Units"
    c.setFillColor(INK)
    c.setFont(BOLD, 8.8)
    c.drawString(LEFT, y, title)
    y -= 10.5
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 8.5)
    c.drawString(LEFT, y, "Munim Thahmid and Sadia Sharmin. Accepted to INTERSPEECH 2026.")
    y -= 16

    # Skills
    y = draw_section(c, y, "Technical skills")
    skill_lines = [
        ("Formal methods", "TLA+, TLAPS/TLAPM, machine-checkable proof evaluation"),
        ("Programming & systems", "Python, C/C++, TypeScript/JavaScript, Bash, Linux, Docker, Kubernetes, Git"),
        ("ML & research", "PyTorch, Hugging Face, Whisper, XLS-R, scikit-learn, pandas, NumPy, statistical evaluation"),
    ]
    for label, values in skill_lines:
        c.setFillColor(INK)
        c.setFont(BOLD, 8.45)
        c.drawString(LEFT, y, f"{label}:")
        label_width = width(f"{label}:", BOLD, 8.45)
        c.setFillColor(MUTED)
        c.setFont(REGULAR, 8.45)
        c.drawString(LEFT + label_width + 5, y, values)
        y -= 11.2

    c.setFillColor(Color(0.33, 0.4, 0.38, alpha=0.7))
    c.setFont(REGULAR, 6.8)
    c.drawRightString(RIGHT, 20, "Updated July 2026")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_resume(OUTPUT)
    print(OUTPUT)
