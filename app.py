import streamlit as st
import matplotlib.pyplot as plt
import math

def is_zero(val: float, tol: float = 1e-9) -> bool:
    return math.isclose(val, 0.0, abs_tol=tol)

def iloczyn_wektorowy(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def na_odcinku(p, a, b):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def dystans_kwadrat(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def rozwiaz_przeciecie(A, B, C, D):
    typ_wyniku, wynik = "NIE", None
    if A == B and C == D:
        if A == C: typ_wyniku, wynik = "PUNKT", A
    elif A == B:
        if na_odcinku(A, C, D) and is_zero(iloczyn_wektorowy(C, D, A)): typ_wyniku, wynik = "PUNKT", A
    elif C == D:
        if na_odcinku(C, A, B) and is_zero(iloczyn_wektorowy(A, B, C)): typ_wyniku, wynik = "PUNKT", C
    else:
        cp1, cp2, cp3, cp4 = iloczyn_wektorowy(A, B, C), iloczyn_wektorowy(A, B, D), iloczyn_wektorowy(C, D, A), iloczyn_wektorowy(C, D, B)
        if ((cp1 > 0 and cp2 < 0) or (cp1 < 0 and cp2 > 0)) and ((cp3 > 0 and cp4 < 0) or (cp3 < 0 and cp4 > 0)):
            mianownik = (A[0] - B[0]) * (C[1] - D[1]) - (A[1] - B[1]) * (C[0] - D[0])
            if not is_zero(mianownik):
                px = ((A[0] * B[1] - A[1] * B[0]) * (C[0] - D[0]) - (A[0] - B[0]) * (C[0] * D[1] - C[1] * D[0])) / mianownik
                py = ((A[0] * B[1] - A[1] * B[0]) * (C[1] - D[1]) - (A[1] - B[1]) * (C[0] * D[1] - C[1] * D[0])) / mianownik
                typ_wyniku, wynik = "PUNKT", (px, py)
        else:
            pw = []
            if is_zero(cp1) and na_odcinku(C, A, B): pw.append(C)
            if is_zero(cp2) and na_odcinku(D, A, B): pw.append(D)
            if is_zero(cp3) and na_odcinku(A, C, D): pw.append(A)
            if is_zero(cp4) and na_odcinku(B, C, D): pw.append(B)
            if pw:
                unikalne = sorted(list(set(pw)))
                if len(unikalne) == 1: typ_wyniku, wynik = "PUNKT", unikalne[0]
                else: typ_wyniku, wynik = "ODCINEK", (unikalne[0], unikalne[-1])
    return typ_wyniku, wynik

def wyznacz_otoczke(punkty):
    unikalne = sorted(list(set(punkty)))
    n = len(unikalne)
    typ, otoczka = "", []
    if n == 1: typ, otoczka = "punkt", unikalne
    elif n == 2: typ, otoczka = "odcinek", unikalne
    else:
        wspolliniowe = True
        for i in range(2, n):
            if not is_zero(iloczyn_wektorowy(unikalne[0], unikalne[1], unikalne[i])):
                wspolliniowe = False
                break
        if wspolliniowe: typ, otoczka = "odcinek", [unikalne[0], unikalne[-1]]
        else:
            start = min(unikalne, key=lambda p: (p[0], p[1]))
            obecny = start
            while True:
                otoczka.append(obecny)
                nastepny = unikalne[0]
                for p in unikalne:
                    if p == obecny: continue
                    cp = iloczyn_wektorowy(obecny, nastepny, p)
                    if nastepny == obecny or cp > 0 or (is_zero(cp) and dystans_kwadrat(obecny, p) > dystans_kwadrat(obecny, nastepny)): nastepny = p
                obecny = nastepny
                if obecny == start: break
            if len(otoczka) == 3: typ = "trójkąt"
            elif len(otoczka) == 4: typ = "czworokąt"
    return typ, otoczka

st.set_page_config(page_title="Geometria Obliczeniowa", layout="wide")
st.title("📐 Geometria Obliczeniowa")
tab1, tab2 = st.tabs(["✂️ Przecięcie odcinków", "🛑 Otoczka wypukła"])

with tab1:
    st.header("Zbiór punktów przecięcia dwóch odcinków")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Odcinek 1")
        Ax = st.number_input("Punkt A (x)", value=0.0)
        Ay = st.number_input("Punkt A (y)", value=0.0)
        Bx = st.number_input("Punkt B (x)", value=5.0)
        By = st.number_input("Punkt B (y)", value=5.0)
    with col2:
        st.subheader("Odcinek 2")
        Cx = st.number_input("Punkt C (x)", value=0.0)
        Cy = st.number_input("Punkt C (y)", value=5.0)
        Dx = st.number_input("Punkt D (x)", value=5.0)
        Dy = st.number_input("Punkt D (y)", value=0.0)

    if st.button("Oblicz przecięcie", type="primary"):
        typ, wynik = rozwiaz_przeciecie((Ax, Ay), (Bx, By), (Cx, Cy), (Dx, Dy))
        if typ == "NIE": st.warning("Odcinki nie przecinają się")
        elif typ == "PUNKT": st.success(f"Punkt: ({wynik[0]:.2f}, {wynik[1]:.2f})")
        elif typ == "ODCINEK": st.success(f"Odcinek: ({wynik[0][0]:.2f}, {wynik[0][1]:.2f}) do ({wynik[1][0]:.2f}, {wynik[1][1]:.2f})")
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([Ax, Bx], [Ay, By], 'b-', label='Odcinek 1')
        ax.plot([Cx, Dx], [Cy, Dy], 'g-', label='Odcinek 2')
        if typ == "PUNKT": ax.plot(wynik[0], wynik[1], 'ro')
        elif typ == "ODCINEK": ax.plot([wynik[0][0], wynik[1][0]], [wynik[0][1], wynik[1][1]], 'r-', linewidth=4)
        ax.grid(True)
        st.pyplot(fig)

with tab2:
    st.header("Otoczka wypukła zbioru czterech punktów")
    cols = st.columns(4)
    punkty = []
    for i in range(4):
        with cols[i]:
            x = st.number_input(f"P{i+1} (x)", value=float(i), key=f"x{i}")
            y = st.number_input(f"P{i+1} (y)", value=float(i%2), key=f"y{i}")
            punkty.append((x, y))

    if st.button("Wyznacz otoczkę", type="primary"):
        typ, otoczka = wyznacz_otoczke(punkty)
        st.success(f"Figura: {typ.upper()}")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot([p[0] for p in punkty], [p[1] for p in punkty], 'bo')
        hx = [p[0] for p in otoczka] + [otoczka[0][0]] if len(otoczka)>2 else [p[0] for p in otoczka]
        hy = [p[1] for p in otoczka] + [otoczka[0][1]] if len(otoczka)>2 else [p[1] for p in otoczka]
        ax.plot(hx, hy, 'r-')
        ax.grid(True)
        st.pyplot(fig)
