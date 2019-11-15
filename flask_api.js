$(document).ready(function () {
  


  function ajaxCallsFunc(type, url, contentType, data, callback) {
    $.ajax({
      type: type,
      url: url,
      contentType: contentType,
      data: data,
      success: callback
    });
  }
  // $("#divReadOnlyFields :input").attr("disabled", true);

  
  //document.getElementById("drawGraph").disabled = true;
  $("#drawGraph").prop("disabled", true);
  
  $("#drawGraph").click(function () {
    
     var dummydata3 = JSON.stringify({
      "url": 'git@git.cs.slu.edu:courses/fall19/csci_5030/sample_application.git'
    });
    
    ajaxCallsFunc('POST', "http://127.0.0.1:5000/run", 'application/json', dummydata3, function (branches) {

	var commitCollection = "<a class=\"collection-item\"><span class=\"new badge\">{0}</span>{1}</a>"
	$commit_col = $("#test_cases")
	for(var x in branches){
	  if (branches[x] == "Success"){
	    $commit_col.append("<a class=\"collection-item\"><span class=\"new badge green\" data-badge-caption=\" \">"+branches[x]+"</span>"+x+"</a>")  
	  }
	  else{
	    $commit_col.append("<a class=\"collection-item\"><span class=\"new badge red\" data-badge-caption=\" \">"+branches[x]+"</span>"+x+"</a>")
	    
	  }
	  
	}
	
	console.log(branches)

      });
    
    });
  
  $("#commit").click(function () {
    
     var dummydata3 = JSON.stringify({
      "url": 'git@git.cs.slu.edu:courses/fall19/csci_5030/sample_application.git'
    });
    
    ajaxCallsFunc('POST', "http://127.0.0.1:5000/get_commits", 'application/json', dummydata3, function (branches) {
	var commitCollection = "<a class=\"collection-item\"><span class=\"new badge\">{0}</span>{1}</a>"
	$commit_col = $("#commit_col")
	for(var x in branches){
	  $commit_col.append("<a class=\"collection-item\"><span class=\"new badge\" data-badge-caption=\" \">'commit time'</span>"+branches[x]+"</a>")
	}
	console.log(branches)
	$("#drawGraph").prop("disabled", false);
      });
    
    
    
    
    });

}); 
