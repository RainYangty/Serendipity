<?php
    header('Content-type: text/html; charset=utf-8');
    mb_internal_encoding('UTF-8');
    $file_name =  $_FILES['file']['name']; //getting file name
    $tmp_name = $_FILES['file']['tmp_name']; //getting temp_name of file
    $name = explode('.',$file_name);
    $file_flag = $_POST["load_file_name"];
    echo $_POST["load_file_name"];
    $file_name = iconv("GB2312//IGNORE","UTF-8", $file_name);
    echo "    ".$file_name;
    $file_up_name = $file_name;
    move_uploaded_file($tmp_name, "files/".$file_up_name);
    $file_write = fopen("files/ans.txt", "a+", "UTF-8");
    fwrite($file_write, $file_flag."_".$file_up_name."\n");
?>
