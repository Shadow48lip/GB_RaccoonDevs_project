from mainapp.models import Post, Comment, AuthorLike, PostLike, CommentLike


class DataMixin:
    @staticmethod
    def get_user_context(user, **kwargs):
        context = kwargs
        context['post_count'] = Post.objects.filter(author=user, is_published=True, is_blocked=False).count()
        context['comment_count'] = Comment.objects.filter(user=user, is_published=True).count()
        like_author = AuthorLike.objects.filter(author=user).count()
        like_posts = PostLike.objects.filter(post__author=user).count()
        like_comment = CommentLike.objects.filter(comment__user=user).count()
        context['like_receive_count'] = like_author + like_posts + like_comment

        # print('usermixin:\n', context)
        return context
