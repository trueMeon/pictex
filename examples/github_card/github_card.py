"""
PicTex Example: GitHub Repository Card
Demonstrates v2.0 features: positioning, flex properties, size constraints

Usage: Change REPO to any public GitHub repository
"""

import requests
from pictex import *

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION - Change this to generate card for any public repo
# ═══════════════════════════════════════════════════════════════════════════
REPO = "francozanardi/pictex"

# ═══════════════════════════════════════════════════════════════════════════
# FETCH DATA FROM GITHUB API
# ═══════════════════════════════════════════════════════════════════════════
def fetch_repo_data(repo: str) -> dict:
    """Fetch repository data from GitHub API (no auth needed for public repos)"""
    base_url = f"https://api.github.com/repos/{repo}"
    
    # Get repo info
    repo_data = requests.get(base_url).json()
    
    # Get languages
    languages = requests.get(f"{base_url}/languages").json()
    
    return {
        "name": repo_data.get("name", repo.split("/")[-1]),
        "full_name": repo_data.get("full_name", repo),
        "description": repo_data.get("description", "No description provided"),
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "watchers": repo_data.get("subscribers_count", 0),
        "topics": repo_data.get("topics", [])[:6],  # Limit to 6 topics
        "languages": languages,
        "owner_avatar": repo_data.get("owner", {}).get("avatar_url", ""),
    }

def format_number(num: int) -> str:
    """Format large numbers (1234 -> 1.2k)"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)

# ═══════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════
COLORS = {
    "bg": "#0d1117",
    "card_bg": "#161b22",
    "border": "#30363d",
    "text_primary": "#e6edf3",
    "text_secondary": "#8b949e",
    "accent": "#58a6ff",
    "star": "#e3b341",
    "topic_bg": "#388bfd26",
    "topic_text": "#58a6ff",
}

# Language colors (GitHub style)
LANG_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Rust": "#dea584",
    "Go": "#00ADD8",
    "Ruby": "#701516",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C": "#555555",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
}

# ═══════════════════════════════════════════════════════════════════════════
# COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════
def create_topic_tag(topic: str) -> Text:
    """Creates a topic tag pill"""
    return (
        Text(topic)
        .font_size(12)
        .color(COLORS["topic_text"])
        .background_color(COLORS["topic_bg"])
        .padding(4, 10)
        .border_radius(12)
    )

def create_language_bar(languages: dict) -> Row:
    """Creates the language breakdown bar with colored segments"""
    if not languages:
        return Row()
    
    total = sum(languages.values())
    bar_width = 400
    
    segments = []
    for lang, bytes_count in list(languages.items())[:4]:
        percentage = bytes_count / total
        segment_width = max(4, int(bar_width * percentage))  # min_width equivalent
        color = LANG_COLORS.get(lang, "#8b949e")
        
        segment = Row().size(width=segment_width, height=8).background_color(color)
        segments.append(segment)
    
    return Row(*segments).border_radius(4)

def create_language_legend(languages: dict) -> Row:
    """Creates legend showing language percentages"""
    if not languages:
        return Row()
    
    total = sum(languages.values())
    items = []
    
    for lang, bytes_count in list(languages.items())[:4]:  # Top 4 languages
        percentage = (bytes_count / total) * 100
        color = LANG_COLORS.get(lang, "#8b949e")
        
        dot = Row().size(8, 8).background_color(color).border_radius("50%")
        label = Text(f"{lang} {percentage:.1f}%").font_size(12).color(COLORS["text_secondary"])
        
        items.append(Row(dot, label).align_items("center").gap(6))
    
    # flex_wrap() for responsive layout
    return Row(*items).gap(16).flex_wrap("wrap")

def create_stat(icon: str, value: str, label: str, icon_color: str = None) -> Column:
    """Creates a stat column"""
    icon_text = Text(icon).font_size(16)
    if icon_color:
        icon_text.color(icon_color)
    
    return Column(
        Row(
            icon_text,
            Text(value).font_size(18).font_weight(600).color(COLORS["text_primary"])
        ).align_items("center").gap(6),
        Text(label).font_size(12).color(COLORS["text_secondary"])
    ).align_items("center").gap(2)

# ═══════════════════════════════════════════════════════════════════════════
# BUILD THE CARD
# ═══════════════════════════════════════════════════════════════════════════
print(f"Fetching data for {REPO}...")
data = fetch_repo_data(REPO)

# Header: repo icon + name
repo_icon = (
    Text("📁")
    .font_size(32)
    .padding(12)
    .background_color("#21262d")
    .border_radius(8)
)

# Star badge on repo icon (absolute_position - parent relative)
star_badge = (
    Text(f"★ {format_number(data['stars'])}")
    .font_size(11)
    .font_weight(600)
    .color("#ffffff")
    .background_color(COLORS["star"])
    .padding(2, 8)
    .border_radius(10)
    .absolute_position(top=-8, right=-12)
)

repo_icon_with_badge = Row(repo_icon, star_badge)

repo_name = (
    Text(data["full_name"])
    .font_size(20)
    .font_weight(600)
    .color(COLORS["accent"])
)

header = Row(repo_icon_with_badge, repo_name).align_items("center").gap(16)

# Description (flex_grow to fill available space)
description = (
    Text(data["description"] or "No description")
    .font_size(14)
    .color(COLORS["text_secondary"])
    .line_height(1.5)
)

# Topics with flex_wrap
topics_row = Row()
if data["topics"]:
    topic_tags = [create_topic_tag(t) for t in data["topics"]]
    topics_row = Row(*topic_tags).gap(8).flex_wrap("wrap")

# Language bar
lang_section = Column(
    create_language_bar(data["languages"]),
    create_language_legend(data["languages"])
).gap(12 if data["languages"] else 0)

# Stats row (needs width for justify_content to work)
stats_row = Row(
    create_stat("⭐", format_number(data["stars"]), "stars", COLORS["star"]),
    create_stat("🍴", format_number(data["forks"]), "forks"),
    create_stat("👁", format_number(data["watchers"]), "watching"),
).size(width="100%").justify_content("space-around")

# Main card
card = (
    Column(
        header,
        description,
        topics_row,
        lang_section,
        stats_row,
    )
    .size(width=480)
    .gap(20)
    .padding(24)
    .background_color(COLORS["card_bg"])
    .border(1, COLORS["border"])
    .border_radius(12)
)

# Trending badge (fixed_position - canvas relative)
# Only show if repo has 1000+ stars
trending_badge = None
if data["stars"] >= 1000:
    trending_badge = (
        Text("🔥 TRENDING")
        .font_size(12)
        .font_weight(700)
        .color("#ffffff")
        .background_color("#f85149")
        .padding(6, 12)
        .border_radius(0, 0, 0, 8)
        .fixed_position(top=0, right=0)
    )

# Canvas
canvas = (
    Canvas()
    .font_family("Arial")
    .background_color(COLORS["bg"])
    .padding(40)
)

# Render with optional trending badge
if trending_badge:
    result = canvas.render(card, trending_badge, scale_factor=4)
else:
    result = canvas.render(card, scale_factor=4)
result.save("github_card.png")

print(f"Generated github_card.png for {data['full_name']}")
