s = open('alex.py', 'r').read()
i = s.find("print('''DOOM")
print(i)
print(s[i - 100:i + 100])

for j in range(i - 100, i + 100):
    print(j, '"%s"' % s[j:j+2], s[j:j+2] == r"\ ")

print(i)
print("trying to find ...")
for j in range(0, len(s)):
    if s[j:j+2] == r"\ ":
        print("FOUND ... j:", j)
        
