# encoding=utf-8


# TODO: add more checks for validating blog identifiers
def validate_blog_identifier(blog_identifier: str):
    if blog_identifier.endswith('.tumblr.com'):
        end_pos = blog_identifier.rfind('.tumblr.com')
        if len(blog_identifier[:end_pos]) > 32:
            # Invalid blog name length
            return False
    return True
