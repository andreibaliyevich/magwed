from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MinimumImageSizeValidator:
    """ Minimum Image Size Validator """
    message = _(
        'Error! Size of your image: %(width)d x %(height)d. '
        'Required minimum %(min_width)d x %(min_height)d.'
    )
    code = 'invalid_min_size'

    def __init__(self, min_width, min_height):
        self.min_width = min_width
        self.min_height = min_height

    def __call__(self, image):
        width, height = get_image_dimensions(image)

        if width < self.min_width or height < self.min_height:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'width': width,
                    'height': height,
                    'min_width': self.min_width,
                    'min_height': self.min_height,
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.min_width == other.min_width
            and self.min_height == other.min_height
            and self.message == other.message
            and self.code == other.code
        )
