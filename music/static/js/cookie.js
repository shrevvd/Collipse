function getCSRFToken() {
    var cookie = document.cookie.split('; ').find(function(row) { return row.startsWith('csrftoken='); });
    return cookie ? cookie.split('=')[1] : '';
}