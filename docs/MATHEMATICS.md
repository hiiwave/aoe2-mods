# Mathematics of shortening a house sprite

This page integrates the earlier lecture and distinguishes its **historical screenshot experiment** from the **current native-sprite implementation**. It does not recover the game's 3D geometry from a screenshot. See [Technical specification](TECHNICAL-SPEC.md) for delivered parameters and [Test status](TEST-STATUS.md) for evidence.

## 1. Three meanings of height

Keep separate: world height; screen distance between chosen landmarks; and decoded main-alpha bounding-box height.

The lecture chose screen top $v_0=75$ and fixed front-ground reference $B=229$:

```math
H=B-v_0=154.
```

A 30% reduction meant:

```math
H_{\mathrm{target}}=(1-0.30)154=107.8,\qquad v_0'=229-107.8=121.2.
```

That excludes the screenshot selection border. It is **not** the native sprite-alpha definition. Our current trial measures the main layer's visible bounding-box height, excluding the separate shadow, and targets 110 px. Source heights for Dark2/Feudal2/Castle2 are 119/155/153 px. Thus:

```math
1-\frac{110}{119}\approx7.56\%,\qquad
1-\frac{110}{155}\approx29.03\%,\qquad
1-\frac{110}{153}\approx28.10\%.
```

Equal final height does not imply equal roof scale or wall compression.

## 2. World projection and missing depth

Let $(x,y,z)$ be hypothetical world coordinates, with $z$ height. Let screen $(u,v)$ increase rightward/downward. A useful parallel-projection model is:

```math
u=u_c+a(x-y),\qquad v=v_c+b(x+y)-cz,\qquad a,b,c\gt0.
```

The world axes project down-right, down-left and upward. This is not an estimated game camera. Calling it uniformly scaled orthographic projection in orthonormal world units additionally requires:

```math
2a^2=2b^2+c^2.
```

Adding any multiple of the following vector leaves both screen coordinates unchanged:

```math
(1,1,2b/c).
```

Indeed, $a(1-1)=0$ and $b(1+1)-c(2b/c)=0$. One screen point therefore has a line of possible world preimages.

If height $z$ is independently known, set:

```math
U=\frac{u-u_c}{a},\qquad V=\frac{v-v_c+cz}{b}.
```

Then $x-y=U$ and $x+y=V$, giving:

```math
x=\frac{V+U}{2},\qquad y=\frac{V-U}{2}.
```

A known ground point has $z=0$; an arbitrary roof pixel does not.

### True world-height scaling

For a world deformation $z\mapsto sz$ with $x,y$ fixed, define that point's projected ground position $g=v_c+b(x+y)$. Since $v=g-cz$:

```math
v'=g-csz=g+s(v-g)=sv+(1-s)g.
```

Ground points remain fixed. But $g$ depends on surface depth; it is not generally one universal ground line per screen column. Uniformly squashing the sprite also squashes its projected ground footprint. More guessed landmarks do not recover missing depth.

The lecture's assumed-depth mesh used:

```math
H(s)=B-\min_i\{sv_i+(1-s)g_i\}.
```

Its visible reduction is $1-H(s)/H(1)$, not $1-s$. Its example $s\approx0.4923$ was a mesh-specific calibration, **not** the calibration for the rigid or hybrid methods below. The function can have corners when the highest landmark changes.

## 3. Join a roof to a fixed ground line

In image space, trace a roof/wall seam $t(u)$ and foot line $\beta(u)$, with:

```math
L(u)=\beta(u)-t(u)\gt0.
```

These are manually annotated, piecewise-linear curves, not recovered 3D surfaces.

Choose a new seam $q(u)\lt\beta(u)$. Seek an affine map in each wall column:

```math
W(u,v)=q(u)+\lambda(u)(v-t(u)).
```

Imposing $W(u,\beta(u))=\beta(u)$ determines:

```math
\lambda(u)=\frac{\beta(u)-q(u)}{\beta(u)-t(u)}.
```

Consequently:

```math
W(u,t(u))=q(u),\qquad W(u,\beta(u))=\beta(u).
```

This is affine in the vertical coordinate for each fixed column, not necessarily one global affine transformation.

**Order preservation.** If the roof map increases vertically, maps $t$ to $q$, and $q\lt\beta$, its join to the wall and unchanged ground is continuous and increasing in each column. Different columns retain different horizontal coordinates, so the continuous map is injective. This prevents foldovers, not ugly proportions or lost raster details.

## 4. Rigid Roof-Shift

Translate the roof downward without changing its shape:

```math
R_\Delta(v)=v+\Delta,\qquad q(u)=t(u)+\Delta.
```

Substitution into the wall formula gives:

```math
\lambda(u)=1-\frac{\Delta}{L(u)}.
```

Valid positive-height walls require:

```math
0\le\Delta\lt\min_u L(u).
```

At equality a wall collapses; beyond it the column reverses. Even before collapse, a door may become unreadable.

For the historical height $H=154$, rigid20 used 30.8 px and rigid30 used 46.2 px. A sampled column had $t=175$, $\beta=219$, hence $L=44$:

```math
L'_{20}=44-30.8=13.2\gt0,\qquad
L'_{30}=44-46.2=-2.2\lt0.
```

The rigid30 image was a diagnostic failure, not valid finished art.

## 5. Roof-Shift Hybrid

Compress the roof vertically about anchor $A$ by $k$, then translate it by $d$:

