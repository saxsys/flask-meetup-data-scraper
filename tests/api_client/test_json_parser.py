import time
from datetime import datetime
from time import sleep

import pytest

from meetup_search.meetup_api_client.exceptions import (
    EventAlreadyExists,
    InvalidResponse,
)
from meetup_search.meetup_api_client.json_parser import (
    get_category_from_response,
    get_event_from_response,
    get_event_host_from_response,
    get_group_from_response,
    get_group_organizer_from_response,
    get_meta_category_from_response,
    get_topic_from_response,
    get_venue_from_response,
)
from meetup_search.models.group import Event, Group, Topic
from tests.meetup_api_demo_response import (
    get_category_response,
    get_event_host_response,
    get_event_response,
    get_group_response,
    get_member_response,
    get_meta_category_response,
    get_topic_response,
    get_venue_response,
)


def test_get_group_from_response():
    # set group response
    group_1_response: dict = get_group_response(
        meetup_id=1, urlname="group_1", content=False
    )
    group_2_response: dict = get_group_response(
        meetup_id=2, urlname="group_2", content=True
    )

    # get group model
    group_1: Group = get_group_from_response(response=group_1_response)
    group_2: Group = get_group_from_response(response=group_2_response)

    # assert group_1
    assert isinstance(group_1, Group)
    assert group_1.meetup_id == group_1_response["id"]
    assert group_1.urlname == group_1_response["urlname"]
    assert (
        time.mktime(group_1.created.timetuple()) == group_1_response["created"] / 1000
    )
    assert group_1.description == group_1_response["description"]
    assert group_1.location == {
        "lat": group_1_response["lat"],
        "lon": group_1_response["lon"],
    }
    assert group_1.link == group_1_response["link"]
    assert group_1.members == group_1_response["members"]
    assert group_1.name == group_1_response["name"]
    assert group_1.nomination_acceptable is False
    assert group_1.status == group_1_response["status"]
    assert group_1.timezone == group_1_response["timezone"]
    assert group_1.visibility == group_1_response["visibility"]
    assert group_1.short_link is None
    assert group_1.welcome_message is None
    assert group_1.city is None
    assert group_1.city_link is None
    assert group_1.untranslated_city is None
    assert group_1.country is None
    assert group_1.localized_country_name is None
    assert group_1.localized_location is None
    assert group_1.state is None
    assert group_1.join_mode is None
    assert group_1.fee_options_currencies_code is None
    assert group_1.fee_options_currencies_default is None
    assert group_1.fee_options_type is None
    assert group_1.member_limit is None
    assert group_1.who is None

    # category
    assert group_1.category_id is None
    assert group_1.category_name is None
    assert group_1.category_shortname is None
    assert group_1.category_sort_name is None

    # meta_category
    assert group_1.meta_category_id is None
    assert group_1.meta_category_shortname is None
    assert group_1.meta_category_name is None
    assert group_1.meta_category_sort_name is None

    # topics
    assert len(group_1.topics) == 0

    # organizer
    assert group_1.organizer_id is None
    assert group_1.organizer_name is None
    assert group_1.organizer_bio is None

    # assert group_2
    assert isinstance(group_2, Group)
    assert group_2.meetup_id == group_2_response["id"]
    assert group_2.urlname == group_2_response["urlname"]
    assert (
        time.mktime(group_2.created.timetuple()) == group_2_response["created"] / 1000
    )
    assert group_2.description == group_2_response["description"]
    assert group_2.location == {
        "lat": group_2_response["lat"],
        "lon": group_2_response["lon"],
    }
    assert group_2.link == group_2_response["link"]
    assert group_2.members == group_2_response["members"]
    assert group_2.name == group_2_response["name"]
    assert group_2.nomination_acceptable is True
    assert group_2.status == group_2_response["status"]
    assert group_2.timezone == group_2_response["timezone"]
    assert group_2.visibility == group_2_response["visibility"]
    assert group_2.short_link == group_2_response["short_link"]
    assert group_2.welcome_message == group_2_response["welcome_message"]
    assert group_2.city == group_2_response["city"]
    assert group_2.city_link == group_2_response["city_link"]
    assert group_2.untranslated_city == group_2_response["untranslated_city"]
    assert group_2.country == group_2_response["country"]
    assert group_2.localized_country_name == group_2_response["localized_country_name"]
    assert group_2.localized_location == group_2_response["localized_location"]
    assert group_2.state == group_2_response["state"]
    assert group_2.join_mode == group_2_response["join_mode"]
    assert (
        group_2.fee_options_currencies_code
        == group_2_response["fee_options"]["currencies"]["code"]
    )
    assert (
        group_2.fee_options_currencies_default
        == group_2_response["fee_options"]["currencies"]["default"]
    )
    assert group_2.fee_options_type == group_2_response["fee_options"]["type"]
    assert group_2.member_limit == group_2_response["member_limit"]
    assert group_2.who == group_2_response["who"]

    # category
    assert group_2.category_id == group_2_response["category"]["id"]
    assert group_2.category_name is None
    assert group_2.category_shortname is None
    assert group_2.category_sort_name is None

    # meta_category
    assert group_2.meta_category_id == group_2_response["meta_category"]["id"]
    assert (
        group_2.meta_category_shortname
        == group_2_response["meta_category"]["shortname"]
    )
    assert group_2.meta_category_name == group_2_response["meta_category"]["name"]
    assert (
        group_2.meta_category_sort_name
        == group_2_response["meta_category"]["sort_name"]
    )

    # topics
    assert len(group_2.topics) == 1
    assert isinstance(group_2.topics[0], Topic)

    # organizer
    assert group_2.organizer_id == group_2_response["organizer"]["id"]
    assert group_2.organizer_name is None
    assert group_2.organizer_bio is None


