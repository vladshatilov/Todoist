import logging

from django.core.management.base import BaseCommand, CommandError
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from django_33_finalPrj import settings
from goals.models import Goal, GoalCategory
from goals.serializers import GoalCategorySerializer
from goals.statuses import Priority, Status


class Command(BaseCommand):
    help = 'run bot'
    loaddata_command = "runbot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)
        self.categories = []
        self.goal_name_picking_flag = False
        self.category_name = ''
        self.goal_name = ''

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        print(f'111111111111111111111111111 msg.text- {msg.text}')
        logging.info(f'111111111111111111111111112 msg.text- {msg.text}')
        tg_user.set_verification_code()
        tg_user.save(update_fields=["verification_code"])
        self.tg_client.send_message(
            msg.chat.id, f"[verification code] {tg_user.verification_code}"
        )

    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in gls]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def fetch_categories(self, msg: Message, tg_user: TgUser):
        cats = GoalCategory.objects.filter(board__board_participants__user=tg_user.user, is_deleted=False)
        if cats.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in cats]
            self.categories = [f"{item.title}" for item in cats]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[category list is empty]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if "/goals" in msg.text:
            self.fetch_tasks(msg, tg_user)
        elif "/create" in msg.text:
            self.tg_client.send_message(msg.chat.id, "[Choose category]")
            self.fetch_categories(msg, tg_user)
        elif "/cancel" in msg.text:
            self.tg_client.send_message(msg.chat.id, "[Cancel operation]")
            self.categories = []
            self.goal_name_picking_flag = False
            self.category_name = ''
        elif self.goal_name_picking_flag:
            self.goal_name = msg.text
            validated_data = {
                "title": self.goal_name,
                "description": None,
                "due_date": None,
                "status": Status.to_do,
                "priority": Priority.medium,
                "category": GoalCategory.objects.get(title=self.category_name),
                "user": tg_user.user
            }
            Goal.objects.create(**validated_data)
            goal = Goal.objects.get(title=self.goal_name)
            self.categories = []
            self.goal_name_picking_flag = False
            self.category_name = ''
            self.tg_client.send_message(msg.chat.id, "[Successfully created goal]")
            self.tg_client.send_message(msg.chat.id, f"[Link: http://todo-some.ml/api/goals/goal/{goal.id}]")
        elif msg.text in self.categories and len(self.categories) > 0:
            self.tg_client.send_message(msg.chat.id, "[Type new goal name]")
            self.category_name = msg.text
            self.goal_name_picking_flag = True
        elif msg.text not in self.categories and len(self.categories) > 0:
            self.tg_client.send_message(msg.chat.id, "[No category with that name]")
        else:
            self.tg_client.send_message(msg.chat.id, "[unknown command]")
            # self.tg_client.send_message(msg["chat"]["id"], "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            user_ud=msg.from_.id,
            defaults={
                "chat_id": msg.chat.id,
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[greeting]")

        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                self.handle_message(item.message)
