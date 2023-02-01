var inputlogin = false;

$(document).ready(function(){

    $(".nav-list-1").click(function() { 
        $(".nav-list-1").removeClass("active-tab");
        $(this).addClass("active-tab")
    });

    setTimeout(function(){
        $('body').addClass('loaded');
        $('#loader-wrapper .loader-section').fadeOut(500);
      }, 3000);

      $("#user-menu").hover(function() {
        var isHovered = $(this).is(":hover");
        if (isHovered) {
          $(this).children("div").stop().slideDown(300);
        } else {
          $(this).children("div").stop().slideUp(300);
        }
      }); 

  });

// =======  Forgot password  ==========

function keyUp() {
    var loc1 = $(".login-container .login-form").length;  
    var loc2 = 0;
    for (var i = 0; i<loc1; i++ ) {
        if(!$('.login-container .login-form:eq('+i+')').val()) {
            loc2++; 
        }
    };
    if(loc2 == 0) {
        $("#remember").attr("disabled", false);
    } else { 
        
        $("#remember").attr("disabled", true);
    } 
}

function forgotPass() {
    $("#forgotPass-0").hide();
    $("#forgotPass-2").show(); 
}
function forgotCancel() {
    $("#forgotPass-0").show(); 
    $("#forgotPass-2").hide();
}
 