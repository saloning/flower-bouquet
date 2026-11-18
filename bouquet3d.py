"""
ASCII 3D Flower Bouquet
-----------------------
A separate animated window showing a colourful, character-built bouquet.
The bouquet rotates continuously in 3D.

Run:
    python3 bouquet3d.py

Controls:
    Click / Space : pause or resume
    Left / Right  : rotate manually while paused
    Escape        : close
"""

import math
import random
import tkinter as tk

BG = "#202433"
PALETTE = {
    "pink": "#ff68b4",
    "hotpink": "#f43d9c",
    "blush": "#ffb0d1",
    "red": "#ff454b",
    "orange": "#ff963d",
    "yellow": "#ffe34f",
    "gold": "#ffbd39",
    "purple": "#bd82ff",
    "lilac": "#e0b4ff",
    "white": "#f3f0eb",
    "green": "#70e66f",
    "lime": "#a0f078",
    "deepgreen": "#299d61",
    "leaflight": "#b0f28b",
    "paper": "#c9c9bd",
    "paperdark": "#858c91",
    "ribbon": "#ff6cae",
    "spark": "#f6f4ff",
}

# Each point is x, y, z, glyph, colour, point-size.
POINTS = []


def put(x, y, z, glyph, colour, size=10):
    POINTS.append((x, y, z, glyph, PALETTE.get(colour, colour), size))


def mix(a, b, t):
    return a * (1 - t) + b * t


def add_line(a, b, colour, glyph="|", count=45, size=10):
    for i in range(count + 1):
        t = i / count
        p = [mix(a[k], b[k], t) for k in range(3)]
        put(*p, glyph, colour, size)


def add_leaf(base, direction, length, width, phase=0):
    """A broad, pointed leaf with ASCII texture and a central vein."""
    dx, dy, dz = direction
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    dx, dy, dz = dx/mag, dy/mag, dz/mag
    sx, sy, sz = -dy, dx, 0.18
    sm = math.sqrt(sx*sx + sy*sy + sz*sz)
    sx, sy, sz = sx/sm, sy/sm, sz/sm
    for i in range(22):
        t = i / 21
        half = width * math.sin(math.pi*t)**0.8
        cx = base[0] + dx*length*t
        cy = base[1] + dy*length*t
        cz = base[2] + dz*length*t + 0.10*math.sin(math.pi*t)
        for j in range(-4, 5):
            q = j / 4
            x = cx + sx*half*q
            y = cy + sy*half*q
            z = cz + sz*half*q
            glyph = "~" if j == 0 else ("*" if (i+j+phase) % 5 == 0 else ".")
            col = "leaflight" if abs(q) < 0.55 and i % 3 == 0 else "green"
            put(x, y, z, glyph, col, 9 if j == 0 else 8)
    add_line(base, (base[0]+dx*length, base[1]+dy*length,
                    base[2]+dz*length), "deepgreen", "·", 28, 8)


def add_flower(center, color, radius=0.62, petals=10, tilt=(0, -0.1, 1)):
    """A layered flower, sampled as curved petal surfaces."""
    cx, cy, cz = center
    tx, ty, tz = tilt
    tm = math.sqrt(tx*tx + ty*ty + tz*tz)
    nx, ny, nz = tx/tm, ty/tm, tz/tm
    # Face basis vectors.
    rx, ry, rz = 1.0, 0.0, -nx/max(0.3, nz)
    rm = math.sqrt(rx*rx + ry*ry + rz*rz)
    rx, ry, rz = rx/rm, ry/rm, rz/rm
    ux, uy, uz = (ny*rz-nz*ry, nz*rx-nx*rz, nx*ry-ny*rx)
    alternate = {
        "pink": "blush", "hotpink": "pink", "red": "orange",
        "orange": "yellow", "yellow": "gold", "purple": "lilac"
    }.get(color, "blush")

    inner = {
        "pink": "hotpink", "hotpink": "blush", "red": "hotpink",
        "orange": "red", "yellow": "orange", "purple": "pink",
        "white": "lilac"
    }.get(color, alternate)
    for layer, (count, r, w, col) in enumerate([
        (petals + 2, radius, 0.34*radius, color),
        (max(8, petals), radius*0.80, 0.27*radius, alternate),
        (max(7, petals-3), radius*0.57, 0.19*radius, inner)
    ]):
        for p in range(count):
            angle = 2*math.pi*p/count + layer*0.19
            vx = math.cos(angle)*rx + math.sin(angle)*ux
            vy = math.cos(angle)*ry + math.sin(angle)*uy
            vz = math.cos(angle)*rz + math.sin(angle)*uz
            wx = -math.sin(angle)*rx + math.cos(angle)*ux
            wy = -math.sin(angle)*ry + math.cos(angle)*uy
            wz = -math.sin(angle)*rz + math.cos(angle)*uz
            for i in range(17):
                t = i/16
                half = w*math.sin(math.pi*t)**0.75
                for j in range(-4, 5):
                    q = j/4
                    along = radius*(0.12 + 0.98*t)
                    across = half*q
                    cup = radius*(0.12*math.sin(math.pi*t) + 0.07*t*t)
                    x = cx + vx*along + wx*across + nx*cup
                    y = cy + vy*along + wy*across + ny*cup
                    z = cz + vz*along + wz*across + nz*cup
                    glyph = ("*" if abs(q) < 0.72 else
                             ("·" if (i+j) % 2 else "."))
                    put(x, y, z, glyph, col, 10 if abs(q) < 0.7 else 8)

    # Pollen-filled centre, built from dense little characters.
    for ring in range(4):
        rr = radius*(0.045 + ring*0.035)
        for j in range(18):
            a = 2*math.pi*j/18
            x = cx + nx*radius*0.15 + rr*math.cos(a)*rx + rr*math.sin(a)*ux
            y = cy + ny*radius*0.15 + rr*math.cos(a)*ry + rr*math.sin(a)*uy
            z = cz + nz*radius*0.15 + rr*math.cos(a)*rz + rr*math.sin(a)*uz
            put(x, y, z, "oO@"[(j+ring)%3],
                "gold" if ring % 2 else "white", 9)


