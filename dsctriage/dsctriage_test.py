"""Test discourse-triage modules with pytest"""
import datetime
import pytest
import json

from dsctriage.discourse_post import DiscoursePost


@pytest.mark.parametrize('post_id, name, username, data, created, updated, post_string', [
    (4592175, 'User Name', 'username1', None, datetime.datetime(2022, 5, 16, 13, 59, 43, 661000, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 5, 19, 15, 32, 33, 361000, tzinfo=datetime.timezone.utc), '{"id":4592175,"name":"User Name","username":"username1","avatar_template":"/user_avatar/discourse.ubuntu.com/username1/{size}/103124_2.png","created_at":"2022-05-16T13:59:43.661Z","cooked":"\u003cp\u003e\u003ca Test comment \u003e","post_number":2,"post_type":1,"updated_at":"2022-05-19T15:32:33.361Z","reply_count":1,"reply_to_post_number":null,"quote_count":0,"incoming_link_count":3,"reads":33,"readers_count":32,"score":26.6,"yours":false,"topic_id":11522,"topic_slug":"test-slug","display_username":"","primary_group_name":null,"primary_group_flair_url":null,"primary_group_flair_bg_color":null,"primary_group_flair_color":null,"version":1,"can_edit":true,"can_delete":false,"can_recover":false,"can_wiki":true,"read":true,"user_title":null,"bookmarked":false,"actions_summary":[{"id":2,"can_act":true},{"id":3,"can_act":true},{"id":4,"can_act":true},{"id":8,"can_act":true},{"id":6,"can_act":true},{"id":7,"can_act":true}],"moderator":false,"admin":false,"staff":false,"user_id":11234234231,"hidden":false,"trust_level":0,"deleted_at":null,"user_deleted":false,"edit_reason":null,"can_view_edit_history":true,"wiki":false,"notice":{"type":"new_user"},"can_accept_answer":true,"can_unaccept_answer":false,"accepted_answer":false}'),
    (None, None, None, None, None, None, '{}'),
    ('', '', '', '', None, None, '{"id":"","name":"","username":"","raw":"","updated_at":"","created_at":""}')
])
def test_create_post_from_json(post_id, name, username, data, created, updated, post_string):
    """Test that DiscoursePost extracts json correctly"""
    post_json = json.loads(post_string)
    post = DiscoursePost(post_json)
    assert str(post.get_id()) == str(post_id)
    assert post.get_author_name() == name
    assert post.get_author_username() == username
    assert post.get_data() == data
    assert post.get_creation_time() == created
    assert post.get_update_time() == updated

    if post.get_id() is None:
        assert str(post) == 'Invalid Post'
    else:
        assert str(post.get_id()) in str(post)
