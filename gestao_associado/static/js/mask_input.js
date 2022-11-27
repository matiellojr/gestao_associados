// DataComMascara = Date.toString("dd/MM/yyyy")

$(document).ready(function () {
    $("#cpf").mask('000.000.000-00');
    $("#data").mask('00/00/0000');
    $("#telefone").mask('(00) 0 0000-0000');
    $("#money").mask('000');
    $("#money_update").mask('000');
    $("#data_mensalidade").mask("00/00/0000"), {placeholder:"dd/MM/yyyy"} ;
});