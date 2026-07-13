#!/usr/bin/env python3
"""Generate 20 mock course brochures (.txt) for the Cooking & Bakery Training Center.

These plain-text brochures are designed to be uploaded to Google Drive and ingested
into a vector database (Supabase / Pinecone) for the RAG customer-service chatbot.
Run:  python3 _generate_brochures.py
"""
import os

CAMPUSES = {
    "Bakehouse": "Sweet Heights Bakery Campus, 123 Orchard Road, #04-12, Singapore 238888",
    "Culinary": "Flavour Lab Culinary Campus, 88 Bukit Timah Road, #02-05, Singapore 229841",
}

# (code, title, category, level, weeks, hours, fee, campus, intakes, learn, cert)
COURSES = [
    ("BAK-101", "Artisan Sourdough Bread Baking", "Bakery", "Beginner", 4, 24, 680,
     "Bakehouse", "Jan, Apr, Jul, Oct",
     ["Building & maintaining a wild yeast starter", "Autolyse, bulk fermentation & shaping",
      "Scoring patterns and oven steam techniques", "Reading crumb structure & troubleshooting"],
     "Certificate in Artisan Sourdough Baking"),
    ("BAK-102", "French Pastry & Viennoiserie", "Bakery", "Intermediate", 8, 48, 1480,
     "Bakehouse", "Feb, Jun, Sep",
     ["Laminated doughs: croissant & pain au chocolat", "Choux pastry, éclairs & profiteroles",
      "Classic tarts, crémeux & mousse", "Plating and patisserie presentation"],
     "Diploma in French Pastry Arts"),
    ("BAK-103", "Wedding Cake Design & Decoration", "Bakery", "Advanced", 6, 36, 1280,
     "Bakehouse", "Mar, Aug, Nov",
     ["Tiered cake structure & stacking", "Fondant covering & sharp edges",
      "Sugar flowers & royal icing piping", "Colour theory & client consultation"],
     "Certificate in Cake Design"),
    ("BAK-104", "Macaron Masterclass", "Bakery", "Intermediate", 2, 12, 420,
     "Bakehouse", "Monthly",
     ["French vs Italian meringue method", "Macaronage & achieving the perfect 'feet'",
      "Ganache, buttercream & fruit fillings", "Colouring, flavouring & storage"],
     "Certificate of Completion"),
    ("BAK-105", "Chocolate & Confectionery Making", "Bakery", "Intermediate", 4, 24, 760,
     "Bakehouse", "Jan, May, Sep",
     ["Tempering chocolate (tabling & seeding)", "Moulded & filled bonbons",
      "Truffles, pralines & ganache", "Caramel, nougat & brittle"],
     "Certificate in Chocolate Artistry"),
    ("BAK-106", "Cupcake & Cake Pops Workshop", "Bakery", "Beginner", 1, 8, 220,
     "Bakehouse", "Weekly",
     ["Moist cupcake base recipes", "Swiss meringue buttercream",
      "Piping swirls & decorative toppings", "Cake pop dipping & display"],
     "Certificate of Completion"),
    ("BAK-107", "Bread Making Fundamentals", "Bakery", "Beginner", 3, 18, 480,
     "Bakehouse", "Jan, Apr, Jul, Oct",
     ["Yeast, flour & gluten science", "Kneading, proofing & baking basics",
      "White, wholemeal & enriched loaves", "Soft rolls, focaccia & dinner buns"],
     "Certificate in Bread Baking"),
    ("BAK-108", "Cookie & Biscuit Baking", "Bakery", "Beginner", 1, 8, 180,
     "Bakehouse", "Weekly",
     ["Drop, rolled & piped cookies", "Achieving chewy vs crisp textures",
      "Shortbread & sablé biscuits", "Icing & decorating cookies"],
     "Certificate of Completion"),
    ("BAK-109", "Pie & Tart Specialist", "Bakery", "Intermediate", 3, 18, 560,
     "Bakehouse", "Mar, Jul, Nov",
     ["Shortcrust, sweet & puff pastry", "Blind baking & avoiding soggy bases",
      "Fruit, custard & savoury fillings", "Lattice tops & decorative crimping"],
     "Certificate in Pastry Making"),
    ("BAK-110", "Korean & Asian Bakery", "Bakery", "Intermediate", 4, 24, 720,
     "Bakehouse", "Feb, Jun, Oct",
     ["Soft milk bread & tangzhong method", "Cream buns, garlic bread & soboro",
      "Castella & chiffon cakes", "Mochi, daifuku & Asian desserts"],
     "Certificate in Asian Baking"),
    ("CUL-201", "Italian Cuisine Mastery", "Cooking", "Intermediate", 6, 36, 1180,
     "Culinary", "Feb, Jun, Oct",
     ["Fresh pasta & gnocchi from scratch", "Risotto, sauces & ragù",
      "Wood-fired style pizza & focaccia", "Antipasti, secondi & dolci"],
     "Diploma in Italian Cooking"),
    ("CUL-202", "Thai Street Food Cooking", "Cooking", "Beginner", 3, 18, 540,
     "Culinary", "Monthly",
     ["Curry pastes & balancing flavours", "Pad Thai, pad krapow & stir-fries",
      "Tom yum & tom kha soups", "Mango sticky rice & Thai desserts"],
     "Certificate in Thai Cuisine"),
    ("CUL-203", "Japanese Sushi & Sashimi", "Cooking", "Intermediate", 4, 24, 980,
     "Culinary", "Jan, May, Sep",
     ["Sushi rice seasoning & handling", "Fish selection, breakdown & knife work",
      "Nigiri, maki & temaki rolling", "Sashimi plating & food safety"],
     "Certificate in Japanese Cuisine"),
    ("CUL-204", "French Culinary Foundations", "Cooking", "Beginner", 8, 48, 1580,
     "Culinary", "Feb, Sep",
     ["The five mother sauces", "Stocks, soups & emulsions",
      "Classic meat, poultry & fish cookery", "Mise en place & kitchen discipline"],
     "Diploma in French Cuisine"),
    ("CUL-205", "Chinese Wok Cooking", "Cooking", "Beginner", 3, 18, 520,
     "Culinary", "Monthly",
     ["Mastering wok hei & high-heat control", "Stir-fry, steaming & braising",
      "Classic dishes: kung pao, mapo tofu", "Fried rice, noodles & sauces"],
     "Certificate in Chinese Cooking"),
    ("CUL-206", "Indian Curry & Spices", "Cooking", "Beginner", 3, 18, 500,
     "Culinary", "Mar, Jul, Nov",
     ["Spice blending & tempering (tadka)", "North & South Indian curries",
      "Biryani, dal & flatbreads", "Vegetarian & tandoori-style dishes"],
     "Certificate in Indian Cuisine"),
    ("CUL-207", "Healthy Meal Prep & Nutrition", "Cooking", "Beginner", 2, 12, 360,
     "Culinary", "Monthly",
     ["Macro & portion planning", "Batch cooking & storage",
      "Balanced bowls, salads & proteins", "Low-sugar & low-sodium swaps"],
     "Certificate in Healthy Cooking"),
    ("CUL-208", "Vegetarian & Vegan Cuisine", "Cooking", "Beginner", 3, 18, 540,
     "Culinary", "Feb, Jun, Oct",
     ["Plant-based proteins & tofu mastery", "Dairy-free sauces & cheeses",
      "Global vegan mains & bowls", "Flavour layering without meat"],
     "Certificate in Plant-Based Cooking"),
    ("CUL-209", "Grilling & BBQ Mastery", "Cooking", "Intermediate", 2, 12, 460,
     "Culinary", "Mar, Jun, Sep, Dec",
     ["Direct vs indirect grilling", "Low-and-slow smoking & rubs",
      "Steaks, ribs, seafood & veg", "Marinades, glazes & BBQ sauces"],
     "Certificate in Grilling & BBQ"),
    ("CUL-210", "Knife Skills & Kitchen Essentials", "Cooking", "Beginner", 1, 8, 160,
     "Culinary", "Weekly",
     ["Knife grip, sharpening & safety", "Classic cuts: julienne, brunoise, chiffonade",
      "Mise en place & station setup", "Basic stocks & flavour building"],
     "Certificate of Completion"),
]


