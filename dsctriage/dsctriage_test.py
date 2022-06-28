"""Test discourse-triage modules with pytest"""
import datetime
import pytest
import json

from dsctriage import DiscoursePost, DiscourseTopic


@pytest.mark.parametrize('post_id, name, username, data, created, updated, post_string', [
    (4592175, 'User Name', 'username1', None, datetime.datetime(2022, 5, 16, 13, 59, 43, 661000, tzinfo=datetime.timezone.utc), datetime.datetime(2022, 5, 19, 15, 32, 33, 361000, tzinfo=datetime.timezone.utc), '{"id":4592175,"name":"User Name","username":"username1","avatar_template":"/user_avatar/discourse.ubuntu.com/username1/{size}/103124_2.png","created_at":"2022-05-16T13:59:43.661Z","cooked":"\u003cp\u003e\u003ca Test comment \u003e","post_number":2,"post_type":1,"updated_at":"2022-05-19T15:32:33.361Z","reply_count":1,"reply_to_post_number":null,"quote_count":0,"incoming_link_count":3,"reads":33,"readers_count":32,"score":26.6,"yours":false,"topic_id":11522,"topic_slug":"test-slug","display_username":"","primary_group_name":null,"primary_group_flair_url":null,"primary_group_flair_bg_color":null,"primary_group_flair_color":null,"version":1,"can_edit":true,"can_delete":false,"can_recover":false,"can_wiki":true,"read":true,"user_title":null,"bookmarked":false,"actions_summary":[{"id":2,"can_act":true},{"id":3,"can_act":true},{"id":4,"can_act":true},{"id":8,"can_act":true},{"id":6,"can_act":true},{"id":7,"can_act":true}],"moderator":false,"admin":false,"staff":false,"user_id":11234234231,"hidden":false,"trust_level":0,"deleted_at":null,"user_deleted":false,"edit_reason":null,"can_view_edit_history":true,"wiki":false,"notice":{"type":"new_user"},"can_accept_answer":true,"can_unaccept_answer":false,"accepted_answer":false}'),
    (None, None, None, None, None, None, '{}'),
    ('', '', '', '', None, None, '{"id":"","name":"","username":"","raw":"","updated_at":"","created_at":""}')
])
def test_create_post_from_json(post_id, name, username, data, created, updated, post_string):
    """Test that DiscoursePost extracts json correctly"""
    post_json = json.loads(post_string)
    post = DiscoursePost(post_json)
    assert post.get_id() == post_id
    assert post.get_author_name() == name
    assert post.get_author_username() == username
    assert post.get_data() == data
    assert post.get_creation_time() == created
    assert post.get_update_time() == updated

    if post_id is None:
        assert str(post) == 'Invalid Post'
    else:
        assert str(post.get_id()) in str(post)


@pytest.mark.parametrize('topic_id, name, slug, topic_string', [
    (11522, 'Virtualization - libvirt', 'virtualization-libvirt', '{"id":11522,"title":"Virtualization - libvirt","fancy_title":"Virtualization - libvirt","slug":"virtualization-libvirt","posts_count":10,"reply_count":5,"highest_post_number":10,"image_url":null,"created_at":"2019-06-24T11:20:59.936Z","last_posted_at":"2022-06-13T17:56:31.210Z","bumped":true,"bumped_at":"2022-06-13T17:56:31.210Z","archetype":"regular","unseen":false,"last_read_post_number":2,"unread":0,"new_posts":0,"pinned":false,"unpinned":null,"visible":true,"closed":false,"archived":false,"notification_level":1,"bookmarked":false,"liked":false,"tags":[],"views":10466,"like_count":1,"has_summary":false,"last_poster_username":"chxsec","category_id":26,"pinned_globally":false,"featured_link":null,"has_accepted_answer":false,"posters":[{"extras":null,"description":"Original Poster","user_id":37,"primary_group_id":49},{"extras":null,"description":"Frequent Poster","user_id":11016,"primary_group_id":null},{"extras":null,"description":"Frequent Poster","user_id":3783,"primary_group_id":49},{"extras":null,"description":"Frequent Poster","user_id":10864,"primary_group_id":null},{"extras":"latest","description":"Most Recent Poster","user_id":19034,"primary_group_id":null}]}'),
    (None, None, None, '{}'),
    ('', '', '', '{"id":"","title":"","slug":""}')
])
def test_create_topic_from_json(topic_id, name, slug, topic_string):
    topic_json = json.loads(topic_string)
    topic = DiscourseTopic(topic_json)
    assert topic.get_id() == topic_id
    assert topic.get_name() == name
    assert topic.get_slug() == slug

    if topic_id is None or name is None:
        assert str(topic) == 'Invalid Topic'
    else:
        assert topic.get_name() in str(topic)


def test_add_posts_to_topic():
    topic = DiscourseTopic(json.loads('{"id":"12345","title":"Test Topic","slug":"test-topic"}'))
    assert len(topic.get_posts()) == 0

    post_1 = DiscoursePost(json.loads('{"id":1,"name":"User","username":"","raw":"","updated_at":"","created_at":""}'))
    topic.add_post(post_1)
    assert len(topic.get_posts()) == 1

    post_2 = DiscoursePost(json.loads('{"id":2,"name":"User","username":"","raw":"","updated_at":"","created_at":""}'))
    topic.add_post(post_2)
    assert len(topic.get_posts()) == 2

    with pytest.raises(TypeError) as err:
        topic.add_post(None)
    assert "not a DiscoursePost" in str(err.value)

    with pytest.raises(TypeError) as err_2:
        topic.add_post(123)
    assert "not a DiscoursePost" in str(err_2.value)

    assert len(topic.get_posts()) == 2
