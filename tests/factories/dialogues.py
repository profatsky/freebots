import factory
from faker import Faker

from src.dialogues.schemas import DialogueCreateSchema, TriggerCreateSchema, TriggerUpdateSchema
from src.enums import TriggerEventType

fake = Faker()


class TriggerCreateSchemaFactory(factory.Factory):
    class Meta:
        model = TriggerCreateSchema

    event_type = factory.Iterator([kb_type.value for kb_type in TriggerEventType])
    value = factory.LazyFunction(lambda: fake.sentence(nb_words=5))


class DialogueCreateSchemaFactory(factory.Factory):
    class Meta:
        model = DialogueCreateSchema

    trigger = TriggerCreateSchemaFactory()


class TriggerUpdateSchemaFactory(TriggerCreateSchemaFactory):
    pass