def test_get_event_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_event_1")
    )

    # set event response
    event_1_response: dict = get_event_response(meetup_id="1", content=False)
    event_2_response: dict = get_event_response(meetup_id="2", content=True)

    # get event model
    event_1: Event = get_event_from_response(response=event_1_response, group=group_1)
    event_2: Event = get_event_from_response(response=event_2_response, group=group_1)

    # assert event_1
    assert isinstance(event_1, Event)
    assert event_1.meetup_id == event_1_response["id"]
    assert event_1.time == datetime.fromtimestamp(event_1_response["time"] / 1000)
    assert event_1.created is None
    assert event_1.name == event_1_response["name"]
    assert event_1.link == event_1_response["link"]
    assert event_1.attendance_count is None
    assert event_1.attendance_sample is None
    assert event_1.attendee_sample is None
    assert event_1.date_in_series_pattern is False
    assert event_1.description is None
    assert event_1.description is None
    assert event_1.duration is None
    # event_hosts
    assert event_1.fee_accepts is None
    assert event_1.fee_amount is None
    assert event_1.fee_currency is None
    assert event_1.fee_description is None
    assert event_1.fee_label is None
    assert event_1.how_to_find_us is None
    assert event_1.status is None
    assert event_1.updated is None
    assert event_1.utc_offset is None
    # venue
    assert event_1.venue_visibility is None
    assert event_1.visibility is None

    # save group
    group_1.add_event(event_1)
    group_1.add_event(event_2)
    group_1.save()
    sleep(1)

    # assert event_2
    assert isinstance(event_2, Event)
    assert event_2.meetup_id == event_2_response["id"]
    assert event_2.time == datetime.fromtimestamp(event_2_response["time"] / 1000)
    assert event_2.created == datetime.fromtimestamp(event_2_response["created"] / 1000)
    assert event_2.name == event_2_response["name"]
    assert event_2.link == event_2_response["link"]
    assert event_2.attendance_count == event_2_response["attendance_count"]
    assert event_2.attendance_sample == event_2_response["attendance_sample"]
    assert event_2.attendee_sample == event_2_response["attendee_sample"]
    assert event_2.date_in_series_pattern == event_2_response["date_in_series_pattern"]
    assert event_2.description == event_2_response["description"]
    assert event_2.description == event_2_response["description"]
    assert event_2.duration == event_2_response["duration"]
    # event_hosts
    assert event_2.fee_accepts == event_2_response["fee"]["accepts"]
    assert event_2.fee_amount == event_2_response["fee"]["amount"]
    assert event_2.fee_currency == event_2_response["fee"]["currency"]
    assert event_2.fee_description == event_2_response["fee"]["description"]
    assert event_2.fee_label == event_2_response["fee"]["label"]
    assert event_2.how_to_find_us == event_2_response["how_to_find_us"]
    assert event_2.status == event_2_response["status"]
    assert event_2.updated == datetime.fromtimestamp(event_2_response["updated"] / 1000)
    assert event_2.utc_offset == event_2_response["utc_offset"] / 1000
    # venue
    assert event_2.venue_visibility == event_2_response["venue_visibility"]
    assert event_2.visibility == event_2_response["visibility"]

    # check when event already exists
    with pytest.raises(EventAlreadyExists):
        get_event_from_response(response=event_1_response, group=group_1)

    # check when with invalid response
    with pytest.raises(InvalidResponse):
        del event_1_response["id"]
        get_event_from_response(response=event_1_response, group=group_1)


