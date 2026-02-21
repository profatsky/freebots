import factory
from faker import Faker

from src.api.v1.dialogues.schemas import DialogueCreateSchema, DialogueTriggerCreateSchema
from src.apps.enums import TriggerEventType

fake = Faker()


class TriggerCreateSchemaFactory(factory.Factory):
    class Meta:
        model = DialogueTriggerCreateSchema

    event_type = factory.Iterator([kb_type.value for kb_type in TriggerEventType])
    value = factory.LazyFunction(lambda: fake.sentence(nb_words=5))


class DialogueCreateSchemaFactory(factory.Factory):
    class Meta:
        model = DialogueCreateSchema

    trigger = TriggerCreateSchemaFactory()


class TriggerUpdateSchemaFactory(TriggerCreateSchemaFactory):
    pass
