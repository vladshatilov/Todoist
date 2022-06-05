from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from core.models import Profile
from goals.statuses import Priority, Status


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда модель только создается – у нее нет id
            self.created = timezone.now()
        self.updated = timezone.now()  # Каждый раз, когда вызывается save, проставляем свежую дату обновления
        return super().save(*args, **kwargs)


class UserModelMixin(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(Profile, verbose_name="Автор", on_delete=models.PROTECT)


class Board(DatesModelMixin):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    editable_choices = Role.choices
    editable_choices.pop(0)

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="board_participants",
    )
    user = models.ForeignKey(
        Profile,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner,
    )


class GoalCategory(DatesModelMixin, UserModelMixin, models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="parent_board"#, null=True
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin, UserModelMixin, models.Model):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=255, validators=[MinLengthValidator(1, message="Title should have length bigger than 1")])
    description = models.TextField(verbose_name="Описание", null=True)
    due_date = models.DateField(verbose_name="Дата выполнения", null=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    category = models.ForeignKey(to=GoalCategory, related_name='category', related_query_name='categories', verbose_name='Категория', on_delete=models.CASCADE) #, blank=True, null=True,


class Comment(DatesModelMixin, UserModelMixin, models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.CharField(verbose_name="Название", max_length=255, null=False, )
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, null=False, )

