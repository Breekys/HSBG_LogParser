from re import finditer
for match in finditer("pattern", "string"):
    print(match.span(), match.group())