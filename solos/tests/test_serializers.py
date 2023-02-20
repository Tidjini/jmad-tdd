from unittest import TestCase


from solos.serializers import SoloSerializer


class SoloSerializerTestCase(TestCase):

    def test_validate(self):
        # Test that SoloSerializer.validate() adds a sluged version of the
        # Artist attribute to the data
        serializer = SoloSerializer()
        data = serializer.validate({
            "artist": "Ray Brown"
        })

        self.assertEqual(data, {
            'artist': 'Ray Brown',
            'slug': 'ray-brown'
        })
