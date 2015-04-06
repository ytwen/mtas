<?php
  set_time_limit(0);
  include("../include/PostgreDB.class.php");
  $db=new DB();
  $handle = @fopen('pst_spatial_check_input', "r");
  $count = 0;
  if ($handle) {
    while (($line = fgets($handle)) !== false) {
      $record = explode(":",$line);
      $grids = explode(" ",$record[1]);
      $gridSize = count($grids);
      echo "$record[0]: $gridSize ";
      $sql_grids='';
      foreach($grids AS $grid) {
        $grid = str_replace(array("\r\n", "\n", "\r"), ' ', $grid);
        $sql_grids.="'$grid ',";
      }
      $sql_grids.="''";
      // echo "\n$sql_grids\n";
      $result=$db->query("select * from mtas.pst_exp where pattern in ($sql_grids)");
      $total_grids=$db->num_rows();
      echo "$total_grids\n";
      if ($gridSize ==  $total_grids)
        $count++;
//      break;
    }
  echo "count = $count\n";
 //   if (!feof($handle)) {
  //    echo "Error: unexpected fgets() fail\n";
//    }
    fclose($handle);
  }
?>

