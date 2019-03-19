/**
 * Created by wupeiqi on 17/2/24.
 * 用于基本图表的展示
 */

Highcharts.setOptions({
    global: {
        useUTC: false
    },
    credits: {
        text: 'www.bokeyuan.com',
        href: 'http://www.bokeyuan.com'
    }
});
function initChart(){
    var config = {
        chart: {
            type: 'spline'
        },
        title: {
            text: '报障处理不同员工每月数量图'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: '处理单数'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: true
        },
        exporting: {
            enabled: false
        },
        series: [
            {
                name: 'A',
                data: [
                    [1491535949788.035, 7.0],
                    [1491535949888.035, 6.0],
                    [1491535949988.035, 10.0],
                    [1491535950088.035, 1.0],
                ]
            },
            {
                name: 'B',
                data: [
                    [1491535949788.035, 8.0],
                    [1491535949888.035, 2.0],
                    [1491535949988.035, 40.0],
                    [1491535950088.035, 1.0],
                ]
            }
            ,
            {
                name: 'C',
                data: [
                    [1491535949788.035, 10.0],
                    [1491535949888.035, 2.0],
                    [1491535949988.035, 10.0],
                    [1491535950088.035, 8.0],
                ]
            }
        ]
    };

    $.ajax({
        url: '/backend/trouble-json-report.html',
        dataType: 'json',
        success:function(arg){
            config['series'] = arg;
            $('#container').highcharts(config);
        }
    })
}

function initCategory() {
var options = {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Browser market shares January, 2015 to May, 2015'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: false
            },
            showInLegend: true
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'IE',
            y: 56.33
        }, {
            name: 'Chrome',
            y: 24.03,
            sliced: true,
            selected: true
        }, {
            name: 'Firefox',
            y: 10.38
        }, {
            name: 'Safari',
            y: 4.77
        }, {
            name: 'Opera',
            y: 0.91
        }, {
            name: 'Propri',
            y: 0.2
        }]
    }]
};
$('#container_category').highcharts(options);
}

function initGroup() {
var options = {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Historic World Population by Region'
    },
    subtitle: {
        text: 'Source: <a href="https://en.wikipedia.org/wiki/World_population">Wikipedia.org</a>'
    },
    xAxis: {
        categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
        title: {
            text: null
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Population (millions)',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    tooltip: {
        valueSuffix: ' millions'
    },
    plotOptions: {
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 80,
        floating: true,
        borderWidth: 1,
        backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        shadow: true
    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'Year 1800',
        data: [107, 31, 635, 203, 2]
    }, {
        name: 'Year 1900',
        data: [133, 156, 947, 408, 6]
    }, {
        name: 'Year 2012',
        data: [1052, 954, 4250, 740, 38]
    }]
};
$('#container_group').highcharts(options);
}