#coding: utf-8

import re
from cStringIO import StringIO

try:
    from PIL import Image, ImageFile, ImageDraw
except ImportError:
    import Image, ImageFile, ImageDraw

from . import settings



bgpos_pat = re.compile(r'^(?P<value>\d+)(?P<unit>%|px)$')
geometry_pat = re.compile(r'^(?P<x>\d+)?(?:x(?P<y>\d+))?$')


class ThumbnailError(Exception):
    pass

class ThumbnailParseError(ThumbnailError):
    pass

def toint(number):
    """
    Helper to return rounded int for a float or just the int it self.
    """
    if isinstance(number, float):
        number = round(number, 0)
    return int(number)


def parse_geometry(geometry, ratio=None):
    """
    Parses a geometry string syntax and returns a (width, height) tuple
    """
    m = geometry_pat.match(geometry)
    def syntax_error():
        return ThumbnailParseError('Geometry does not have the correct '
                'syntax: %s' % geometry)
    if not m:
        raise syntax_error()
    x = m.group('x')
    y = m.group('y')
    if x is None and y is None:
        raise syntax_error()
    if x is not None:
        x = int(x)
    if y is not None:
        y = int(y)
    # calculate x or y proportionally if not set but we need the image ratio
    # for this
    if ratio is not None:
        ratio = float(ratio)
        if x is None:
            x = toint(y * ratio)
        elif y is None:
            y = toint(x / ratio)
    return x, y


def parse_crop(crop, xy_image, xy_window):
    """
    Returns x, y offsets for cropping. The window area should fit inside
    image but it works out anyway
    """
    def syntax_error():
        raise ThumbnailParseError('Unrecognized crop option: %s' % crop)
    x_alias_percent = {
        'left': '0%',
        'center': '50%',
        'right': '100%',
    }
    y_alias_percent = {
        'top': '0%',
        'center': '50%',
        'bottom': '100%',
    }
    
    
    
    xy_crop = crop.split(' ')
    
    if len(xy_crop) == 1:
        
        if crop in x_alias_percent:
            x_crop = x_alias_percent[crop]
            y_crop = '50%'
        elif crop in y_alias_percent:
            y_crop = y_alias_percent[crop]
            x_crop = '50%'
        else:
            x_crop, y_crop = crop, crop
    elif len(xy_crop) == 2:
        x_crop, y_crop = xy_crop
        x_crop = x_alias_percent.get(x_crop, x_crop)
        y_crop = y_alias_percent.get(y_crop, y_crop)
    else:
        syntax_error()

    def get_offset(crop, epsilon):
        m = bgpos_pat.match(crop)
        if not m:
            syntax_error()
        value = int(m.group('value')) # we only take ints in the regexp
        unit = m.group('unit')
        if unit == '%':
            value = epsilon * value / 100.0
        # return ∈ [0, epsilon]
        return int(max(0, min(value, epsilon)))

    offset_x = get_offset(x_crop, xy_image[0] - xy_window[0])
    offset_y = get_offset(y_crop, xy_image[1] - xy_window[1])
    return offset_x, offset_y


class EngineBase(object):
    """
    ABC for Thumbnail engines, methods are static
    """
    def create(self, image, geometry, options):
        """
        Processing conductor, returns the thumbnail as an image engine instance
        """
        image = self.orientation(image, geometry, options)
        image = self.colorspace(image, geometry, options)
        image = self.scale(image, geometry, options)
        image = self.crop(image, geometry, options)
        return image

    def orientation(self, image, geometry, options):
        """
        Wrapper for ``_orientation``
        """
        if options.get('orientation', settings.THUMBNAIL_ORIENTATION):
            return self._orientation(image)
        return image

    def colorspace(self, image, geometry, options):
        """
        Wrapper for ``_colorspace``
        """
        colorspace = options['colorspace']
        return self._colorspace(image, colorspace)

    def scale(self, image, geometry, options):
        """
        Wrapper for ``_scale``
        """
        crop = options['crop']
        upscale = options['upscale']
        x_image, y_image = map(float, self.get_image_size(image))
        # calculate scaling factor
        factors = (geometry[0] / x_image, geometry[1] / y_image)
        factor = max(factors) if crop else min(factors)
        if factor < 1 or upscale:
            width = toint(x_image * factor)
            height = toint(y_image * factor)
            image = self._scale(image, width, height)
        return image

    def crop(self, image, geometry, options):
        """
        Wrapper for ``_crop``
        """
        crop = options['crop']
        if not crop or crop == 'noop':
            return image
        x_image, y_image = self.get_image_size(image)
        if geometry[0] > x_image or geometry[1] > y_image:
            return image
        x_offset, y_offset = parse_crop(crop, (x_image, y_image), geometry)
        return self._crop(image, geometry[0], geometry[1], x_offset, y_offset)

    def write(self, image, options):
        """
        Wrapper for ``_write``
        """
        format_ = options['format']
        quality = options['quality']
        # additional non-default-value options:
        progressive = options.get('progressive', settings.THUMBNAIL_PROGRESSIVE)
        raw_data = self._get_raw_data(image, format_, quality,
            progressive=progressive
            )
        thumbnail.write(raw_data)

    def get_image_ratio(self, image):
        """
        Calculates the image ratio
        """
        x, y = self.get_image_size(image)
        return float(x) / y

