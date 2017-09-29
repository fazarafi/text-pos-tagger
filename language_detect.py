from polyglot.text import Text

blob = """We will meet at eight o'clock on Thursday morning."""
text = Text(blob)

print(text.pos_tags)
