<?php

$name = "as";
echo htmlspecialchars("$name\n"); 
var_dump(get_html_translation_table(HTML_SPECIALCHARS, ENT_QUOTES));