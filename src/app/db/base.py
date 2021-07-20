# Import all the models, so that Base has them before being
# imported by Alembic

from app.db.base_class import Base # noqa
from app.models.banned_string import BannedString # noqa
from app.models.cash import Cash # noqa
from app.models.cash_series import CashSeries # noqa
from app.models.cash_writer import CashWriter # noqa
from app.models.comment import Comment # noqa
from app.models.coupon import Coupon # noqa
from app.models.coupon_series import CouponSeries # noqa
from app.models.genre import Genre # noqa
from app.models.language import Language # noqa
from app.models.novel import Novel, NovelDay # noqa
from app.models.novel_notice import NovelNotice # noqa
from app.models.novel_tag import NovelTag # noqa
from app.models.other_novel import OtherNovel # noqa
from app.models.paragraph import Paragraph # noqa
from app.models.recommend import Recommend, RecommendStatistic # noqa
from app.models.region import Region # noqa
from app.models.series import Series, SeriesStatistic, SeriesStatus # noqa
from app.models.tag import Tag # noqa
from app.models.temp_save import TempSave # noqa
from app.models.thumbnail import Thumbnail # noqa
from app.models.user import User, SnsAccount, BankingInfo # noqa
from app.models.user_genre import UserGenre # noqa
from app.models.user_novel import UserLike # noqa
from app.models.user_other_novel import UserOtherNovel # noqa
from app.models.user_paragraph import UserParagraph # noqa
from app.models.user_rating import UserRating # noqa
from app.models.user_read import UserRead # noqa
from app.models.user_recommend_like import UserRecommendLike # noqa
from app.models.user_tag import UserTag # noqa
from app.models.user_translate_like import UserTranslateLike # noqa
from app.models.writer import Writer, Commission # noqa
