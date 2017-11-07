$(function() {
	/*初始化个人中心侧栏*/
	var href = window.location.href;
	$(".usrMenuItem").find("a").each(function(){
		if($(this).attr("href").indexOf("/uc/bill/list/sequence")>=0 && 
				(href.indexOf("/bill/")>=0 && href.indexOf("/sequence")>=0)){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/uc/bill/list/oligo")>=0 && 
				(href.indexOf("/bill/")>=0 && href.indexOf("/oligo")>=0)){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/uc/order/list/oligo")>=0 && 
				(href.indexOf("/order/")>=0 && href.indexOf("/oligo")>=0)){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/uc/order/list/sequence")>=0 && 
				(href.indexOf("/order/")>=0 && href.indexOf("/sequence")>=0)){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/integration")>=0 && href.indexOf("/integration")>=0){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/to_reset_pwd")>=0 && href.indexOf("/to_reset_pwd")>=0){
			$(this).addClass("usrMenuLinkCur");
		}else if($(this).attr("href").indexOf("/uc/user_info")>=0 && href.indexOf("/uc/user_info")>=0){
			$(this).addClass("usrMenuLinkCur");
		}
		
	});
});