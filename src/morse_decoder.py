MORSE_MAP = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D",
    ".": "E", "..-.": "F", "--.": "G", "....": "H",
    "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P",
    "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}


def decode_morse(symbols):
    """Convert a Morse sequence into a character."""
    return MORSE_MAP.get(symbols, "?")


def is_valid_morse(symbols):
    """Check whether a Morse sequence exists in the dictionary."""
    return symbols in MORSE_MAP