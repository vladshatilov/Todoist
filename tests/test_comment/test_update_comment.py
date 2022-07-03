from http import HTTPStatus

import pytest

from goals.serializers import GoalCommentSerializer

UPDATED_COMMENT = "Updated comment"


def get_patch_response(client, comment):
    return client.patch(
        f"/goals/goal_comment/{comment.id}",
        {"text": UPDATED_COMMENT},
        content_type="application/json",
    )


@pytest.mark.django_db
def test_partial_update_by_owner(client, logged_in_user, comment):
    expected_response = GoalCommentSerializer(comment).data
    expected_response["text"] = UPDATED_COMMENT

    response = get_patch_response(client, comment)

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response


@pytest.mark.django_db
def test_partial_update_forbidden_to_unauthorized_user(client, comment):
    expected_response = GoalCommentSerializer(comment).data
    expected_response["text"] = UPDATED_COMMENT

    response = get_patch_response(client, comment)

    assert response.status_code == HTTPStatus.FORBIDDEN



@pytest.mark.django_db
def test_partial_update_allowed_to_writer(
    client, logged_in_user, comment_for_goal_user2_user1_writer
):
    comment = comment_for_goal_user2_user1_writer
    response = get_patch_response(client, comment)

    expected_response = GoalCommentSerializer(comment).data
    expected_response["text"] = UPDATED_COMMENT

    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    response_json.pop("updated")
    expected_response.pop("updated")

    assert response_json == expected_response

