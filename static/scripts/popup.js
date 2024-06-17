function b() {
    const popupLinks = document.querySelectorAll(".popup-link");
    const body = document.querySelector("body");
    const lockPadding = document.querySelectorAll(".lock-padding");

    let unlock = true;

    const timeout = 600;

    if (popupLinks.length > 0) {
        for (let index = 0; index < popupLinks.length; index++) {
            const popupLink = popupLinks[index];
            popupLink.addEventListener("click", function (e) {
                const popupName = popupLink.getAttribute("href").replace("#", "");
                const curentPopup = document.getElementById(popupName);
                popupOpen(curentPopup);
                e.preventDefault();
            });
        }

        const popupCloseIcon = document.querySelectorAll(".close-popup")
        if (popupCloseIcon.length > 0) {
            for (let index = 0; index < popupCloseIcon.length; index++) {
                const el = popupCloseIcon[index];
                el.addEventListener("click", function (e) {
                    popupClose(el.closest(".popup"));
                    e.preventDefault();
                });
            }
        }
    }

    function popupOpen(curentPopup) {
        if (curentPopup && unlock) {
            const popupActive = document.querySelector(".popup.open");
            if (popupActive) {
                popupClose(popupActive, false);
            } else {
                bodyLock();
            }
            curentPopup.classList.add("open");
            curentPopup.addEventListener("mousedown", function (e) {
                if (!e.target.closest(".popup__content")) {
                    popupClose(e.target.closest(".popup"));
                }
            });
        }
    }

    function popupClose(popupActive, doUnlock = true) {
        if (unlock) {
            popupActive.classList.remove("open");
            if (doUnlock) {
                bodyUnLock()
            }
        }
    }

    function bodyLock() {
        const lockPaddingValue = window.innerWidth - document.querySelector('body').offsetWidth + 'px';

        for (let index = 0; index < lockPadding.length; index++) {
            const el = lockPadding[index];
            el.style.paddingRight = lockPaddingValue;
        }
        body.style.paddingRight = lockPaddingValue;
        body.classList.add('lock');

        unlock = false;
        setTimeout(function () {
            unlock = true;
        }, timeout);
    }

    function bodyUnLock() {
        setTimeout(function () {
            for (let index = 0; index < lockPadding.length; index++) {
                const el = lockPadding[index];
                el.style.paddingRight = '18px';
            }
            body.style.paddingRight = '0px';
            body.classList.remove('lock');
        }, timeout);

        unlock = false;
        setTimeout(function () {
            unlock = true;
        }, timeout);
    }

    document.addEventListener("keydown", function (e) {
        if (e.which === 27) {
            const popupActive = document.querySelector(".popup.open");
            popupClose(popupActive)
        }
    });
}


let a = 1;
window.onload = function (){
    b();
    formRevers();
    if(document.getElementById('message-reg')){
        formRevers();
    }
    let error = document.querySelector('.error-message');
    if(error && error.innerHTML !== ""){
        if(!document.getElementById('message-add')){
            document.getElementById('popup-a').click();
        }
        let btn = document.querySelector('.error-message');
        btn.style.opacity = 1;
        setTimeout(()=>{
            setInterval(() => {
                if(btn.style.opacity > 0.5){
                    btn.style.opacity -= 0.01;
                }
                else if(btn.style.opacity > 0){
                    btn.style.opacity -= 0.03;
                }
                else {
                    btn.style.display = 'none';
                }
            }, 20);
        }, 3000)
    }
}
function formRevers(){
    if (a === 1){
        document.querySelector('.popup__title').innerHTML = 'ВХІД';
        document.querySelector('.form_login').action = '/login';
        document.getElementById('name').style.display = 'none';
        document.getElementById('surname').style.display = 'none';
        document.getElementById('password2').style.display = 'none';

        document.getElementById('submit').value = 'УВІЙТИ';
        document.querySelector('.form__nosubmit').innerHTML = 'СТВОРИТИ АККАУНТ';
        document.getElementById('onclick_a').onclick = formRevers;
        a = 0;
    } else {
        document.querySelector('.popup__title').innerHTML = 'РЕЄСТРАЦІЯ';
        document.querySelector('.form_login').action = '/register';
        document.getElementById('name').style.display = 'block';
        document.getElementById('surname').style.display = 'block';
        document.getElementById('password2').style.display = 'block';

        document.getElementById('submit').value = 'СТВОРИТИ АККАУНТ';
        document.querySelector('.form__nosubmit').innerHTML = 'УВІЙТИ В АКАУНТ';
        document.getElementById('onclick_a').onclick = formRevers;
        a = 1;
    }
    b();
}