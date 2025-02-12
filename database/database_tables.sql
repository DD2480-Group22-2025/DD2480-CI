CREATE TABLE build_log(
    commit_hash     TEXT UNIQUE   NOT NULL,
    build_date      TEXT          NOT NULL,
    linter_result   TEXT          NOT NULL,
    test_result     TEXT          NOT NULL
);
