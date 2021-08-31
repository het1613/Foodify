var modal = document.getElementById("modal1");
var btn = document.getElementById("goalbtn");
var closebtn = document.getElementsByClassName("close-modal")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

closebtn.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}