$(document).ready(function(){

	$(".next2it").click(function() {
		$(this).next().next(".slide").addClass("placed");
		$(this).parent(".slide").addClass("superplaced");
	});
	$(".closeit").click(function() {
		$(this).parent(".slide").removeClass("placed");
		$(this).parent().parent(".slide").removeClass("superplaced");
	});
    
});