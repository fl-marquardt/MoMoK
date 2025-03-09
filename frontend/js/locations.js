// Locations page functionality
let locationsMap;
let locationMarkers = [];
let locationData = [];

document.addEventListener('DOMContentLoaded', function() {
    // Initialize view toggle buttons
    const listViewBtn = document.getElementById('listViewBtn');
    const mapViewBtn = document.getElementById('mapViewBtn');
    const listView = document.getElementById('listView');
    const mapView = document.getElementById('mapView');
    
    // Add event listeners for view toggle
    if (listViewBtn && mapViewBtn) {
        listViewBtn.addEventListener('click', function() {
            listView.style.display = 'block';
            mapView.style.display = 'none';
            listViewBtn.classList.add('active');
            mapViewBtn.classList.remove('active');
        });
        
        mapViewBtn.addEventListener('click', function() {
            listView.style.display = 'none';
            mapView.style.display = 'block';
            mapViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            
            // Initialize map if it hasn't been initialized yet
            if (!locationsMap) {
                initLocationsMap();
            }
            
            // Make sure the map renders correctly after becoming visible
            if (locationsMap) {
                locationsMap.invalidateSize();
            }
        });
    }
    
    // Load locations data
    loadLocationsData();
});

function initLocationsMap() {
    // Create the map centered on Germany
    locationsMap = L.map('locationsMap').setView([51.1657, 10.4515], 6);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(locationsMap);
}

function loadLocationsData() {
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
    
    // Use the static data
    locationData = staticLocations;
    
    // Populate the table with locations
    populateLocationsTable(staticLocations);
    
    // If map view is active, show locations on map
    if (document.getElementById('mapViewBtn').classList.contains('active')) {
        showAllLocationsOnMap();
    }
}

function populateLocationsTable(locations) {
    const tableBody = document.querySelector('#locationsTable tbody');
    if (!tableBody) return;
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Add a row for each location
    locations.forEach(location => {
        const row = document.createElement('tr');
        
        // Create cells for each column
        row.innerHTML = `
            <td>${location.id}</td>
            <td>${location.name}</td>
            <td>${location.description || '-'}</td>
            <td>${location.cluster || '-'}</td>
            <td>
                <button class="view-btn" data-id="${location.id}">Ansehen</button>
                <button class="edit-btn" data-id="${location.id}">Bearbeiten</button>
                <button class="delete-btn" data-id="${location.id}">Löschen</button>
                <button class="show-on-map-btn" data-id="${location.id}">Auf Karte zeigen</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Add event listeners for the action buttons
    addTableButtonListeners();
}

function addTableButtonListeners() {
    // View button
    document.querySelectorAll('.view-btn').forEach(button => {
        button.addEventListener('click', function() {
            const locationId = this.getAttribute('data-id');
            window.location.href = `location-detail.html?id=${locationId}`;
        });
    });
    
    // Edit button
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const locationId = this.getAttribute('data-id');
            window.location.href = `location-edit.html?id=${locationId}`;
        });
    });
    
    // Delete button
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const locationId = this.getAttribute('data-id');
            if (confirm('Sind Sie sicher, dass Sie diesen Standort löschen möchten?')) {
                deleteLocation(locationId);
            }
        });
    });
    
    // Show on map button
    document.querySelectorAll('.show-on-map-btn').forEach(button => {
        button.addEventListener('click', function() {
            const locationId = this.getAttribute('data-id');
            const location = locationData.find(loc => loc.id == locationId);
            
            if (location) {
                // Switch to map view
                document.getElementById('mapViewBtn').click();
                
                // Show the location on the map
                showLocationOnMap(location);
            }
        });
    });
}

function showLocationOnMap(location) {
    // Make sure the map is initialized
    if (!locationsMap) {
        initLocationsMap();
    }
    
    // Clear existing markers
    clearLocationMarkers();
    
    // Add marker for the location
    addLocationMarker(location);
    
    // Center the map on the location
    const coords = parseCoordinates(location.coordinates);
    if (coords) {
        locationsMap.setView([coords.lat, coords.lng], 10);
    }
}

function showAllLocationsOnMap() {
    // Make sure the map is initialized
    if (!locationsMap) {
        initLocationsMap();
    }
    
    // Clear existing markers
    clearLocationMarkers();
    
    // Add markers for all locations
    locationData.forEach(location => {
        addLocationMarker(location);
    });
    
    // Fit the map to show all markers
    if (locationMarkers.length > 0) {
        const group = new L.featureGroup(locationMarkers);
        locationsMap.fitBounds(group.getBounds().pad(0.1));
    }
}

function addLocationMarker(location) {
    // Check if location has coordinates
    if (!location.coordinates) {
        console.warn(`Location ${location.name} has no coordinates`);
        return;
    }
    
    // Parse coordinates
    const coords = parseCoordinates(location.coordinates);
    if (!coords) return;
    
    // Create marker
    const marker = L.marker([coords.lat, coords.lng]).addTo(locationsMap);
    
    // Add popup with location info
    marker.bindPopup(`
        <h3>${location.name}</h3>
        <p>${location.description || 'Keine Beschreibung verfügbar'}</p>
        <a href="location-detail.html?id=${location.id}">Details anzeigen</a>
    `);
    
    // Store marker for later reference
    locationMarkers.push(marker);
}

function clearLocationMarkers() {
    // Remove all markers from the map
    locationMarkers.forEach(marker => {
        locationsMap.removeLayer(marker);
    });
    
    // Clear markers array
    locationMarkers = [];
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

function deleteLocation(locationId) {
    // Delete location via API
    fetch(`/api/locations/${locationId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            // Reload locations after successful deletion
            loadLocationsData();
            showStatusMessage('Standort erfolgreich gelöscht.', 'success');
        } else {
            throw new Error('Failed to delete location');
        }
    })
    .catch(error => {
        console.error('Error deleting location:', error);
        showStatusMessage('Fehler beim Löschen des Standorts.', 'error');
    });
}

function showStatusMessage(message, type = 'info') {
    const statusElement = document.getElementById('statusMessage');
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.className = 'status-message ' + type;
        statusElement.style.display = 'block';
        
        // Hide the message after 5 seconds
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 5000);
    }
}

// Add search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', function() {
            const searchTerm = searchInput.value.trim().toLowerCase();
            
            if (!searchTerm) {
                // If search is empty, show all locations
                populateLocationsTable(locationData);
                return;
            }
            
            // Filter locations by name or description
            const filteredLocations = locationData.filter(location => 
                location.name.toLowerCase().includes(searchTerm) || 
                (location.description && location.description.toLowerCase().includes(searchTerm))
            );
            
            // Update the table with filtered locations
            populateLocationsTable(filteredLocations);
            
            // If in map view, update the map markers
            if (document.getElementById('mapView').style.display !== 'none') {
                clearLocationMarkers();
                filteredLocations.forEach(location => {
                    addLocationMarker(location);
                });
            }
            
            // If no results, show message
            if (filteredLocations.length === 0) {
                showStatusMessage('Keine Standorte gefunden, die dem Suchbegriff entsprechen.', 'info');
            }
        });
    }
}); 