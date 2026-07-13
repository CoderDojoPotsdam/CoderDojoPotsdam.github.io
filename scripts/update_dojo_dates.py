#!/usr/bin/env python3
"""Aktualisiert die Dojo-Termine in index.md.

Regel: Jedes Dojo findet am 2. Samstag im Monat statt. Das Skript entfernt
vergangene Termine aus der Liste und ergaenzt bei Bedarf neue Standard-Termine,
sodass immer NUM_UPCOMING zukuenftige Termine gelistet sind. Bestehende (ggf.
manuell angepasste) Zeilen werden nicht veraendert. Der hervorgehobene Hinweis
oben bekommt das Datum des naechsten Termins.

Idempotent: mehrfaches Ausfuehren am selben Tag aendert nichts.
"""

from __future__ import annotations

import calendar
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

INDEX_FILE = Path(__file__).resolve().parent.parent / "index.md"
NUM_UPCOMING = 3
TIMEZONE = ZoneInfo("Europe/Berlin")

LIST_HEADING = "### Unsere nächsten Dojos"
DATE_RE = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")
# Zeile eines Listeneintrags, z.B. "* **11.07.2026**, 14-17 Uhr, ..."
ENTRY_RE = re.compile(r"^\s*\*\s*\*\*(\d{2}\.\d{2}\.\d{4})\*\*")


def parse_de_date(text: str) -> date:
    """Parst ein Datum im Format TT.MM.JJJJ."""
    day, month, year = (int(part) for part in text.split("."))
    return date(year, month, day)


def format_de_date(value: date) -> str:
    return value.strftime("%d.%m.%Y")


def second_saturday(year: int, month: int) -> date:
    """Liefert den 2. Samstag des Monats."""
    weeks = calendar.monthcalendar(year, month)
    saturdays = [week[calendar.SATURDAY] for week in weeks if week[calendar.SATURDAY] != 0]
    return date(year, month, saturdays[1])


def next_second_saturday_after(after: date) -> date:
    """Erster 2.-Samstag-Termin, der echt nach `after` liegt."""
    year, month = after.year, after.month
    while True:
        candidate = second_saturday(year, month)
        if candidate > after:
            return candidate
        month += 1
        if month > 12:
            month = 1
            year += 1


def standard_entry_line(value: date) -> str:
    return (
        f"* **{format_de_date(value)}**, 14-17 Uhr, "
        "Haus H, Raum E.51/52: offenes Dojo"
    )


def update_content(content: str, today: date) -> str:
    lines = content.splitlines()

    # Listenblock unter der Ueberschrift finden.
    try:
        heading_idx = next(i for i, line in enumerate(lines) if line.strip() == LIST_HEADING)
    except StopIteration:
        raise SystemExit(f"Ueberschrift '{LIST_HEADING}' nicht in index.md gefunden.")

    start = heading_idx + 1
    while start < len(lines) and lines[start].strip() == "":
        start += 1

    end = start
    entries: list[tuple[date, str]] = []
    while end < len(lines) and ENTRY_RE.match(lines[end]):
        match = ENTRY_RE.match(lines[end])
        entries.append((parse_de_date(match.group(1)), lines[end]))
        end += 1

    if not entries:
        raise SystemExit("Keine Dojo-Termine im Listenblock gefunden.")

    # Vergangene Termine entfernen, Rest sortieren.
    future = sorted((d, line) for d, line in entries if d >= today)

    # Auf NUM_UPCOMING auffuellen.
    while len(future) < NUM_UPCOMING:
        seed = future[-1][0] if future else today - timedelta(days=1)
        new_date = next_second_saturday_after(seed)
        future.append((new_date, standard_entry_line(new_date)))

    future = future[:NUM_UPCOMING]
    new_list_lines = [line for _, line in future]
    lines[start:end] = new_list_lines

    content = "\n".join(lines)
    if content.endswith("\n") is False and content:
        content += "\n"

    # Hinweiszeile ("Nächstes Dojo: ... am TT.MM.JJJJ ...") auf naechsten Termin setzen.
    next_date_str = format_de_date(future[0][0])
    content = re.sub(
        r"(Nächstes Dojo:.*?am )\d{2}\.\d{2}\.\d{4}",
        lambda m: m.group(1) + next_date_str,
        content,
        count=1,
    )
    return content


def main() -> None:
    today = datetime.now(TIMEZONE).date()
    original = INDEX_FILE.read_text(encoding="utf-8")
    updated = update_content(original, today)
    if updated != original:
        INDEX_FILE.write_text(updated, encoding="utf-8")
        print("index.md aktualisiert.")
    else:
        print("Keine Aenderung noetig.")


if __name__ == "__main__":
    main()
