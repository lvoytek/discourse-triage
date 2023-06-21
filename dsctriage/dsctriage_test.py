"""Test discourse-triage modules with pytest."""
import datetime
import json
import pytest

from dsctriage import DiscoursePost, DiscourseTopic, DiscourseCategory, dscfinder


EXAMPLE_USER_STRING = (
    '{"id":4592175,"name":"User Name","username":"username1",'
    '"avatar_template":"/user_avatar/discourse.ubuntu.com/username1/{size}/103124_2.png",'
    '"created_at":"2022-05-16T13:59:43.661Z","cooked":"\u003cp\u003e\u003ca Test comment \u003e","post_number":2,'
    '"post_type":1,"updated_at":"2022-05-19T15:32:33.361Z","reply_count":1,"reply_to_post_number":1,'
    '"quote_count":0,"incoming_link_count":3,"reads":33,"readers_count":32,"score":26.6,"yours":false,'
    '"topic_id":11522,"topic_slug":"test-slug","display_username":"","primary_group_name":null,'
    '"primary_group_flair_url":null,"primary_group_flair_bg_color":null,"primary_group_flair_color":null,'
    '"version":1,"can_edit":true,"can_delete":false,"can_recover":false,"can_wiki":true,"read":true,'
    '"user_title":null,"bookmarked":false,"actions_summary":[{"id":2,"can_act":true},{"id":3,"can_act":true},'
    '{"id":4,"can_act":true},{"id":8,"can_act":true},{"id":6,"can_act":true},{"id":7,"can_act":true}],'
    '"moderator":false,"admin":false,"staff":false,"user_id":11234234231,"hidden":false,"trust_level":0,'
    '"deleted_at":null,"user_deleted":false,"edit_reason":null,"can_view_edit_history":true,"wiki":false,'
    '"notice":{"type":"new_user"},"can_accept_answer":true,"can_unaccept_answer":false,"accepted_answer":false}'
)


EXAMPLE_TOPIC_STRING = (
    '{"id":11522,"title":"Virtualization - libvirt","fancy_title":"Virtualization - libvirt",'
    '"slug":"virtualization-libvirt","posts_count":10,"reply_count":5,"highest_post_number":10,"image_url":null,'
    '"created_at":"2019-06-24T11:20:59.936Z","last_posted_at":"2022-06-13T17:56:31.210Z","bumped":true,'
    '"bumped_at":"2022-06-13T17:56:31.210Z","archetype":"regular","unseen":false,"last_read_post_number":2,'
    '"unread":0,"new_posts":0,"pinned":false,"unpinned":null,"visible":true,"closed":false,"archived":false,'
    '"notification_level":1,"bookmarked":false,"liked":false,"tags":[],"views":10466,"like_count":1,'
    '"has_summary":false,"last_poster_username":"chxsec","category_id":26,"pinned_globally":false,'
    '"featured_link":null,"has_accepted_answer":false,"posters":[{"extras":null,"description":"Original Poster",'
    '"user_id":37,"primary_group_id":49},{"extras":null,"description":"Frequent Poster","user_id":11016,'
    '"primary_group_id":null},{"extras":null,"description":"Frequent Poster","user_id":3783,"primary_group_id":49},'
    '{"extras":null,"description":"Frequent Poster","user_id":10864,"primary_group_id":null},{"extras":"latest",'
    '"description":"Most Recent Poster","user_id":19034,"primary_group_id":null}]}'
)


EXAMPLE_CATEGORY_STRING = (
    '{"id":17,"name":"Server","color":"0E76BD","text_color":"FFFFFF","slug":"server","topic_count":156,'
    '"post_count":1068,"position":23,"description":"A place to discuss Ubuntu Server.","description_text":"A place '
    'to discuss Ubuntu Server.","description_excerpt":"A place to discuss Ubuntu Server.",'
    '"topic_url":"/t/about-the-server-category/738","read_restricted":false,"permission":1,"notification_level":1,'
    '"topic_template":"","has_children":true,"sort_order":"","sort_ascending":null,"show_subcategory_list":false,'
    '"num_featured_topics":3,"default_view":"latest","subcategory_list_style":"rows_with_featured_topics",'
    '"default_top_period":"all","default_list_filter":"all","minimum_required_tags":0,'
    '"navigate_to_first_post_after_read":false,"topics_day":0,"topics_week":0,"topics_month":1,"topics_year":42,'
    '"topics_all_time":318,"subcategory_ids":[26,54],"uploaded_logo":null,"uploaded_background":null}'
)


