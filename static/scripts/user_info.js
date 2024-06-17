radio = document.querySelectorAll('.user_info_nav input');
for(let i = 0; i < radio.length; i++){
    radio[i].addEventListener('click', function (){
        rad = document.querySelectorAll('.user_info_nav input');
        for(let i = 0; i < radio.length; i++){
            labelradio = document.querySelector('label[for=' + radio[i].id + ']');
            content = document.querySelectorAll('.user_info_content div.user_info_content_block');
            if (rad[i].checked === true){
                content[i].style.display = 'flex';
                labelradio.style.backgroundColor = '#464646';
                labelradio.style.color = '#f4f4f4';
                sessionStorage['user_info'] = i;
            }
            else {
                content[i].style.display = 'none';
                labelradio.style.backgroundColor = 'white';
                labelradio.style.color = 'black';
            }
        }
        console.log();
    })
}
if(sessionStorage['user_info'])
    radio[sessionStorage['user_info']].click();
else
    radio[0].click();
