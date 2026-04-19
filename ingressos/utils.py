def criar_mensagem_whatsapp(
    id_venda: int,
    evento: str,
    data_evento: str,
    quantidade: int,
    valor_total: float,
    comprador: str,
):
    mensagem = f""" *Notificação de Sistema*
A venda {id_venda} teve seu pagamento confirmado.
Seguem os detalhes da venda:
Evento: {evento}
Data do evento: {data_evento}
Quantidade: {quantidade}
Valor Total (R$): {valor_total}
Comprador: {comprador}
"""
    return mensagem
