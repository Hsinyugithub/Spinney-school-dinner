import streamlit as st
import re
from datetime import datetime, timedelta, date

# -----------------------------
# Mobile‑Friendly Styling
# -----------------------------

st.markdown("""
    <style>
    /* Reduce padding on mobile */
    @media (max-width: 600px) {
        .block-container {
            padding: 0.8rem 1rem !important;
        }

        h1, h2, h3 {
            font-size: 1.2rem !important;
        }

        label, .stRadio label {
            font-size: 0.9rem !important;
        }

        input[type="date"] {
            font-size: 0.9rem !important;
        }
    }

    /* Smaller button style */
    .small-button button {
        padding: 0.4rem 0.7rem !important;
        font-size: 0.9rem !important;
        border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Data Setup
# -----------------------------

SPINNEY_LUNCH1 = {
    "Monday": "Chicken Curry served with Savoury Vegetable Rice",
    "Tuesday": "Pork Sausage in a Crusty Bun served with Jacket Wedges, Crispy Salad Sticks &amp; a Selection of Sauces",
    "Wednesday": "Savoury Mince served with Mash Potato &amp; Seasonal Vegetables",
    "Thursday": "Roast Chicken served with Potatoes, Yorkshire Pudding, Carrots, Cauliflower and Gravy",
    "Friday": "Fish Fingers or Salmon Fish Fingers served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
}

SPINNEY_LUNCH2 = {
    "Monday": "Cheese &amp; Potato Pie served with Peas &amp; Sweetcorn",
    "Tuesday": "Jacket Potato with choice of toppings served with fresh salad",
    "Wednesday": "Fish Fingers served with Creamy Mash Potato &amp; Spaghetti Hoops",
    "Thursday": "Roast Gammon served with Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy",
    "Friday": "Chicken Nuggets served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
}

SPINNEY_LUNCH3 = {
    "Monday": "Meat Wholemeal Pizza served with Baked Baby Potatoes, Peas &amp; Sweetcorn",
    "Tuesday": "Fish Fillet served with Potato Wedges &amp; Seasonal Vegetables",
    "Wednesday": "Beef Bolognese served with Spaghetti, Wholemeal Garlic &amp; Herb bread, Seasonal Vegetables",
    "Thursday": "Roast Pork served with Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy",
    "Friday": "Chicken Burger served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
}

VEG_LUNCH1 = {
    "Monday": "Vegetable Nuggets served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
    "Tuesday": "Quorn Roast served with Yorkshire Pudding, Carrots, Cauliflower and Gravy",
    "Wednesday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
    "Thursday": "Quorn Sausage in a Crusty Bun served with Jacket Wedges, Crispy Salad Sticks &amp; a Selection of Sauces",
    "Friday": "Pasta Twists with Homemade Tomato and Vegetable Sauce served with Fresh Salad and Chunky Bread",
}

VEG_LUNCH2 = {
    "Monday": "Quorn Sausage served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
    "Tuesday": "Jacket Potato with Cheese &amp; Beans &amp; Fresh Salad",
    "Wednesday": "Traditional Macaroni Cheese served with Wholemeal Garlic &amp; Herb bread, Seasonal Vegetables",
    "Thursday": "Broccoli &amp; Cauliflower Cheese Bake, Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy",
    "Friday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
}

VEG_LUNCH3 = {
    "Monday": "Vegetable Burger served with Chips, Garden Peas or Baked Beans &amp; Ketchup",
    "Tuesday": "Quorn Sausage Roast served with Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy",
    "Wednesday": "Jacket Potato with Choice of Toppings served with Fresh Salad",
    "Thursday": "Crispy Vegetable Bites served with Potatoes Wedges &amp; Seasonal Vegetables",
    "Friday": "Pasta Twists with Homemade Tomato and Vegetable Sauce served with Fresh Salad and Chunky Bread",
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
    expanded = set()
    for w in words:
        w = w.lower()
        expanded.add(w)
        if w.endswith("o"):
            expanded.add(w + "es")
        expanded.add(w + "s")
    return list(expanded)

def highlight_text_markdown(text, words):
    if not words:
        return text
    pattern = "|".join(re.escape(w) for w in words)
    return re.sub(
        pattern,
        lambda m: f"**:orange[{m.group(0)}]:**",
        text,
        flags=re.IGNORECASE,
    )

def determine_menu_week(user_date):
    for week_name, dates in MENU_WEEKS_2026.items():
        for date_str in dates:
            start = datetime.strptime(date_str + "/2026", "%d/%m/%Y")
            end = start + timedelta(days=4)
            if start <= user_date <= end:
                return week_name
    return None

def get_meals_for_date(user_date):
    if user_date.weekday() >= 5:
        return None, None
    week_name = determine_menu_week(user_date)
    if not week_name:
        return None, None
    weekday = user_date.strftime("%A")
    return (
        LUNCH_MAP[week_name].get(weekday),
        VEG_MAP[week_name].get(weekday),
    )

# -----------------------------
# Streamlit App
# -----------------------------

st.title("🍽️ Spinney School Lunch Menu Finder")

# --- Session date tracking ---
if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

# --- Date input ---
selected_date = st.date_input(
    "Choose a date (01/01/2026–31/03/2026)",
    value=st.session_state.selected_date,
    min_value=datetime(2026, 1, 1),
    max_value=datetime(2026, 3, 31),
    format="DD/MM/YYYY",
)
st.session_state.selected_date = selected_date

user_date = datetime.combine(st.session_state.selected_date, datetime.min.time())
st.info(f"📅 That date is a **{user_date.strftime('%A')}**.")

# -----------------------------
# Buttons (mobile‑friendly)
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="small-button">', unsafe_allow_html=True)
    if st.button("← Previous Day", key="prev"):
        prev_day = st.session_state.selected_date - timedelta(days=1)
        if prev_day >= date(2026, 1, 1):
            st.session_state.selected_date = prev_day
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-button">', unsafe_allow_html=True)
    if st.button("Next Day →", key="next"):
        next_day = st.session_state.selected_date + timedelta(days=1)
        if next_day <= date(2026, 3, 31):
            st.session_state.selected_date = next_day
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Menu Choice
# -----------------------------

menu_choice = st.radio(
    "Choose which menu to show:",
    ["Standard", "Vegetarian", "Both"],
    index=2,
)

highlight_input = st.text_input("Words to highlight (comma separated):", "potato")
highlight_words = expand_word_variants(
    [w.strip() for w in highlight_input.split(",") if w.strip()]
)

meal_std, meal_veg = get_meals_for_date(user_date)

if not meal_std and not meal_veg:
    st.warning("❌ No menu available for this date.")
    st.stop()

# -----------------------------
# Menu Display
# -----------------------------

if menu_choice in ["Standard", "Both"]:
    st.subheader("Standard Menu")
    st.markdown(highlight_text_markdown(meal_std, highlight_words))

if menu_choice in ["Vegetarian", "Both"]:
    st.subheader("Vegetarian Menu")
    st.markdown(highlight_text_markdown(meal_veg, highlight_words))