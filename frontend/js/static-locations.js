// Static locations data for testing map functionality
document.addEventListener('DOMContentLoaded', function() {
    // Override the loadLocationsData function to use static data instead of API
    window.loadLocationsData = function() {
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
    };
}); 