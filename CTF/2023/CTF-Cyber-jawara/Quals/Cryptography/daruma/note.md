# Note
$n = p \cdot q$
$n2 = n^2$
$\phi = n2 \cdot (p - 1) \cdot (q - 1)$
$k$ is coprime with $n2$
$1 < k < n2$
$e$ is coprime with $\phi$
$1 < e < \phi$
$d = e^{-1} \mod{\phi}$
$\beta = g^l \mod{n2}$

#### Encryption
public is $(n2,e,\beta)$
input $(n,e,\beta,m)$
$$\begin{aligned}
r &= k^e \mod n2 \\
s &= m \cdot k \cdot \beta^l \mod n2 
\end{aligned}$$
output $(r,s)$

#### Decryption
private is $(d,l)$
$$\begin{aligned}
m &= s \cdot r^{-d} \cdot \beta^{-l} \mod n2
\end{aligned}$$
output $(m)$

#### Solve
$$\begin{aligned}
s &= m \cdot k \cdot \beta^l \mod n2 \\
m &= s \cdot k^{-1} \cdot \beta^{-l} \mod n2 \\
s \cdot k^{-1} \cdot \beta^{-l} \mod n2 &\equiv s \cdot r^{-d} \cdot \beta^{-l} \mod n2 \\
k^{-1} &\equiv r^{-d} \mod n2 
\end{aligned}$$
user controlled encryption variable is $(n,e,\beta,m)$ (input)
restriction:
- $2000 < nBitLength < 10000$
- $nBitLength$ is not prime

if $e = 1$
$$\begin{aligned}
r_{inp} &= k^{e_{inp}} \mod n2 \\
r_{inp} &= k^1 \mod n2 \\
r_{inp} &= k \mod n2
\end{aligned}$$
we leak $k$
then if $m = 1$
$$\begin{aligned}
s_{inp} &= m_{inp} \cdot k \cdot \beta^l \mod n2 \\
s_{inp} &= 1 \cdot k \cdot \beta^l \mod n2 \\
s_{inp} &= k \cdot \beta^l \mod n2 \\
s^{-1}_{inp} &= k^{-1} \cdot \beta^{-l}  \mod n2 \\ \\
m_{flag} &= s_{flag} \cdot s_{inp}^{-1} \mod n2 \\ 
m_{flag} &= s_{flag} \cdot k^{-1} \cdot \beta^{-l} \mod n2
\end{aligned}$$
we got the flag