def test_get_venue_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_venue_1")
    )

    # set event response
    event_1_response: dict = get_event_response(meetup_id="1", content=False)

    # set venue response
    venue_1_response: dict = get_venue_response(content=False)
    venue_2_response: dict = get_venue_response(content=True)
    venue_3_response: dict = get_venue_response(
        content=True, lat=37.387474060058594, lon=-122.05754089355469
    )

    # get event model
    event_1: Event = get_event_from_response(response=event_1_response, group=group_1)

    # get venue_1 from repsonse
    event_2: Event = get_venue_from_response(response=venue_1_response, event=event_1)

    # assert event_2
    assert isinstance(event_2, Event)
    assert event_2.venue_address_1 is None
    assert event_2.venue_address_2 is None
    assert event_2.venue_address_3 is None
    assert event_2.venue_city is None
    assert event_2.venue_country is None
    assert event_2.venue_localized_country_name is None
    assert event_2.venue_name is None
    assert event_2.venue_phone is None
    assert event_2.venue_zip_code is None
    assert event_2.venue_location is None

    # get venue_2 from repsonse
    event_3: Event = get_venue_from_response(response=venue_2_response, event=event_1)

    # assert event_3
    assert isinstance(event_3, Event)
    assert event_3.venue_address_1 == venue_2_response["address_1"]
    assert event_3.venue_address_2 == venue_2_response["address_2"]
    assert event_3.venue_address_3 == venue_2_response["address_3"]
    assert event_3.venue_city == venue_2_response["city"]
    assert event_3.venue_country == venue_2_response["country"]
    assert (
        event_3.venue_localized_country_name
        == venue_2_response["localized_country_name"]
    )
    assert event_3.venue_name == venue_2_response["name"]
    assert event_3.venue_phone == venue_2_response["phone"]
    assert event_3.venue_zip_code == venue_2_response["zip_code"]
    assert event_3.venue_location == {
        "lat": venue_2_response["lat"],
        "lon": venue_2_response["lon"],
    }

    # get venue_3 from repsonse
    event_4: Event = get_venue_from_response(response=venue_3_response, event=event_1)

    # assert event_3
    assert isinstance(event_4, Event)
    assert event_4.venue_location == {
        "lat": venue_3_response["lat"],
        "lon": venue_3_response["lon"],
    }

    # save group
    group_1.save()


