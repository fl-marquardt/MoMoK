// Initialize the map
let map;
let markers = [];

document.addEventListener('DOMContentLoaded', function() {
    initMap();
    loadLocations();
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
    // Fetch locations from the API
    fetch('/api/locations')
        .then(response => response.json())
        .then(locations => {
            // Clear existing markers
            clearMarkers();
            
            // Add markers for each location
            locations.forEach(location => {
                addMarker(location);
            });
        })
        .catch(error => {
            console.error('Error loading locations:', error);
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

// Search functionality
document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();
    
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