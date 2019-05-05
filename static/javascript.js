var daterange = new Kalendae.Input("dateselect", {
            months:3,
            direction:'today-past',
            mode:'range'
        });

document.getElementById('daterangequery').onclick = function() {
    var dr = daterange.getSelectedAsText();
    if (dr.length===1) {
        var start = Kalendae.moment(dr[0], Kalendae.moment.isoFormat);
        var end = Kalendae.moment(dr[0], Kalendae.moment.isoFormat).add(1, 'days');
        var url =  window.location.protocol+ '//'+window.location.host +window.location.pathname +"?start="+start.local().toISOString()+"&end="+end.local().toISOString();
        window.location.href = url;
    }
    else if(dr[0] === dr[1]){
        var start = Kalendae.moment(dr[0], Kalendae.moment.isoFormat);
        var end = Kalendae.moment(dr[0], Kalendae.moment.isoFormat).add(1, 'days');
        var url =  window.location.protocol+ '//'+window.location.host +window.location.pathname +"?start="+start.local().toISOString()+"&end="+end.local().toISOString();
        window.location.href = url;
    } 
    else
    {
        var start = Kalendae.moment(dr[0], Kalendae.moment.isoFormat);
        var end = Kalendae.moment(dr[1], Kalendae.moment.isoFormat);
        var url =  window.location.protocol+ '//'+window.location.host +window.location.pathname  +"?start="+start.local().toISOString()+"&end="+end.local().toISOString();
        window.location.href = url;
    }
}



var makeData = function(name, color, m2x_data){
    var final_data = {label: name,
                      strokeColor: color,
                      data: []
                  };

    for(var i = 0; i < m2x_data['values'].length; i++) {
        final_data.data.push({x: new Date(m2x_data['values'][i]['timestamp']), y: m2x_data['values'][i]['value']});
    };
    return final_data;
};

var data = [makeData('Shey', '#A600FF', temp1), 
             makeData('Mary', '#00EAC5', temp2),
             ];


var ctx = document.getElementById("myChart").getContext("2d");

new Chart(ctx).Scatter(data, {
    responsive: true,
    scaleType: "date",
    useUtc: false,
    bezierCurve: false,
    pointDot: false,
    scaleShowLabels: true,
    maintainAspectRatio: false,
    hover: [{
            mode: "label"
        }],
    scaleFontFamily: "'Times New Roman', 'Times', serif"
});





