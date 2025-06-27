def count_vowels(s):
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

def count_letters(s):
    return sum(1 for char in s if char.isalpha()) 