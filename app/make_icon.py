# MAN'S WAR app icon: night sky over a Kings St. skyline, a yellow crown, "MW" in the title's white-on-red style.
import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 1024
out = sys.argv[1]
# 'casual' = the MW Casual app: sunset sky, teal shadow, so the two icons are easy to tell apart
CASUAL = len(sys.argv) > 2 and sys.argv[2] == 'casual'
SKY = ((255, 120, 90), (90, 40, 120)) if CASUAL else ((38, 58, 96), (10, 14, 20))
SHADOW = (20, 170, 160) if CASUAL else (232, 53, 43)
img = Image.new('RGB', (S, S))
d = ImageDraw.Draw(img)
# sky: navy at the top to almost black at the street
for y in range(S):
    k = y / S
    a, b = SKY; c = tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
    d.line([(0, y), (S, y)], fill=c)

# skyline with lit windows
rnd = random.Random(7)
x = -20
while x < S:
    w = rnd.randint(90, 170); h = rnd.randint(170, 330)
    top = S - h
    d.rectangle([x, top, x + w, S], fill=(14, 16, 24))
    if rnd.random() < 0.35:   # water tower
        tx = x + w // 2
        d.rectangle([tx - 22, top - 52, tx + 22, top - 12], fill=(14, 16, 24))
        d.polygon([(tx - 26, top - 52), (tx, top - 78), (tx + 26, top - 52)], fill=(14, 16, 24))
        d.rectangle([tx - 18, top - 12, tx - 14, top], fill=(14, 16, 24)); d.rectangle([tx + 14, top - 12, tx + 18, top], fill=(14, 16, 24))
    for wy in range(top + 22, S - 10, 34):
        for wx in range(x + 14, x + w - 18, 28):
            if rnd.random() < 0.38:
                d.rectangle([wx, wy, wx + 12, wy + 16], fill=(255, 196, 92) if rnd.random() < 0.8 else (255, 236, 170))
    x += w + rnd.randint(4, 14)

# soft glow behind the letters
glow = Image.new('L', (S, S), 0)
ImageDraw.Draw(glow).ellipse([150, 250, 874, 760], fill=120)
glow = glow.filter(ImageFilter.GaussianBlur(120))
img.paste((255, 220, 120) if CASUAL else (255, 70, 50), (0, 0), glow.point(lambda v: v // 3))

# yellow crown
cx, cy = S // 2, 250
crown = [(cx - 150, cy + 70), (cx - 165, cy - 50), (cx - 80, cy + 10), (cx, cy - 80), (cx + 80, cy + 10), (cx + 165, cy - 50), (cx + 150, cy + 70)]
d.polygon(crown, fill=(242, 183, 5))
d.rectangle([cx - 150, cy + 70, cx + 150, cy + 100], fill=(242, 183, 5))
for px, py in [(cx - 165, cy - 50), (cx, cy - 80), (cx + 165, cy - 50)]:
    d.ellipse([px - 18, py - 18, px + 18, py + 18], fill=(242, 183, 5))

# "MW": red offset shadow, then white, like the title
f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Impact.ttf', 470)
text = 'MW'
bb = d.textbbox((0, 0), text, font=f)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
tx, ty = (S - tw) // 2 - bb[0], 330 - bb[1]
d.text((tx + 22, ty + 18), text, font=f, fill=(20, 8, 8))
d.text((tx + 12, ty + 10), text, font=f, fill=SHADOW)
d.text((tx, ty), text, font=f, fill=(255, 255, 255))
# red rule under it, like the title
d.rectangle([200, ty + th + bb[1] + 40, S - 200, ty + th + bb[1] + 54], fill=SHADOW)

img.save(out)
print('saved', out)
