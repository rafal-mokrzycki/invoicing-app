// edit_invoice.html
function sumNetFunction() {
    // Capture item number

    // Capture the entered values of two input boxes
    var amount = document.getElementById('amount').value;
    var price_net = document.getElementById('price_net').value;
    // Multiply them and display
    var multiplication = amount * price_net;
    document.getElementById('sum_net').value = multiplication;
}
function sumGrossFunction() {
    // Capture the entered values of two input boxes
    var amount = document.getElementById('amount').value;
    var price_net = document.getElementById('price_net').value;
    var tax_rate = document.getElementById('tax_rate').value;
    // Multiply them and display
    var multiplication = amount * price_net + (amount * price_net * tax_rate);
    document.getElementById('sum_gross').value = multiplication;
}
function addNextFn() {
    var parent_element = document.getElementById("invoice-items-values");
    var example_item = document.getElementById("invoice-item-0");
    var new_item = example_item.cloneNode(true);
    new_item.id = "invoice-item-2";
    parent_element.appendChild(new_item);
}
function deletePosition() {
}
