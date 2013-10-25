$(document).ready(function(){
	$("button.edit").click(function(){
		var form = $(this).parent();
		formdata = {};
		elements = form.serializeArray();
		for (index in elements){
			element = elements[index];
			formdata[element.name] = element.value;
		}
		$.post("/get_editor", formdata, function(data){
		  form.parent().html(data);
		});
	});
});
