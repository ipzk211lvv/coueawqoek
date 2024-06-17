cart();
function update(event, jewelry_id, price){
    let count = parseInt(document.getElementById('count-'+jewelry_id).innerText);
    if(event === '+'){
        document.getElementById('count-'+jewelry_id).innerText = ++count;
    }else{
        if (count - 1 > 0){
            document.getElementById('count-'+jewelry_id).innerText = --count;
        }
    }
    getPrice(jewelry_id, count, price);
    submit_form(jewelry_id);
    go();
}
function getPrice(jewelry_id, count, price){
    document.getElementById('price-'+jewelry_id).innerText = 'Ціна: ' + price*count +'грн';
    document.getElementById('buy-'+jewelry_id).setAttribute('href', '/buy/' + jewelry_id + '+' + count)
}


function cart(){
    if (document.querySelectorAll('.cart_one_block').length === 0){
        document.querySelector('.cart_buy_all').style.display = 'none';
        document.getElementById('not_cart').style.display = 'block';
    }
}

function cart_del(jewelry_id){
    document.getElementById('block-'+jewelry_id).remove();
    submit_form();
    cart();
    go();
}



function submit_form(){
    let blocks = document.querySelectorAll('.cart_one_block');
    let array_cart = '{';
    for (let i = 0; i < blocks.length; i++) {
        let block = blocks[i];
        if(i === blocks.length - 1){
            array_cart += block.id.replace('block-', '') + ': ' + block.querySelector('.count').innerText;
        } else {
            array_cart += block.id.replace('block-', '') + ': ' + block.querySelector('.count').innerText + ', ';
        }
    }
    array_cart += '}';
    document.getElementById('array_cart').value = array_cart;
    document.getElementById('btn').click()
}


//ajax
$( document ).ready(function() {
    $("#btn").click(
		function(){
			sendAjaxForm('result_form', 'cart_form', '/cart');
			return false;
		}
	);
});

function sendAjaxForm(result_form, ajax_form, url) {
    $.ajax({
        url: url,
        type: "POST", //метод отправки
        dataType: "html", //формат данных
        data: $("#"+ajax_form).serialize()

 	});
}

let err = document.getElementById('message-cart');
if (err){
    err.style.opacity = 1;
    let wid = err.style.width;
    setTimeout(()=>{
        setInterval(() => {
            if(err.style.opacity > 0.6) {
                err.style.opacity -= 0.01;
            }
            else if(err.style.opacity > 0) {
                err.style.opacity -= 0.04;
            }
            else {
                err.style.display = 'none';
            }
        }, 20);
    }, 8000)
}


let hr = document.querySelectorAll('input[type=checkbox]');
for(let i = 0; i < hr.length; i++){
    hr[i].addEventListener('click', go);
}
go();
function go() {
    let check = document.querySelectorAll('input[type=checkbox]');
    let jewelry = '';
    let price = 0;
    for (let i = 0; i < check.length; i++) {
        if (check[i].checked) {
            let el = document.querySelector('#block-' + check[i].dataset.id)
            jewelry += check[i].dataset.id + '+' + el.querySelector('#count-' + check[i].dataset.id).innerHTML + '&';
            price += parseInt(el.querySelector('#price-' + check[i].dataset.id).innerHTML.match(/\d+/));
        }
    }
    document.getElementById('cart_buy_all').innerText = 'Придбати все(' + price + 'грн)';
    document.getElementById('cart_buy_all').setAttribute('href', '/buy/'+jewelry.slice(0,-1))
}