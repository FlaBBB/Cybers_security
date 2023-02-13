<?php
ini_set('memory_limit', '2000M');
function sampling($chars, $size, $combinations = array())
{

    # if it's the first iteration, the first set 
    # of combinations is the same as the set of characters
    if (empty($combinations)) {
        $combinations = $chars;
    }

    # we're done if we're at size 1
    if ($size == 1) {
        return $combinations;
    }

    # initialise array to put new values in
    $new_combinations = array();

    # loop through existing combinations and character set to create strings
    foreach ($combinations as $combination) {
        foreach ($chars as $char) {
            $new_combinations[] = $combination . $char;
        }
    }

    # call same function again for the next iteration
    return sampling($chars, $size - 1, $new_combinations);
}

$magic_hash = "0e200317437806422913347546193344";
$sugar = "198";
$spice = "471";
$everythingnice = "hello";

$ss = "abxdefghijklmnopqrstuvwxyz";
$i = 0;
$array_string = [];
while (isset($ss[$i])) {
    array_splice($array_string, 0, 0, $ss[$i]);
    $i++;
}

$len = 1;
while (true) {
    echo "** Start Brute for Length $len **" . PHP_EOL;
    $combination_array = sampling($array_string, $len);
    $i = 0;
    while (isset($combination_array[$i])) {
        // echo "* Test For Key = " . $combination_array[$i] . PHP_EOL;
        if (md5($combination_array[$i]) == $magic_hash) {
            echo $combination_array[$i];
            die;
        }
        $i++;
    }
    $len++;
}
