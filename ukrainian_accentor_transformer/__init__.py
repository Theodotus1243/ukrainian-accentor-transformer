from typing import List, Union, Tuple

from huggingface_hub import snapshot_download
import sentencepiece as spm
import ctranslate2


class Accentor:
    _hf_repo = "theodotus/ukrainian-accentor-transformer@v0.1"
    
    split_tokens = set([".",",","!","?"])

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

        tokenized_sentences = self.sp.encode(clean_sentences, out_type=str)
        splitted_sentences, join_list = self._split_long(tokenized_sentences)

        results = self.model.translate_batch(splitted_sentences, **self._run_config)
        accented_tokens = [result.hypotheses[0] for result in results]

        join_sentences = self._join_long(accented_tokens, join_list)
        accented_sentences = self.sp.decode(join_sentences)

        return accented_sentences

    def _clean_accents(self, sentences: List[str]) -> List[str]:
        clean_sentences = [sentence.replace("\u0301","") for sentence in sentences]
        return clean_sentences

    def _split_long(self, tokenized_sentences: List[List[str]]) -> Tuple[List[List[str]], List[int]]:
        splitted_sentences = []
        join_list = []
        for tokenized in tokenized_sentences:
            splitted = self._split_sentence(tokenized)
            splitted_sentences += splitted
            join_list.append(len(splitted))
        return splitted_sentences, join_list

    def _split_sentence(self, tokenized: List[str]) -> List[List[str]]:
        splitted = []
        start_idx = 0
        for idx, token in enumerate(tokenized, start = 1):
            if token in self.split_tokens:
                splitted.append(tokenized[start_idx:idx])
                start_idx = idx
        else:
            if (start_idx < len(tokenized)):
                splitted.append(tokenized[start_idx:])
        return splitted

    def _join_long(self, splitted_sentences: List[List[str]], join_list: List[int]) -> List[List[str]]:
        join_sentences = []
        sentence_idx = 0
        for join_len in join_list:
            sentence = sum(splitted_sentences[sentence_idx:sentence_idx + join_len], [])
            join_sentences.append(sentence)
            sentence_idx += join_len
        return join_sentences

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