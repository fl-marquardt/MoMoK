// Initialize the map
let map;
let markers = [];

document.addEventListener('DOMContentLoaded', function() {
    // Only initialize the map on the index page
    if (document.getElementById('map')) {
        initMap();
        loadLocations();
    }
});

function initMap() {
    // Create the map centered on Germany
    map = L.map('map').setView([51.1657, 10.4515], 6);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

function loadLocations() {
    // Use static location data instead of fetching from API
    console.log("Using static location data for testing");
    
    // Static location data
    const staticLocations = [
        {
            id: 1,
            name: 'Nordmoor-Standort 1',
            description: 'Messstandort im noerdlichen Moorgebiet',
            coordinates: 'POINT(10.5 53.5)',
            cluster_id: 1,
            cluster_name: 'Nordmoor'
        },
        {
            id: 2,
            name: 'Suedmoor-Standort 1',
            description: 'Messstandort im suedlichen Moorgebiet',
            coordinates: 'POINT(13.5 52.5)',
            cluster_id: 2,
            cluster_name: 'Suedmoor'
        },
        {
            id: 3,
            name: 'Ostmoor-Standort 1',
            description: 'Messstandort im oestlichen Moorgebiet',
            coordinates: 'POINT(14.0 52.0)',
            cluster_id: 3,
            cluster_name: 'Ostmoor'
        },
        {
            id: 4,
            name: 'Westmoor-Standort 1',
            description: 'Messstandort im westlichen Moorgebiet',
            coordinates: 'POINT(9.5 53.0)',
            cluster_id: 4,
            cluster_name: 'Westmoor'
        },
        {
            id: 5,
            name: 'Zentralmoor-Standort 1',
            description: 'Messstandort im zentralen Moorgebiet',
            coordinates: 'POINT(12.0 52.5)',
            cluster_id: 5,
            cluster_name: 'Zentralmoor'
        }
    ];
    
    // Clear existing markers
    clearMarkers();
    
    // Add markers for each location
    staticLocations.forEach(location => {
        addMarker(location);
    });
}

function addMarker(location) {
    // Check if location has coordinates
    if (!location.coordinates) {
        console.warn(`Location ${location.name} has no coordinates`);
        return;
    }
    
    // Parse coordinates from WKT format
    const coords = parseCoordinates(location.coordinates);
    if (!coords) return;
    
    // Create marker
    const marker = L.marker([coords.lat, coords.lng]).addTo(map);
    
    // Add popup with location info
    marker.bindPopup(`
        <h3>${location.name}</h3>
        <p>${location.description || 'Keine Beschreibung verfügbar'}</p>
        <a href="location-detail.html?id=${location.id}">Details anzeigen</a>
    `);
    
    // Store marker for later reference
    markers.push(marker);
}

function clearMarkers() {
    // Remove all markers from the map
    markers.forEach(marker => {
        map.removeLayer(marker);
    });
    
    // Clear markers array
    markers = [];
}

function parseCoordinates(coordinates) {
    // This is a simple parser for the WKT POINT format
    // In a real application, you might want to use a proper WKT parser library
    
    if (!coordinates) return null;
    
    // Handle GeoJSON format
    if (typeof coordinates === 'object' && coordinates.type === 'Point') {
        return {
            lng: coordinates.coordinates[0],
            lat: coordinates.coordinates[1]
        };
    }
    
    // Handle WKT format
    if (typeof coordinates === 'string') {
        // Extract coordinates from POINT(lng lat) format
        const match = coordinates.match(/POINT\(([^ ]+) ([^)]+)\)/);
        if (match) {
            return {
                lng: parseFloat(match[1]),
                lat: parseFloat(match[2])
            };
        }
    }
    
    return null;
}

// Search functionality for the index page
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    
    // Only add event listener on the index page
    if (searchButton && searchInput && document.getElementById('map')) {
        searchButton.addEventListener('click', function() {
            const searchTerm = searchInput.value.trim().toLowerCase();
            
            if (!searchTerm) {
                loadLocations();
                return;
            }
            
            // Fetch all locations and filter them
            fetch('/api/locations')
                .then(response => response.json())
                .then(locations => {
                    // Clear existing markers
                    clearMarkers();
                    
                    // Filter locations by name or description
                    const filteredLocations = locations.filter(location => 
                        location.name.toLowerCase().includes(searchTerm) || 
                        (location.description && location.description.toLowerCase().includes(searchTerm))
                    );
                    
                    // Add markers for filtered locations
                    filteredLocations.forEach(location => {
                        addMarker(location);
                    });
                    
                    // If no results, show message
                    if (filteredLocations.length === 0) {
                        alert('Keine Standorte gefunden, die dem Suchbegriff entsprechen.');
                    }
                })
                .catch(error => {
                    console.error('Error searching locations:', error);
                });
        });
        
        // Add event listener for search input (Enter key)
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && document.getElementById('map')) {
                searchButton.click();
            }
        });
    }
}); 