def add_wrapper():
    """A tapered paper wrap made from rows of ASCII strokes."""
    levels = [(0.35, 0.35), (0.85, 0.58), (1.55, 0.98), (2.55, 1.42)]
    for k in range(len(levels)-1):
        z0, r0 = levels[k]
        z1, r1 = levels[k+1]
        for iz in range(12):
            t = iz/11
            z = mix(z0, z1, t)
            radius = mix(r0, r1, t)
            for j in range(58):
                a = 2*math.pi*j/58
                x = radius*math.cos(a)
                y = radius*0.63*math.sin(a)
                # Faceted paper texture.
                glyph = ("/", "\\", "|", "·")[(j//4 + iz//3) % 4]
                col = "paper" if (j//5 + iz) % 3 else "white"
                put(x, y, z, glyph, col, 9)
    # Open top rim.
    for j in range(70):
        a = 2*math.pi*j/70
        put(1.43*math.cos(a), 0.90*math.sin(a), 2.55,
            "_", "white", 9)


def add_bow():
    # Front-facing bow loops and dangling tails.
    for sign in (-1, 1):
        previous = None
        for i in range(30):
            t = i/29
            point = (sign*(0.08+0.65*t),
                     -0.91-0.07*math.sin(math.pi*t),
                     1.78+sign*0.26*math.sin(math.pi*t))
            if previous:
                add_line(previous, point, "ribbon", "~", 3, 11)
            previous = point
        add_line((sign*0.12, -0.94, 1.66),
                 (sign*0.34, -0.94, 1.12), "ribbon", "/", 20, 11)
    for i in range(24):
        a = 2*math.pi*i/24
        put(0.10*math.cos(a), -0.98, 1.77+0.10*math.sin(a),
            "o", "hotpink", 11)


def add_filler_sprig(origin, direction, length=0.72, colour="white", seed=0):
    """Tiny baby's-breath-style blossoms on branching green stems."""
    random.seed(100 + seed)
    ox, oy, oz = origin
    dx, dy, dz = direction
    end = (ox + dx*length, oy + dy*length, oz + dz*length)
    add_line(origin, end, "deepgreen", "|", 26, 8)
    for branch in range(5):
        t = 0.22 + branch*0.15
        bx, by, bz = ox+dx*length*t, oy+dy*length*t, oz+dz*length*t
        side = -1 if branch % 2 else 1
        tip = (bx + side*random.uniform(0.15,0.30),
               by + random.uniform(-0.12,0.12),
               bz + random.uniform(0.08,0.22))
        add_line((bx,by,bz), tip, "green", "/", 9, 8)
        for petal in range(5):
            a = petal*2*math.pi/5
            put(tip[0]+0.055*math.cos(a), tip[1]+0.04*math.sin(a),
                tip[2]+0.045*math.sin(a), "✿" if petal == 0 else "*",
                colour if petal % 2 else "yellow", 9)


def build_bouquet():
    POINTS.clear()
    # A lush, rounded hand-tied arrangement with overlapping focal blooms.
    flowers = [
        ((-1.82, 0.20, 4.45), "yellow",  0.62, 12, (-0.22,-0.16,1)),
        ((-1.15, 0.38, 5.02), "pink",    0.58, 12, (-0.12,-0.14,1)),
        ((-0.43, 0.48, 5.42), "purple",  0.60, 13, (-0.05,-0.12,1)),
        (( 0.38, 0.43, 5.48), "red",     0.63, 13, ( 0.04,-0.12,1)),
        (( 1.20, 0.34, 5.12), "yellow",  0.60, 12, ( 0.13,-0.13,1)),
        (( 1.87, 0.15, 4.48), "purple",  0.62, 12, ( 0.22,-0.16,1)),
        ((-1.43,-0.36, 3.92), "hotpink", 0.55, 12, (-0.18,-0.10,1)),
        ((-0.55,-0.48, 4.28), "orange",  0.57, 12, (-0.08,-0.08,1)),
        (( 0.42,-0.50, 4.30), "white",   0.56, 12, ( 0.08,-0.08,1)),
        (( 1.36,-0.35, 3.98), "pink",    0.56, 12, ( 0.18,-0.10,1)),
        ((-0.05, 0.65, 4.62), "white",   0.43, 10, ( 0.00, 0.10,1)),
        (( 0.90, 0.68, 4.55), "hotpink", 0.42, 10, ( 0.12, 0.10,1)),
    ]
    for idx, (head, col, size, petals, tilt) in enumerate(flowers):
        base = (head[0]*0.17, head[1]*0.12, 1.40+(idx%4)*0.08)
        add_line(base, head, "green", "|", 72, 10)
        add_flower(head, col, size, petals, tilt)

    # Miniature accent blooms fill gaps between the main flowers.
    mini_blooms = [
        ((-2.05,-0.10,3.90),"pink"), ((-1.70,-0.48,4.70),"white"),
        ((-0.92,-0.55,4.82),"yellow"), ((0.05,-0.58,4.92),"purple"),
        ((1.58,-0.48,4.72),"orange"), ((2.08,-0.08,3.92),"yellow"),
    ]
    for center, colour in mini_blooms:
        add_flower(center, colour, 0.27, 8, (0,-0.18,1))

    # Layered foliage fans around and between the stems.
    leaf_specs = [
        ((-0.58,0.00,1.82),(-1.0,-0.10,0.50),1.40,0.34,0),
        (( 0.42,0.02,1.85),( 1.0,-0.10,0.52),1.42,0.35,1),
        ((-0.28,0.20,2.20),(-1.0,0.12,0.48),1.22,0.30,2),
        (( 0.30,0.18,2.28),( 1.0,0.12,0.50),1.24,0.31,3),
        ((-0.16,-0.16,2.55),(-0.72,-0.12,0.72),1.02,0.27,4),
        (( 0.22,-0.15,2.62),( 0.72,-0.12,0.72),1.02,0.27,5),
        (( 0.00,0.28,2.08),( 0.12,0.42,1.0),1.05,0.29,6),
        ((-0.42,0.30,2.48),(-0.62,0.30,0.80),0.92,0.24,7),
        (( 0.40,0.28,2.50),( 0.62,0.30,0.82),0.94,0.24,8),
        ((-0.12,-0.30,2.90),(-0.90,-0.18,0.42),0.88,0.22,9),
        (( 0.16,-0.30,2.92),( 0.90,-0.18,0.42),0.88,0.22,10),
        (( 0.00,0.34,2.72),( 0.08,0.55,0.85),0.86,0.22,11),
    ]
    for spec in leaf_specs:
        add_leaf(*spec)

    # Airy baby's-breath filler sprigs peeking through the main blooms.
    add_filler_sprig((-1.35,0.30,3.55),(-0.45,0.12,1.0),0.92,"white",1)
    add_filler_sprig(( 1.28,0.28,3.62),( 0.45,0.12,1.0),0.90,"lilac",2)
    add_filler_sprig(( 0.10,0.45,3.75),( 0.08,0.30,1.0),0.95,"white",3)

    add_wrapper()
    add_bow()

    # A denser halo of tiny twinkles around the flower heads.
    random.seed(17)
    for _ in range(105):
        x = random.uniform(-2.55, 2.55)
        y = random.uniform(-0.75, 0.95)
        z = random.uniform(2.7, 6.1)
        put(x, y, z, random.choice(["·", "✦", "•", "⋆", "✧"]),
            "spark", random.choice([7, 8, 9, 10]))


class BouquetWindow:
    def __init__(self, root):
        self.root = root
        root.title("3D ASCII Bouquet")
        root.geometry("1200x900")
        root.minsize(600, 500)
        root.configure(bg=BG)

        # The artwork fills the complete window, without header/footer UI.
        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0,
                                borderwidth=0)
        self.canvas.pack(fill="both", expand=True)

        self.angle = 0.0
        self.paused = False
        self.canvas.bind("<Button-1>", self.toggle)
        root.bind("<space>", self.toggle)
        root.bind("<Left>", lambda e: self.step(-0.12))
        root.bind("<Right>", lambda e: self.step(0.12))
        root.bind("<Escape>", lambda e: root.destroy())
        self.draw()

    def toggle(self, event=None):
        self.paused = not self.paused

    def step(self, amount):
        self.angle += amount
        self.draw_once()

    def project(self, point, w, h):
        x, y, z = point
        c, s = math.cos(self.angle), math.sin(self.angle)
        xr, yr = x*c-y*s, x*s+y*c

        # Perspective camera looking slightly down at the bouquet.
        cam = (0.0, -10.5, 6.0)
        target = (0.0, 0.0, 2.85)
        forward = (target[0]-cam[0], target[1]-cam[1], target[2]-cam[2])
        fl = math.sqrt(sum(v*v for v in forward))
        forward = tuple(v/fl for v in forward)
        right = (forward[2], 0.0, -forward[0])
        rl = math.sqrt(sum(v*v for v in right))
        right = tuple(v/rl for v in right)
        # Camera-up must point toward world +Z. Use forward x right;
        # right x forward flips the projected scene upside down.
        up = (forward[1]*right[2]-forward[2]*right[1],
              forward[2]*right[0]-forward[0]*right[2],
              forward[0]*right[1]-forward[1]*right[0])
        rel = (xr-cam[0], yr-cam[1], z-cam[2])
        depth = sum(rel[i]*forward[i] for i in range(3))
        sx = sum(rel[i]*right[i] for i in range(3))
        sy = sum(rel[i]*up[i] for i in range(3))
        focal = min(w, h)*1.15
        factor = focal/max(2.5, depth)
        return w/2+sx*factor, h*0.50-sy*factor, depth

    def draw_once(self):
        self.canvas.delete("all")
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())

        # Project all points, then scale the bouquet to nearly fill the window.
        projected = []
        for x, y, z, glyph, color, size in POINTS:
            px, py, depth = self.project((x, y, z), w, h)
            projected.append([px, py, depth, glyph, color, size])

        if not projected:
            return

        min_x = min(item[0] for item in projected)
        max_x = max(item[0] for item in projected)
        min_y = min(item[1] for item in projected)
        max_y = max(item[1] for item in projected)
        bounds_w = max(1.0, max_x - min_x)
        bounds_h = max(1.0, max_y - min_y)

        fit = min((w * 0.96) / bounds_w, (h * 0.96) / bounds_h)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        cell_w, cell_h = 9, 13
        cols = max(1, int(w / cell_w))
        rows = max(1, int(h / cell_h))
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        depth_grid = [[float("inf") for _ in range(cols)] for _ in range(rows)]

        for px, py, depth, glyph, color, size in projected:
            px = (px - center_x) * fit + w / 2
            py = (py - center_y) * fit + h / 2
            col = int(px / cell_w)
            row = int(py / cell_h)
            if 0 <= col < cols and 0 <= row < rows:
                if depth < depth_grid[row][col]:
                    depth_grid[row][col] = depth
                    grid[row][col] = (glyph, color, size, depth)

        # Render colored character runs, preserving the ASCII-art appearance.
        for r, line in enumerate(grid):
            c = 0
            while c < cols:
                cell = line[c]
                if cell is None:
                    c += 1
                    continue
                color = cell[1]
                font_size = max(7, min(16, int(cell[2] * 10.5 / max(5.5, cell[3]) * fit)))
                run = []
                start_col = c
                while c < cols and line[c] is not None and line[c][1] == color:
                    run.append(line[c][0])
                    c += 1
                self.canvas.create_text(
                    start_col * cell_w, r * cell_h,
                    text="".join(run), fill=color, anchor="nw",
                    font=("Menlo", font_size, "bold"), justify="left"
                )

    def draw(self):
        self.draw_once()
        if not self.paused:
            self.angle += 0.018
        self.root.after(40, self.draw)


def main():
    build_bouquet()
    root = tk.Tk()
    BouquetWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
