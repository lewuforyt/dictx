
function getname(){
    var name = window.prompt("Hangi başlığa bakınız verilecek?");
    if (name!= null && name!= ""){
        var text = document.getElementById("editor").value+= "(bkz: "+name+")";
        kelimeSayaci()
    }
}

function createLikeSys(id1, id2){
    document.getElementById(id1).addEventListener("click", displayDate);



    function displayDate() {
        document.getElementById(id1).className = "far fa-heart liked";
        document.getElementById(id1).id = id2;

        document.getElementById(id2).addEventListener("click", displayDate2);
    }

    function displayDate2() {
        document.getElementById(id2).className = "far fa-heart like";
        document.getElementById(id2).id = id1;

        document.getElementById(id1).addEventListener("click", displayDate);
    }
}

function w3_open() {
    document.getElementById("main").style.marginLeft = "25%";
    document.getElementById("mySidebar").style.width = "20%";
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("openNav").style.display = 'none';
    }

    function w3_close() {
    document.getElementById("main").style.marginLeft = "0%";
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("openNav").style.display = "inline-block";
    } 

    
    w3_open()

    function likeit(id){
        document.getElementById(id).className = "far fa-heart liked";
        //post işlemleri
    }

function kelimeSayaci(){
    var uzunluk = document.getElementById("editor").value.length;

    document.getElementById("sayac").innerText = uzunluk+"/500";
}

function entryEkle(){
    var http = new XMLHttpRequest();
    var url = '/ekle';
    var id = document.getElementById("yolla").getAttribute("name");

    var params = 'message='+document.getElementById("editor").value+"&baslikId="+id;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            document.getElementById("editor").value = "";
            location.reload();
        }
        else if (http.readyState == 4 && http.status == 429)
        {
            alert("Çok hızlı entry giriyorsun. Saatte 12 entry girebilirsin.")
        }
        
    } 
    http.send(params);
    
}

function report(){
    var http = new XMLHttpRequest();
    var id = document.getElementById("yolla").getAttribute("name");
    var url = '/report/'+id;


    var params = 'reason='+document.getElementById("editor").value+"&entryId="+id;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            location.reload();
        }
        
    }
    http.send(params);
}


function deleteMsg(id){
    var http = new XMLHttpRequest();
    var url = '/deleteMessage';

    var params = "entryId="+id;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            location.reload();
        }
        
    }
    http.send(params);
}

