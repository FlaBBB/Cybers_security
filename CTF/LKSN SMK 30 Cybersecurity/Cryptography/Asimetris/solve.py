# p+q =  223379143686991605913757974086904956084745586781597190619692710985715650928911483513137509353123147597339665299059424072622476694246904156546927298408118269271123361806343238722602036442655115818340034688896232223189973295741658184001817204589243258978967212714184766370816815910237779187926328093977218881808
# p-q =  8041188401302580231953232611470031705073372820076201961972980796044157146478209529522752670787863054017473957201598215740991630617215055640514254433826877554617215635857445835948266118499779235308281783120188321470356533581561152123025082918028073334752568205606113149574997211657553613234856299620174308066

p = (223379143686991605913757974086904956084745586781597190619692710985715650928911483513137509353123147597339665299059424072622476694246904156546927298408118269271123361806343238722602036442655115818340034688896232223189973295741658184001817204589243258978967212714184766370816815910237779187926328093977218881808 + 8041188401302580231953232611470031705073372820076201961972980796044157146478209529522752670787863054017473957201598215740991630617215055640514254433826877554617215635857445835948266118499779235308281783120188321470356533581561152123025082918028073334752568205606113149574997211657553613234856299620174308066) // 2
q = 223379143686991605913757974086904956084745586781597190619692710985715650928911483513137509353123147597339665299059424072622476694246904156546927298408118269271123361806343238722602036442655115818340034688896232223189973295741658184001817204589243258978967212714184766370816815910237779187926328093977218881808 - p
c = 10300835035449517657293596853464312614316283989546934826954268189206177754618159391493847628846386983594848973069333222681289574265506479282594430832281272626025503015619922945095110975459270730895415932764100259581369195606835752929525904329946439591174871297686126596470454219680065756528222657418502021813782109875446270491960835278563354484559753896586269193126227786098131973668060123305060570045988964442710962288533797999964923158348729711945491538777073724367351632467294727199953799815141141954884309061637335804185473426855488521046963093636687150594055437166201408552467239350431374970659499102590050673445
e = 65537
N = p*q

phi = (p-1)*(q-1)
d = pow(e,-1,phi)
M = pow(c,d,N)

from Crypto.Util.number import long_to_bytes
print(long_to_bytes(M).decode())