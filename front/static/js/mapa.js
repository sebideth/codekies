const input = document.getElementById("ubicacion");
const suggestionsDiv = document.getElementById("suggestions");
const mapDiv = document.getElementById("map");

// centrado en Arg
const map = L.map(mapDiv).setView([-34.6037, -58.3816], 5);  

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '© OpenStreetMap contributors',
}).addTo(map);

// API Key geoapify
const apiKey = "9d82b10b02a649e883471f803f7ffed5";

input.addEventListener("input", function() {
    const query = input.value.trim();
    if (query.length >= 3) {  
        fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${query}&filter=countrycode:ar&format=json&apiKey=${apiKey}`)
            .then(response => response.json())
            .then(data => {
                suggestionsDiv.innerHTML = "";
                data.results.forEach(result => {
                    const suggestion = document.createElement("div");
                    suggestion.classList.add("suggestion-item");
                    suggestion.innerText = result.formatted;
                    suggestion.addEventListener("click", function() {
                        input.value = result.formatted;
                        map.setView([result.lat, result.lon], 13);  
                        L.marker([result.lat, result.lon]).addTo(map);  
                        suggestionsDiv.innerHTML = "";  
                    });
                    suggestionsDiv.appendChild(suggestion);
                });
            })
            .catch(error => {
                console.error("Error al obtener los datos:", error);
            });
    } else {
        suggestionsDiv.innerHTML = "";
    }
});