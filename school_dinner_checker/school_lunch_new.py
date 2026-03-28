import streamlit as st
import re
from datetime import datetime, timedelta, date

# -----------------------------
# Page config (MUST be first)
# -----------------------------
st.set_page_config(
    page_title="Spinney School Lunch Menu",
    layout="wide",
)

# -----------------------------
# iPhone-optimised CSS
# -----------------------------
st.markdown(
    """
    <style>
    /* ---- Base font tuning (iPhone-friendly) ---- */
    html, body, [class*="css"] {
        font-size: 14px;
        -webkit-text-size-adjust: 100%;
    }

    /* ---- Headings ---- */
    h1 { 
        font-size: 1.5rem; 
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }

    h2 { 
        font-size: 1.15rem; 
        margin-top: 1rem;
    }

    h3 { 
        font-size: 1.05rem; 
    }

    /* ---- Reduce vertical padding ---- */
    .block-container {
        padding-top: 0.75rem;
        padding-bottom: 0.75rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* ---- Buttons: Apple tap target size ---- */
    button {
        min-height: 44px;
        font-size: 0.95rem;
    }

    /* ---- Inputs ---- */
    input {
        font-size: 0.95rem;
    }

    /* ---- Alerts ---- */
    .stAlert {
        font-size: 0.9rem;
        padding: 0.5rem;
    }

    /* ---- Slightly smaller text on small iPhones ---- */
    @media (max-width: 430px) {
        html, body {
            font-size: 13.5px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data Setup
# -----------------------------

SPINNEY_LUNCH1_CHOICE_1 = {
    "Monday": "Rainbow Wholemeal Pizza served with Jacket Potato Wedges, Crunchy Carrot & Cucumber Sticks(V)",
    "Tuesday": "Jacket Potato with Choice of Toppings served with Fresh Salad(V)",
    "Wednesday": "Roasted Vegetable & Lentil Lasagne served with Wholemeal Garlic & Herb Bread, Mixed Vegetables or Salad(V)",
    "Thursday": "Quorn Fillet served with Roast Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy(V)",
    "Friday": "Fish Fingers or Salmon Fish Fingers served with Chips, Garden Peas or Baked Beans & Ketchup",
}
SPINNEY_LUNCH2_CHOICE_1 = {
    "Monday": "Butternut Squash & Cauliflower Korma served with Rice, Naan Bread finger & Seasonal Vegetables(V)",
    "Tuesday": "Margherita Wholemeal Pizza Pinwheel served with Baked Potato Wedges, Peas & Sweetcorn(V)",
    "Wednesday": "Powerballs in a Tomato Sauce served with Pasta, Homemade Wholemeal Garlic & Herb Bread and Seasonal Vegetables(VE)",
    "Thursday": "Crispy Topped Baked Lentil Roast served with Potatoes, Yorkshire Pudding, Carrots, Broccoli and Gravy(V)",
    "Friday": "Breaded Fish Fillet served with Chips, Garden Peas or Baked Beans & Ketchup",
}
SPINNEY_LUNCH3_CHOICE_1 = {
    "Monday": "Mild Tex Mex Bean Taco served with Savoury Vegetable Rice(VE)",
    "Tuesday": "Jacket Potato with Choice of Toppings served with Fresh Salad(V)",
    "Wednesday": "Big Bold Vegetable & Lentil Bolognese served with Spaghetti, Garlic & Herb Bread and Seasonal Vegetables(VE)",
    "Thursday": "Herby Quorn Sausage served with Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy(V)",
    "Friday": "Vegetable Burger in a Bun served with Chips, Garden Peas or Baked Beans & Ketchup(V)",
}
SPINNEY_LUNCH1_CHOICE_2 = {
    "Monday": "Jambalaya Jamboree served with Crusty Wholemeal Bread & Salad(VE)",
    "Tuesday": "Baked Pork Sausage Roll served with Seasoned Cubed Potatoes & Baked Beans or Fresh Salad",
    "Wednesday": "Homemade Beef Lasagne served with Wholemeal Garlic & Herb Bread, Mixed Vegetables or Salad",
    "Thursday": "Roast Chicken served with Roast Potatoes, Carrots, Cabbage, Yorkshire Pudding and Gravy",
    "Friday": "Quorn Sausage served with Chips, Garden Peas or Baked Beans & Ketchup(VE)",
}
SPINNEY_LUNCH2_CHOICE_2 = {
    "Monday": "Traditional Macaroni Cheese served with Wholemeal Garlic & Herb Bread and Seasonal Vegetables(V)",
    "Tuesday": "Chicken Wholemeal Pizza Pinwheel served with Baked Potato Wedges, Peas & Sweetcorn",
    "Wednesday": "Meatballs in a Tomato Sauce served with Pasta, Homemade Wholemeal Garlic & Herb Bread and Seasonal Vegetables",
    "Thursday": "Roast Chicken served with Potatoes, Yorkshire Pudding, Carrots, Broccoli and Gravy",
    "Friday": "Vegetable Nuggets served with Chips, Garden Peas or Baked Beans & Ketchup(VE)",
}
SPINNEY_LUNCH3_CHOICE_2 = {
    "Monday": "Margherita Wholemeal Pizza served with Savoury Vegetable Rice Salad(V)",
    "Tuesday": "Lunchtime Breakfast Brunch - Pork Sausage, Bacon, Hash Browns & Baked Beans",
    "Wednesday": "Beef Bolognese Pasta served with Garlic & Herb Bread and Seasonal Vegetables",
    "Thursday": "Roast Pork served with Roast Potatoes, Carrots, Broccoli, Yorkshire Pudding and Gravy",
    "Friday": "Chicken Burger in a Bun served with Fries, Garden Peas or Baked Beans & Ketchup",
}

MENU_WEEKS_2026 = {
    "Week 1": ["13/04", "04/05", "01/06","22/06", "13/07", "31/08", "21/09", "12/10"],
    "Week 2": ["20/04", "11/05", "08/06", "29/06", "20/07", "07/09", "28/09", "19/10"],
    "Week 3": [ "27/04", "18/05","15/06", "06/07", "14/09", "05/10"],
}

LUNCH_MAP = {
    "Week 1": SPINNEY_LUNCH1_CHOICE_1,
    "Week 2": SPINNEY_LUNCH2_CHOICE_1,
    "Week 3": SPINNEY_LUNCH3_CHOICE_1,
}

VEG_MAP = {
    "Week 1": SPINNEY_LUNCH1_CHOICE_2,
    "Week 2": SPINNEY_LUNCH2_CHOICE_2,
    "Week 3": SPINNEY_LUNCH3_CHOICE_2,
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
        else:
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
# App UI
# -----------------------------

st.title("🍽️ Spinney School Lunch Menu Finder")

MENU_START = date(2026, 4, 13)
MENU_END   = date(2026, 10, 23)

if "selected_date" not in st.session_state:
    today = date.today()
    st.session_state.selected_date = max(MENU_START, min(today, MENU_END))

selected_date = st.date_input(
    "📅 Pick a date (13/04/2026–23/10/2026)",
    value=st.session_state.selected_date,
    min_value=MENU_START,
    max_value=MENU_END,
    format="DD/MM/YYYY",
)
st.session_state.selected_date = selected_date

user_date = datetime.combine(selected_date, datetime.min.time())
st.caption(f"📅 {user_date.strftime('%A')}")

# -----------------------------
# Navigation Buttons
# -----------------------------

if st.button("⬅️ Previous day", use_container_width=True):
    prev_day = selected_date - timedelta(days=1)
    if prev_day >= date(2026, 4, 13):
        st.session_state.selected_date = prev_day
        st.rerun()

if st.button("Next day ➡️", use_container_width=True):
    next_day = selected_date + timedelta(days=1)
    if next_day <= date(2026, 10, 23):
        st.session_state.selected_date = next_day
        st.rerun()

# -----------------------------
# Highlight Input
# -----------------------------

with st.expander("🔍 Highlight words (potato by default)"):
    highlight_input = st.text_input(
        "Comma separated words",
        "potato",
        label_visibility="collapsed",
    )

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

st.subheader("1st Choice Menu")
st.markdown(
    highlight_text_markdown(meal_std, highlight_words)
    if meal_std else "No meal for this day."
)

st.subheader("2nd Choice Menu")
st.markdown(
    highlight_text_markdown(meal_veg, highlight_words)
    if meal_veg else "No vegetarian meal for this day."
)
