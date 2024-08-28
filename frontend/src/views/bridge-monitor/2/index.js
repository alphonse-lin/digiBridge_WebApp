const dataBJ = [
    [1, 55, 9, 56, 0.46, 18, 6, 'Good'],
    [2, 25, 11, 21, 0.65, 34, 9, 'Excellent'],
    [3, 56, 7, 63, 0.3, 14, 5, 'Good'],
    [4, 33, 7, 29, 0.33, 16, 6, 'Excellent'],
    [5, 42, 24, 44, 0.76, 40, 16, 'Excellent'],
    [6, 82, 58, 90, 1.77, 68, 33, 'Good'],
    [7, 74, 49, 77, 1.46, 48, 27, 'Good'],
    [8, 78, 55, 80, 1.29, 59, 29, 'Good'],
    [9, 267, 216, 280, 4.8, 108, 64, 'Severe Pollution'],
    [10, 185, 127, 216, 2.52, 61, 27, 'Moderate Pollution'],
    [11, 39, 19, 38, 0.57, 31, 15, 'Excellent'],
    [12, 41, 11, 40, 0.43, 21, 7, 'Excellent'],
    [13, 64, 38, 74, 1.04, 46, 22, 'Good'],
    [14, 108, 79, 120, 1.7, 75, 41, 'Light Pollution'],
    [15, 108, 63, 116, 1.48, 44, 26, 'Light Pollution'],
    [16, 33, 6, 29, 0.34, 13, 5, 'Excellent'],
    [17, 94, 66, 110, 1.54, 62, 31, 'Good'],
    [18, 186, 142, 192, 3.88, 93, 79, 'Moderate Pollution'],
    [19, 57, 31, 54, 0.96, 32, 14, 'Good'],
    [20, 22, 8, 17, 0.48, 23, 10, 'Excellent'],
    [21, 39, 15, 36, 0.61, 29, 13, 'Excellent'],
    [22, 94, 69, 114, 2.08, 73, 39, 'Good'],
    [23, 99, 73, 110, 2.43, 76, 48, 'Good'],
    [24, 31, 12, 30, 0.5, 32, 16, 'Excellent'],
    [25, 42, 27, 43, 1, 53, 22, 'Excellent'],
    [26, 154, 117, 157, 3.05, 92, 58, 'Moderate Pollution'],
    [27, 234, 185, 230, 4.09, 123, 69, 'Severe Pollution'],
    [28, 160, 120, 186, 2.77, 91, 50, 'Moderate Pollution'],
    [29, 134, 96, 165, 2.76, 83, 41, 'Light Pollution'],
    [30, 52, 24, 60, 1.03, 50, 21, 'Good'],
    [31, 46, 5, 49, 0.28, 10, 6, 'Excellent']
]
const dataGZ = [
    [1, 26, 37, 27, 1.163, 27, 13, 'Excellent'],
    [2, 85, 62, 71, 1.195, 60, 8, 'Good'],
    [3, 78, 38, 74, 1.363, 37, 7, 'Good'],
    [4, 21, 21, 36, 0.634, 40, 9, 'Excellent'],
    [5, 41, 42, 46, 0.915, 81, 13, 'Excellent'],
    [6, 56, 52, 69, 1.067, 92, 16, 'Good'],
    [7, 64, 30, 28, 0.924, 51, 2, 'Good'],
    [8, 55, 48, 74, 1.236, 75, 26, 'Good'],
    [9, 76, 85, 113, 1.237, 114, 27, 'Good'],
    [10, 91, 81, 104, 1.041, 56, 40, 'Good'],
    [11, 84, 39, 60, 0.964, 25, 11, 'Good'],
    [12, 64, 51, 101, 0.862, 58, 23, 'Good'],
    [13, 70, 69, 120, 1.198, 65, 36, 'Good'],
    [14, 77, 105, 178, 2.549, 64, 16, 'Good'],
    [15, 109, 68, 87, 0.996, 74, 29, 'Light Pollution'],
    [16, 73, 68, 97, 0.905, 51, 34, 'Good'],
    [17, 54, 27, 47, 0.592, 53, 12, 'Good'],
    [18, 51, 61, 97, 0.811, 65, 19, 'Good'],
    [19, 91, 71, 121, 1.374, 43, 18, 'Good'],
    [20, 73, 102, 182, 2.787, 44, 19, 'Good'],
    [21, 73, 50, 76, 0.717, 31, 20, 'Good'],
    [22, 84, 94, 140, 2.238, 68, 18, 'Good'],
    [23, 93, 77, 104, 1.165, 53, 7, 'Good'],
    [24, 99, 130, 227, 3.97, 55, 15, 'Good'],
    [25, 146, 84, 139, 1.094, 40, 17, 'Light Pollution'],
    [26, 113, 108, 137, 1.481, 48, 15, 'Light Pollution'],
    [27, 81, 48, 62, 1.619, 26, 3, 'Good'],
    [28, 56, 48, 68, 1.336, 37, 9, 'Good'],
    [29, 82, 92, 174, 3.29, 0, 13, 'Good'],
    [30, 106, 116, 188, 3.628, 101, 16, 'Light Pollution'],
    [31, 118, 50, 0, 1.383, 76, 11, 'Light Pollution']
]
const dataSH = [
    [1, 91, 45, 125, 0.82, 34, 23, 'Good'],
    [2, 65, 27, 78, 0.86, 45, 29, 'Good'],
    [3, 83, 60, 84, 1.09, 73, 27, 'Good'],
    [4, 109, 81, 121, 1.28, 68, 51, 'Light Pollution'],
    [5, 106, 77, 114, 1.07, 55, 51, 'Light Pollution'],
    [6, 109, 81, 121, 1.28, 68, 51, 'Light Pollution'],
    [7, 106, 77, 114, 1.07, 55, 51, 'Light Pollution'],
    [8, 89, 65, 78, 0.86, 51, 26, 'Good'],
    [9, 53, 33, 47, 0.64, 50, 17, 'Good'],
    [10, 80, 55, 80, 1.01, 75, 24, 'Good'],
    [11, 117, 81, 124, 1.03, 45, 24, 'Light Pollution'],
    [12, 99, 71, 142, 1.1, 62, 42, 'Good'],
    [13, 95, 69, 130, 1.28, 74, 50, 'Good'],
    [14, 116, 87, 131, 1.47, 84, 40, 'Light Pollution'],
    [15, 108, 80, 121, 1.3, 85, 37, 'Light Pollution'],
    [16, 134, 83, 167, 1.16, 57, 43, 'Light Pollution'],
    [17, 79, 43, 107, 1.05, 59, 37, 'Good'],
    [18, 71, 46, 89, 0.86, 64, 25, 'Good'],
    [19, 97, 71, 113, 1.17, 88, 31, 'Good'],
    [20, 84, 57, 91, 0.85, 55, 31, 'Good'],
    [21, 87, 63, 101, 0.9, 56, 41, 'Good'],
    [22, 104, 77, 119, 1.09, 73, 48, 'Light Pollution'],
    [23, 87, 62, 100, 1, 72, 28, 'Good'],
    [24, 168, 128, 172, 1.49, 97, 56, 'Moderate Pollution'],
    [25, 65, 45, 51, 0.74, 39, 17, 'Good'],
    [26, 39, 24, 38, 0.61, 47, 17, 'Excellent'],
    [27, 39, 24, 39, 0.59, 50, 19, 'Excellent'],
    [28, 93, 68, 96, 1.05, 79, 29, 'Good'],
    [29, 188, 143, 197, 1.66, 99, 51, 'Moderate Pollution'],
    [30, 174, 131, 174, 1.55, 108, 50, 'Moderate Pollution'],
    [31, 187, 143, 201, 1.39, 89, 53, 'Moderate Pollution']
]
const schema = [
    { name: 'date', index: 0, text: 'Day' },
    { name: 'AQIndicator', index: 1, text: 'AQI indicator' },
    { name: 'PM25', index: 2, text: 'PM2.5' },
    { name: 'PM10', index: 3, text: 'PM10' },
    { name: 'CO', index: 4, text: 'CO' },
    { name: 'NO2', index: 5, text: 'NO2' },
    { name: 'SO2', index: 6, text: 'SO2' }
]
const itemStyle = {
    opacity: 0.8,
    shadowBlur: 10,
    shadowOffsetX: 0,
    shadowOffsetY: 0,
    shadowColor: 'rgba(0,0,0,0.3)'
}
export const popChartOption = {
    color: ['#dd4444', '#fec42c', '#80F1BE'],
    grid: {
        left: '12%',
        right: '5%',
        top: '5%',
        bottom: '12%'
    },
    tooltip: {
        backgroundColor: 'rgba(255,255,255,0.7)',
        formatter: function(param) {
            const value = param.value
                // prettier-ignore
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' +
                param.seriesName + ' ' + value[0] + 'Day：' +
                value[7] +
                '</div>' +
                schema[1].text + '：' + value[1] + '<br>' +
                schema[2].text + '：' + value[2] + '<br>' +
                schema[3].text + '：' + value[3] + '<br>' +
                schema[4].text + '：' + value[4] + '<br>' +
                schema[5].text + '：' + value[5] + '<br>' +
                schema[6].text + '：' + value[6] + '<br>'
        }
    },
    xAxis: {
        type: 'value',
        name: 'Date',
        nameGap: 16,
        nameTextStyle: {
            fontSize: 16
        },
        max: 31,
        splitLine: {
            show: false
        }
    },
    yAxis: {
        type: 'value',
        name: 'AQI',
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
            fontSize: 16
        },
        splitLine: {
            show: false
        }
    },
    series: [{
            name: 'Location 1',
            type: 'scatter',
            itemStyle,
            data: dataBJ
        },
        {
            name: 'Location 2',
            type: 'scatter',
            itemStyle,
            data: dataSH
        },
        {
            name: 'Location 3',
            type: 'scatter',
            itemStyle,
            data: dataGZ
        }
    ]
}

