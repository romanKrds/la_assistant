from la_assistant.models import User, UserVocabulary, Vocabulary


def populate_users(db):
    users = [
        User(username='test', password='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
        User(username='other', password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79')
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()


def populate_user_vocabulary(db):
    user_vocabulary = [
        # the item beyond the limits that should not be included in list responses
        UserVocabulary(user_id=1, vocabulary_id=1, times_showed=5, times_reviewed=5),
        UserVocabulary(user_id=1, vocabulary_id=2, times_showed=1, times_reviewed=0)
    ]

    for item in user_vocabulary:
        db.session.add(item)

    db.session.commit()


def populate_vocabulary(db):
    vocabularies = [
        Vocabulary(id=1, language='de', sentence='Die Zeit wartet auf keinen Menschen.', word_1='Zeit', word_2='Person'),
        Vocabulary(id=2, language='de', sentence='Dieses Jahr habe ich einen neuen Weg zum Erfolg gefunden.', word_1='Jahr', word_2='Weg')
    ]

    for vocabulary in vocabularies:
        db.session.add(vocabulary)

    db.session.commit()