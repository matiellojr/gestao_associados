var cidades = $('select[name="cidade"] option');
$('select[name="uf"]').on('change', function () {
    var uf = this.value;
    var novoSelect = cidades.filter(function () {
        return $(this).data('uf') == uf
    });
    $('select[name="cidade"]').html(novoSelect);
})