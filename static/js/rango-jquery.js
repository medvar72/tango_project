$(document).ready(function() {

        // JQuery code to be added in here.
        $("#about-btn2").click( function(event){
            alert("You clicked the Button using JQuery!");
        });

        $("p").hover(function(){
            $(this).css('color','red');
        },
        function(){
            $(this).css('color','blue');
        }
        );

        $("#about-btn1").addClass('btn btn-info');
        $("#about-btn2").addClass('btn btn-info');

        $("#about-btn2").click(function(event){
            msgstr = $("#msg").html();
            msgstr = msgstr + "o";
            $("#msg").html(msgstr);

        });

        // JQuery code to be added in here.
        $(".rango-add").click( function(event){
            alert("You clicked the Button using JQuery!");
        });

});

