$(document).ready(function(){


    //pour mettre une hauteur minimum
    var Hscreen=screen.height;
    $("#mainContainer").css("min-height",Hscreen-300)

    //texte défilant
    var elem = document.getElementById("move")
    var pos = 0
    function frame(){
        if(pos === document.body.clientWidth){
            pos = -10
            pos++
        }
 
        else{
            pos++
            elem.style.left = pos + 'px'
        }
    }
    setInterval(frame,8)

    var produit = $(".cartItem")

    function calculTotalPrice(pid){

        var pu = parseFloat($("#pu"+pid).text()); 
        
        var q = parseInt($("#q"+pid).text());

        $("#pt"+pid).text(pu*q);
    }
    
    for (let i=0;i<produit.length;i++){

        var id = produit[i].id.slice(3)
        console.log(id);

        calculTotalPrice(id);
    }


    //ajouter les quantités dans le panier
    $(".addquantite").on("click",function(e){
        var pr_id = this.id.slice(4)
        var elt = $(this)

        $.ajax(
            {
                type:"post",
                url : "/panier/"+pr_id+"/plusq",
                
                success: function( data ) 
                {   console.log(data)

                    elt.next().children().first().text(function(i, origText){
                        number = 1 + parseInt(origText)        
                        return number;
                    });
                    
                    calculTotalPrice(pr_id);


                    
                },
                error : function(err){
                    console.log(err)
                    if (err.status == 403){

                        window.location.href = "/login"

                    }

                    else{
                        console.log(err.statusText+" "+err.status)
                        alert(err.statusText+" "+err.status)
                    }

                }
            }
        )




    })

    //diminuer les quantités dans le panier
    $(".removequantite").on("click",function(e){
        var pr_id = this.id.slice(5)
        var elt = $(this)

        $.ajax(
            {
                type:"post",
                url : "/panier/"+pr_id+"/moinsq",
                
                success: function( data ) 
                {   console.log(data)

                    elt.prev().children().first().text(function(i, origText){
                        number = parseInt(origText) 
                        
                        if(number <= 1)
                            return number
                        else
                            return number-1;
                    });

                    calculTotalPrice(pr_id);

                    
                },
                error : function(err){
                    console.log(err)
                    if (err.status == 403){

                        window.location.href = "/login"

                    }

                    else{
                        console.log(err.statusText+" "+err.status)
                        alert(err.statusText+" "+err.status)
                    }

                }
            }
        )




    })


    
});