from typing import List, Union

from huggingface_hub import snapshot_download
import sentencepiece as spm
import ctranslate2


class Accentor:
    _hf_repo = "theodotus/ukrainian-accentor-transformer@v0.1"

    _init_config = {
        "inter_threads": 2, 
        "intra_threads": 1
    }

    _run_config = {
        "repetition_penalty": 1.2,
        "max_batch_size": 8
    }

    def __init__(self, device: str = "cpu"):
        self._init_model(device = device)

    def __call__(self, sentence: Union[List[str],str],
                        symbol: str = "stress", mode: str = "reduced") -> Union[List[str],str]:
        """
        Add word stress to texts in Ukrainian
        Args:
            sentence: sentence to accent

        Returns:
            accented_sentence

        Examples:
            Simple usage.

            >>> from ukrainian_accentor_transformer import Accentor
            >>> accentor = Accentor()
            >>> accented_sentence = accentor("Привіт хлопче")
        """

        if (type(sentence) is str):
            sentences = [sentence]
        elif (type(sentence) is list):
            sentences = sentence

        accented_sentences = self._accent(sentences=sentences, symbol=symbol, mode=mode)

        if (type(sentence) is str):
            accented_sentence = accented_sentences[0]
        elif (type(sentence) is list):
            accented_sentence = accented_sentences

        return accented_sentence

    def _accent(self, sentences: List[str], symbol: str, mode: str) -> List[str]:
        """
        Internal accent function
        Args:
            sentences: list of sentences to accent

        Returns:
            accented_sentences
        """
     
        clean_sentences = self._clean_accents(sentences)

        tokenized = self.sp.encode(clean_sentences, out_type=str)

        results = self.model.translate_batch(tokenized, **self._run_config)

        accented_tokens = [result.hypotheses[0] for result in results]

        accented_sentences = self.sp.decode(accented_tokens)

        return accented_sentences

    def _clean_accents(self, sentences: List[str]) -> List[str]:
        clean_sentences = [sentence.replace("\u0301","") for sentence in sentences]
        return clean_sentences

    def _init_model(self, device: str) -> None:
        """
        Initialize a model and tokenizer
        Args:
            device: device where to run model: "cpu" or "cuda"
        """
        repo_path = self._download_huggingface(self._hf_repo)

        self.model = ctranslate2.Translator(f"{repo_path}/ctranslate2/", device=device, **self._init_config)
        self.sp = spm.SentencePieceProcessor(model_file=f"{repo_path}/tokenizer.model")

    @staticmethod
    def _download_huggingface(repo_name: str) -> str:
        """
        Download a file from Huggingface
        Args:
            repo_name: name of repository to download

        Returns:
            repo_path
        """

        # get revision
        repo_name, *suffix = repo_name.split("@")
        revision = dict(enumerate(suffix)).get(0, None)

        repo_path = snapshot_download(repo_name, revision=revision)

        return repo_path