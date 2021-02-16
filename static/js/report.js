function deleteReport(){
    var http = new XMLHttpRequest();
    var url = '/deleteReport';
    var id = document.getElementById("delete-sil").getAttribute("name");

    var params = "reportId="+id;
    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            location.reload();
        }
        
    }
    http.send(params);
}