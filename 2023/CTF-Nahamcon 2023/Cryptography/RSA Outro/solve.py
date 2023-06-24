from Crypto.Util.number import long_to_bytes
from sympy import symbols, Eq, solve

e = 65537
d = 53644719720574049009405552166157712944703190065471668628844223840961631946450717730498953967365343322420070536512779060129496885996597242719829361747640511749156693869638229201455287585480904214599266368010822834345022164868996387818675879350434513617616365498180046935518686332875915988354222223353414730233
phi = 245339427517603729932268783832064063730426585298033269150632512063161372845397117090279828761983426749577401448111514393838579024253942323526130975635388431158721719897730678798030368631518633601688214930936866440646874921076023466048329456035549666361320568433651481926942648024960844810102628182268858421164
ct = 37908069537874314556326131798861989913414869945406191262746923693553489353829208006823679167741985280446948193850665708841487091787325154392435232998215464094465135529738800788684510714606323301203342805866556727186659736657602065547151371338616322720609504154245460113520462221800784939992576122714196812534

p, q = symbols('p q')

equation1 = Eq((p-1)*(q-1), phi)
equation2 = Eq(q*2 + 1, p)

solutions = solve((equation1, equation2), (p, q))

for s in solutions:
    if s[0] > 0 and s[1] > 0: # Get the positive number
        p = s[0]
        q = s[1]
        break

## get q & p with Sagemath :
# solve(
#     [
#         (p-1)*(q-1) == <phi>,
#         q*2+1 == p
#     ], 
#     (p,q)
# )
## Result :
# p = 22151272086162624260144964773788306359813483408214028844466693184639848324793741261237369277221994060881987589587864054264727856701343324425970746727696679
# q = 11075636043081312130072482386894153179906741704107014422233346592319924162396870630618684638610997030440993794793932027132363928350671662212985373363848339

N = int(p*q)

M = pow(ct, d, N)

print(long_to_bytes(M).decode().strip())