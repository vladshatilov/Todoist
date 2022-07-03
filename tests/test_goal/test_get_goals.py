from http import HTTPStatus

import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_get_all_by_owner(client, logged_in_user, goals_for_category, boardparticipant_user1_owner):
    goal_1, goal_2 = goals_for_category

    expected_response = {'count': 2,
         'next': None,
         'previous': None,
         'results': [
        GoalSerializer(goal_1).data,
        GoalSerializer(goal_2).data,
    ]}
    response = client.get("/goals/goal/list")

    assert response.status_code == HTTPStatus.OK
    # assert sorted(response.json(), key=lambda x: x["id"]) == expected_response
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_forbidden_to_user_wo_rights(
    client, logged_in_user, goals_for_category_user2
):
    response = client.get("/goals/goal/list")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'count': 0, 'next': None, 'previous': None, 'results': []}


@pytest.mark.django_db
def test_get_all_forbidden_to_unauthorized_user(
    client, user2, goals_for_category_user2
):
    response = client.get("/goals/goal/list")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_get_all_allowed_to_reader(
    client, logged_in_user, goals_for_category_user2_user1_reader
):
    goal_1, goal_2 = goals_for_category_user2_user1_reader

    expected_response = {'count': 2,
         'next': None,
         'previous': None,
         'results': [
        GoalSerializer(goal_1).data,
        GoalSerializer(goal_2).data,
    ]}
    response = client.get("/goals/goal/list")

    assert response.status_code == HTTPStatus.OK
    # assert sorted(response.json(), key=lambda x: x["id"]) == expected_response
    assert response.json() == expected_response


@pytest.mark.django_db
def test_get_all_allowed_to_writer(
    client, logged_in_user, goals_for_category_user2_user1_writer
):
    goal_1, goal_2 = goals_for_category_user2_user1_writer

    expected_response = {'count': 2,
         'next': None,
         'previous': None,
         'results': [
        GoalSerializer(goal_1).data,
        GoalSerializer(goal_2).data,
    ]}
    response = client.get("/goals/goal/list")

    assert response.status_code == HTTPStatus.OK
    # assert sorted(response.json(), key=lambda x: x["id"]) == expected_response
    assert response.json() == expected_response
