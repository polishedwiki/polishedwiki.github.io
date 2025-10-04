const index = document.getElementById("site-index").href;
var searchData = null;

async function loadSearchData() {
    try {
        const response = await fetch(index + 'search-data.json');
        searchData = await response.json();
    } catch(e) {
        console.error(e.message);
    }
}
loadSearchData();

var onSearchItem = false;
var dropdown = document.getElementById("search-dropdown");
dropdown.style.paddingLeft = "1%";
document.getElementById("search-bar").value = "";

function hideDropdown() {
    if(!onSearchItem) dropdown.style.display = "none";
}
function showDropdown() {
    dropdown.style.display = "block";
}
function createSearchHeading(s) {
    let h = document.createElement("strong");
    h.addEventListener("mouseenter", (e) => {
        onSearchItem = true;
    });
    h.addEventListener("mouseleave", (e) => {
        onSearchItem = false;
    });
    h.appendChild(document.createTextNode(s));
    return h;
}
function createSearchLink(url, name, sec) {
    let a = document.createElement("a");
    a.addEventListener("mouseenter", (e) => {
        onSearchItem = true;
    });
    a.addEventListener("mouseleave", (e) => {
        onSearchItem = false;
    });
    a.href = index + sec + "/" + url;
    a.text = name;
    return a;
}
function querySearch() {
    dropdown.innerHTML = "";
    var input = document.getElementById("search-bar").value;
    input = input.toLowerCase().replace(' ', '').replace('.', '').replace("'", '').replace('-', '');
    if(input.length > 0 && searchData) {
        showDropdown();
        // grab category matches
        var dexMatches = searchData.dexlist.filter(function(x) {
            return x[0].startsWith(input);
        });
        var moveMatches = searchData.movelist.filter(function(x) {
            return x[0].startsWith(input);
        });
        var abilityMatches = searchData.abilitylist.filter(function(x) {
            return x[0].startsWith(input);
        });
        var itemMatches = searchData.itemlist.filter(function(x) {
            return x[0].startsWith(input);
        });
        var tierMatches = searchData.tierlist.filter(function(x) {
            return x.toLowerCase().startsWith(input);
        });
        // insert match links
        if(dexMatches.length > 0) {
            dropdown.appendChild(createSearchHeading("Dex"));
            dexMatches.forEach(x => {
                dropdown.appendChild(createSearchLink(x[0], x[1], "dex"));
            });
        }
        if(moveMatches.length > 0) {
            dropdown.appendChild(createSearchHeading("Moves"));
            moveMatches.forEach(x => {
                dropdown.appendChild(createSearchLink(x[0], x[1], "move"));
            });
        }
        if(abilityMatches.length > 0) {
            dropdown.appendChild(createSearchHeading("Abilities"));
            abilityMatches.forEach(x => {
                dropdown.appendChild(createSearchLink(x[0], x[1], "ability"));
            });
        }
        if(itemMatches.length > 0) {
            dropdown.appendChild(createSearchHeading("Items"));
            itemMatches.forEach(x => {
                dropdown.appendChild(createSearchLink(x[0], x[1], "item"));
            });
        }
        if(tierMatches.length > 0) {
            dropdown.appendChild(createSearchHeading("Tiers"));
            tierMatches.forEach(x => {
                dropdown.appendChild(createSearchLink(x.toLowerCase(), x, "tier"));
            });
        }
    }
    else hideDropdown();
}
