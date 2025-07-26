import factory
from faker import Faker

from src.apps.enums import KeyboardType
from src.apps.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema

fake = Faker()


class ProjectCreateSchemaFactory(factory.Factory):
    class Meta:
        model = ProjectCreateSchema

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    start_message = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    start_keyboard_type = factory.Iterator([kb_type.value for kb_type in KeyboardType])


class ProjectUpdateSchemaFactory(ProjectCreateSchemaFactory):
    class Meta:
        model = ProjectUpdateSchema
