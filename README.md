# Password Strength Checker

A small Python script that rates how strong a password is and suggests how to improve it.

- Estimates strength in bits from length and character variety
- Penalizes common passwords, repeated characters and sequences like `abc` / `123`
- Input is hidden with `getpass`; nothing is saved or sent anywhere

## Usage

```
python passwordChecker.py
```

Requires Python 3. No third-party packages.