class PILEngine(EngineBase):
    def get_image(self, source):
        return source

    def get_image_size(self, image):
        return image.size

    def is_valid_image(self, raw_data):
        buf = StringIO(raw_data)
        try:
            trial_image = Image.open(buf)
            trial_image.verify()
        except Exception:
            return False
        return True

    def _orientation(self, image):
        try:
            exif = image._getexif()
        except AttributeError:
            exif = None
        if exif:
            orientation = exif.get(0x0112)
            if orientation == 2:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                image = image.rotate(180)
            elif orientation == 4:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                image = image.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                image = image.rotate(-90)
            elif orientation == 7:
                image = image.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                image = image.rotate(90)
        return image

    def _colorspace(self, image, colorspace):
        if colorspace == 'RGB':
            if image.mode == 'RGBA':
                return image # RGBA is just RGB + Alpha
            if image.mode == 'P' and 'transparency' in image.info:
                return image.convert('RGBA')
            return image.convert('RGB')
        if colorspace == 'GRAY':
            return image.convert('L')
        return image

    def _scale(self, image, width, height):
        return image.resize((width, height), resample=Image.ANTIALIAS)

    def _crop(self, image, width, height, x_offset, y_offset):
        return image.crop((x_offset, y_offset,
                           width + x_offset, height + y_offset))

    def _get_raw_data(self, image, format_, quality, progressive=False):
        ImageFile.MAXBLOCK = 1024 * 1024
        buf = StringIO()
        params = {
            'format': format_,
            'quality': quality,
            'optimize': 1,
        }
        if format_ == 'JPEG' and progressive:
            params['progressive'] = True
        try:
            image.save(buf, **params)
        except IOError:
            params.pop('optimize')
            image.save(buf, **params)
        raw_data = buf.getvalue()
        buf.close()
        return raw_data


EXTENSIONS = {
    'JPEG': 'jpg',
    'PNG': 'png',
}


class ThumbnailBackend(object):
    """
    The main class for sorl-thumbnail, you can subclass this if you for example
    want to change the way destination filename is generated.
    """
    default_options = {
        'format': settings.THUMBNAIL_FORMAT,
        'quality': settings.THUMBNAIL_QUALITY,
        'colorspace': settings.THUMBNAIL_COLORSPACE,
        'upscale': settings.THUMBNAIL_UPSCALE,
        'crop': False,
    }

    extra_options = (
        ('progressive', 'THUMBNAIL_PROGRESSIVE'),
        ('orientation', 'THUMBNAIL_ORIENTATION'),
    )

    def __init__(self):
        self.engine = PILEngine()

    def get_thumbnail(self, file_, geometry_string, **options):
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. First it will try to get it from the key value store,
        secondly it will create it.
        """
        source = Image.open(file_)
        for key, value in self.default_options.iteritems():
            options.setdefault(key, value)
        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames beeing generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(settings, attr):
                options.setdefault(key, value)
        source_image = self.engine.get_image(source)
        # We might as well set the size since we have the image in memory
        #size = self.engine.get_image_size(source_image)
        #source.set_size(size)
        thumbnail = self._create_thumbnail(source_image, geometry_string, options)
        return thumbnail

    def delete(self, file_, delete_file=True):
        """
        Deletes file_ references in Key Value store and optionally the file_
        it self.
        """
        image_file = ImageFile(file_)
        if delete_file:
            image_file.delete()

    def _create_thumbnail(self, source_image, geometry_string, options):
        """
        Creates the thumbnail by using default.engine
        """
        ratio = self.engine.get_image_ratio(source_image)
        geometry = parse_geometry(geometry_string, ratio)
        image = self.engine.create(source_image, geometry, options)
        # It's much cheaper to set the size here
        #size = self.engine.get_image_size(image)
        #image.set_size(size)
        return image


