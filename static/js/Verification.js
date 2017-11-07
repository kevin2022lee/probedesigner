<script language="javascript">
$(document).ready(function() {
	 $("input#username").blur(function(){
	  var username = $.trim($("input#username").val());
	  var len=username.length
	  if(len<6){
		  $('label#name_errors').html('<font color="red"><span>这个名字“' + username + '”不能少于6个字符</span></font>');
		  $('#submit').hide();
	  }else{
		  $('#submit').show();
		  $.get("http://{{ localip }}/MyBlog/checkuser/?username="+username,function(data,status){
			     if (data == "null"){
			      $('label#name_errors').html('<font color="red"><span>“' + username + '”可以注册</span></font>');
			      $('#submit').show();
			     }else{
			      $('label#name_errors').html('<font color="red"><span>“' + username + '”已被注册</span></font>');
			      $('#submit').hide();
			     }});
	  }});
	 $("input#password").blur(function(){
		 $('#submit').show();
		 var password = $.trim($("input#password").val());
		 var plen =password.length;
		 if(plen<6){
			 $('label#password_errors').html('<font color="red"><span>密码不能少于6个字符！</span></font>');
			 $('#submit').hide();
		 }else{
			 $('label#password_errors').html('<font color="red"><span>密码符合规范！</span></font>');
			 $('#submit').show();
		 }
	 });
	 $("input#password2").blur(function(){
		 $('#submit').show();
		 var password = $.trim($("input#password").val());
		 var password2 = $.trim($("input#password2").val());
		 var plen =password2.length;
		 if(plen<6){
			 $('label#password2_errors').html('<font color="red"><span>密码不能少于6个字符！</span></font>');
			 $('#submit').hide();
		 }else if(password==password2){
			 $('label#password2_errors').html('<font color="red"><span>两次密码一致！</span></font>');
			 $('#submit').show();
		 }else{
			 $('label#password2_errors').html('<font color="red"><span>两次密码不一致，请重新输入！</span></font>');
			 $('#submit').hide();
		 }
	 });
	 $("input#email").blur(function(){
		 var email_addr=$.trim($("input#email").val());
		 if (!email_addr.match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)){
			 $('label#email_errors').html('<font color="red"><span>邮箱格式不正确！</span></font>');
			 $('#submit').hide();
		 }else{
			 $('label#email_errors').html('<font color="red"><span>邮箱格式正确，请提交注册信息！</span></font>');
			 $('#submit').show();
		 }
	 });
	 });
</script>