// prettier-ignore
const hours = [
        '12a', '1a', '2a', '3a', '4a', '5a', '6a',
        '7a', '8a', '9a', '10a', '11a',
        '12p', '1p', '2p', '3p', '4p', '5p',
        '6p', '7p', '8p', '9p', '10p', '11p'
    ]
    // prettier-ignore
const days = [
        'Saturday', 'Friday', 'Thursday',
        'Wednesday', 'Tuesday', 'Monday', 'Sunday'
    ]
    // prettier-ignore
const data = [
    [0, 0, 5],
    [0, 1, 1],
    [0, 2, 0],
    [0, 3, 0],
    [0, 4, 0],
    [0, 5, 0],
    [0, 6, 0],
    [0, 7, 0],
    [0, 8, 0],
    [0, 9, 0],
    [0, 10, 0],
    [0, 11, 2],
    [0, 12, 4],
    [0, 13, 1],
    [0, 14, 1],
    [0, 15, 3],
    [0, 16, 4],
    [0, 17, 6],
    [0, 18, 4],
    [0, 19, 4],
    [0, 20, 3],
    [0, 21, 3],
    [0, 22, 2],
    [0, 23, 5],
    [1, 0, 7],
    [1, 1, 0],
    [1, 2, 0],
    [1, 3, 0],
    [1, 4, 0],
    [1, 5, 0],
    [1, 6, 0],
    [1, 7, 0],
    [1, 8, 0],
    [1, 9, 0],
    [1, 10, 5],
    [1, 11, 2],
    [1, 12, 2],
    [1, 13, 6],
    [1, 14, 9],
    [1, 15, 11],
    [1, 16, 6],
    [1, 17, 7],
    [1, 18, 8],
    [1, 19, 12],
    [1, 20, 5],
    [1, 21, 5],
    [1, 22, 7],
    [1, 23, 2],
    [2, 0, 1],
    [2, 1, 1],
    [2, 2, 0],
    [2, 3, 0],
    [2, 4, 0],
    [2, 5, 0],
    [2, 6, 0],
    [2, 7, 0],
    [2, 8, 0],
    [2, 9, 0],
    [2, 10, 3],
    [2, 11, 2],
    [2, 12, 1],
    [2, 13, 9],
    [2, 14, 8],
    [2, 15, 10],
    [2, 16, 6],
    [2, 17, 5],
    [2, 18, 5],
    [2, 19, 5],
    [2, 20, 7],
    [2, 21, 4],
    [2, 22, 2],
    [2, 23, 4],
    [3, 0, 7],
    [3, 1, 3],
    [3, 2, 0],
    [3, 3, 0],
    [3, 4, 0],
    [3, 5, 0],
    [3, 6, 0],
    [3, 7, 0],
    [3, 8, 1],
    [3, 9, 0],
    [3, 10, 5],
    [3, 11, 4],
    [3, 12, 7],
    [3, 13, 14],
    [3, 14, 13],
    [3, 15, 12],
    [3, 16, 9],
    [3, 17, 5],
    [3, 18, 5],
    [3, 19, 10],
    [3, 20, 6],
    [3, 21, 4],
    [3, 22, 4],
    [3, 23, 1],
    [4, 0, 1],
    [4, 1, 3],
    [4, 2, 0],
    [4, 3, 0],
    [4, 4, 0],
    [4, 5, 1],
    [4, 6, 0],
    [4, 7, 0],
    [4, 8, 0],
    [4, 9, 2],
    [4, 10, 4],
    [4, 11, 4],
    [4, 12, 2],
    [4, 13, 4],
    [4, 14, 4],
    [4, 15, 14],
    [4, 16, 12],
    [4, 17, 1],
    [4, 18, 8],
    [4, 19, 5],
    [4, 20, 3],
    [4, 21, 7],
    [4, 22, 3],
    [4, 23, 0],
    [5, 0, 2],
    [5, 1, 1],
    [5, 2, 0],
    [5, 3, 3],
    [5, 4, 0],
    [5, 5, 0],
    [5, 6, 0],
    [5, 7, 0],
    [5, 8, 2],
    [5, 9, 0],
    [5, 10, 4],
    [5, 11, 1],
    [5, 12, 5],
    [5, 13, 10],
    [5, 14, 5],
    [5, 15, 7],
    [5, 16, 11],
    [5, 17, 6],
    [5, 18, 0],
    [5, 19, 5],
    [5, 20, 3],
    [5, 21, 4],
    [5, 22, 2],
    [5, 23, 0],
    [6, 0, 1],
    [6, 1, 0],
    [6, 2, 0],
    [6, 3, 0],
    [6, 4, 0],
    [6, 5, 0],
    [6, 6, 0],
    [6, 7, 0],
    [6, 8, 0],
    [6, 9, 0],
    [6, 10, 1],
    [6, 11, 0],
    [6, 12, 2],
    [6, 13, 1],
    [6, 14, 3],
    [6, 15, 4],
    [6, 16, 0],
    [6, 17, 0],
    [6, 18, 0],
    [6, 19, 0],
    [6, 20, 1],
    [6, 21, 2],
    [6, 22, 2],
    [6, 23, 6]
]
const singleAxis = []
const series = []
days.forEach(function(day, idx) {
    singleAxis.push({
        left: '5%',
        type: 'category',
        boundaryGap: false,
        data: hours,
        top: (idx * 100) / 7 + 5 + '%',
        height: 100 / 7 - 10 + '%',
        axisLabel: {
            interval: 2
        }
    })
    series.push({
        singleAxisIndex: idx,
        coordinateSystem: 'singleAxis',
        type: 'scatter',
        data: [],
        symbolSize: function(dataItem) {
            return dataItem[1] * 2
        }
    })
})
data.forEach(function(dataItem) {
    series[dataItem[0]].data.push([dataItem[1], dataItem[2]])
})
export const singleChartOption = {
    tooltip: {
        position: 'top'
    },
    singleAxis,
    series
}

export const sensorChartOption = (xData, yData) => {
    return {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        grid: {
            top: '5%',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: xData
        }],
        yAxis: [{
            type: 'value'
        }],
        series: [{
            name: 'acceleration',
            type: 'line',
            stack: 'Total',
            smooth: true,
            areaStyle: {},
            emphasis: {
                focus: 'series'
            },
            data: yData
        }]
    }
}