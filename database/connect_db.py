import time

import boto3, json, datetime
from connect_config import conf
from boto3.dynamodb.conditions import Key, Attr

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, TIMESTAMP, update
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class BotBoard(Base):
    __tablename__ = "botboard"
    idx = Column(Integer, primary_key=True)
    article_id = Column(Text)
    state = Column(Text)
    type = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class RssMedia(Base):
    __tablename__ = "rssmedia"
    no = Column(Integer, primary_key=True)
    idx = Column(Text)
    name = Column(Text)
    rss_url = Column(Text)

class RssFeed(Base):
    __tablename__ = "rssfeed"
    no = Column(Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text)
    updated_at = Column(Text)
    media_idx = Column(Text)

rdb = conf["postgre"]
engine = create_engine(
    f"postgresql://{rdb['username']}:{rdb['password']}@{rdb['host']}:{rdb['port']}/{rdb['dbname']}?client_encoding=utf8")


def get_rdb_session():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def get_dynamo_resource():
    dynamo = conf["dynamo"]
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=dynamo["region"],
        aws_access_key_id=dynamo["access_key"],
        aws_secret_access_key=dynamo["secret_key"])
    return dynamodb
def change_record_state(state, record, session):
    record.state = state
    record.updated_at = datetime.datetime.now()
    session.add(record)
    session.commit()

def get_rss_media_all():
    session = get_rdb_session()
    records = session.query(RssMedia).all()
    return records

def delete_rss_feed_all():
    session = get_rdb_session()
    session.query(RssFeed).delete()
    session.commit()

def delete_rss_feed(media_idx):
    session = get_rdb_session()
    session.query(RssFeed).filter(RssFeed.media_idx == media_idx).delete()
    session.commit()
def add_rss_feed(record):
    session = get_rdb_session()
    session.add(record)
    session.commit()

def repeat(session, get_chat_message, gemini_action, max_token):
    records = session.query(BotBoard).limit(10).all()
    docs = get_dynamo_resource().Table("article")
    for record in records:
        if record.state != 'wait':
            continue

        change_record_state("work", record, session)

        query = {
            "KeyConditionExpression": Key("author").eq("kkennib") & Key("articleId").eq(record.article_id)
        }
        query_res = docs.query(**query)
        if len(query_res["Items"]) == 0:
            continue

        doc = query_res["Items"][0]
        contents = f"{doc['title']}\n"
        inventory = json.loads(doc["inventory"])
        for item in inventory:
            if item["type"] == "text":
                contents += f"{item['contents']}\n"

        get_message_func = None
        if record.type == "chat_gpt":
            get_message_func = get_chat_message
        elif record.type == "gemini":
            get_message_func = gemini_action

        feedback_new = []
        if get_message_func is not None:
            try:
                feedback_new = get_message_func(contents[0:max_token])
            except Exception as e:
                print(e)
                feedback_new = None

        print(feedback_new)

        feedbacks = [] if doc.get("feedback") is None else json.loads(doc["feedback"])

        index, total_count = 0, len(feedbacks)
        while index < total_count:
            feedback = feedbacks[index]
            if record.type == feedback["bot"]:
                del feedbacks[index]
                index, total_count = 0, len(feedbacks)
                continue
            index = index + 1

        print(feedbacks)
        print("=== Feedback ===")
        if feedback_new is not None:
            feedbacks.append(feedback_new)
            dump_res = json.dumps(feedbacks, ensure_ascii=False).replace('\"', '"')
            print(dump_res)
            doc["feedback"] = dump_res
            docs.put_item(Item=doc)

        change_record_state("finish", record, session)
        time.sleep(3)


def monit(chat_gpt_action, gemini_action, max_token):
    session = get_rdb_session()
    repeat(session, chat_gpt_action, gemini_action, max_token)
    session.close()

# docs = get_dynamo_resource().Table("article")
# docs.update_item(
#     Key={"articleId": "36d751db-5f51-4323-ad79-819691b8c100"},
#     AttributeUpdates={
#         'status': 'complete',
#     },
#
# )


# table.put_item(Item=data)
