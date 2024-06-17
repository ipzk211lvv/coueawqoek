var loadFile = function(event) {
    let output = document.querySelector(".addimage");
    let img = URL.createObjectURL(event.target.files[0]);
    output.style.backgroundImage = "url(" + img + ")";
    output.value = '';
    output.style.border = "1px solid black";
};
checkBoxs = document.querySelectorAll(".add__checkbox_block input");
for (let i = 0; i < checkBoxs.length; i++) {
    checkBoxs[i].addEventListener("click", function () {
        checkBox = document.querySelectorAll(".add__checkbox_block input");
        document.getElementById("stone").value = "";
        for(let j = 0; j < checkBox.length; j++){
            if(checkBox[j].checked){
                document.getElementById("stone").value += checkBox[j].value+";";
            }
        }
        document.getElementById("stone").value = document.getElementById("stone").value.slice(0, -1);
    });
}
update2 = document.querySelectorAll("#metal");
proba2 = document.querySelector("#proba");
for(let i = 0; i < update2.length; i++){
    update2[i].addEventListener('click', function(){
        update2[i].valueOf().value === "Золото" ? proba2.valueOf().value= "585" : proba2.valueOf().value = "925";
    })
}