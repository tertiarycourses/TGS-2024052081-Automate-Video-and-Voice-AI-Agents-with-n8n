#!/usr/bin/env python3
"""Build the GG Hair Salon knowledge-base PDF that learners upload to ElevenLabs.

    pip install reportlab
    python3 build_kb_pdf.py

Output: gg-hair-salon-handbook.pdf (in this folder).
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).with_name("gg-hair-salon-handbook.pdf")

MAUVE = colors.HexColor("#8E6E85")
ROSE = colors.HexColor("#C9A227")
INK = colors.HexColor("#2B2B2B")
LIGHT = colors.HexColor("#F5EFF2")

styles = getSampleStyleSheet()
title = ParagraphStyle(
    "title", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=24, textColor=MAUVE, spaceAfter=4,
)
subtitle = ParagraphStyle(
    "subtitle", parent=styles["Normal"], fontSize=11, textColor=INK,
    alignment=TA_CENTER, spaceAfter=18,
)
h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=13.5, textColor=MAUVE, spaceBefore=14, spaceAfter=6,
)
body = ParagraphStyle(
    "body", parent=styles["Normal"], fontSize=10.5, leading=15, textColor=INK,
    spaceAfter=5,
)
qa = ParagraphStyle("qa", parent=body, leftIndent=10, spaceAfter=7)

SERVICES = [
    ["Service", "Price", "Slot", "Good to know"],
    ["Women's Cut & Style", "$65", "1 hour", "Precision cut, wash and blow-dry included."],
    ["Men's Cut", "$35", "1 hour", "Classic or modern, styling included."],
    ["Full Color", "$120", "1 hour", "All-over single-process colour."],
    ["Highlights / Balayage", "$180", "1 hour", "Hand-painted or foil; patch test advised."],
    ["Keratin Smoothing", "$250", "1 hour", "Frizz-free for 8-12 weeks."],
    ["Blowout", "$45", "1 hour", "Professional blow-dry and styling."],
]

STYLISTS = [
    ["Stylist", "Specialty", "Works"],
    ["Grace Goh", "Balayage, colour correction", "Tue-Sat"],
    ["Marcus Tan", "Men's cuts, fades", "Mon-Fri"],
    ["Priya Nair", "Keratin, curly hair", "Wed-Sat"],
    ["Elena Wong", "Bridal and event styling", "Thu-Sat"],
]

FAQS = [
    ("What are your opening hours?",
     "Monday to Saturday, 8:00 AM to 9:00 PM. We are closed on Sundays and on public holidays."),
    ("Where are you located?",
     "123 Orchard Road, Singapore 238888. We are a 4-minute walk from Somerset MRT, Exit B. "
     "Paid parking is available in the mall basement; we do not validate parking."),
    ("How long is an appointment?",
     "Every appointment is booked as a 1-hour slot, whichever service you choose. "
     "Colour and keratin services may run slightly longer if your hair is very long or thick."),
    ("Do I need to pay a deposit?",
     "No deposit for cuts and blowouts. Colour, highlights and keratin services require a "
     "$30 deposit, charged when you arrive and applied to your final bill."),
    ("What is your cancellation policy?",
     "Cancel or reschedule free of charge up to 12 hours before your slot. Inside 12 hours, "
     "or if you do not show up, we charge 50% of the service price."),
    ("How late can I arrive?",
     "We hold your chair for 15 minutes. After that we may need to shorten the service or "
     "move you to the next free slot."),
    ("Do you take walk-ins?",
     "Walk-ins are welcome when a chair is free, but booked appointments always take priority. "
     "Booking by voice with Nina is the surest way to get the slot you want."),
    ("Can I ask for a specific stylist?",
     "Yes. Tell Nina the stylist's name when you book and she will check that stylist's "
     "availability for the day you want."),
    ("What payment methods do you accept?",
     "Cash, PayNow, NETS, Visa, Mastercard and American Express. We do not accept cheques."),
    ("Do you offer a first-visit discount?",
     "Yes, 15% off your first service. Mention 'first visit' when you book and the discount is "
     "applied at the counter."),
    ("Do you have gift cards?",
     "Yes, in $50, $100 and $200 values. They are valid for 12 months and can be used on any "
     "service or retail product."),
    ("Is there a patch test for colour?",
     "For a first-time colour or highlights, we recommend a patch test at least 48 hours before "
     "your appointment. It takes 5 minutes and is free."),
    ("Can I bring my child?",
     "Yes. We cut children's hair from age 5 at the Men's Cut price. Children must stay seated "
     "with an adult while you are being served."),
    ("How should I care for a keratin treatment?",
     "Do not wash your hair for 72 hours, use a sulphate-free shampoo, and avoid tying it "
     "tightly for the first three days. Results last 8 to 12 weeks."),
    ("Do you sell products?",
     "Yes, we retail the shampoos, masks and styling products our stylists use. Ask at the "
     "counter, or ask Nina to note it on your booking."),
]


def table(data, widths):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MAUVE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8CBD2")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def main():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="GG Hair Salon - Salon Handbook",
        author="GG Hair Salon",
    )
    s = [
        Paragraph("GG Hair Salon", title),
        Paragraph(
            "Salon Handbook &amp; Frequently Asked Questions<br/>"
            "123 Orchard Road, Singapore 238888 &nbsp;·&nbsp; Mon-Sat, 8:00 AM - 9:00 PM",
            subtitle,
        ),

        Paragraph("Services and Prices", h2),
        Paragraph(
            "All prices are in Singapore dollars and include GST. Every appointment is a "
            "1-hour slot.", body),
        table(SERVICES, [4.6 * cm, 2 * cm, 1.8 * cm, 8.6 * cm]),

        Paragraph("Our Stylists", h2),
        table(STYLISTS, [4.6 * cm, 7.4 * cm, 5 * cm]),

        Paragraph("Frequently Asked Questions", h2),
    ]
    for q, a in FAQS:
        s.append(Paragraph(f"<b>Q: {q}</b>", qa))
        s.append(Paragraph(f"A: {a}", qa))

    s += [
        Spacer(1, 10),
        Paragraph("Contact", h2),
        Paragraph(
            "Phone: +65 6123 4567 &nbsp;·&nbsp; Email: hello@gghairsalon.example &nbsp;·&nbsp; "
            "Web: gghairsalon.example<br/>"
            "<i>Mock document created for Lab 4 of the Tertiary Infotech n8n course. "
            "GG Hair Salon is fictional; every detail here is invented for training use.</i>",
            body,
        ),
    ]

    doc.build(s)
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
