// Debug function to check if data is loaded
function checkDataLoaded() {
    console.log("Checking search data...");
    console.log("vocab keys:", Object.keys(vocab || {}).length);
    console.log("lookup keys:", Object.keys(lookup || {}).length); 
    console.log("postmeta keys:", Object.keys(postmeta || {}).length);
}

function renderSearchResult(postId, matchedTerms) {
    const meta = postmeta[postId];
    if (!meta) {
        console.warn("No metadata found for post ID:", postId);
        return '';
    }
    
    // Build thumbnail HTML if post has image
    let thumbnailHtml = '';
    if (meta.hasImage) {
        thumbnailHtml = `<img src="${meta.preview}" alt="Preview" class="blog-thumbnail">`;
    }
    
    // Build matched terms display
    const matchedTermsHtml = `<div class="matched-terms">Matched terms: <em>[${matchedTerms.join(', ')}]</em></div>`;
    const archivedLabel = meta.archived ? '<span class="archived-tag">[ARCHIVED]</span>' : '';
    // Build full blog entry HTML similar to blog listing
    return `<div class="blog-entry${meta.hasImage ? '' : ' no-image'}">
        ${thumbnailHtml}
        <div class="blog-content">
            <div class="blog-header">
                <a href="/blog/${meta.dirname}/">${meta.title}</a>
                <span class="blog-date">${meta.date}</span>
                ${archivedLabel}
            </div>
            <div class="minidescription">${meta.description}</div>
            ${matchedTermsHtml}
        </div>
    </div>`;
}

function search() {
    console.log("Search function called");
    checkDataLoaded();
    
    var query = $("#search_input").val().toLowerCase().trim();
    console.log("Search query:", query);
    
    if (query.length == 0) {
        $("#results").html("");
        return;
    }
    
    // Check if required data exists
    if (!vocab || !postmeta || !lookup) {
        $("#results").html("<p>Search data not loaded properly. Please refresh the page.</p>");
        return;
    }
    
    var words = query.split(" ").filter(word => word.length > 0);
    var matches = {};
    var matchedTerms = {};
    
    console.log("Search words:", words);
    
    // Find matches for each word
    for (var i = 0; i < words.length; i++) {
        var word = words[i];
        console.log("Looking for word:", word);
        
        if (word in vocab) {
            var postIds = Array.from(vocab[word]); // Convert Set to Array if needed
            console.log("Found", postIds.length, "posts for word:", word);
            
            for (var j = 0; j < postIds.length; j++) {
                var postId = postIds[j];
                if (!(postId in matches)) {
                    matches[postId] = 0;
                    matchedTerms[postId] = [];
                }
                matches[postId]++;
                if (matchedTerms[postId].indexOf(word) === -1) {
                    matchedTerms[postId].push(word);
                }
            }
        } else {
            console.log("Word not found in vocab:", word);
        }
    }
    
    console.log("Total matches found:", Object.keys(matches).length);
    
    // sort results by number of matched terms (relevance)
    // var sortedMatches = Object.keys(matches).sort(function(a, b) {
    //     return matches[b] - matches[a];
    // });

    // since we don't have that many posts, let's always do reverse chronological
    // instead of frequency, TODO: best match score + tiebreak with date
    var sortedMatches = Object.keys(matches).sort(function(a, b) {
        if (!(a in postmeta) || !(b in postmeta)) {
            return 0; // If metadata is missing, consider them equal
        }
        if (!postmeta[a].date || !postmeta[b].date) {
            return 0; // If date is missing, consider them equal
        }
        var dateA = new Date(postmeta[a].date);
        var dateB = new Date(postmeta[b].date);
        return dateB - dateA; // Newest first
    });
    
    // create HTML for results
    var html = "";
    if (sortedMatches.length == 0) {
        html = "<p>No results found for \"" + query + "\"</p>";
    } else {
        html = "<h3>Found " + sortedMatches.length + " result" + (sortedMatches.length == 1 ? "" : "s") + " for \"" + query + "\":</h3>";
        for (var i = 0; i < sortedMatches.length; i++) {
            var postId = sortedMatches[i];
            var resultHtml = renderSearchResult(postId, matchedTerms[postId]);
            if (resultHtml) {
                html += resultHtml;
            }
        }
    }
    
    $("#results").html(html);
    console.log("Search results rendered");
}

// Wait for document and jQuery to be ready
$(document).ready(function() {
    console.log("Document ready, setting up search handlers");
    
    // Execute search when button is clicked or Enter is pressed
    $("#go_search").click(function(e) {
        e.preventDefault();
        search();
    });
    
    $("#search_input").keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            search();
        }
    });
    
    // Hide loading message
    $(".hideme").hide();
    
    // Debug: Log initial state
    setTimeout(checkDataLoaded, 1000);
});