from django.db import models, transaction


class Tipo(models.IntegerChoices):
    RECEITA = 1, "Receita"
    DESPESA = 2, "Despesa"


class Categoria(models.Model):
    tipo = models.IntegerField(
        choices=Tipo.choices,
        default=Tipo.DESPESA,
    )

    nome = models.CharField(
        verbose_name="Nome da categoria",
        max_length=80,
    )

    class Meta:
        db_table = "categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
    tipo = models.IntegerField(
        choices=Tipo.choices,
        default=Tipo.DESPESA,
    )

    conta = models.ForeignKey(
        "contas.Conta",
        verbose_name="Conta em que a movimentação ocorreu",
        on_delete=models.PROTECT,
    )

    categoria = models.ForeignKey(
        Categoria,
        verbose_name="Categoria da movimentação",
        on_delete=models.PROTECT,
    )

    liquidada = models.BooleanField(
        verbose_name="Despesa descontada/receita recebida?",
        editable=False,
        default=False,
    )

    descricao = models.CharField(
        verbose_name="Descrição",
        max_length=50,
    )

    valor = models.DecimalField(
        verbose_name="Valor da movimentação",
        max_digits=10,
        decimal_places=2,
    )

    data = models.DateField(
        verbose_name="Data da movimentação"
    )

    def save(self, *args, **kwargs):
        if not self.liquidada:
            try:

                with transaction.atomic():
                    self.conta.liquidar_movimentacao(
                        self.tipo, self.valor
                    )
                    self.conta.save()

                    self.liquidada = True

                    super(Movimentacao, self).save(*args, **kwargs)

            except Exception:
                raise Exception(
                    "Ocorreu um erro. Por favor, tente novamente mais tarde"
                )

        super(Movimentacao, self).save(*args, **kwargs)


    class Meta:
        db_table = "movimentacao"
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"

    def __str__(self):
        return f"R$ {self.valor} | {self.conta}"
