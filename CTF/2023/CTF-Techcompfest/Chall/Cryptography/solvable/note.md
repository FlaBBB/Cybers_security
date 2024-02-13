{p, q, r} has size 512 bits.
$$\begin{aligned}
    n &= p \cdot q \cdot r \\
    c &= m^e \mod{n} \\
    \\
    s &\equiv q \cdot r \mod{2^{512}} \\
    u &\equiv e^{s} + e^{-s} + e^{-2s} \mod{N} \\
    ue^{2s} &\equiv e^{3s} + e^{s} + 1 \mod{N} \\
    e^{3s} + e^{s} + 1 - ue^{2s} &\equiv 0 \mod{N} \\
    \\
    x &= e^{s} \\
    x^3 + x + 1 - ux^2 &\equiv 0 \mod{N} \\
\end{aligned}$$
we got polynomials form. we can get candidate of $s$ by solving this polynomial, and do discrete log with $e$ to get $s$.
$$\begin{aligned}
    qr &\equiv s \mod{2^{512}} \\
    \\
    pqr &\equiv n \mod{2^{512}} \\
    p &\equiv n(qr)^{-1} \mod{2^{512}} \\
    p &\equiv ns^{-1} \mod{2^{512}} \\
\end{aligned}$$
then now we get the $p$ and $s$, and we can get $m$ using only $p$.
$$\begin{aligned}
    m^e &\equiv c \mod{n} \\
    m^e &\equiv c \mod{p} \\
    m &\equiv c^d \mod{p} \\
\end{aligned}$$