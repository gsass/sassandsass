<?php 
	
	global $lvl_adjust;
	$lvl_adjust=2;
	
	$root_offset=get_root_adjust($lvl_adjust);
	require($root_offset."inc/functions.php");	require_once($root_offset."inc/simplepie/simplepie.inc");	
/* 	NOTE THIS LINE.  THIS IS WHERE ALL UNIQUE PAGE CONTENT IS LOADED */
	load_local_content($root_offset."content/aboutus.xml");
	
	include($root_offset."inc/header.php");
	include($root_offset."inc/bodyopen.php");
	include($root_offset."inc/lccontent.php");
/*loading some twitter data via SimplePie*/	load_twitter_content();?>			<div id="rightcolumn">				<div class="news">					<span><b>News</b></span>					<div class="leftbracket"></div>					<p><a href="http://www.twitter.com/sassandsass"><?php 						global $tweets; 						$twv=array_values($tweets);						echo $twv[0]; ?></a>					<br>					<!-- <a class="icon" href="blog"><img src= "<?php echo get_root_adjust($lvl_adjust)."img/wplogo.png" ?>" /></a> -->					<a class="icon" href="http://www.twitter.com/sasandsass"><img src= "<?php echo get_root_adjust($lvl_adjust)."img/twlogo.png" ?>" /> </a>										</p>								</div>								<div class="story">					<?php					load_tumblr_content();					global $posts;					$twv=array_values($posts);					for(i=0; i<count($posts); i++){						echo $posts[i];						echo "<br />";					}					?>				</div>							</div>		</div>	<?php		include($root_offset."inc/nav.php");
	
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