def build(c):
    (code, title, cat, level, weeks, hours, fee, campus_key, intakes, learn, cert) = c
    loc = CAMPUSES[campus_key]
    learn_lines = "\n".join(f"  - {x}" for x in learn)
    per_week = round(hours / weeks)
    return f"""================================================================
{title.upper()}
Cooking & Bakery Training Center  |  Course Brochure
================================================================

Course Code   : {code}
Category      : {cat}
Skill Level   : {level}

----------------------------------------------------------------
COURSE SUMMARY
----------------------------------------------------------------
The {title} programme is a hands-on, {cat.lower()} course designed for
{level.lower()} learners who want to gain practical, job-ready skills under the
guidance of professional chefs. Every session is conducted in a fully
equipped studio kitchen with small class sizes (max 12 students) so each
learner gets individual attention and plenty of practice.

----------------------------------------------------------------
KEY DETAILS
----------------------------------------------------------------
Duration      : {weeks} week(s)  ({hours} hours total, approx. {per_week} hours/week)
Course Fee    : SGD ${fee} (includes ingredients, apron & take-home recipes)
Location      : {loc}
Intake Dates  : {intakes}
Class Size    : Maximum 12 students
Certification : {cert}

----------------------------------------------------------------
WHAT YOU WILL LEARN
----------------------------------------------------------------
{learn_lines}

----------------------------------------------------------------
WHO SHOULD ATTEND
----------------------------------------------------------------
Home cooks and baking enthusiasts, aspiring entrepreneurs planning a home
business or cafe, and anyone looking to build a foundation for a career in
the {cat.lower()} industry. No prior experience required for beginner courses.

----------------------------------------------------------------
WHAT'S INCLUDED
----------------------------------------------------------------
  - All ingredients and equipment for in-class practice
  - Printed and digital recipe booklet
  - Branded apron to keep
  - Certificate upon successful completion
  - Take home everything you bake/cook each session

----------------------------------------------------------------
ENROLMENT & ENQUIRIES
----------------------------------------------------------------
Phone   : +65 6888 1234
Email   : enrol@cookbakeacademy.sg
Website : www.cookbakeacademy.sg
Note    : 10% early-bird discount for sign-ups 4 weeks before intake.

(Fees are inclusive of GST. Schedules subject to availability.)
"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    for c in COURSES:
        code, title = c[0], c[1]
        slug = title.lower().replace("&", "and").replace(" ", "_")
        slug = "".join(ch for ch in slug if ch.isalnum() or ch == "_")
        fname = f"{code}_{slug}.txt"
        with open(os.path.join(here, fname), "w") as f:
            f.write(build(c))
        print("wrote", fname)
    print(f"\nDone. {len(COURSES)} brochures generated.")


if __name__ == "__main__":
    main()
