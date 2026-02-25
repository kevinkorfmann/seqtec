# Configuration file for the Sphinx documentation builder.

project = "SeqTec"
copyright = "2026, SeqTec Authors"
author = "SeqTec Authors"
release = "1.0"

extensions = [
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "titles_only": False,
}

# Copy button settings
copybutton_prompt_text = r"^\$ |^>>> |^\.\.\. "
copybutton_prompt_is_regexp = True

# Tabs settings
sphinx_tabs_disable_tab_closing = True
