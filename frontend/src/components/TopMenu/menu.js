export const menus = [{
        id: '1',
        label: 'Drone and IoT',
        children: [{
            id: '1-1',
            label: 'Drone Station',
            url: 'http://localhost:8080/Dashboard/Drone_Workflow.html/'
        }]
    },
    {
        id: '2',
        label: 'Digital Twins',
        children: [{
                id: '2-1',
                label: 'Image Processing',
                url: 'http://localhost:8000/',
                children: [
                    { id: '2-1-1', label: 'Corrosion Segmentation and Quantification', url: 'http://localhost:8000/' },
                    { id: '2-1-2', label: 'Crack Segmentation and Quantification', url: 'http://localhost:7870/' }
                ]
            },
            {
                id: '2-2',
                label: 'DT Synchronisation',
                url: 'http://localhost:8600/'
            },
            {
                id: '2-3',
                label: 'Data Streaming',
                url: 'http://localhost:8080/Dashboard/Spanwise_Dashboard.html'
            }
        ]
    },
    {
        id: '3',
        label: 'Structural Health Monitoring',
        children: [
            { id: '3-1-1', label: 'FEA Visualisation', url: 'http://localhost:8080/Dashboard/FEA_Home.html/' },
            { id: '3-1-2', label: 'Real-time SHM', url: 'http://localhost:8080/Dashboard/SHM.html/' },
            { id: '3-1-3', label: 'Degradation Analysis', url: 'http://localhost:8501/' },
            { id: '3-1-4', label: 'Defect Localisation', url: 'https://book.douban.com/' }
        ]
    },
    {
        id: '4',
        label: 'Knowledge-based Maintenance',
        children: [
            { id: '4-1-1', label: 'Standard-based Defect Assessment', url: 'http://localhost:8888/' },
            { id: '4-1-2', label: 'Automated Maintenance Strategy Generation', url: 'http://localhost:8888/' }
        ]
    }
];