<?php 
	
	global $lvl_adjust;
	$lvl_adjust=2;
	
	$root_offset=get_root_adjust($lvl_adjust);
	require($root_offset."inc/functions.php");







	
/* 	Ignore this.  It doesn't matter to you. */
	
	function get_root_adjust($lvl_adjust){
		global $lvl_adjust;
		
		switch($lvl_adjust){
			case -1:
				return "";
				break;
			default:
				if($lvl_adjust>=0)
					return str_repeat("../",$lvl_adjust+1);
				else
					die("root offset improperly set");
				break;
		}
		
	}
	
?>