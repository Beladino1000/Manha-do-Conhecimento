function add1() {
    var value = parseInt(document.getElementById('valor').innerHTML, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('number').innerHTML = value;
}