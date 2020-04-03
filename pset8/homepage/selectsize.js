document.querySelector('select').onchange = function(){
    document.querySelector('p').style.fontSize = this.value;
}