function doSearch() 
{
    // get all terms
    var terms = $("#search_input").val().split(" ");
    
    var results = {};
    
    // go through each term and find target pages
    for (var x in terms)
    {
        var term = terms[x];
        if (term in vocab)
        {
            var matches = vocab[term];
            for (var y in matches)
            {
                var match = matches[y];
                if (!(match in results))
                    results[match] = [];
                
                results[match].push(term);
            }
        }
    }
    
    var output = "<p>";
    
    for (var id in results)
    {
        var words = results[id];
        output += "Post #<a href=\"/" + id + "\">"+id+"</a> contains [" + words + "]<br>";
    }
    
    output += "</p>";
    
    $("#results").html(output);
}

$(function() {
    $(".hideme").hide();
    
    $("#search_input").keydown(function(e) {
        if (e.which == 13)
            doSearch();
    });
    $("#go_search").click(function() {
        doSearch();
    });
    
});