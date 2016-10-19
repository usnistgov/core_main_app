from django_mongoengine import fields, Document


class XslTransformation(Document):
    name = fields.StringField(blank=False, unique=True)
    filename = fields.StringField(blank=False)
    content = fields.StringField(blank=False)

    @staticmethod
    def get_all():
        return XslTransformation.objects.all()

    @staticmethod
    def get_by_name(xslt_name):
        return XslTransformation.objects.get(name=xslt_name)


