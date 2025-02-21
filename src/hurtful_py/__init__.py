__author__ = 'Dyachenko Danil (Puker228)'
__version__ = '0.0.1'
__license__ = 'MIT'

class AudioSource(object):
    def __init__(self):
        raise NotImplementedError("this is abstract class")

    def __enter__(self):
        raise NotImplementedError("this is abstract class")

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError("this is abstract class")

class Microphone(AudioSource):
    def __init__(self, chunk_size=1024, sample_rate=None, microphone_index=None):
        """
        :param chunk_size: audio block size
        :param sample_rate: sampling rate
        :param microphone_index: device index
        """
        assert microphone_index is None or isinstance(microphone_index, int), 'Microphone index must be None or positive integer.'
        assert sample_rate is None or (isinstance(sample_rate, int) and sample_rate > 0), 'Sample rate must be None or positive integer.'
        assert isinstance(chunk_size, int) and chunk_size > 0, 'Chunk size must be positive integer.'

        self.pyaudio_modules = self.get_pyaudio_lib()
        audio = self.pyaudio_modules.PyAudio()

        # setup pyaudio
        try:
            count = audio.get_device_count()  # obtain device count
            if microphone_index is not None:
                assert microphone_index in range(0, count), f'Microphone index must be in range between 0 and {count - 1}.'
            if sample_rate is None:
                device_info = audio.get_device_info_by_index(microphone_index) if microphone_index is not None else audio.get_default_input_device_info()
                sample_rate = int(device_info["defaultSampleRate"])
        finally:
            audio.terminate()

        self.chunk = chunk_size
        self.format = self.pyaudio_modules.paInt16
        self.sample_rate = sample_rate
        self.microphone_index = microphone_index
        self.stream = None

    def __enter__(self):
        self.audio = self.pyaudio_modules.PyAudio()
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=1,
                rate=self.sample_rate,
                input=True
            )
        except Exception:
            self.audio.terminate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.stream.stop_stream()
            self.stream.close()
        finally:
            self.stream = None
            self.audio.terminate()


    @staticmethod
    def get_pyaudio_lib():
        try:
            import pyaudio
        except ImportError:
            raise AttributeError("Could not find PyAudio; check installation in readme.md")
        return pyaudio
