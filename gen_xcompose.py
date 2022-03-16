#! /usr/bin/python3

from typing import List, Generator, Optional, Tuple

import unicodedata
import sys

small_latin_alphabet = [(chr(ord('A') + i), chr(ord('a') + i))
                        for i in range(26)]
capital_latin_alphabet = [(a, b.upper()) for a, b in small_latin_alphabet]

greek_alphabet = [
    ("alpha", "a"),
    ("beta", "b"),
    ("gamma", "g"),
    ("delta", "d"),
    ("epsilon", "e"),
    ("zeta", "z"),
    ("eta", "h"),
    ("theta", "T"),
    ("iota", "i"),
    ("kappa", "k"),
    ("lamda", "l"),
    ("mu", "m"),
    ("nu", "n"),
    ("xi", "X"),
    ("omicron", "o"),
    ("pi", "p"),
    ("rho", "r"),
    ("sigma", "s"),
    ("tau", "t"),
    ("upsilon", "u"),
    ("phi", "f"),
    ("chi", "x"),
    ("psi", "P"),
    ("omega", "O")
]

greek_small_alphabet = greek_alphabet + [("final sigma", "S")]
greek_capital_alphabet = greek_alphabet  # + [("theta symbol", "S")]

# Other greek-ish characters that we don’t generate for now:
#"partial differential",
#"lunate epsilon symbol",
#"theta symbol",
#"kappa symbol",
#"phi symbol",
#"rho symbol",
#"pi symbol",
#"nabla"


digits = [
    ("zero", "0"),
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9")
]

latin_fonts = [
    ("bold", "b"),
    ("italic", "i"),
    ("bold italic", "I"),
    ("script", "s"),
    ("bold script", "S"),
    ("fraktur", "f"),
    ("double-struck", "B"),
    ("bold fraktur", "F"),
    ("monospace", "m"),
    ("sans-serif", "a"),
    ("sans-serif bold", "A"),
    ("sans-serif italic", "n"),
    ("sans-serif bold italic", "N"),
]

greek_fonts = [
    ("GREEK", "g"),
    ("bold", "b"),
    ("italic", "i"),
    ("bold italic", "I"),
    ("sans-serif bold", "A"),
    ("sans-serif bold italic", "N"),
]

digit_fonts = [
    ("bold", "b"),
    ("double-struck", "B"),
    ("monospace", "m"),
    ("sans-serif", "a"),
    ("sans-serif bold", "A"),
]


def lookup_char(kind: str, case: str, letter: str) -> Optional[str]:
    if kind == "GREEK":
        return unicodedata.lookup(f"GREEK {case} LETTER {letter}")
    try:
        return unicodedata.lookup(f"MATHEMATICAL {kind} {case} {letter}")
    except KeyError:
        pass
    try:
        return unicodedata.lookup(f"{kind} {case} {letter}")
    except KeyError:
        pass
    if kind == 'FRAKTUR':
        try:
            return unicodedata.lookup(f"BLACK-LETTER {case} {letter}")
        except KeyError:
            pass
    elif (kind, case, letter) == ('ITALIC', 'SMALL', 'H'):
        return unicodedata.lookup(f"planck constant")
    return None


def gen_compositions(
        kind: str, compose_char: str, indicator: str, case: str, alphabet: List[Tuple[str, str]]) -> Generator[str, None, None]:
    yield f"\n# {kind.lower()} {case.lower()} letter ⟨{compose_char}⟩:"
    for letter, key in alphabet:
        character: Optional[str] = None
        character = lookup_char(kind, case, letter)
        if character is None:
            print(
                f"Error failed to find “{kind}” version of {case} {letter}",
                file=sys.stderr)
            yield f"#<Multi_key> <f> {indicator}<{compose_char}> <{key}> : TODO"
            continue
        if kind == "GREEK":
            yield f"<Multi_key> {indicator}<{key}> : \"{character}\""
        else:
            yield f"<Multi_key> <f> {indicator}<{compose_char}> <{key}> : \"{character}\""


def main(_: List[str]) -> int:
    for indicator, case, alphabet, fonts in [("", "CAPITAL", capital_latin_alphabet, latin_fonts),
                                             ("", "SMALL", small_latin_alphabet,
                                              latin_fonts),
                                             ("<g> ", "SMALL",
                                              greek_small_alphabet, greek_fonts),
                                             ("<G> ",
                                              "CAPITAL",
                                              greek_capital_alphabet,
                                              greek_fonts),
                                             ("", "DIGIT", digits, digit_fonts)]:
        for kind, compose_char in fonts:
            for s in gen_compositions(
                    kind.upper(), compose_char, indicator, case, alphabet):
                print(s)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print("Error: {}".format(e))
        sys.exit(-1)
