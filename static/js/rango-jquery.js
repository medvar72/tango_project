$(document).ready(function() {

        // JQuery code to be added in here.
        $("#about-btn").click( function(event){
            alert("You clicked the Button using JQuery!");
        });

        $("p").hover(function(){
            $(this).css('color','red');
        },
        function(){
            $(this).css('color','blue');
        }
        );

        $("about-btn").addClass('btn btn-primary');

        $("#about-btn").click(function(event){
            msgstr = $("#msg").html();
            msgstr = msgstr + "o";
            $("#msg").html(msgstr);

        });
});