def test_get_event_host_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_event_host_1")
    )

    # set event response
    event_1_response: dict = get_event_response(meetup_id="1", content=False)

    # set event_host response
    event_host_1_response: dict = get_event_host_response(content=False)
    event_host_2_response: dict = get_event_host_response(content=True)

    # get event model
    event_1: Event = get_event_from_response(response=event_1_response, group=group_1)

    # get event_host_2 from repsonse
    event_2: Event = get_event_host_from_response(
        response=event_host_1_response, event=event_1
    )

    # assert event_2
    assert isinstance(event_2, Event)
    assert event_2.event_host_host_count is None
    assert event_2.event_host_id is None
    assert event_2.event_host_intro is None
    assert event_2.event_host_join_date is None
    assert event_2.event_host_name is None

    # get event_host_3 from repsonse
    event_3: Event = get_event_host_from_response(
        response=event_host_2_response, event=event_1
    )

    # assert event_3
    assert isinstance(event_3, Event)
    assert event_3.event_host_host_count == event_host_2_response["host_count"]
    assert event_3.event_host_id == event_host_2_response["id"]
    assert event_3.event_host_intro == event_host_2_response["intro"]
    assert (
        time.mktime(event_3.event_host_join_date.timetuple())
        == event_host_2_response["join_date"] / 1000
    )
    assert event_3.event_host_name == event_host_2_response["name"]

    # save group
    group_1.save()


def test_get_group_organizer_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_organizer_1")
    )

    # set organizer response
    organizer_1_response: dict = get_member_response(content=False)
    organizer_2_response: dict = get_member_response(content=True)

    # get organizer from repsonse
    group_2: Group = get_group_organizer_from_response(
        response=organizer_1_response, group=group_1
    )

    # assert group
    assert isinstance(group_2, Group)
    assert group_2.organizer_id == organizer_2_response["id"]
    assert group_2.organizer_name is None
    assert group_2.organizer_bio is None

    # get organizer from repsonse
    group_3: Group = get_group_organizer_from_response(
        response=organizer_2_response, group=group_1
    )

    # assert group
    assert isinstance(group_3, Group)
    assert group_3.organizer_id == organizer_2_response["id"]
    assert group_3.organizer_name == organizer_2_response["name"]
    assert group_3.organizer_bio == organizer_2_response["bio"]

    # save group
    group_1.save()


def test_get_category_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_category_1")
    )

    # set category response
    category_1_response: dict = get_category_response(content=False)
    category_2_response: dict = get_category_response(content=True)

    # get category from repsonse
    group_2: Group = get_category_from_response(
        response=category_1_response, group=group_1
    )

    # assert group
    assert isinstance(group_2, Group)
    assert group_2.category_id == category_1_response["id"]
    assert group_2.category_name is None
    assert group_2.category_shortname is None
    assert group_2.category_sort_name is None

    # get category from repsonse
    group_3: Group = get_category_from_response(
        response=category_2_response, group=group_1
    )

    # assert group
    assert isinstance(group_3, Group)
    assert group_3.category_id == category_2_response["id"]
    assert group_3.category_name == category_2_response["name"]
    assert group_3.category_shortname == category_2_response["shortname"]
    assert group_3.category_sort_name == category_2_response["sort_name"]

    # save groups
    group_1.save()
    group_2.save()
    group_3.save()


def test_get_meta_category_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_meta_category_1")
    )

    # set meta_category response
    meta_category_1_response: dict = get_meta_category_response()

    # get meta_category from repsonse
    group_2: Event = get_meta_category_from_response(
        response=meta_category_1_response, group=group_1
    )

    # assert group
    assert isinstance(group_2, Group)
    assert group_2.meta_category_id == meta_category_1_response["id"]
    assert group_2.meta_category_name == meta_category_1_response["name"]
    assert group_2.meta_category_shortname == meta_category_1_response["shortname"]
    assert group_2.meta_category_sort_name == meta_category_1_response["sort_name"]

    # save group
    group_1.save()


def test_get_topic_from_response():
    # set group model
    group_1: Group = get_group_from_response(
        response=get_group_response(urlname="group_topic_1")
    )

    # set topic response
    topic_1_response: dict = get_topic_response(meetup_id=1)

    # get topic from repsonse
    topic_1: Topic = get_topic_from_response(response=topic_1_response)

    # assert topic
    assert isinstance(topic_1, Topic)
    assert topic_1.meetup_id == topic_1_response["id"]
    assert topic_1.lang == topic_1_response["lang"]
    assert topic_1.name == topic_1_response["name"]
    assert topic_1.urlkey == topic_1_response["urlkey"]

    # save group
    group_1.save()
