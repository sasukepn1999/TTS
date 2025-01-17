from dataclasses import asdict, dataclass, field
from typing import List

from coqpit import MISSING, Coqpit, check_argument

from TTS.config import BaseAudioConfig, BaseDatasetConfig, BaseTrainingConfig


@dataclass
class GSTConfig(Coqpit):
    """Defines the Global Style Token Module

    Args:
        gst_style_input_wav (str):
            Path to the wav file used to define the style of the output speech at inference. Defaults to None.
        gst_style_input_weights (dict):
            Defines the weights for each style token used at inference. Defaults to None.
        gst_embedding_dim (int):
            Defines the size of the GST embedding vector dimensions. Defaults to 256.
        gst_num_heads (int):
            Number of attention heads used by the multi-head attention. Defaults to 4.
        gst_num_style_tokens (int):
            Number of style token vectors. Defaults to 10.
    """

    gst_style_input_wav: str = None
    gst_style_input_weights: dict = None
    gst_embedding_dim: int = 256
    gst_use_speaker_embedding: bool = False
    gst_num_heads: int = 4
    gst_num_style_tokens: int = 10

    def check_values(
        self,
    ):
        """Check config fields"""
        c = asdict(self)
        super().check_values()
        check_argument("gst_style_input_weights", c, restricted=False)
        check_argument("gst_style_input_wav", c, restricted=False)
        check_argument("gst_embedding_dim", c, restricted=True, min_val=0, max_val=1000)
        check_argument("gst_use_speaker_embedding", c, restricted=False)
        check_argument("gst_num_heads", c, restricted=True, min_val=2, max_val=10)
        check_argument("gst_num_style_tokens", c, restricted=True, min_val=1, max_val=1000)


@dataclass
class CharactersConfig(Coqpit):
    """Defines character or phoneme set used by the model

    Args:
        pad (str):
            characters in place of empty padding. Defaults to None.
        eos (str):
            characters showing the end of a sentence. Defaults to None.
        bos (str):
            characters showing the beginning of a sentence. Defaults to None.
        characters (str):
            character set used by the model. Characters not in this list are ignored when converting input text to
            a list of sequence IDs. Defaults to None.
        punctuations (str):
            characters considered as punctuation as parsing the input sentence. Defaults to None.
        phonemes (str):
            characters considered as parsing phonemes. Defaults to None.
        unique (bool):
            remove any duplicate characters in the character lists. It is a bandaid for compatibility with the old
            models trained with character lists with duplicates.
    """

    pad: str = None
    eos: str = None
    bos: str = None
    characters: str = None
    punctuations: str = None
    phonemes: str = None
    unique: bool = True  # for backwards compatibility of models trained with char sets with duplicates

    def check_values(
        self,
    ):
        """Check config fields"""
        c = asdict(self)
        check_argument("pad", c, restricted=True)
        check_argument("eos", c, restricted=True)
        check_argument("bos", c, restricted=True)
        check_argument("characters", c, restricted=True)
        check_argument("phonemes", c, restricted=True)
        check_argument("punctuations", c, restricted=True)


@dataclass
class BaseTTSConfig(BaseTrainingConfig):
    """Shared parameters among all the tts models.

    Args:
        audio (BaseAudioConfig):
            Audio processor config object instance.
        use_phonemes (bool):
            enable / disable phoneme use.
        compute_input_seq_cache (bool):
            enable / disable precomputation of the phoneme sequences. At the expense of some delay at the beginning of
            the training, It allows faster data loader time and precise limitation with `max_seq_len` and
            `min_seq_len`.
        text_cleaner (str):
            Name of the text cleaner used for cleaning and formatting transcripts.
        enable_eos_bos_chars (bool):
            enable / disable the use of eos and bos characters.
        test_senteces_file (str):
            Path to a txt file that has sentences used at test time. The file must have a sentence per line.
        phoneme_cache_path (str):
            Path to the output folder caching the computed phonemes for each sample.
        characters (CharactersConfig):
            Instance of a CharactersConfig class.
        batch_group_size (int):
            Size of the batch groups used for bucketing. By default, the dataloader orders samples by the sequence
            length for a more efficient and stable training. If `batch_group_size > 1` then it performs bucketing to
            prevent using the same batches for each epoch.
        loss_masking (bool):
            enable / disable masking loss values against padded segments of samples in a batch.
        min_seq_len (int):
            Minimum input sequence length to be used at training.
        max_seq_len (int):
            Maximum input sequence length to be used at training. Larger values result in more VRAM usage.
        compute_f0 (int):
            (Not in use yet).
        use_noise_augment (bool):
            Augment the input audio with random noise.
        add_blank (bool):
            Add blank characters between each other two characters. It improves performance for some models at expense
            of slower run-time due to the longer input sequence.
        datasets (List[BaseDatasetConfig]):
            List of datasets used for training. If multiple datasets are provided, they are merged and used together
            for training.
    """

    audio: BaseAudioConfig = field(default_factory=BaseAudioConfig)
    # phoneme settings
    use_phonemes: bool = False
    phoneme_language: str = None
    compute_input_seq_cache: bool = False
    text_cleaner: str = MISSING
    enable_eos_bos_chars: bool = False
    test_sentences_file: str = ""
    phoneme_cache_path: str = None
    # vocabulary parameters
    characters: CharactersConfig = None
    # training params
    batch_group_size: int = 0
    loss_masking: bool = None
    # dataloading
    min_seq_len: int = 1
    max_seq_len: int = float("inf")
    compute_f0: bool = False
    use_noise_augment: bool = False
    add_blank: bool = False
    # dataset
    datasets: List[BaseDatasetConfig] = field(default_factory=lambda: [BaseDatasetConfig()])
