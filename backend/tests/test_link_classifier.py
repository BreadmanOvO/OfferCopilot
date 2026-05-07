from app.tools.link_classifier import classify_url


def test_classify_job_board():
    assert classify_url("https://www.zhipin.com/job/123") == "job_board"
    assert classify_url("https://www.linkedin.com/jobs/view/123") == "job_board"


def test_classify_general_web():
    assert classify_url("https://anthropic.com") == "general_web"
    assert classify_url("https://news.ycombinator.com") == "general_web"
