const botones = document.getElementsByClassName("boton-eliminar");

function confirmation(event) {
	var answer = confirm("Confirma para borrar la publicación")
	if (answer){
		alert("Publicación eliminada con éxito")
		window.location = boton.href
	}
	else{
        event.preventDefault()
	}
}

for (var boton of botones) {
    boton.addEventListener("click", confirmation)
}
