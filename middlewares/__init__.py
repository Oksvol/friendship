from .throttling import ThrottlingMiddleware
# from .big_brother import BigBrother


from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(BigBrother())
