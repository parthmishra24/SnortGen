from questionary import Style

custom_style = Style([
    ("qmark", "fg:#87ceeb"),               # subtle blue question mark
    ("question", "fg:#ffffff"),            # plain white question text
    ("answer", "fg:#ffffff bold"),         # white answer text
    ("pointer", "fg:#ffffff bold"),        # white pointer ">"
    ("highlighted", "fg:#ffffff bg:#4e4e4e"),  # white on dark gray
    ("selected", "fg:#ffffff bg:#4e4e4e"),     # same as highlighted
    ("instruction", "fg:#b0b0b0 italic"),   # muted gray instruction
    ("text", "fg:#ffffff"),                # regular white input
    ("disabled", "fg:#808080 italic")      # gray italic for disabled
])
