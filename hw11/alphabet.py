class Alphabet:
    def __init__(self, lang, letters):
        self.lang = lang
        self.letters = letters

    def print(self):
        print("Alphabet letters:")
        print(self.letters)

    def letters_num(self):
        return len(self.letters)


class EngAlphabet(Alphabet):

    __letters_num = 26

    def __init__(self):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        super().__init__("En", letters)

    def is_en_letter(self, letter):
        return letter.upper() in self.letters

    def letters_num(self):
        return EngAlphabet.__letters_num

    @staticmethod
    def example():
        return "This is an example text in English."


# =========================
# TESTS (MAIN)
# =========================

eng_alphabet = EngAlphabet()
eng_alphabet.print()

print("\nNumber of letters:")
print(eng_alphabet.letters_num())

print("\nCheck letter 'F':")
print(eng_alphabet.is_en_letter('F'))

print("\nCheck letter 'Щ':")
print(eng_alphabet.is_en_letter('Щ'))

print("\nExample text:")
print(EngAlphabet.example())