EXAMPLE_SUBCATEGORY_SET_STRING = (
    '{"id":6,"name":"General Discussions","color":"92278F","text_color":"FFFFFF","slug":"general-discussions",'
    '"topic_count":4253,"post_count":11038,"position":1,"description":"Got something to say about Kubernetes?",'
    '"description_text":"Got something to say about Kubernetes?",'
    '"topic_url":"/t/about-the-general-discussions-category/18","read_restricted":false,"permission":null,'
    '"notification_level":1,"has_children":true,"sort_order":"","sort_ascending":null,"show_subcategory_list":false,'
    '"num_featured_topics":3,"default_view":"latest","subcategory_list_style":"rows_with_featured_topics",'
    '"default_top_period":"quarterly","default_list_filter":"all","minimum_required_tags":0,'
    '"navigate_to_first_post_after_read":false,"topics_day":3,"topics_week":14,"topics_month":67,"topics_year":965,'
    '"topics_all_time":4884,"subcategory_ids":[22,26],"uploaded_logo":null,"uploaded_logo_dark":null,'
    '"uploaded_background":null,"subcategory_list":[{"id":22,"name":"Windows","color":"0078d4","text_color":"FFFFFF",'
    '"slug":"windows","topic_count":77,"post_count":197,"position":19,'
    '"description":"Welcome to the Windows containers in Kubernetes discussion.",'
    '"description_text":"Welcome to the Windows containers in Kubernetes discussion.",'
    '"description_excerpt":"Welcome to the Windows containers in Kubernetes discussion.",'
    '"topic_url":"/t/about-the-windows-category/5633","read_restricted":false,"permission":null,"parent_category_id":6,'
    '"notification_level":1,"topic_template":"","has_children":false,"sort_order":"","sort_ascending":null,'
    '"show_subcategory_list":false,"num_featured_topics":3,"default_view":"",'
    '"subcategory_list_style":"rows_with_featured_topics","default_top_period":"all","default_list_filter":"all",'
    '"minimum_required_tags":0,"navigate_to_first_post_after_read":false,"topics_day":0,"topics_week":0,'
    '"topics_month":1,"topics_year":16,"topics_all_time":77,"subcategory_ids":[],"uploaded_logo":null,'
    '"uploaded_logo_dark":null,"uploaded_background":null},'
    '{"id":26,"name":"microk8s","color":"E95420","text_color":"FFFFFF","slug":"microk8s","topic_count":554,'
    '"post_count":1947,"position":23,'
    '"description":"<strong>MicroK8s</strong> is a low-ops, minimal production Kubernetes.",'
    '"description_text":"MicroK8s is a low-ops, minimal production Kubernetes.",'
    '"description_excerpt":"MicroK8s is a low-ops, minimal production Kubernetes.",'
    '"topic_url":"/t/microk8s-documentation-home/11243","read_restricted":false,"permission":null,'
    '"parent_category_id":6,"notification_level":1,"topic_template":"",'
    '"has_children":false,"sort_order":"","sort_ascending":null,"show_subcategory_list":false,"num_featured_topics":3,'
    '"default_view":"latest","subcategory_list_style":"rows_with_featured_topics","default_top_period":"yearly",'
    '"default_list_filter":"all","minimum_required_tags":0,"navigate_to_first_post_after_read":false,"topics_day":0,'
    '"topics_week":4,"topics_month":8,"topics_year":150,"topics_all_time":554,"subcategory_ids":[],'
    '"uploaded_logo":null,"uploaded_logo_dark":null,"uploaded_background":null}]}'
)


