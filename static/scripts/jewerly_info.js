var inf = document.getElementById('form')
//ajax
$( document ).ready(function() {
    $("#form").click(
		function(){
            inf.innerText = '✓ В кошику';
			sendAjaxForm('result_form', 'form', '/cart/' + inf.dataset.user + '/' + inf.dataset.jw);
			return false;
		}
	);
});

function sendAjaxForm(result_form, ajax_form, url) {
    $.ajax({
        url: url, //url страницы (action_ajax_form.php)
        type: "POST", //метод отправки
        dataType: "html", //формат данных
        data: $("#"+ajax_form).serialize()  // Сеарилизуем объект
 	});
}