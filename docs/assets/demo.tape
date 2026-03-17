# CertPepper demo — generates docs/assets/demo.gif
# Requires: VHS (https://github.com/charmbracelet/vhs)
#
# Before recording:
#   cd /path/to/cert-pepper
#   cp .env.example .env
#   uv sync
#   uv run cert-pepper db init
#   uv run cert-pepper ingest
#
# Then: vhs docs/assets/demo.tape

Output docs/assets/demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1200
Set Height 650
Set Padding 16
Set Theme "Dracula"
Set TypingSpeed 40ms

# --- Study session (3 questions) ---
Type "uv run cert-pepper study --count 3 --no-ai"
Enter
Sleep 3s

# Answer Q1
Type "B"
Enter
Sleep 1.5s

# FSRS rating
Type "3"
Enter
Sleep 2s

# Answer Q2
Type "A"
Enter
Sleep 1.5s

# FSRS rating
Type "3"
Enter
Sleep 2s

# Answer Q3
Type "C"
Enter
Sleep 1.5s

# FSRS rating
Type "3"
Enter
Sleep 3s

# --- Progress dashboard ---
Type "uv run cert-pepper progress"
Enter
Sleep 5s