# pylint: disable=too-many-arguments
@pytest.mark.parametrize(
    "post_id, name, username, data, post_number, created, updated, rep_cnt, rep_to, post_string",
    [
        (
            4592175,
            "User Name",
            "username1",
            None,
            2,
            datetime.datetime(2022, 5, 16, 13, 59, 43, 661000, tzinfo=datetime.timezone.utc),
            datetime.datetime(2022, 5, 19, 15, 32, 33, 361000, tzinfo=datetime.timezone.utc),
            1,
            1,
            EXAMPLE_USER_STRING,
        ),
        (None, None, None, None, None, None, None, None, None, "{}"),
        (
            "",
            "",
            "",
            "",
            None,
            None,
            None,
            None,
            None,
            '{"id":"","name":"","username":"","raw":"","updated_at":"","created_at":"","reply_to_post_number":null}',
        ),
    ],
)
def test_create_post_from_json(
    post_id,
    name,
    username,
    data,
    post_number,
    created,
    updated,
    rep_cnt,
    rep_to,
    post_string,
):
    """Test that DiscoursePost extracts json correctly."""
    post_json = json.loads(post_string)
    post = DiscoursePost(post_json)
    assert post.get_id() == post_id
    assert post.get_author_name() == name
    assert post.get_author_username() == username
    assert post.get_data() == data
    assert post.get_creation_time() == created
    assert post.get_update_time() == updated
    assert post.get_post_number() == post_number
    assert post.get_num_replies() == rep_cnt
    assert post.get_reply_to_number() == rep_to

    if post_id is None:
        assert str(post) == "Invalid Post"
    else:
        assert str(post.get_id()) in str(post)


@pytest.mark.parametrize(
    "topic_id, name, slug, update_time, topic_string",
    [
        (
            11522,
            "Virtualization - libvirt",
            "virtualization-libvirt",
            datetime.datetime(2022, 6, 13, 17, 56, 31, 210000, tzinfo=datetime.timezone.utc),
            EXAMPLE_TOPIC_STRING,
        ),
        (None, None, None, None, "{}"),
        ("", "", "", None, '{"id":"","title":"","slug":"", "last_posted_at":""}'),
    ],
)
def test_create_topic_from_json(topic_id, name, slug, update_time, topic_string):
    """Test that DiscourseTopic extracts json correctly."""
    topic_json = json.loads(topic_string)
    topic = DiscourseTopic(topic_json)
    assert topic.get_id() == topic_id
    assert topic.get_name() == name
    assert topic.get_slug() == slug
    assert topic.get_latest_update_time() == update_time

    if topic_id is None or name is None:
        assert str(topic) == "Invalid Topic"
    else:
        assert topic.get_name() in str(topic)


def test_add_posts_to_topic():
    """Test that DiscourseTopic adds and provides posts correctly."""
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


@pytest.mark.parametrize(
    "category_id, name, description, category_string",
    [
        (
            17,
            "Server",
            "A place to discuss Ubuntu Server.",
            EXAMPLE_CATEGORY_STRING,
        ),
        (None, None, None, "{}"),
        ("", "", "", '{"id":"","name":"","description_text":""}'),
    ],
)
def test_create_category_from_json(category_id, name, description, category_string):
    """Test that DiscourseCategory extracts json correctly."""
    category_json = json.loads(category_string)
    category = DiscourseCategory(category_json)
    assert category.get_id() == category_id
    assert category.get_name() == name
    assert category.get_description() == description

    if name is None or category_id is None:
        assert str(category) == "Invalid Category"
    else:
        assert name in str(category)


@pytest.mark.parametrize(
    "subcategory_id, name, description, category_string",
    [
        (
            22,
            "Windows",
            "Welcome to the Windows containers in Kubernetes discussion.",
            EXAMPLE_SUBCATEGORY_SET_STRING,
        ),
        (None, None, None, '{"id":1,"subcategory_list":[{}]}'),
        (
            "",
            "",
            "",
            '{"id":1,"name":"Test","description_text":"","subcategory_list":[{"id":"","name":"",'
            '"description_text":""}]}',
        ),
    ],
)
def test_create_subcategory_from_json(subcategory_id, name, description, category_string):
    """Test that DiscourseCategory extracts subcategory json correctly."""
    category_json = json.loads(category_string)
    category = DiscourseCategory(category_json)
    assert category.get_subcategories()[0].get_id() == subcategory_id
    assert category.get_subcategories()[0].get_name() == name
    assert category.get_subcategories()[0].get_description() == description

    if name is None or subcategory_id is None:
        assert str(category.get_subcategories()[0]) == "Invalid Category"
    else:
        assert name in str(category.get_subcategories()[0])


