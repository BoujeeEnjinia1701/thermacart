"""ThermaCart sizing calculations, TCT-CAL-001 v0.3 (TRL 3, constructable design, TCT-DDR-003).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, tagged [A1], [B2] and so on.
Geometry comes from cad/src/model.py (PARAMS, derived() and the build123d solids), costs
from bom/bom.csv and the value-engineering target (`budget_usd`) from project.yaml. The shell carries the dark finish decided in
TCT-DDR-002 (O8), so the dark-finish (emissivity 0.9) results are the design values; the bare
mill-finish results are kept for comparison. First-principles estimates for a paper
proof of concept; not a substitute for tests. Masses and the bail thermal break follow the
constructable design of TCT-DDR-003 (lug angles, bolts and washers, sealed radial screws, G 1/2 port).
`budget_usd` is a value-engineering target, not a limit (STANDARDS section 18).
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, build_components, build_parts, derived  # noqa: E402

D = derived(P)
SIG = 5.670e-8           # Stefan-Boltzmann constant, W/(m2 K4)
K0 = 273.15


def tag(t, text):
    print(f"[{t}] {text}")


# ---------------------------------------------------------------- material data
# Rubitherm datasheets (RT 5 HC, RT 25 HC, RT 70 HC), fetched 2026-09-25:
# heat storage capacity (latent plus sensible over a 15 K span, +/-7.5 %), cp 2 kJ/(kg K),
# k 0.2 W/(m K) in both phases, densities, maximum operating temperature.
GRADES = {
    #        H_ds kJ/kg, span K, melt lo, melt hi, nominal, rho_s, rho_l, T(rho_l), T max op
    "C5":  dict(H=250.0, span=15.0, m_lo=5.0, m_hi=6.0, nom=5.0, rho_s=0.85, rho_l=0.76, T_rl=20.0, T_max=45.0),
    "C25": dict(H=230.0, span=15.0, m_lo=22.0, m_hi=26.0, nom=25.0, rho_s=0.88, rho_l=0.77, T_rl=40.0, T_max=65.0),
    "H70": dict(H=260.0, span=15.0, m_lo=69.0, m_hi=71.0, nom=70.0, rho_s=0.90, rho_l=0.80, T_rl=80.0, T_max=90.0),
}
CP = 2000.0              # J/(kg K), both phases (datasheets)
K_PCM = 0.2              # W/(m K)
TOL = 0.075              # datasheet tolerance on heat storage capacity, taken at the low side
BETA_L = 0.001           # 1/K, volumetric expansion of liquid paraffin (assumption)
BETA_S = 0.0003          # 1/K, volumetric expansion of solid paraffin (assumption)
BAND = 3.0               # K either side of the nominal melt point (R3)

RHO_AL, CP_AL = 2700.0, 900.0
YIELD_6063_T52 = 110.0   # MPa, minimum (ASTM B221, 16 ksi)
SF = 1.5
E_AL = 69000.0           # MPa


def latent(g):
    """Latent heat left after removing the sensible part of the datasheet span, J/kg, low side of tolerance."""
    return (g["H"] * (1 - TOL) - CP / 1000 * g["span"]) * 1000


def h_of_T(g, T):
    """Specific enthalpy relative to 0 degC solid, J/kg; latent spread evenly over the melt range."""
    L = latent(g)
    lo, hi = g["m_lo"], g["m_hi"]
    if T <= lo:
        return CP * T
    if T >= hi:
        return CP * T + L
    return CP * T + L * (T - lo) / (hi - lo)


def T_of_h(g, h):
    L = latent(g)
    lo, hi = g["m_lo"], g["m_hi"]
    if h <= CP * lo:
        return h / CP
    if h >= CP * hi + L:
        return (h - L) / CP
    # inside the melt range: h = CP*T + L*(T-lo)/(hi-lo)
    return (h + L * lo / (hi - lo)) / (CP + L / (hi - lo))


def rho_l(g, T):
    return g["rho_l"] * 1000 / (1 + BETA_L * (T - g["T_rl"]))


# ---------------------------------------------------------------- A. geometry and mass
print("A. Geometry and mass (R2, R4, R5)")
tag("A1", f"Cartridge overall {D['overall_l']:.1f} x {D['overall_w']:.1f} x {D['overall_h']:.1f} mm, bail stowed; "
          f"GN 1/3 slot 325 x 176 mm, 65 mm high: margins {325 - D['overall_l']:.1f}, {176 - D['overall_w']:.1f} "
          f"and {65 - D['overall_h']:.1f} mm")
tag("A2", f"Inner space {D['in_w']:.2f} x {D['in_h']:.2f} x {D['in_l']:.1f} mm = {D['v_inner_l']:.3f} L "
          f"(TRL 2 estimate 1.62 L)")
tag("A3", f"Bail finger gap with the bail swung out {D['finger_gap']:.0f} mm; frame {D['frame_l']:.1f} x {D['frame_w']:.1f} mm")

parts = build_parts(P)
COMP = build_components(P)
vol = {k: v.volume / 1e3 for k, v in parts.items()}      # cm3
cvol = {k: c.shape.volume / 1e3 for k, c in COMP.items()}  # cm3, per component
al_parts = ["tube", "fins_bot", "fins_top", "flange_key", "spacer_key", "plug_key", "flange_handle",
            "spacer_handle", "plug_handle", "key", "lugs", "arms", "rod", "guards"]
m_al = sum(cvol[k] for k in al_parts) * RHO_AL / 1e6       # kg
fixed = {                                                   # kg, catalogue masses for bought items
    "silicone grip (1.2 kg/L)": cvol["grip"] * 1.2 / 1e3,
    "FKM O-rings (1.9 kg/L)": (cvol["oring_key"] + cvol["oring_handle"]) * 1.9 / 1e3,
    "12 M5 x 10 A2 button-head screws with bonded seals": 12 * (0.0022 + 0.0006),
    "9 M4 A2 screws and bolts (stack, key, lugs)": 3 * 0.0013 + 2 * 0.0023 + 4 * 0.0027,
    "2 pivot pins with nyloc nuts, 2 M6 x 12 rod-end screws": 2 * 0.005 + 2 * 0.004,
    "G 1/2 anodised aluminium plug and bonded seal": 0.009,
    "label and melt indicator tube with its PCM": 0.006,
    "phenolic thermal-break and head washers": (cvol["thermal_break"] + cvol["head_washers"]) * 1.4 / 1e3,
    "epoxy and sealant": 0.012,
    "matte black high-temperature paint and primer, about 50 um dry (DDR-002, O8)": 0.015,
}
m_shell = m_al + sum(fixed.values())
tag("A4", "Aluminium parts from the model: shell and fins {:.0f} cm3, cap stacks {:.0f} cm3, bail and key {:.0f} cm3, "
          "guards {:.1f} cm3; {:.3f} kg".format(
              cvol["tube"] + cvol["fins_bot"] + cvol["fins_top"],
              sum(cvol[k] for k in ("flange_key", "spacer_key", "plug_key", "flange_handle", "spacer_handle", "plug_handle")),
              sum(cvol[k] for k in ("key", "lugs", "arms", "rod")), cvol["guards"], m_al))
tag("A5", f"Other cartridge parts {sum(fixed.values()):.3f} kg; empty cartridge {m_shell:.2f} kg "
          f"(TRL 2 estimate about 1.5 kg)")

res = {}
for name, g in GRADES.items():
    T_fill = g["T_max"]
    m = P["fill_fraction"] * D["v_inner_l"] / 1000 * rho_l(g, T_fill)
    usable = h_of_T(g, g["nom"] + BAND) - h_of_T(g, g["nom"] - BAND)
    nominal = usable + TOL * g["H"] * 1000
    total = m + m_shell
    res[name] = dict(m=m, T_fill=T_fill, usable=usable, E=m * usable / 3600, E_nom=m * nominal / 3600,
                     total=total, frac=m / total)
    tag("A6", f"{name}: fill at {T_fill:.0f} °C, liquid {rho_l(g, T_fill):.0f} kg/m3, PCM {m:.3f} kg; "
              f"filled {total:.2f} kg; PCM fraction {100 * m / total:.1f} %")

# ---------------------------------------------------------------- B. storage per grade
print("\nB. Usable storage within ±3 K of the melt point (R1, R3)")
for name, g in GRADES.items():
    r = res[name]
    tag("B1", f"{name}: latent {latent(g) / 1000:.1f} kJ/kg (low side), usable in band {r['usable'] / 1000:.1f} kJ/kg; "
              f"{r['E']:.1f} Wh per cartridge ({r['E_nom']:.1f} Wh at nominal datasheet value); target 60 Wh")
wh_kg = {n: res[n]["E"] / res[n]["total"] for n in res}
tag("B2", "Energy density on filled mass: " + ", ".join(f"{n} {v:.1f} Wh/kg" for n, v in wh_kg.items()))

# 2 mm wall option (D5): metric 150 x 50 x 2 mm tube, same length
v2 = (150 - 4) * (50 - 4) * D["in_l"] / 1e6
g5 = GRADES["C5"]
m2 = P["fill_fraction"] * v2 / 1000 * rho_l(g5, g5["T_max"])
tag("B3", f"2 mm wall option (150 x 50 x 2 mm tube): inner {v2:.3f} L (+{100 * (v2 / D['v_inner_l'] - 1):.1f} %), "
          f"C5 {m2 * res['C5']['usable'] / 3600:.1f} Wh")

# ---------------------------------------------------------------- C. pressure and wall stress
print("\nC. Internal pressure and wall stress (R8, D5)")
P0 = 1.01325  # bar abs at sealing


def gas_pressure(g, m, V_in, T_fill, T, phase):
    V_g0 = V_in * (1 - P["fill_fraction"])
    if phase == "l":
        V_pcm = m / rho_l(g, T)
    else:
        V_pcm = m / (g["rho_s"] * 1000 * (1 + BETA_S * (T - g["m_lo"])))
    V_g = V_in - V_pcm
    return P0 * V_g0 / V_g * (T + K0) / (T_fill + K0), V_g / V_in


def wall_stress(dp_bar, b, h, t):
    """Peak bending stress in a closed rectangular tube, all walls loaded, equal wall thickness.
    Corner moment M = p (b^3 + h^3) / (12 (b + h)) per unit length; sigma = 6 M / t^2."""
    p = abs(dp_bar) * 0.1
    M = p * (b ** 3 + h ** 3) / (12 * (b + h))
    return 6 * M / t ** 2


allow = YIELD_6063_T52 / SF
b, h, t = D["in_w"], D["in_h"], P["tube_t"]
V_in = D["v_inner_l"] / 1000
T_COLD = -25.0
for name, g in GRADES.items():
    r = res[name]
    pc, fc = gas_pressure(g, r["m"], V_in, r["T_fill"], T_COLD, "s")
    ph, fh = gas_pressure(g, r["m"], V_in, r["T_fill"], r["T_fill"] + 20, "l")
    r.update(p_cold=pc - P0, p_hot=ph - P0)
    tag("C1", f"{name}: sealed at {r['T_fill']:.0f} °C with {100 * (1 - P['fill_fraction']):.0f} % ullage: "
              f"at {T_COLD:.0f} °C solid {pc - P0:+.2f} bar gauge (ullage {100 * fc:.1f} %); "
              f"at {r['T_fill'] + 20:.0f} °C (20 K over limit) {ph - P0:+.2f} bar gauge (ullage {100 * fh:.1f} %)")
worst_vac = min(r["p_cold"] for r in res.values())
worst_hot = max(r["p_hot"] for r in res.values())
tag("C2", f"At the fill temperature the gauge pressure is 0.00 bar by construction; worst case over-limit +{worst_hot:.2f} bar "
          f"(R8 target 0.5 bar)")
s_vac, s_full, s_hot = wall_stress(worst_vac, b, h, t), wall_stress(-1.0, b, h, t), wall_stress(worst_hot, b, h, t)
tag("C3", f"3.175 mm wall: {s_vac:.0f} MPa at {worst_vac:+.2f} bar, {s_full:.0f} MPa at full vacuum, {s_hot:.0f} MPa at "
          f"+{worst_hot:.2f} bar; allowable {allow:.0f} MPa (yield {YIELD_6063_T52:.0f} MPa / {SF})")
s2_vac = wall_stress(worst_vac, 146.0, 46.0, 2.0)
tag("C4", f"2 mm wall: {s2_vac:.0f} MPa at {worst_vac:+.2f} bar, {s2_vac / YIELD_6063_T52:.2f} of yield; "
          f"pressure for the allowable stress {allow / wall_stress(1.0, 146.0, 46.0, 2.0):.2f} bar")
# face deflection, 3.175 mm wall, beam strip with the corner moment
p_mpa = abs(worst_vac) * 0.1
I = t ** 3 / 12
Mc = p_mpa * (b ** 3 + h ** 3) / (12 * (b + h))
w_mid = 5 * p_mpa * b ** 4 / (384 * E_AL * I) - Mc * b ** 2 / (8 * E_AL * I)
tag("C5", f"Face deflection at {worst_vac:+.2f} bar: {w_mid:.2f} mm at mid-span (3.175 mm wall)")
F_cap = worst_hot * 0.1 * b * h
tag("C6", f"Cap load at +{worst_hot:.2f} bar: {F_cap:.0f} N, {F_cap / P['cap_screws']:.0f} N per radial M5 screw")

# end-on drop of a molten cartridge: hydraulic surge, indicative only (R6)
v = math.sqrt(2 * 9.81 * 1.0)
stop = 0.004
a = v ** 2 / (2 * stop)
p_surge = rho_l(GRADES["H70"], 80) * a * D["in_l"] / 1000 / 1e5
F_surge = p_surge * 0.1 * b * h
tag("C7", f"1 m end-on drop, 4 mm stopping distance: {a / 9.81:.0f} g, surge up to {p_surge:.1f} bar on the lower cap "
          f"if the liquid column is not cushioned; {F_surge / 1000:.1f} kN, {F_surge / P['cap_screws']:.0f} N per screw "
          f"(M5 A2-70 proof load about 6,400 N)")

# ---------------------------------------------------------------- D. hold times
print("\nD. Hold times (R10, R11)")
A_eff = 0.85 * (D["area_tube_m2"] + D["area_fins_m2"] + D["area_ends_m2"])
tag("D1", f"Outer area: tube {D['area_tube_m2']:.4f} m2, fins {D['area_fins_m2']:.4f} m2, ends {D['area_ends_m2']:.4f} m2; "
          f"effective (85 %) {A_eff:.4f} m2")


def h_air(Ts, Ta, eps):
    dT = max(abs(Ts - Ta), 0.5)
    hc = 1.32 * (dT / 0.15) ** 0.25
    Tk, Ak = Ts + K0, Ta + K0
    hr = eps * SIG * (Tk ** 2 + Ak ** 2) * (Tk + Ak)
    return hc + hr


def hold(g, m, n, T_p0, T_f0, C_f, UA, T_amb, eps, lo, hi, dt=10.0, tmax=48 * 3600):
    """Two-node model: n cartridges (PCM plus aluminium) and the box contents (food or produce, air, liner).
    Returns hours until the contents leave [lo, hi]."""
    C_al = m_shell * CP_AL
    H = m * h_of_T(g, T_p0) + C_al * T_p0          # per cartridge, J (reference 0 degC)
    Tf = T_f0
    tt = 0.0
    while tt < tmax:
        # PCM and shell share one temperature: solve for T from H
        Tp = T_of_h(g, (H - C_al * 0) / m)             # first guess ignoring shell
        for _ in range(3):
            Tp = T_of_h(g, (H - C_al * Tp) / m)
        q = n * h_air(Tp, Tf, eps) * A_eff * (Tp - Tf)  # W into contents
        leak = UA * (T_amb - Tf)
        Tf += (q + leak) * dt / C_f
        H -= q / n * dt
        tt += dt
        if Tf < lo or Tf > hi:
            return tt / 3600, Tp
    return tmax / 3600, Tp


g = GRADES["C5"]
C_prod = 5.0 * 3900 + 2000       # 5 kg produce at 3.9 kJ/(kg K) plus air and liner
E2 = 2 * res["C5"]["E"]
t_energy = E2 / (0.5 * (32 - 5))
tag("D2", f"R10 energy only: two C5 give {E2:.0f} Wh in band; 0.5 W/K x 27 K = 13.5 W; {t_energy:.1f} h")
for eps, lab in ((0.10, "bare mill finish"), (0.90, "painted or anodized dark")):
    hA = h_air(5, 8, eps) * A_eff
    Tss = (0.5 * 32 + 2 * hA * 5.5) / (0.5 + 2 * hA)
    T_amb_ok = 8 + 2 * hA * (8 - 5.5) / 0.5
    t_h, _ = hold(g, res["C5"]["m"], 2, 2.0, 5.0, C_prod, 0.5, 32.0, eps, 2.0, 8.0)
    tag("D3", f"R10 {lab} (emissivity {eps}): h {hA / A_eff:.1f} W/(m2 K), {hA:.2f} W/K per cartridge; "
              f"contents settle near {Tss:.1f} °C while the PCM melts; within 2 to 8 °C for {t_h:.1f} h at 32 °C; "
              f"band holds while melting up to {T_amb_ok:.1f} °C ambient")
    t25, _ = hold(g, res["C5"]["m"], 2, 2.0, 5.0, C_prod, 0.5, 25.0, eps, 2.0, 8.0)
    tag("D4", f"R10 {lab} at 25 °C ambient: {t25:.1f} h")
res["R10_bare"] = hold(g, res["C5"]["m"], 2, 2.0, 5.0, C_prod, 0.5, 32.0, 0.10, 2.0, 8.0)[0]
res["R10_dark"] = hold(g, res["C5"]["m"], 2, 2.0, 5.0, C_prod, 0.5, 32.0, 0.90, 2.0, 8.0)[0]
for n_c in (3,):
    t3, _ = hold(g, res["C5"]["m"], n_c, 2.0, 5.0, C_prod, 0.5, 32.0, 0.90, 2.0, 8.0)
    tag("D5", f"R10 three dark C5 cartridges at 32 °C: {t3:.1f} h")

g = GRADES["H70"]
C_food = 4.0 * 3500 + 2000       # 4 kg cooked food at 3.5 kJ/(kg K) plus carrier liner
for eps, lab in ((0.10, "bare mill finish"), (0.90, "painted or anodized dark")):
    t_h, Tp = hold(g, res["H70"]["m"], 1, 85.0, 75.0, C_food, 0.25, 25.0, eps, 63.0, 200.0)
    res[f"R11_{eps}"] = t_h
    tag("D6", f"R11 {lab}: food from 75 °C with one H70 charged to 85 °C, carrier 0.25 W/K at 25 °C: "
              f"63 °C or more for {t_h:.1f} h (PCM at {Tp:.1f} °C at that time)")
t_food_only = C_food / 0.25 * math.log((75 - 25) / (63 - 25)) / 3600
tag("D7", f"R11 food alone, no cartridge: {t_food_only:.1f} h")

# ---------------------------------------------------------------- E. recharge
print("\nE. Recharge (R12)")
A_face = 2 * D["in_w"] * D["in_l"] / 1e6       # the two broad inner faces, m2


def recharge(g, m, T0, T_env, h_fn, s_max, faces_area, target, dt=10.0):
    """Quasi-steady Stefan model: lumped sensible phases; during the phase change the flow crosses
    the external film and a growing layer of changed PCM (k = 0.2) of thickness up to s_max.
    target 'freeze' or 'melt'. Returns hours until the whole fill has changed phase."""
    C_al = m_shell * CP_AL
    L = latent(g)
    H = m * h_of_T(g, T0) + C_al * T0
    H_end = (m * h_of_T(g, g["m_lo"] - 1) + C_al * (g["m_lo"] - 1)) if target == "freeze" else \
            (m * h_of_T(g, g["m_hi"] + 1) + C_al * (g["m_hi"] + 1))
    H_lo = m * h_of_T(g, g["m_lo"]) + C_al * g["m_lo"]
    H_hi = m * h_of_T(g, g["m_hi"]) + C_al * g["m_hi"]
    tt = 0.0
    while (H > H_end) if target == "freeze" else (H < H_end):
        Tp = T_of_h(g, H / (m + 1e-9) - 0)
        for _ in range(3):
            Tp = T_of_h(g, (H - C_al * Tp) / m)
        R_ext = 1 / (h_fn(Tp, T_env) * A_eff)
        if H_lo <= H <= H_hi:
            frac = (H_hi - H) / (H_hi - H_lo) if target == "freeze" else (H - H_lo) / (H_hi - H_lo)
            R_int = frac * s_max / (K_PCM * faces_area)
        else:
            R_int = 0.0
        q = (Tp - T_env) / (R_ext + R_int)
        H -= q * dt
        tt += dt
        if tt > 200 * 3600:
            break
    return tt / 3600


s_half = D["in_h"] / 2 / 1000
for eps, lab in ((0.10, "bare"), (0.90, "dark")):
    hf = lambda Ts, Ta, e=eps: h_air(Ts, Ta, e)
    t_c5 = recharge(GRADES["C5"], res["C5"]["m"], 8.0, -18.0, hf, s_half, A_face, "freeze")
    t_c5f = recharge(GRADES["C5"], res["C5"]["m"], 8.0, 2.0, hf, s_half, A_face, "freeze")
    t_c25f = recharge(GRADES["C25"], res["C25"]["m"], 28.0, -18.0, hf, s_half, A_face, "freeze")
    t_c25r = recharge(GRADES["C25"], res["C25"]["m"], 28.0, 4.0, hf, s_half, A_face, "freeze")
    res[f"R12_{lab}"] = (t_c5, t_c25f, t_c25r)
    tag("E1", f"{lab} surface: C5 in a -18 °C freezer {t_c5:.1f} h; C5 in a 2 °C refrigerator {t_c5f:.1f} h; "
              f"C25 in a -18 °C freezer {t_c25f:.1f} h; C25 in a 4 °C refrigerator {t_c25r:.1f} h (still air)")
    hov = lambda Ts, Ta, e=eps: 15.0 + h_air(Ts, Ta, e) - 1.32 * (max(abs(Ts - Ta), 0.5) / 0.15) ** 0.25
    t_oven = recharge(GRADES["H70"], res["H70"]["m"], 25.0, 85.0, hov, s_half, A_face, "melt")
    res[f"R12_oven_{lab}"] = t_oven
    tag("E2", f"{lab} surface: H70 in a fan oven at 85 °C (h 15 W/(m2 K) plus radiation) from 25 °C: {t_oven:.1f} h")
gH = GRADES["H70"]
E_pad = (res["H70"]["m"] * (h_of_T(gH, 80) - h_of_T(gH, 25)) + m_shell * CP_AL * 55) / 3600
t_pad = E_pad / (60 * 0.8)
s_full = D["in_h"] / 1000
t_cond = res["H70"]["m"] / (D["in_w"] * D["in_l"] / 1e6 * D["in_h"] / 1000) * latent(gH) * s_full ** 2 / (2 * K_PCM * 20) / 3600
tag("E3", f"H70 on a 60 W pad (80 % into the cartridge) from 25 to 80 °C: {E_pad:.0f} Wh, {t_pad:.1f} h if heat reaches the PCM; "
          f"melting upward from a 90 °C base by conduction alone would take {t_cond:.1f} h (upper bound)")
res["E_pad"], res["t_pad"], res["t_cond"] = E_pad, t_pad, t_cond
E_above = (res["H70"]["m"] * (h_of_T(gH, 80) - h_of_T(gH, 63)) + m_shell * CP_AL * 17) / 3600
tag("E4", f"H70 energy flow on the pad: input {E_pad / 0.8:.0f} Wh, stored 25 to 80 °C {E_pad:.0f} Wh, "
          f"released above 63 °C {E_above:.0f} Wh, below 63 °C {E_pad - E_above:.0f} Wh, charger loss {E_pad / 0.8 - E_pad:.0f} Wh")

# ---------------------------------------------------------------- F. handle temperature
print("\nF. Handle temperature (R14)")
# Constructable design (TCT-DDR-003, P5): each lug angle stands on two phenolic washers (OD 9, ID 4.5,
# 3 mm) and its two M4 bolts carry a 3 mm phenolic washer under the head, so the steel bolt (at
# cartridge temperature) touches the angle only through phenolic; the bolt passes the angle in a
# 6.5 mm hole with an air gap.
wo, wi = P["break_washer"]
ho, hi, ht = P["head_washer"]
A_brk = 4 * math.pi / 4 * (wo ** 2 - wi ** 2) / 1e6
A_head = 4 * math.pi / 4 * (ho ** 2 - hi ** 2) / 1e6
G_brk = 0.25 * A_brk / (P["break_t"] / 1000) + 0.25 * A_head / (ht / 1000)
A_handle = (COMP["lugs"].shape.area + COMP["arms"].shape.area + COMP["rod"].shape.area) / 1e6 \
    - math.pi * P["rod_d"] / 1000 * P["grip_l"] / 1000   # exposed angles, arms and rod, m2 (from the model)
G_air = 8.0 * A_handle
C_handle = (cvol["lugs"] + cvol["arms"] + cvol["rod"]) * RHO_AL / 1e6 * CP_AL
for T_c in (71.0, 80.0):
    T_h = (G_brk * T_c + G_air * 25) / (G_brk + G_air)
    tag("F1", f"Cartridge at {T_c:.0f} °C: bail on the thermal break settles at {T_h:.1f} °C "
              f"(break {G_brk:.3f} W/K through washers and bolt-head washers, air {G_air:.3f} W/K over {A_handle:.4f} m2)")
tau = C_handle / (G_brk + G_air)
T_inf = (G_brk * 80 + G_air * 25) / (G_brk + G_air)
t55 = tau * math.log((85 - T_inf) / (55 - T_inf)) / 60
tag("F2", f"Out of an 85 °C oven the bail starts at 85 °C; time constant {tau / 60:.0f} min; below 55 °C after {t55:.0f} min")
tag("F3", "Assumed ISO 13732-1 burn thresholds for 10 s contact: about 55 °C for bare metal, about 70 °C for plastics "
          "and rubber (to confirm against the standard)")

# ---------------------------------------------------------------- G. keying
print("\nG. Grade keying (R9)")
ky = P["key_y"]
ok = True
for a_ in ky:
    for s_ in ky:
        k_lo, k_hi = ky[a_] - P["key_w"] / 2, ky[a_] + P["key_w"] / 2
        s_lo, s_hi = ky[s_] - P["key_w"] / 2 - P["slot_clear"], ky[s_] + P["key_w"] / 2 + P["slot_clear"]
        fits = s_lo <= k_lo and k_hi <= s_hi
        if fits != (a_ == s_):
            ok = False
tag("G1", f"Key positions {', '.join(f'{k} {v:+.0f} mm' for k, v in ky.items())}; each frame accepts only its own grade: {ok}")

# ---------------------------------------------------------------- H. cost
print("\nH. Cost (R16) against the value-engineering targets")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = {r["item"]: int(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
frame_cost = sum(v for k, v in cost.items() if k.startswith("7 "))
cart_cost = sum(cost.values()) - frame_cost
import yaml  # noqa: E402
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
over = cart_cost + frame_cost - budget
tag("H1", f"Cartridge ${cart_cost:.2f} (R16 target $50, ${cart_cost - 50:.2f} over), frame ${frame_cost:.2f} (target $20); "
          f"one C5 cartridge and one frame ${cart_cost + frame_cost:.2f} against the ${budget:.0f} value-engineering target "
          f"(${abs(over):.2f} {'over' if over > 0 else 'under'})")
pcm_price = 10.0
pcm_row = sum(v for k, v in cost.items() if k.startswith("2 "))
set3 = 3 * (cart_cost - pcm_row) + pcm_price * sum(res[n]["m"] for n in res if n in GRADES) + frame_cost
tag("H2", f"One cartridge of each grade plus one frame: ${set3:.2f}")
tag("H3", f"PCM at $20/kg instead of $10/kg adds ${pcm_price * res['C5']['m']:.2f} per C5 cartridge")

# ---------------------------------------------------------------- summary for the results table
print("\nSummary")
tag("S1", f"R3 C5 {res['C5']['E']:.1f}, C25 {res['C25']['E']:.1f}, H70 {res['H70']['E']:.1f} Wh; "
          f"R4 max filled {max(res[n]['total'] for n in GRADES):.2f} kg; "
          f"R5 fraction {min(res[n]['frac'] for n in GRADES) * 100:.1f} to {max(res[n]['frac'] for n in GRADES) * 100:.1f} %")
