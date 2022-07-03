import pytest

from goals.models import Board, BoardParticipant, Comment, Goal, GoalCategory
from tests.factories import UserFactory

TEST_USERNAME = "james"
TEST_USERNAME_2 = "user2"
USER_PASSWORD = "qwerty123"
CATEGORY_NAME = "Testing category name"
CATEGORY_NAME_2 = "Testing category name 2"
GOAL_NAME = "Testing goal name"
GOAL_NAME_2 = "Testing goal name 2"
DUE_DATE = "2022-07-01"
COMMENT_TEXT = "Testing comment"
COMMENT_TEXT_2 = "Testing comment 2"
EMAIL = 'TEST@mail.ru'


@pytest.fixture
@pytest.mark.django_db
def user1(django_user_model):
    # return UserFactory()
    return django_user_model.objects.create_user(
        username=TEST_USERNAME, password=USER_PASSWORD, email=EMAIL, last_name='', first_name=''
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username=TEST_USERNAME_2, password=USER_PASSWORD, email=EMAIL, last_name='', first_name=''
    )


@pytest.fixture
def logged_in_user(client, user1):
    client.login(username=user1.username, password=USER_PASSWORD)
    return user1


@pytest.fixture
def logged_in_user2(client, user2):
    client.login(username=TEST_USERNAME_2, password=USER_PASSWORD)
    return user2


@pytest.fixture
def board(user1):
    board_name = "Testing board name"
    board_item = Board.objects.create(title=board_name)
    # board_participant = BoardParticipant.objects.create(board=board_item, user=user1, role=1)
    return board_item


@pytest.fixture
def board2(user1):
    board_name = "Testing board name 2"
    board_item = Board.objects.create(title=board_name)
    # board_participant = BoardParticipant.objects.create(board=board_item, user=user1, role=1)
    return board_item


@pytest.fixture
def category_for_user1(user1, board):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
def goal_for_category(user1, category_for_user1):
    return Goal.objects.create(
        title=GOAL_NAME, category=category_for_user1, due_date=DUE_DATE, user=user1
    )


@pytest.fixture
def goal_for_category_user2(user2, category_for_user2):
    return Goal.objects.create(
        title=GOAL_NAME, category=category_for_user2, due_date=DUE_DATE, user=user2
    )


@pytest.fixture
def goal_for_category_user2_user1_reader(user2, category_for_board_user2_user1_reader):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_reader,
        due_date=DUE_DATE,
        user=user2
    )


@pytest.fixture
def goal_for_category_user2_user1_writer(user2, category_for_board_user2_user1_writer):
    return Goal.objects.create(
        title=GOAL_NAME,
        category=category_for_board_user2_user1_writer,
        due_date=DUE_DATE,
        user=user2
    )


def make_categories(user, board):
    category = GoalCategory.objects.create(title=CATEGORY_NAME, user=user, board=board)
    category_2 = GoalCategory.objects.create(
        title=CATEGORY_NAME_2, user=user, board=board
    )
    return category, category_2


def make_goals(user,category):
    goal = Goal.objects.create(title=GOAL_NAME, category=category, due_date=DUE_DATE,user=user)
    goal_2 = Goal.objects.create(
        title=GOAL_NAME_2, category=category, due_date=DUE_DATE,user=user
    )
    return goal, goal_2


def make_comments(goal, user):
    comment = Comment.objects.create(text=COMMENT_TEXT, goal=goal, user=user)
    comment_2 = Comment.objects.create(text=COMMENT_TEXT_2, goal=goal, user=user)
    return comment, comment_2


@pytest.fixture
@pytest.mark.django_db
def goals_for_category(user1, category_for_user1):
    return make_goals(user1,category_for_user1)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2(user2, category_for_user2):
    return make_goals(user2, category_for_user2)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2_user1_reader(user1,category_for_board_user2_user1_reader):
    return make_goals(user1, category_for_board_user2_user1_reader)


@pytest.fixture
@pytest.mark.django_db
def goals_for_category_user2_user1_writer(user1,category_for_board_user2_user1_writer):
    return make_goals(user1, category_for_board_user2_user1_writer)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user1(user1, board, boardparticipant_user1_owner):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2(user2, board, boardparticipant_user2_owner):
    return make_categories(user2, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2_user1_reader(
        user1, board, boardparticipant_user2_owner, boardparticipant_user1_reader
):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def categories_for_user2_user1_writer(
        user1, board, boardparticipant_user1_writer, boardparticipant_user2_owner
):
    return make_categories(user1, board)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_owner(board, user1):
    return BoardParticipant.objects.create(board=board, user=user1)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_owner(board2, user1):
    return BoardParticipant.objects.create(board=board2, user=user1)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user2_owner(board, user2):
    return BoardParticipant.objects.create(board=board, user=user2)


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_reader(board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.reader
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_reader(board2, user1):
    return BoardParticipant.objects.create(
        board=board2, user=user1, role=BoardParticipant.Role.reader
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_user1_writer(board, user1):
    return BoardParticipant.objects.create(
        board=board, user=user1, role=BoardParticipant.Role.writer
    )


@pytest.fixture
@pytest.mark.django_db
def boardparticipant_board2_user1_writer(board2, user1):
    return BoardParticipant.objects.create(
        board=board2, user=user1, role=BoardParticipant.Role.writer
    )


@pytest.fixture
@pytest.mark.django_db
def category_for_user2(board, user2, boardparticipant_user2_owner):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user2, board=board)


@pytest.fixture
@pytest.mark.django_db
def category_for_board_user2_user1_reader(
        board, user1, user2, boardparticipant_user1_reader
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
@pytest.mark.django_db
def category_for_board_user2_user1_writer(
        board, user1, user2, boardparticipant_user1_writer
):
    return GoalCategory.objects.create(title=CATEGORY_NAME, user=user1, board=board)


@pytest.fixture
@pytest.mark.django_db
def comment(user1, goal_for_category):
    return Comment.objects.create(text=COMMENT_TEXT, goal=goal_for_category, user=user1)


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2(user1, goal_for_category_user2):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2_user1_reader(user1, goal_for_category_user2_user1_reader):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_reader, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comment_user2_for_goal_user2_user1_reader(
        user2, goal_for_category_user2_user1_reader
):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_reader, user=user2
    )


@pytest.fixture
@pytest.mark.django_db
def comment_user2_for_goal_user2_user1_writer(
        user2, goal_for_category_user2_user1_writer
):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_writer, user=user2
    )


@pytest.fixture
@pytest.mark.django_db
def comment_for_goal_user2_user1_writer(user1, goal_for_category_user2_user1_writer):
    return Comment.objects.create(
        text=COMMENT_TEXT, goal=goal_for_category_user2_user1_writer, user=user1
    )


@pytest.fixture
@pytest.mark.django_db
def comments(user1, goal_for_category):
    return make_comments(goal_for_category, user1)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2(user2, goal_for_category_user2):
    return make_comments(goal_for_category_user2, user2)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2_user1_reader(user2, goal_for_category_user2_user1_reader):
    return make_comments(goal_for_category_user2_user1_reader, user2)


@pytest.fixture
@pytest.mark.django_db
def comments_for_goal_user2_user1_writer(user2, goal_for_category_user2_user1_writer):
    return make_comments(goal_for_category_user2_user1_writer, user2)
