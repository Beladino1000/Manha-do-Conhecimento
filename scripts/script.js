function add1() {
    var value = parseInt(document.getElementById('valor').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('number').value = value;
}