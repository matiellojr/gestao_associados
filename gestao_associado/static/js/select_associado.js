var associado = $('select[name="id_nome_associado"] option');
$('select[name="id_nome_associado"]').on('change', function () {
    var id_associado = this.value;
    
    var component_add_todos = document.getElementById("add_todos");
    var component_add_um = document.getElementById("add_um");

    if(id_associado != 0){
        component_add_todos.classList.add("disabled");
        component_add_um.classList.remove("disabled");
    }else{
        component_add_todos.classList.remove("disabled");
        component_add_um.classList.add("disabled");
    }
})