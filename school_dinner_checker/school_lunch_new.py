import streamlit as st
import re
from datetime import datetime, timedelta

# -----------------------------
# Data Setup
# -----------------------------

SPINNEY_LUNCH1 = {
    "Monday": "Chicken Curry served with Savoury Vegetable Rice",
    "Tuesday": "Pork Sausage in a Crusty Bun served with Jacket Wedges, Crispy Salad Sticks & a Selection of Sauces",
    "Wednesday": "Savoury Mince served with Mash Potato & Seasonal Vegetables",
    "Thursday": "Roast Chicken served with Potatoes, Yorkshire Pudding, Carrots, Cauliflower and Gravy",
    "Friday": "Fish Fingers or Salmon Fish Fingers served with Chips, Garden Peas or Baked Beans & Ketchup",
}

SPINNEY_LUNCH2 = {
    "Monday": "Cheese & Potato Pie served with Peas & Sweetcorn",
    "Tuesday": "Jacket Potato with choice of toppings served with fresh salad",
    "Wednesday": "Fish Fingers served with Creamy Mash Potato & Spaghetti Hoops",
    "Thursday": "Roast Gammon served with Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy",
    "Friday": "Chicken Nuggets served with Chips, Garden Peas or Baked Beans & Ketchup",
}

SPINNEY_LUNCH3 = {
    "Monday": "Meat Wholemeal Pizza served with Baked Baby Potatoes, Peas & Sweetcorn",
    "Tuesday": "Fish Fillet served with Potato Wedges & Seasonal Vegetables",
    "Wednesday": "Beef Bolognese served with Spaghetti, Wholemeal Garlic & Herb bread, Seasonal Vegetables",
    "Thursday": "Roast Pork served with Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy",
    "Friday": "Chicken Burger served with Chips, Garden Peas or Baked Beans & Ketchup",
}

VEG_LUNCH1 = {
    "Monday": "Pasta Twists with Homemade Tomato and Vegetable Sauce served with Fresh Salad and Chunky Bread",
    "Tuesday": "Quorn Sausage in a Crusty Bun served with Jacket Wedges, Crispy Salad Sticks & a Selection of Sauces",
    "Wednesday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
    "Thursday": "Quorn Roast served with Yorkshire Pudding, Carrots, Cauliflower and Gravy",
    "Friday": "Vegetable Nuggets served with Chips, Garden Peas or Baked Beans & Ketchup",   
}

VEG_LUNCH2 = {
    "Monday": "Traditional Macaroni Cheese served with Wholemeal Garlic & Herb bread, Seasonal Vegetables",
    "Tuesday": "Jacket Potato with Cheese & Beans & Fresh Salad",
    "Wednesday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
    "Thursday": "Broccoli & Cauliflower Cheese Bake, Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy",
    "Friday": "Quorn Sausage served with Chips, Garden Peas or Baked Beans & Ketchup",  
}

VEG_LUNCH3 = {
    "Monday": "Pasta Twists with Homemade Tomato and Vegetable Sauce served with Fresh Salad and Chunky Bread",
    "Tuesday": "Crispy Vegetable Bites served with Potatoes Wedges & Seasonal Vegetables",
    "Wednesday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
    "Thursday": "Quorn Sausage Roast served with Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy",
    "Friday": "Vegetable Burger served with Chips, Garden Peas or Baked Beans & Ketchup",
 }

MENU_WEEKS_2026 = {
    "Week 1": ["19/01", "09/02", "09/03"],
    "Week 2": ["26/01", "16/02", "16/03"],
    "Week 3": ["02/02", "02/03", "23/03"],
}

LUNCH_MAP = {
    "Week 1": SPINNEY_LUNCH1,
    "Week 2": SPINNEY_LUNCH2,
    "Week 3": SPINNEY_LUNCH3,
}

VEG_MAP = {
    "Week 1": VEG_LUNCH1,
    "Week 2": VEG_LUNCH2,
    "Week 3": VEG_LUNCH3,
}

# -----------------------------
# Helper Functions
# -----------------------------

def expand_word_variants(words):
    """Add plural variants for highlighting (potato → potatoes, apple → apples)."""
    expanded = set()
    for w in words:
        w = w.lower()
        expanded.add(w)
        if w.endswith("o"):
            expanded.add(w + "es")
        expanded.add(w + "s")
    return list(expanded)

def highlight_text_markdown(text, words):
    """Highlight words in Streamlit using Markdown."""
    if not words:
        return text
    pattern = "|".join(re.escape(w) for w in words)
    return re.sub(pattern, lambda m: f"**:orange[{m.group(0)}]:**", text, flags=re.IGNORECASE)

def parse_user_date(date_str):
    """Parse date dd/mm or dd/mm/yyyy, default year 2026."""
    try:
        if len(date_str) == 5:
            return datetime.strptime(date_str + "/2026", "%d/%m/%Y")
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def determine_menu_week(user_date):
    """Find the menu week for a given date."""
    for week_name, dates in MENU_WEEKS_2026.items():
        for date_str in dates:
            start = datetime.strptime(date_str + "/2026", "%d/%m/%Y")
            end = start + timedelta(days=4)
            if start <= user_date <= end:
                return week_name
    return None

def get_meals_for_date(user_date):
    """Return both standard and vegetarian meals for a date."""
    if user_date.weekday() >= 5:
        return None, None  # No meals on weekends
    week_name = determine_menu_week(user_date)
    if not week_name:
        return None, None
    weekday = user_date.strftime("%A")
    return LUNCH_MAP[week_name].get(weekday), VEG_MAP[week_name].get(weekday)

# -----------------------------
# Streamlit App
# -----------------------------

st.title("🍽️ Spinney School Lunch Menu Finder")
st.write("Enter a date to see the lunch served on that day (standard & vegetarian).")

date_input = st.text_input("Enter a date (dd/mm or dd/mm/yyyy):")
highlight_input = st.text_input("Words to highlight (comma separated):", "potato")

if date_input:
    highlight_words = expand_word_variants([w.strip() for w in highlight_input.split(",") if w.strip()])
    user_date = parse_user_date(date_input)

    if not user_date:
        st.error("❌ Invalid date. Use dd/mm or dd/mm/yyyy.")
        st.stop()

    st.info(f"📅 That date is a **{user_date.strftime('%A')}**.")

    meal_std, meal_veg = get_meals_for_date(user_date)

    if not meal_std and not meal_veg:
        st.warning("❌ No menu available for this date.")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Standard Menu")
        st.markdown(highlight_text_markdown(meal_std, highlight_words) if meal_std else "No meal for this day.")

    with col2:
        st.subheader("Vegetarian Menu")
        st.markdown(highlight_text_markdown(meal_veg, highlight_words) if meal_veg else "No meal for this day.")

   