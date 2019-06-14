class BaseHelper:
    explanation = ''

    @classmethod
    def function(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_dict(cls):
        return dict(function=cls.function,
                    explanation=cls.explanation)