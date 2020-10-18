from content_parser import html


def test_basic():
    assert html('"hello"') == "hello"


def test_boldface():
    assert html('(bf "hello")') == "<b>hello</b>"


def test_italics():
    assert html('(it "hello")') == "<i>hello</i>"


def test_concat():
    assert html('($ "abc" "def" "ghi")') == "abcdefghi"
    assert html('($ "abc" (bf "def") "ghi")') == "abc<b>def</b>ghi"


def test_heading():
    assert html('((h 2) "hello" " " "world")') == "<h2>hello world</h2>"


def test_style_inline():
    assert html('((style "color: red") "text")') == '<span style="color: red">text</span>'


def test_list_unordered():
    assert (
        html('(list-unordered "hello" ($ "a" "b") "c")')
        == '<ul><li>hello</li><li>ab</li><li>c</li></ul>'
    )


def test_list_ordered():
    assert (
        html('(list-ordered "hello" ($ "a" "b") "c")')
        == '<ol><li>hello</li><li>ab</li><li>c</li></ol>'
    )