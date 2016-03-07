function doSearch() 
{
    // get all terms
    var terms = $("#search_input").val().toLowerCase();
    
    terms = terms.replace(/[?!-.:/]/g, " ").split(" ");;
    
    // set terms to hash
    location.hash = terms.join(":");
    
    var results = {};
    
    // go through each term and find target pages
    for (var x in terms)
    {
        // ignore empty string and space
        if (x == "" || x == " ")
            continue;
        
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
    
    // if a hash is set, fill input text and search
    if (location.hash != "" && location.haah != "#")
    {
        var terms = location.hash.split(":");
        if (terms[0][0] == "#")
            terms[0] = terms[0].substring(1);
        
        $("#search_input").val(terms.join(" "));
        $("#go_search").click();
    }
});