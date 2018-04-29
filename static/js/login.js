function login(){
    var user = $(".login-name").val();
    var pass = $(".login-password").val();

    if(user == "" || pass == ""){
        $(".login-alert").removeClass("hidden");
        $(".login-alert").html("Please Fill Out all Fields!");
        return;
    }

    $.post("/login", {"user": user, "pass": pass}, function(data){
        console.log(data);
        $(".login-alert").removeClass("hidden");
        $(".login-alert").html("Incorrect Username or Password");
    });
}

function signup(){
    var user = $(".signup-name").val();
    var pass = $(".signup-password").val();
    //why not just use required attribute?
    if(user == "" || pass == ""){
        $(".signup-alert").removeClass("hidden");
        $(".signup-alert").html("Please Fill Out all Fields!");
        return;
    }

    $.post("/signup", {"user": user, "pass": pass}, function(data){
        console.log(data);
        $(".signup-alert").removeClass("hidden");
        $(".signup-alert").html("User with that name already exists!");
    });

}

$(document).ready(function() {
    $(".login").click(login);
    $(".signup").click(signup);
    $(".signup-form").keypress(function (e) {
      if (e.which == 13) {
        signup();
        return false;
      }
    });
    $(".login-form").keypress(function (e) {
      if (e.which == 13) {
        login();
        return false;
      }
    });
    $.post("/login", function(data){
        console.log(data);
    });

});



