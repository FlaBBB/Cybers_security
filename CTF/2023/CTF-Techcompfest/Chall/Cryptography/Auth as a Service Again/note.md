#### initial Auth
- $p$, prime $512$ bit (**public**)
- $q,\ g = (\lfloor\frac{p - 1}{k}\rfloor,\ 2^{k} \mod{p}) \begin{cases}k&(2\leq k\lt 129)\end{cases}$ (**public**)
- $2\leq x\lt q$ (**private**)
- $y = g^x \mod{p}$ (**private**)

in here, $k$ can get from finding discrete log of $g$ to base $2$ in $\mathbb{Z}_p^*$ or get from intersection of $p - 1$ and $q$.

#### register
**input:**
- username

**process:**
- cookies ($m$), generated from username, is_admin, and uuid
- $hm = hash(m)$
- $2\leq k\leq q - 2$
- $r = (g^k \mod{p}) \mod{q}$
- $$\begin{align}
    s &= ((hm + x \cdot r) \cdot k^{-1})^{sbit(m)} \mod{q} \\
    s &= (hm + x \cdot r)^{sbit(m)} \cdot k^{-sbit(m)} \mod{q} \\
\end{align}$$

**output:**
- cookies ($m, r, s$)


#### login
**input:**
- cookies ($m, r, s$)

**verify:**
- check_input = $s$ if $sbit(m) \neq 0$ else $[sq, p-sq] \begin{cases} sq = sqrtMod(s, q) \end{cases}$

$$\begin{align}
    t &= s^{sbit(m)^{-1}\mod{\phi(q)}} \mod{q} \\
    u_1 &= g^{hm \cdot t^{-1} \mod{q}} \mod{p} \\
    u_2 &= y^{r \cdot t^{-1} \mod{q}} \mod{p} \\
    \\
    u &= u_1 \cdot u_2 \mod{q} \\
\end{align}$$
assert: $r = u \mod{q}$


#### get flag
$$\begin{align}
    t &= (hm + x \cdot r) \cdot k^{-1} \mod{q} \\
    t_{inv} &= (hm + x \cdot r)^{-1} \cdot k \mod{q} \\
    u &= (g^hm \cdot y^r)^{t_{inv}} \mod{q} \\
\end{align}$$