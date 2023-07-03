$.getJSON("https://api.leighhack.org/space.json", function (data) {
    var date = new Date(data.state.lastchange * 1000);
    
    if (data.state.open) {
        $('span#hackspace_status').html('<b>Open</b>');
        $('span#hackspace_lastchange').html(date);
    } else {
        $('span#hackspace_status').html('<b>Closed</b>');
        $('span#hackspace_lastchange').html(date);
    }
});