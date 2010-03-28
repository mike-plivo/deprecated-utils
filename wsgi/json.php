<?php

$fd = fopen("http://127.0.0.1/cc/selfhangup", "r");
$var = stream_get_contents($fd);
fclose($fd);

$jvar = json_decode($var, true);

var_dump($jvar);

?>
