
"""
"""

import uuid

import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm

from sqlalchemy.ext.associationproxy import association_proxy


def init(Base, PersonModel=None, PersonModel_id_attr="_id"):
    """
    """

    global Image
    global ImagePersonTag

    class Image(Base):
        """
        """

        __tablename__ = "images"

        _id = sqlalchemy.Column('id', sqlalchemy.types.Integer,
                                primary_key=True)
        _uuid = sqlalchemy.Column('uuid', sqlalchemy.types.LargeBinary,
                                  index=True,
                                  default=lambda ctx: uuid.uuid4().bytes)

        size_x = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)
        size_y = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)

        _word_tags = sqlalchemy.orm.relationship(
                        lambda: WordTag,
                        primaryjoin=lambda:Image._id==ImageWordTag.image_id,
                        secondary="images_word_tags",
                        secondaryjoin=
                            lambda: WordTag._id==ImageWordTag.word_tag_id,
                        backref="images_tagged_with",
                        collection_class=set)

        word_tags = association_proxy('_word_tags', 'value')
        description = sqlalchemy.Column(sqlalchemy.types.String(1024),
                                        index=True,
                                        nullable=True)

        if PersonModel:
            person_tags = association_proxy('_image_person_tags', 'person')

        # TODO: Not Hybrid Property as I do not know how to convert a UUID
        # to binary in SQL.
        @property
        def uuid(self):
            return uuid.UUID(bytes=self._uuid)

        @uuid.setter
        def uuid(self, value):
            self._uuid = value

    if PersonModel:
        class ImagePersonTag(Base):
            """
            """

            __tablename__ = "images_person_tags"
            __table_args__ = (sqlalchemy.UniqueConstraint('image_id',
                                                          'person_id'),)

            _id = sqlalchemy.Column('id', sqlalchemy.types.Integer,
                                    primary_key=True)
            image_id = sqlalchemy.Column(sqlalchemy.types.Integer,
                            sqlalchemy.ForeignKey(Image._id))
            person_id = sqlalchemy.Column(sqlalchemy.types.Integer,
                            sqlalchemy.ForeignKey(
                                getattr(PersonModel, PersonModel_id_attr)))

            pos_x = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)
            pos_y = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)
            width = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)
            height = sqlalchemy.Column(sqlalchemy.types.Integer, default=0)

            image = sqlalchemy.orm.relationship(Image, backref=
                        sqlalchemy.orm.backref("_image_person_tags",
                                               cascade="all, delete-orphan",
                                               collection_class=set))
            person = sqlalchemy.orm.relationship(PersonModel, backref=
                        sqlalchemy.orm.backref("tagged_images_meta",
                                               cascade="all, delete-orphan",
                                               collection_class=set))

            def __init__(self, person, **kwa):
                Base.__init__(self, **kwa)
                self.person = person

        PersonModel.tagged_images = association_proxy('tagged_images_meta',
                                                      'image')

    class WordTag(Base):
        """
        """

        __tablename__ = "word_tags"

        def __init__(self, value):
            self.value = value

        _id = sqlalchemy.Column('id', sqlalchemy.types.Integer,
                                primary_key=True)
        value = sqlalchemy.Column(sqlalchemy.types.String, index=True,
                                  unique=True)

    class ImageWordTag(Base):
        """
        """

        __tablename__ = "images_word_tags"
        __table_args__ = (sqlalchemy.UniqueConstraint('image_id', 'word_tag_id'),)

        _id = sqlalchemy.Column('id', sqlalchemy.types.Integer,
                                primary_key=True)
        image_id = sqlalchemy.Column(sqlalchemy.types.Integer,
                        sqlalchemy.ForeignKey(Image._id))
        word_tag_id = sqlalchemy.Column(sqlalchemy.types.Integer,
                        sqlalchemy.ForeignKey(WordTag._id))