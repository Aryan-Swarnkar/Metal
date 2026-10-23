from app.search.analyser import analyze


def test_normalizes_unicode_and_case():
    assert analyze("ＡＢＣ CYCLONE") == ["abc", "cyclone"]


def test_splits_on_punctuation_and_underscores():
    assert analyze("hello_world, py-thon!") == [
        "hello",
        "world",
        "py",
        "thon",
    ]


def test_removes_stopwords():
    assert analyze("The cyclone is strong and the winds are powerful") == [
        "cyclone",
        "strong",
        "winds",
        "powerful",
    ]


def test_removes_empty_tokens():
    assert analyze("!!!cyclone,,,storm...") == ["cyclone", "storm"]


def test_empty_text_returns_empty_list():
    assert analyze("") == []


def test_only_stopwords_returns_empty_list():
    assert analyze("the is and are") == []