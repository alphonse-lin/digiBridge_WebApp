export const menus = [{
        id: '1',
        label: 'Drone Station',
        url: 'http://localhost:8080/Dashboard/Drone_Workflow.html/',
        children: []
    },
    {
        id: '2',
        label: 'Image Processing',
        url: 'http://localhost:8000/'
    },
    {
        id: '3',
        label: 'DT Synchronisation',
        url: 'http://localhost:8600/',
        children: []
    },
    {
        id: '4',
        label: 'Data Streaming',
        url: 'http://localhost:8080/Dashboard/Spanwise_Dashboard.html',
        children: []
    },
    {
        id: '5',
        label: 'Structural Health Monitoring',
        url: 'http://localhost:8080/Dashboard/FEA_Home.html/',
        children: [
            { id: '5-1', label: 'FEA Visualisation', url: 'http://localhost:8080/Dashboard/FEA_Home.html/' },
            { id: '5-2', label: 'Real-time SHM', url: 'http://localhost:8080/Dashboard/SHM.html/' },
            { id: '5-3', label: 'Degradation Analysis', url: 'http://localhost:8501/' },
            { id: '5-4', label: 'Defect Localisation', url: 'http://' }
        ]
    },
    {
        id: '6',
        label: 'Knowledge-based Maintenance',
        url: 'http://localhost:8888/',
        children: [ <<
            << << < Updated upstream { id: '6-1', label: 'Standard-based Defect Assessment', url: 'http://localhost:8888/' }, ===
            === = { id: '6-1', label: 'Standard-based Defect Assessment', url: 'http://localhost:6100' }, >>>
            >>> > Stashed changes { id: '6-2', label: 'Automated Maintenance Strategy Generation', url: 'http://localhost:6100' }
        ]
    },
    { id: '7', label: 'BIMSecurity', url: 'http://localhost:7000/', children: [] }
]