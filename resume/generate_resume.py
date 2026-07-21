#!/usr/bin/env python3
"""Generate Munim Thahmid's two-column research resume."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "files" / "Munim_Thahmid_Resume.pdf"

PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT = 38
RIGHT = PAGE_WIDTH - 38
LEFT_COLUMN_WIDTH = 170
GUTTER = 28
RIGHT_COLUMN_X = LEFT + LEFT_COLUMN_WIDTH + GUTTER
RIGHT_COLUMN_WIDTH = RIGHT - RIGHT_COLUMN_X

INK = HexColor("#17191C")
MUTED = HexColor("#4F555B")
ACCENT = HexColor("#087282")
LINE = HexColor("#B9BEC2")

REGULAR = "DejaVuSans"
BOLD = "DejaVuSans-Bold"


def text_width(text: str, font: str, size: float) -> float:
    return stringWidth(text, font, size)


def wrap(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and text_width(candidate, font, size) > max_width:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def draw_wrapped(
    c: canvas.Canvas,
    x: float,
    y: float,
    text: str,
    max_width: float,
    font: str = REGULAR,
    size: float = 8.2,
    leading: float = 10.3,
    color=MUTED,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap(text, font, size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_heading(c: canvas.Canvas, x: float, y: float, title: str, max_width: float) -> float:
    c.setFillColor(INK)
    c.setFont(REGULAR, 14.5)
    c.drawString(x, y, title.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(x, y - 5, x + max_width, y - 5)
    return y - 21


def draw_small_label(c: canvas.Canvas, x: float, y: float, label: str) -> float:
    c.setFillColor(INK)
    c.setFont(BOLD, 8.25)
    c.drawString(x, y, label)
    return y - 10.2


def draw_bullet(
    c: canvas.Canvas,
    x: float,
    y: float,
    text: str,
    max_width: float,
    size: float = 8.15,
    leading: float = 10.1,
) -> float:
    text_x = x + 10
    lines = wrap(text, REGULAR, size, max_width - 10)
    c.setFillColor(ACCENT)
    c.circle(x + 2.5, y + 3.1, 1.45, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(REGULAR, size)
    for line in lines:
        c.drawString(text_x, y, line)
        y -= leading
    return y - 2


def draw_role(
    c: canvas.Canvas,
    y: float,
    role: str,
    organization: str,
    date: str,
) -> float:
    c.setFillColor(INK)
    c.setFont(BOLD, 9.2)
    c.drawString(RIGHT_COLUMN_X, y, role)
    c.setFillColor(ACCENT)
    c.setFont(BOLD, 8.2)
    c.drawRightString(RIGHT, y, date)
    y -= 11
    c.setFillColor(MUTED)
    c.setFont(REGULAR, 8.15)
    c.drawString(RIGHT_COLUMN_X, y, organization)
    return y - 13


def draw_link(c: canvas.Canvas, x: float, y: float, label: str, url: str, size: float = 8.1) -> float:
    c.setFillColor(ACCENT)
    c.setFont(REGULAR, size)
    c.drawString(x, y, label)
    w = text_width(label, REGULAR, size)
    c.linkURL(url, (x, y - 2, x + w, y + size + 1), relative=0)
    return x + w


def build_resume(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont(REGULAR, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont(BOLD, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

    c = canvas.Canvas(str(output), pagesize=letter, pageCompression=1)
    c.setTitle("Munim Thahmid - Research Resume")
    c.setAuthor("Munim Thahmid")
    c.setSubject("Formal Methods and Software Systems Research Resume")

    # Header: preserves the visual character of the previous two-column resume.
    first = "Munim"
    last = "Thahmid"
    first_size = 32
    last_size = 39
    gap = 7
    total = text_width(first, REGULAR, first_size) + gap + text_width(last, BOLD, last_size)
    start_x = (PAGE_WIDTH - total) / 2
    c.setFillColor(INK)
    c.setFont(REGULAR, first_size)
    c.drawString(start_x, 744, first)
    c.setFont(BOLD, last_size)
    c.drawString(start_x + text_width(first, REGULAR, first_size) + gap, 742, last)

    contact_y = 710
    labels = [
        ("Website", "https://munimthahmid.github.io"),
        ("munimthahmid2@gmail.com", "mailto:munimthahmid2@gmail.com"),
        ("LinkedIn", "https://www.linkedin.com/in/munimthahmid/"),
        ("GitHub", "https://github.com/munimthahmid"),
    ]
    separator = "  |  "
    total_contact = sum(text_width(label, REGULAR, 8.1) for label, _ in labels)
    total_contact += (len(labels) - 1) * text_width(separator, REGULAR, 8.1)
    x = (PAGE_WIDTH - total_contact) / 2
    for index, (label, url) in enumerate(labels):
        x = draw_link(c, x, contact_y, label, url)
        if index < len(labels) - 1:
            c.setFillColor(MUTED)
            c.setFont(REGULAR, 8.1)
            c.drawString(x, contact_y, separator)
            x += text_width(separator, REGULAR, 8.1)

    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(0, 691, PAGE_WIDTH, 691)

    # Left column
    left_y = 663
    left_y = draw_heading(c, LEFT, left_y, "Education", LEFT_COLUMN_WIDTH)
    left_y = draw_wrapped(
        c,
        LEFT,
        left_y,
        "Bangladesh University of Engineering and Technology",
        LEFT_COLUMN_WIDTH,
        BOLD,
        9.0,
        10.8,
        INK,
    )
    left_y -= 1
    left_y = draw_wrapped(c, LEFT, left_y, "B.Sc. in Computer Science and Engineering", LEFT_COLUMN_WIDTH, REGULAR, 8.35, 10.1, INK)
    left_y = draw_wrapped(c, LEFT, left_y, "CGPA: 3.46 / 4.00", LEFT_COLUMN_WIDTH, REGULAR, 8.15, 10, MUTED)
    left_y = draw_wrapped(c, LEFT, left_y, "Jan 2022 - May 2026", LEFT_COLUMN_WIDTH, REGULAR, 8.15, 10, MUTED)
    left_y = draw_wrapped(c, LEFT, left_y, "Dhaka, Bangladesh", LEFT_COLUMN_WIDTH, REGULAR, 8.15, 10, MUTED)

    left_y -= 16
    left_y = draw_heading(c, LEFT, left_y, "Research interests", LEFT_COLUMN_WIDTH)
    left_y = draw_wrapped(c, LEFT, left_y, "Formal verification", LEFT_COLUMN_WIDTH, REGULAR, 8.25, 11, INK)
    left_y = draw_wrapped(c, LEFT, left_y, "Machine-assisted reasoning", LEFT_COLUMN_WIDTH, REGULAR, 8.25, 11, INK)
    left_y = draw_wrapped(c, LEFT, left_y, "Distributed systems", LEFT_COLUMN_WIDTH, REGULAR, 8.25, 11, INK)
    left_y = draw_wrapped(c, LEFT, left_y, "Software reliability", LEFT_COLUMN_WIDTH, REGULAR, 8.25, 11, INK)

    left_y -= 16
    left_y = draw_heading(c, LEFT, left_y, "Technical skills", LEFT_COLUMN_WIDTH)
    left_y = draw_small_label(c, LEFT, left_y, "Formal methods")
    left_y = draw_wrapped(c, LEFT, left_y, "TLA+, TLAPS / TLAPM", LEFT_COLUMN_WIDTH, REGULAR, 8.0, 10, MUTED)
    left_y -= 4
    left_y = draw_small_label(c, LEFT, left_y, "Programming")
    left_y = draw_wrapped(c, LEFT, left_y, "Python, C/C++, TypeScript / JavaScript, Bash, SQL", LEFT_COLUMN_WIDTH, REGULAR, 8.0, 10, MUTED)
    left_y -= 4
    left_y = draw_small_label(c, LEFT, left_y, "Systems")
    left_y = draw_wrapped(c, LEFT, left_y, "Linux, Docker, Kubernetes, Git", LEFT_COLUMN_WIDTH, REGULAR, 8.0, 10, MUTED)
    left_y -= 4
    left_y = draw_small_label(c, LEFT, left_y, "ML and research")
    left_y = draw_wrapped(c, LEFT, left_y, "PyTorch, Whisper, XLS-R, scikit-learn, pandas, NumPy, statistical evaluation", LEFT_COLUMN_WIDTH, REGULAR, 8.0, 10, MUTED)

    left_y -= 16
    left_y = draw_heading(c, LEFT, left_y, "Links", LEFT_COLUMN_WIDTH)
    draw_link(c, LEFT, left_y, "munimthahmid.github.io", "https://munimthahmid.github.io")
    left_y -= 13
    draw_link(c, LEFT, left_y, "github.com/munimthahmid", "https://github.com/munimthahmid")
    left_y -= 13
    draw_link(c, LEFT, left_y, "linkedin.com/in/munimthahmid", "https://www.linkedin.com/in/munimthahmid/")

    # Right column
    right_y = 663
    right_y = draw_heading(c, RIGHT_COLUMN_X, right_y, "Research experience", RIGHT_COLUMN_WIDTH)
    right_y = draw_role(
        c,
        right_y,
        "Research Intern",
        "University of Illinois Urbana-Champaign | Advisor: Prof. Tianyin Xu",
        "May 2026 - Present",
    )
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Contribute to TLAPS-Bench, a benchmark for evaluating AI systems on completing and constructing machine-checkable TLA+ proofs.",
        RIGHT_COLUMN_WIDTH,
    )
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Study rigorous evaluation of proof-generating agents, including scalable verification, iterative proof improvement, and measurement of correctness and cost.",
        RIGHT_COLUMN_WIDTH,
    )
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Previously developed a reproducible SREGym incident for Kubernetes node conntrack exhaustion to evaluate diagnosis when normal access paths are disrupted.",
        RIGHT_COLUMN_WIDTH,
    )
    right_y -= 4

    right_y = draw_role(
        c,
        right_y,
        "Undergraduate Researcher",
        "BUET | Supervisor: Dr. Sadia Sharmin",
        "2025 - 2026",
    )
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Investigated Bengali phone-like representations across Whisper encoders using speaker-disjoint layer-wise probing.",
        RIGHT_COLUMN_WIDTH,
    )
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Conducted cross-model comparison with XLS-R and robustness analyses, leading to an accepted INTERSPEECH 2026 paper.",
        RIGHT_COLUMN_WIDTH,
    )

    right_y -= 9
    right_y = draw_heading(c, RIGHT_COLUMN_X, right_y, "Selected publication", RIGHT_COLUMN_WIDTH)
    right_y = draw_wrapped(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Layer-wise Probing of Whisper's Encoder Representations for Bengali Phone-like Units",
        RIGHT_COLUMN_WIDTH,
        BOLD,
        9.0,
        10.8,
        INK,
    )
    right_y -= 1
    right_y = draw_wrapped(c, RIGHT_COLUMN_X, right_y, "Munim Thahmid and Sadia Sharmin", RIGHT_COLUMN_WIDTH, REGULAR, 8.15, 10, MUTED)
    right_y = draw_wrapped(c, RIGHT_COLUMN_X, right_y, "Accepted to INTERSPEECH 2026", RIGHT_COLUMN_WIDTH, BOLD, 8.15, 10, ACCENT)

    right_y -= 10
    right_y = draw_heading(c, RIGHT_COLUMN_X, right_y, "Engineering experience", RIGHT_COLUMN_WIDTH)
    right_y = draw_role(c, right_y, "Software Engineer", "Yobo AI | Intern, then part-time engineer", "Oct 2024 - Feb 2026")
    right_y = draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Spent over a year building backend systems, testing infrastructure, and production features for AI voice-agent applications.",
        RIGHT_COLUMN_WIDTH,
    )
    draw_bullet(
        c,
        RIGHT_COLUMN_X,
        right_y,
        "Developed automated Python testing infrastructure that reduced a regression cycle from roughly eight hours to fifteen minutes.",
        RIGHT_COLUMN_WIDTH,
    )

    c.setFillColor(MUTED)
    c.setFont(REGULAR, 6.7)
    c.drawRightString(RIGHT, 22, "Updated July 2026")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_resume(OUTPUT)
    print(OUTPUT)
