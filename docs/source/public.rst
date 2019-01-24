==========
public API
==========

.. py:method:: get_blog_info(...)

   Retrieve blog info

   This method returns general information about the blog, such as the title, number of posts, and other high-level data.

   :param blog_identifier: The blog whose the info is requested
   :type blog_identifier: str
   :return: API response for get_blog_info
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_avatar(...)

   Retrieve a Blog Avatar

   Retrieve a Blog Avatar as 64x64 pixel image

   :param blog_identifier: The blog whose avatar is requested
   :type blog_identifier: str
   :return: API response for get_blog_avatar
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_avatar_with_size(...)

   Retrieve a Blog Avatar with a specific size

   :param blog_identifier: The blog whose avatar is requested
   :type blog_identifier: str
   :param size: The size of the avatar
   :type size: int
   :return: API response for get_blog_avatar_with_size
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_likes(...)

   Retrieve Blog's Likes

   Retrieve publicly exposed likes from a blog.

   Note: Only one of the optional parameters `offset`, `before` or `after` can be used.

   Note: When requesting posts with an offset above 1000, switch to `before` or `after`.

   :param blog_identifier: The blog whose likes are requested
   :type blog_identifier: str
   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Liked post number to start at
   :type offset: int or None
   :param before: Retrieve posts liked before the specified timestamp
   :type before: int or None
   :param after: Retrieve posts liked after the specified timestamp
   :type after: int or None
   :return: API response for get_blog_likes
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_following(...)

   Retrieve Blog's following

   This method can be used to retrieve the publicly exposed list of blogs that a blog follows, in order from most recently-followed to first.

   :param blog_identifier: The blog whose following is requested
   :type blog_identifier: str
   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Followed blog index to start at
   :type offset: int or None
   :return: API response for get_blog_following
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_followers(...)

   Retrieve a Blog's Followers

   :param blog_identifier: The blog whose followers are requested
   :type blog_identifier: str
   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Result to start at
   :type offset: int or None
   :return: API response for get_blog_followers
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_posts(...)

   Retrieve Published Posts

   :param blog_identifier: The blog whose posts are requested
   :type blog_identifier: str
   :param id: A specific post ID. Returns the single post specified or (if not found) a 404 error.
   :type id: int or None
   :param tag: Limits the response to posts with the specified tag
   :type tag: str or None
   :param limit: The number of posts to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Post number to start at
   :type offset: int or None
   :param reblog_info: Indicates whether to return reblog information. Returns the various `reblogged_` fields.
   :type reblog_info: bool or None
   :param notes_info: Indicates whether to return notes information (specify true or false). Returns note count and note metadata.
   :type notes_info: bool or None
   :param filter: Specifies the post format to return, other than HTML: `text` – Plain text, no HTML; `raw` – As entered by the user (no post-processing); if the user writes in Markdown, the Markdown will be returned rather than HTML
   :type filter: str or None
   :param before: Returns posts published earlier than a specified Unix timestamp, in seconds.
   :type before: int or None
   :return: API response for get_blog_posts
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_posts_with_type(...)

   Retrieve Published Posts of a specific type

   :param blog_identifier: The blog whose posts are requested
   :type blog_identifier: str
   :param type: Type of the post
   :type type: str
   :param id: A specific post ID. Returns the single post specified or (if not found) a 404 error.
   :type id: int or None
   :param tag: Limits the response to posts with the specified tag
   :type tag: str or None
   :param limit: The number of posts to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Post number to start at
   :type offset: int or None
   :param reblog_info: Indicates whether to return reblog information. Returns the various `reblogged_` fields.
   :type reblog_info: bool or None
   :param notes_info: Indicates whether to return notes information (specify true or false). Returns note count and note metadata.
   :type notes_info: bool or None
   :param filter: Specifies the post format to return, other than HTML: `text` – Plain text, no HTML; `raw` – As entered by the user (no post-processing); if the user writes in Markdown, the Markdown will be returned rather than HTML
   :type filter: str or None
   :param before: Returns posts published earlier than a specified Unix timestamp, in seconds.
   :type before: int or None
   :return: API response for get_blog_posts_with_type
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_queue(...)

   Retrieve Queued Posts

   :param blog_identifier: The blog whose queue is requested
   :type blog_identifier: str
   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Post number to start at
   :type offset: int or None
   :param filter: Specifies the post format to return, other than HTML: text – Plain text, no HTML; raw – As entered by the user (no post-processing); if the user writes in Markdown, the Markdown will be returned rather than HTML
   :type filter: str or None
   :return: API response for get_blog_queue
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_drafts(...)

   Retrieve Draft Posts

   :param blog_identifier: The blog whose drafts are requested
   :type blog_identifier: str
   :param before_id: Return posts that have appeared before this ID; Use this parameter to page through the results: first get a set of posts, and then get posts since the last ID of the previous set.
   :type before_id: int or None
   :param filter: Specifies the post format to return, other than HTML: text – Plain text, no HTML; raw – As entered by the user (no post-processing); if the user writes in Markdown, the Markdown will be returned rather than HTML
   :type filter: str or None
   :return: API response for get_blog_drafts
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_blog_submissions(...)

   Retrieve Submission Posts

   :param blog_identifier: The blog whose submissions are requested
   :type blog_identifier: str
   :param offset: Post number to start at
   :type offset: int or None
   :param filter: Specifies the post format to return, other than HTML: text – Plain text, no HTML; raw – As entered by the user (no post-processing); if the user writes in Markdown, the Markdown will be returned rather than HTML
   :type filter: str or None
   :return: API response for get_blog_submissions
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: create_post(...)

   Create a Post (Neue Post Format)

   This methods allows you to create posts (and reblogs) using the Neue Post Format.

   :param blog_identifier: The blog to post to
   :type blog_identifier: str
   :param content: An array of NPF content blocks to be used to make the post.
   :type content: list
   :param layout: An array of NPF layout objects to be used to lay out the post content.
   :type layout: list or None
   :param state: The initial state of the new post, such as `"published"` or `"queued"`. Posts can be in the following "states": `"published"` means the post should be publicly published immediately, `"queue"` means the post should be added to the end of the blog's post queue, `"draft"` means the post should be saved as a draft, `"private"` means the post should be privately published immediately. If omitted, the post will get the state `"published"`
   :type state: str or None
   :param publish_on: The exact date and time (ISO 8601 format) to publish the post, if desired. This parameter will be ignored unless the state parameter is `"queue"`.
   :type publish_on: str or None
   :param tags: A comma-separated list of tags to associate with the post.
   :type tags: str or None
   :param source_url: A source attribution for the post content.
   :type source_url: str or None
   :param send_to_twitter: Whether or not to share this via any connected Twitter account on post publish. Defaults to the blog's global setting.
   :type send_to_twitter: bool or None
   :param send_to_facebook: Whether or not to share this via any connected Facebook account on post publish. Defaults to the blog's global setting.
   :type send_to_facebook: bool or None
   :return: API response for create_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: reblog_post(...)

   Reblog a post (Neue Post Format)

   :param blog_identifier: The blog to reblog to
   :type blog_identifier: str
   :param parent_tumblelog_uuid: The unique public identifier of the Tumblelog that's being reblogged from.
   :type parent_tumblelog_uuid: str
   :param parent_post_id: The unique public post ID being reblogged.
   :type parent_post_id: int
   :param reblog_key: The unique per-post hash validating that this is a genuine reblog action.
   :type reblog_key: str
   :param content: An array of NPF content blocks to be used to make the post.
   :type content: list
   :param layout: An array of NPF layout objects to be used to lay out the post content.
   :type layout: list or None
   :param state: The initial state of the new post, such as `"published"` or `"queued"`. Posts can be in the following "states": `"published"` means the post should be publicly published immediately, `"queue"` means the post should be added to the end of the blog's post queue, `"draft"` means the post should be saved as a draft, `"private"` means the post should be privately published immediately. If omitted, the post will get the state `"published"`
   :type state: str or None
   :param publish_on: The exact date and time (ISO 8601 format) to publish the post, if desired. This parameter will be ignored unless the state parameter is `"queue"`.
   :type publish_on: str or None
   :param tags: A comma-separated list of tags to associate with the post.
   :type tags: str or None
   :param source_url: A source attribution for the post content.
   :type source_url: str or None
   :param send_to_twitter: Whether or not to share this via any connected Twitter account on post publish. Defaults to the blog's global setting.
   :type send_to_twitter: bool or None
   :param send_to_facebook: Whether or not to share this via any connected Facebook account on post publish. Defaults to the blog's global setting.
   :type send_to_facebook: bool or None
   :param hide_trail: Whether or not to hide the reblog trail with this new post. Defaults to false.
   :type hide_trail: bool or None
   :return: API response for reblog_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: fetch_post(...)

   Fetch an individual post

   :param blog_identifier: The blog whose post is requested
   :type blog_identifier: str
   :param post_id: The ID of the post
   :type post_id: int
   :return: API response for fetch_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: edit_post(...)

   Editing a Post (in NPF format)

   This route allows you to edit posts using the Neue Post Format. Note that you can only edit posts in NPF if they were originally created in NPF, or are legacy text posts.

   :param blog_identifier: The blog whose post is requested for editing
   :type blog_identifier: str
   :param post_id: The ID of the post to edit
   :type post_id: int
   :param content: An array of NPF content blocks to be used to make the post.
   :type content: list
   :param layout: An array of NPF layout objects to be used to lay out the post content.
   :type layout: list or None
   :param state: The initial state of the new post, such as `"published"` or `"queued"`. Posts can be in the following "states": `"published"` means the post should be publicly published immediately, `"queue"` means the post should be added to the end of the blog's post queue, `"draft"` means the post should be saved as a draft, `"private"` means the post should be privately published immediately. If omitted, the post will get the state `"published"`
   :type state: str or None
   :param publish_on: The exact date and time (ISO 8601 format) to publish the post, if desired. This parameter will be ignored unless the state parameter is `"queue"`.
   :type publish_on: str or None
   :param tags: A comma-separated list of tags to associate with the post.
   :type tags: str or None
   :param source_url: A source attribution for the post content.
   :type source_url: str or None
   :param send_to_twitter: Whether or not to share this via any connected Twitter account on post publish. Defaults to the blog's global setting.
   :type send_to_twitter: bool or None
   :param send_to_facebook: Whether or not to share this via any connected Facebook account on post publish. Defaults to the blog's global setting.
   :type send_to_facebook: bool or None
   :return: API response for edit_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: edit_reblog(...)

   Editing a Reblogged Post (in NPF format)

   This route allows you to edit reblogs using the Neue Post Format. Note that you can only edit posts in NPF if they were originally created in NPF, or are legacy text posts.

   :param blog_identifier: The blog whose post is requested for editing
   :type blog_identifier: str
   :param post_id: The ID of the post to edit
   :type post_id: int
   :param parent_tumblelog_uuid: The unique public identifier of the Tumblelog that's being reblogged from.
   :type parent_tumblelog_uuid: str
   :param parent_post_id: The unique public post ID being reblogged.
   :type parent_post_id: int
   :param reblog_key: The unique per-post hash validating that this is a genuine reblog action.
   :type reblog_key: str
   :param content: An array of NPF content blocks to be used to make the post.
   :type content: list
   :param layout: An array of NPF layout objects to be used to lay out the post content.
   :type layout: list or None
   :param state: The initial state of the new post, such as `"published"` or `"queued"`. Posts can be in the following "states": `"published"` means the post should be publicly published immediately, `"queue"` means the post should be added to the end of the blog's post queue, `"draft"` means the post should be saved as a draft, `"private"` means the post should be privately published immediately. If omitted, the post will get the state `"published"`
   :type state: str or None
   :param publish_on: The exact date and time (ISO 8601 format) to publish the post, if desired. This parameter will be ignored unless the state parameter is `"queue"`.
   :type publish_on: str or None
   :param tags: A comma-separated list of tags to associate with the post.
   :type tags: str or None
   :param source_url: A source attribution for the post content.
   :type source_url: str or None
   :param send_to_twitter: Whether or not to share this via any connected Twitter account on post publish. Defaults to the blog's global setting.
   :type send_to_twitter: bool or None
   :param send_to_facebook: Whether or not to share this via any connected Facebook account on post publish. Defaults to the blog's global setting.
   :type send_to_facebook: bool or None
   :param hide_trail: Whether or not to hide the reblog trail with this new post. Defaults to false.
   :type hide_trail: bool or None
   :return: API response for edit_reblog
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: delete_post(...)

   Delete a Post

   :param blog_identifier: The blog whose post has to be deleted
   :type blog_identifier: str
   :param id: The ID of the post to delete
   :type id: int
   :return: API response for delete_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_user_info(...)

   Get a User's Information

   Use this method to retrieve the user's account information that matches the OAuth credentials submitted with the request.

   :return: API response for get_user_info
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_user_dashboard(...)

   Retrieve a User's Dashboard

   Use this method to retrieve the dashboard that matches the OAuth credentials submitted with the request.

   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Post number to start at
   :type offset: int or None
   :param type: The type of post to return. Specify one of the following: text, photo, quote, link, chat, audio, video, answer
   :type type: str or None
   :param since_id: Return posts that have appeared after this ID; Use this parameter to page through the results: first get a set of posts, and then get posts since the last ID of the previous set.
   :type since_id: int or None
   :param reblog_info: Indicates whether to return reblog information (specify true or false). Returns the various `reblogged_` fields.
   :type reblog_info: bool or None
   :param notes_info: Indicates whether to return notes information (specify true or false). Returns note count and note metadata.
   :type notes_info: bool or None
   :return: API response for get_user_dashboard
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_user_likes(...)

   Retrieve a User's Likes

   Use this method to retrieve the liked posts that match the OAuth credentials submitted with the request. You can only provide either before, after, or offset. If you provide more than one of these options together you will get an error. You can still use limit with any of those three options to limit your result set. When using the offset parameter the maximum limit on the offset is 1000. If you would like to get more results than that use either before or after.

   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Liked post number to start at
   :type offset: int or None
   :param before: Retrieve posts liked before the specified timestamp
   :type before: int or None
   :param after: Retrieve posts liked after the specified timestamp
   :type after: int or None
   :return: API response for get_user_likes
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: get_user_following(...)

   Retrieve the Blogs a User Is Following

   Use this method to retrieve the blogs followed by the user whose OAuth credentials are submitted with the request.

   :param limit: The number of results to return: 1–20, inclusive
   :type limit: int or None
   :param offset: Result number to start at
   :type offset: int or None
   :return: API response for get_user_following
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: follow_blog(...)

   Follow a blog

   :param url: The URL of the blog to follow
   :type url: str
   :return: API response for follow_blog
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: unfollow_blog(...)

   Unfollow a blog

   :param url: The URL of the blog to unfollow
   :type url: str
   :return: API response for unfollow_blog
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: like_post(...)

   Like a Post

   :param id: The ID of the post to like
   :type id: int
   :param reblog_key: The reblog key for the post id
   :type reblog_key: str
   :return: API response for like_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

.. py:method:: unlike_post(...)

   Unlike a Post

   :param id: The ID of the post to unlike
   :type id: int
   :param reblog_key: The reblog key for the post id
   :type reblog_key: str
   :return: API response for unlike_post
   :rtype: `aiohttp.ClientResponse`
   :raises SyntaxError: if required parameter is missing
   :raises ValueError: if supplied parameter fails validation

