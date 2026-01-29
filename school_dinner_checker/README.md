# 🍽️ Spinney School Lunch Menu Finder

A simple Streamlit web app to find the **school lunch menu** for any given date. Both **standard** and **vegetarian** menus are displayed, with optional ingredient highlighting and the ability to download the menu as a text file.

---

## Features

- Enter a date (`dd/mm` or `dd/mm/yyyy`) to see lunch menus.
- Displays both **Standard** and **Vegetarian** meals.
- Highlight specific words or ingredients (e.g., "potato") in the menu.
- Automatically handles plural variants when highlighting (e.g., `potato → potatoes`).
- Weekend detection: shows a message if no meals are available.

---

## Screenshots

![Menu Finder Screenshot](screenshot.png)  
*Example of the app displaying menus for a selected date.*

---

## Installation

1. Make sure you have Python 3.9+ installed.
2. Install required packages:

```bash
pip install streamlit
```

3. Clone this repository or copy the `app.py` file.
4. Run the app:

```bash
streamlit run app.py
```

5. Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Usage

1. Open the app in your browser.
2. Enter a date in the input field (`dd/mm` or `dd/mm/yyyy`).
3. Optionally, enter a comma-separated list of words to highlight.
4. View the menus for that date.
5. Click the **Download Both Menus as Text** button to save the menu.

---

## File Structure

```
.
├── app.py           # Streamlit application
├── README.md        # This file
└── menus.txt        # Optional sample output
```

---

## Notes

- If the date is on a weekend, the app will indicate that **no meals are available**.
- The menu rotates based on predefined weeks in 2026. If the entered date is not in any menu week, the app will notify the user.
- Highlighted words are **case-insensitive** and include plural forms for better visibility.

---

## License

This project is licensed under the MIT License.  

---

## Acknowledgements

- Streamlit: [https://streamlit.io/](https://streamlit.io/)  
- Inspired by Spinney School lunch menus.

