# passwordChecker.py - Rates how strong a password is and says how to improve it.
# Runs entirely on your machine: nothing is saved, printed back, or sent anywhere.

import re, math, getpass

COMMON = {
    'password', '123456', '12345678', '123456789', 'qwerty', 'abc123', 'letmein',
    'monkey', 'dragon', 'football', 'iloveyou', 'admin', 'welcome', 'login',
    'princess', 'sunshine', 'master', 'shadow', 'passw0rd', 'password1',
    'qwerty123', '111111', '000000', '1234567', '12345', '654321',
}

def poolSize(pw):
    # How many different characters an attacker would have to guess from.
    pool = 0
    if re.search(r'[a-z]', pw): pool += 26
    if re.search(r'[A-Z]', pw): pool += 26
    if re.search(r'\d', pw):    pool += 10
    if re.search(r'[^a-zA-Z0-9]', pw): pool += 32
    return pool

def entropyBits(pw):
    # Rough strength: bits = length * log2(pool). Higher is harder to guess.
    pool = poolSize(pw)
    return len(pw) * math.log2(pool) if pool else 0

def hasSequence(pw):
    # Runs like "abc", "123", "cba", "321".
    p = pw.lower()
    for i in range(len(p) - 2):
        a, b, c = ord(p[i]), ord(p[i + 1]), ord(p[i + 2])
        if (b - a == 1 and c - b == 1) or (a - b == 1 and b - c == 1):
            return True
    return False

def check(pw):
    # Returns (rating, bits, list of tips).
    tips = []
    if len(pw) < 12:
        tips.append('Use at least 12 characters (longer is the biggest win).')
    if not re.search(r'[a-z]', pw):
        tips.append('Add lowercase letters.')
    if not re.search(r'[A-Z]', pw):
        tips.append('Add uppercase letters.')
    if not re.search(r'\d', pw):
        tips.append('Add numbers.')
    if not re.search(r'[^a-zA-Z0-9]', pw):
        tips.append('Add symbols like ! ? # $.')
    if re.search(r'(.)\1\1', pw):
        tips.append('Avoid repeating a character 3+ times (like "aaa").')
    if hasSequence(pw):
        tips.append('Avoid sequences like "abc" or "123".')

    bits = entropyBits(pw)
    # Penalize patterns that make guessing much easier than the math suggests.
    if pw.lower() in COMMON:
        bits = min(bits, 10)
        tips.insert(0, 'This is one of the most commonly used passwords!')
    elif any(word in pw.lower() for word in COMMON if len(word) >= 5):
        bits *= 0.6
        tips.insert(0, 'Contains a very common password word.')
    if re.search(r'(.)\1\1', pw): bits *= 0.8
    if hasSequence(pw):           bits *= 0.8

    if bits < 28:   rating = 'Very weak'
    elif bits < 40: rating = 'Weak'
    elif bits < 60: rating = 'Fair'
    elif bits < 80: rating = 'Strong'
    else:           rating = 'Very strong'
    return rating, bits, tips

if __name__ == '__main__':
    # getpass hides what you type. Never pass passwords as command-line arguments:
    # they get saved in your shell history.
    pw = getpass.getpass('Enter a password to check (hidden): ')
    if not pw:
        raise SystemExit('Nothing entered.')
    rating, bits, tips = check(pw)
    print(f'\nLength:  {len(pw)} characters')
    print(f'Rating:  {rating}  (~{bits:.0f} bits)')
    if tips:
        print('\nHow to improve:')
        for tip in tips:
            print(f'  - {tip}')
    else:
        print('\nNo problems found. Nice password!')
