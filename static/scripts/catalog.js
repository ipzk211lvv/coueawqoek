document.getElementById('btn_filter').addEventListener('click', function (){
    let a = document.getElementById('btn_filter2');
    if (a.classList[0] === 'act'){
        a.classList.remove('act');
        a.classList.add('pas');
    } else {
        a.classList.add('act');
        a.classList.remove('pas');
    }
});

let nav = document.querySelectorAll('  .btn_filter_nav');
for(let i = 0; i < nav.length; i++) {
    nav[i].addEventListener('click', function (){
        let a = document.querySelectorAll('.btn_filter_nav2')[i];
        if (a.classList[2] === 'active'){
            nav[i].querySelector('p:last-child').innerText = '↓';
            a.classList.remove('active');
            a.classList.add('pas');
        } else {
            nav[i].querySelector('p:last-child').innerText = '↑';
            a.classList.add('active');
            a.classList.remove('pas');
        }
    });
}

let hr = document.querySelectorAll('input[type=checkbox], #btn_filter');
for(let i = 0; i < hr.length; i++){
    hr[i].addEventListener('click', go);
}

function go(){
    let href_type = '';
    let type_ = document.querySelectorAll('.type_input label');
    for (let i = 0; i < type_.length; i++){
        if (type_[i].childNodes[0].checked){
            href_type += type_[i].innerText + '+';
        } else {
            href_type = href_type.replace(type_[i].innerText, '')
        }
    }
    href_type = href_type.slice(0, -1);
    href_type+='&';


    let href_metal = '';
    let metal_ = document.querySelectorAll('.metal_input label');
    for (let i = 0; i < metal_.length; i++){
        if (metal_[i].childNodes[0].checked){
            href_metal += metal_[i].innerText + '+';
        } else {
            href_metal = href_metal.replace(metal_[i].innerText, '')
        }
    }
    href_metal = href_metal.slice(0, -1);
    href_metal+='&';


    let href_color = '';
    let color_ = document.querySelectorAll('.color_input label');
    for (let i = 0; i < color_.length; i++){
        if (color_[i].childNodes[0].checked){
            href_color += color_[i].innerText + '+';
        } else {
            href_color = href_color.replace(color_[i].innerText, '')
        }
    }
    href_color = href_color.slice(0, -1);
    href_color+='&';


    let href_gender = '';
    let gender_ = document.querySelectorAll('.gender_input label');
    for (let i = 0; i < color_.length; i++){
        if (gender_[i].childNodes[0].checked){
            href_gender += gender_[i].innerText + '+';
        } else {
            href_gender = href_gender.replace(gender_[i].innerText, '')
        }
    }
    href_gender = href_gender.slice(0, -1);
    href_gender+='&';


    let href_stone = '';
    let stone_ = document.querySelectorAll('.stone_input label');
    for (let i = 0; i < stone_.length; i++){
        if (stone_[i].childNodes[0].checked){
            href_stone += stone_[i].innerText + '+';
        } else {
            href_stone = href_stone.replace(stone_[i].innerText, '')
        }
    }
    href_stone = href_stone.slice(0, -1);
    href_stone+='&';

    let href_price = document.querySelectorAll('.pric input');
    if (href_price[0].value === '')
        href_price[0].value = 0
    if (href_price[1].value === '')
        href_price[1].value = 99999
    href_price = href_price[0].value + '+' + href_price[1].value + '&';

    if(href_type === '&')
        href_type = 'Сережки+Каблучка+Кольє+Браслети+Підвіски&';
    if(href_metal === '&')
        href_metal = 'Золото+Срібло&';
    if(href_color === '&')
        href_color = 'Білий+Жовтий+Червоний&';
    if (href_gender === '&')
        href_gender = 'Жіночі+Чоловічі+Дитячі&';
    if (href_price === '&')
        href_price = '0+99999&'

    let href_ = href_type + href_metal + href_color + href_gender + href_price + href_stone;
    document.getElementById('filter').setAttribute('href','/catalog/'+href_.slice(0, -1));
}










//--------PAGINAT
var count = document.querySelectorAll('.catalog_item').length; //всего записей
var cnt = 16;
let all = document.querySelector('.all_tovar_block');

const screenWidth = window.screen.width
if(screenWidth <= 1000 && screenWidth > 700){
   cnt = 15;
} else if (screenWidth <= 700){
    cnt = 12;
}

var cnt_page = Math.ceil(count / cnt);


var paginator = document.querySelector(".paginator");
var page = "";
for (var i = 0; i < cnt_page; i++) {
  page += "<span class='paginator_pas' data-page=" + i * cnt + "  id=\"page" + (i + 1) + "\">" + (i + 1) + "</span>";
}
paginator.innerHTML = page;

//выводим первые записи {cnt}
var div_num = document.querySelectorAll(".catalog_item");
for (var i = 0; i < div_num.length; i++) {
  if (i < cnt) {
    div_num[i].style.display = "block";
  }
}

var main_page = document.getElementById("page1");
main_page.classList.add("paginator_active");
main_page.classList.remove("paginator_pas");

function pagination(event) {
    var e = event || window.event;
    var target = e.target;
    var id = target.id;

    if (target.tagName.toLowerCase() !== "span") return;

    var num_ = id.substr(4);
    var data_page = +target.dataset.page;
    main_page.classList.remove("paginator_active");
    main_page.classList.add("paginator_pas");
    main_page = document.getElementById(id);
    main_page.classList.add("paginator_active");
    main_page.classList.remove("paginator_pas");

    var j = 0;
    for (var i = 0; i < div_num.length; i++) {
        var data_num = div_num[i].dataset.num;
        if (data_num <= data_page || data_num >= data_page)
        div_num[i].style.display = "none";

    }
    for (var i = data_page; i < div_num.length; i++) {
        if (j >= cnt) break;
        div_num[i].style.display = "block";
        j++;
    }

    var interval;
    interval = setInterval(()=>{
        if (window.innerWidth > 700){
            if(window.pageYOffset >= 400){
            window.scrollTo(0, window.pageYOffset - 25);
            } else {
                clearInterval(interval);
            }
        } else {
            if(window.pageYOffset >= 250){
            window.scrollTo(0, window.pageYOffset - 30);
            } else {
                clearInterval(interval);
            }
        }
    }, 1)
}