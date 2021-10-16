from django.shortcuts import render

from datetime import datetime
from django.db.models import Sum

from contas.models import Conta
from movimentacoes.models import Tipo, Movimentacao


def inicio(request):
    movimentacoes = Movimentacao.objects.order_by("-data")

    mes_atual = datetime.now().month

    total_receitas = (
        movimentacoes.filter(
            tipo=Tipo.RECEITA,
            data__month=mes_atual,
        ).aggregate(total=Sum('valor'))['total']
    )

    total_despesas = (
        movimentacoes.filter(
            tipo=Tipo.DESPESA,
            data__month=mes_atual,
        ).aggregate(total=Sum('valor'))['total']
    )

    ultimas_movimentacoes = movimentacoes[:4]

    conta = Conta.objects.first()
    saldo_em_conta = conta.saldo

    contexto = {
        "ultimas_movimentacoes": ultimas_movimentacoes,
        "saldo_em_conta": saldo_em_conta,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
    }

    return render(request, "index.html", contexto)
