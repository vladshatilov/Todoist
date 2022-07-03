from http import HTTPStatus

import pytest

from goals.serializers import GoalCommentSerializer

URL = "/goals/goal_comment/list"


@pytest.mark.django_db
def test_get_all_by_owner(client, logged_in_user, comments):
    comment_1, comment_2 = comments

    expected_response = {'count': 2,
         'next': None,
         'previous': None,
         'results': [
        GoalCommentSerializer(comment_2).data,
        GoalCommentSerializer(comment_1).data
    ]}
    response = client.get(URL)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response




@pytest.mark.django_db
def test_get_all_forbidden_to_unauthorized_user(client, comments):
    response = client.get(URL)

    assert response.status_code == HTTPStatus.FORBIDDEN

