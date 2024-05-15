function asignaUsuario(idUsuario, grupos){
    document.getElementById('idUsuario').value = idUsuario;
    grps = grupos.split('-');
    grps.length = grps.length - 1;

    $('#formGrupos input[type=checkbox]').each(function(){
        $(this).prop("checked", false);
        if (grps.includes($(this).prop('name'))){
            $(this).prop("checked", true);
        }
    });
}
