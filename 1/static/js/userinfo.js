$(function(){
	$("input").focus(function(){
		$("input").removeClass("focus");
		$(this).addClass("focus");
	});
	
	$(".to_modify").click(function(){
		$(".user_detail_box").hide();
		$(".modify_userinfo_box").show();
	});
	
	$(".modify_userinfo").click(function(){
		var name = $.trim($("input[name='name']").val());
		var companyName = $.trim($("input[name='companyName']").val());
		var FamilyName = $.trim($("input[name='FamilyName']").val());
		var LastName = $.trim($("input[name='LastName']").val());
		if(name == "" || companyName == "" || FamilyName == "" || LastName == ""){
			$(".modify_tips_box").show();
			$(".modify_tips").html("信息不完整，请完善")
		}else{
			$("#modify_userinfo").submit();
		}
	});
});