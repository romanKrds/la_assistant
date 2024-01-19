INSERT INTO user (username, password, token, thread_id)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'thread_1'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'thread_1');

INSERT INTO mistake (user_id, language, origin, explanation, corrected_origin, times_showed, times_reviewed, times_reviewed_correctly)
VALUES
  (1, 'en', 'I live on Earth', 'There is no "the" article before the Earth word', 'I live on the Earth', 0, 0, 0),
  (1, 'en', 'I live on Mars', 'There is no "the" article before the Mars word', 'I live on the Mars', 5, 3, 1);
