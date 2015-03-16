

import os
import sys
import uuid
import unittest 

import sqlalchemy
import sqlalchemy.ext.declarative

import galcore


from galcore.persist import model


def pkg_get_dir(directory):
    pkg_dir = os.path.dirname(galcore.__file__)
    return os.path.join(pkg_dir, directory)


class TestSQLAModel(unittest.TestCase):
    """
    """


    def _init_models(self):
        self.base = sqlalchemy.ext.declarative.declarative_base()
        model.init(self.base)

    def setUp(self):
        # Setup Engine and Session
        self._data_path = pkg_get_dir(os.path.join('tests', 'data'))
        self._db_filepath = os.path.join(self._data_path,
                                         str(uuid.uuid4())+'.db')
        self.engine = engine = sqlalchemy.create_engine('sqlite:///%s'
                                                        % self._db_filepath)
        self.session = sqlalchemy.orm.scoped_session(
                          sqlalchemy.orm.sessionmaker())
        self.session.configure(bind=engine)

        # Set up Base and Models
        self._init_models()

        self.base.metadata.bind = engine
        self.base.metadata.create_all(engine)


    def tearDown(self):
        self.session.close()
        self.engine.dispose()

        try:
            os.unlink(self._db_filepath)
        except FileNotFoundError:
            print("Looks like nothing happened.")


class TestPersistModel(TestSQLAModel):
    """
    """

    def test_image(self):
        image = model.Image()
        self.session.add(image)
        self.session.commit()

        self.assertIsInstance(image._id, int)
        self.assertIsInstance(image._uuid, bytes)
        self.assertIsInstance(image.uuid, uuid.UUID)

        test_image = self.session.query(model.Image).get(image._id)
        self.assertIs(image, test_image)

        for tag in image.word_tags:
            self.assertIs(tag, model.Tag)


class TestWordTagsModel(TestSQLAModel):
    """
    """

    def test_image_word_tags(self):
        image = model.Image(word_tags=['foo', 'bar', 'baz'])
        self.session.add(image)
        self.session.commit()

        test_image = self.session.query(model.Image).get(image._id)
        self.assertEqual(image.word_tags, {'foo', 'bar', 'baz'})

        test_image.word_tags.add('foo')
        test_image.word_tags.add('bar')
        test_image.word_tags.add('baz')
        test_image.word_tags.add('boo')
        self.session.commit()

        self.assertEqual(image.word_tags, {'foo', 'bar', 'baz', 'boo'})

        test_image.word_tags.remove('foo')
        test_image.word_tags.remove('bar')
        self.session.commit()

        self.assertEqual(image.word_tags, {'baz', 'boo'})


class TestPersonTagsModel(TestSQLAModel):
    """
    """

    def _init_models(self):
        self.base = sqlalchemy.ext.declarative.declarative_base()

        class Person(self.base):
            __tablename__ = "person"

            _id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
            name = sqlalchemy.Column(sqlalchemy.types.String(16))

        def __init__(self, *args):
            print(args)

        self.Person = Person

        model.init(self.base, PersonModel=Person)


    def test_image_person_tags(self):
        self.person1 = self.Person(name="foo")
        self.person2 = self.Person(name="bar")
        self.person3 = self.Person(name="baz")
        self.session.add(self.person1)
        self.session.add(self.person2)
        self.session.add(self.person3)
        self.session.commit()

        image = model.Image(person_tags=
                                {self.person1, self.person2, self.person3})

        self.session.add(image)
        self.session.commit()

        test_image = self.session.query(model.Image).get(image._id)
        self.assertEqual(test_image.person_tags,
                            {self.person1, self.person2, self.person3})

        self.assertIn(test_image, self.person1.tagged_images)
        self.assertIn(test_image, self.person2.tagged_images)
        self.assertIn(test_image, self.person3.tagged_images)

        for it in self.person1.tagged_images_meta:
            print(it.image)
            print(it.pos_x)

        assert False