```math
R_h(v)=A+k(v-A)+d=kv+C,\qquad C=(1-k)A+d.
```

Its seam becomes:

```math
q_h(u)=A+k(t(u)-A)+d.
```

Use $q_h$ in the wall map from Section 3. This joins the transformed roof to a fixed foot without a continuous-coordinate gap.

### Solve for total shortening

Assume the top remains on the transformed roof and the reference bottom stays fixed. Desired top displacement $D$ satisfies:

```math
D=R_h(v_0)-v_0=d+(1-k)(A-v_0).
```

For $A\gt v_0$:

```math
k=1-\frac{D-d}{A-v_0}.
```

The lecture used $D=46.2$, $d=30.8$, $A=181$ and $v_0=75$:

```math
k=1-\frac{15.4}{106}\approx0.854717,\qquad C\approx57.096226.
```

Roof vertical height shrank about 14.53%, while landmark height shrank 30%. These percentages have different denominators.

For the earlier column:

```math
q_h\approx206.6717,\qquad
L_h'=219-q_h\approx12.3283,\qquad
\lambda_h\approx0.28019\gt0.
```

The minimum remaining wall height over the sampled screenshot columns was about 11.8843 px. These numbers concern that manually traced screenshot, not every native house.

### Roof slopes

A screen edge of slope $m$ transforms under $u'=u,\ v'=kv+C$ to:

```math
m'=km.
```

The roof gets flatter for $0\lt k\lt1$. This is an intentional image-space approximation, not a claim of unchanged 3D roof geometry.

## 6. Inverse sampling

Moving source pixels forward can leave holes. Instead, for each destination $(u,w)$ find its source vertical coordinate.

Roof, for $w\lt q_h(u)$:

```math
v=\frac{w-C}{k}.
```

Wall, for $q_h(u)\le w\lt\beta(u)$:

```math
v=t(u)+\frac{w-q_h(u)}{\lambda_h(u)}.
```

Ground, for $w\ge\beta(u)$:

```math
v=w.
```

The native implementation rounds to the nearest source pixel with NumPy's ties-to-even rounding and transforms aligned layers. It uses no generative fill. Subsequent native BC1/BC4 encoding is lossy, so copied pre-encoding colors need not remain identical.

These branches require positive roof/wall scales. A continuous injective map is not a bijection of raster pixels: thin features can disappear. The failed rigid30 diagnostic is not a valid nonoverlapping inverse-map partition.

## 7. Retain readable walls, not merely positive walls

Require at least a fraction $\eta$ of each original wall band:

```math
\lambda(u)\ge\eta,\qquad 0\lt\eta\lt1.
```

Equivalently:

```math
q(u)\le\beta(u)-\eta L(u).
```

For rigid translation:

```math
\Delta\le(1-\eta)L(u).
```

For Hybrid, substitute $q_h$. This supplies a parameter-search constraint, but a useful $\eta$ depends on actual doors, windows, roof proportions and gameplay readability. The project has not adopted one universal value for every architecture.

## 8. Roof-Flatten and the 110 px experiments

The later Roof-Flatten experiments keep eaves and walls fixed while reducing roof pitch. They differ from Roof-Shift Hybrid, whose seam moves.

A simple column map about the seam is:

```math
v'=t(u)+k(v-t(u))
```

for roof pixels. It fixes the seam, but varying $t(u)$ can bend a formerly straight ridge. Piecewise-affine meshes can constrain edges, yet moving a ridge below neighboring fixed eaves may invert triangles.

The tested Feudal2 equal-drop mesh needed a 45 px drop to change 155 into 110 px. One ridge vertex moved from 126 to 171, below its fixed eave at 153, folding that mesh.

**This is a failure of the tested constraints, not a theorem that 110 px Roof-Flatten is impossible.** Different ridge displacements, mesh topology or roof redesign may work. If walls are compressed too, call it combined/hybrid rather than pure Roof-Flatten.

## 9. Lecture notation versus native implementation

| Lecture | Technical spec / code |
|---|---|
| horizontal $u$ | $x$, array column |
| vertical $v$ | $y$, array row |
| seam $t(u)$ | seam $t(x)$ |
| foot $\beta(u)$ | foot $b(x)$ |
| transformed seam $q_h(u)$ | $n(x)$ |
| anchor $A$ | anchor $a$ |
| translation $d$ | d |

The current trial's 110 px main-alpha target was calibrated on native sprites, not by reusing the lecture's 30% coefficients:

| Age / variant | Roof scale | Roof shift | Anchor |
|---|---:|---:|---:|
| Dark2 | 0.90 | 3.0 px | 133 |
| Feudal2 | 0.833333... | 29.0 px | 181 |
| Castle2 | 0.70 | 16.6 px | 183 |

Measure encoded/read-back height, masks and hashes after building. Integer sampling, visibility masks and block coding make symbolic height estimates insufficient.

## Source and limits

Integrated from the complete 10-page desktop lecture *Shortening a House Sprite: Projection, rigid roofs, and a hybrid warp*, emailed on 2026-11-16 UTC, then checked against the native implementation. Original PDF SHA256: a97ac6e3ef22435f79f8d082399defd6e3e18f7913e595c684c89ae1a3810f5a.

The PDF's figures came from a single screenshot experiment, with manually selected coordinates; it did not claim automatic segmentation or a deployed mod. Relevant derivations are integrated here; the PDF itself is not uploaded. Historical screenshot numbers and current sprite measurements remain distinct.