@pytest.mark.parametrize(
    "subcategory_id, name, description, category_string",
    [
        (
            22,
            "Windows",
            "Welcome to the Windows containers in Kubernetes discussion.",
            EXAMPLE_SUBCATEGORY_SET_STRING,
        ),
        (
            26,
            "microk8s",
            "MicroK8s is a low-ops, minimal production Kubernetes.",
            EXAMPLE_SUBCATEGORY_SET_STRING,
        ),
        (28, None, None, EXAMPLE_SUBCATEGORY_SET_STRING),
    ],
)
def test_get_subcategory_by_id(subcategory_id, name, description, category_string):
    """Test that DiscourseCategory finds the correct subcategory by id."""
    category_json = json.loads(category_string)
    category = DiscourseCategory(category_json)
    subcategory = category.get_subcategory_by_id(subcategory_id)

    if name is None:
        assert subcategory is None
    else:
        assert subcategory.get_name() == name
        assert subcategory.get_description() == description
        assert name in str(subcategory)


@pytest.mark.parametrize(
    "subcategory_id, name, description, category_string",
    [
        (
            22,
            "Windows",
            "Welcome to the Windows containers in Kubernetes discussion.",
            EXAMPLE_SUBCATEGORY_SET_STRING,
        ),
        (
            26,
            "microk8s",
            "MicroK8s is a low-ops, minimal production Kubernetes.",
            EXAMPLE_SUBCATEGORY_SET_STRING,
        ),
        (None, "test fail", None, EXAMPLE_SUBCATEGORY_SET_STRING),
    ],
)
def test_get_subcategory_by_name(subcategory_id, name, description, category_string):
    """Test that DiscourseCategory finds the correct subcategory by name."""
    category_json = json.loads(category_string)
    category = DiscourseCategory(category_json)
    subcategory = category.get_subcategory_by_name(name)

    if subcategory_id is None:
        assert subcategory is None
    else:
        assert subcategory.get_id() == subcategory_id
        assert subcategory.get_description() == description
        assert name in str(subcategory)


def test_add_topics_to_category():
    """Test that DiscourseCategory adds and provides topics correctly."""
    category = DiscourseCategory(json.loads('{"id":"45678","name":"Test","description_text":"A test category."}'))
    assert len(category.get_topics()) == 0

    topic_1 = DiscourseTopic(json.loads('{"id":"10","title":"Test Topic 1","slug":"test-topic-1"}'))
    category.add_topic(topic_1)
    assert len(category.get_topics()) == 1

    topic_2 = DiscourseTopic(json.loads('{"id":"11","title":"Test Topic 2","slug":"test-topic-2"}'))
    category.add_topic(topic_2)
    assert len(category.get_topics()) == 2

    with pytest.raises(TypeError) as err:
        category.add_topic(None)
    assert "not a DiscourseTopic" in str(err.value)

    with pytest.raises(TypeError) as err_2:
        category.add_topic(123)
    assert "not a DiscourseTopic" in str(err_2.value)

    assert len(category.get_topics()) == 2


@pytest.mark.parametrize(
    "url_out, template, id_var, site",
    [
        (
            "https://discourse.ubuntu.com/posts/12453.json",
            dscfinder.POST_JSON_URL,
            12453,
            None,
        ),
        ("http://test/posts/1111.json", dscfinder.POST_JSON_URL, "1111", "http://test"),
        (
            "https://discourse.ubuntu.com/posts/1/revisions/latest.json",
            dscfinder.POST_LATEST_EDIT_JSON_URL,
            1,
            None,
        ),
        (
            "https://discourse.ubuntu.com/categories.json?include_subcategories=true",
            dscfinder.CATEGORY_LIST_JSON_URL,
            None,
            None,
        ),
    ],
)
def test_dscfinder_create_url(url_out, template, id_var, site):
    """Test that dscfinder creates urls correctly."""
    assert url_out == dscfinder.create_url(template, id_var, site)
