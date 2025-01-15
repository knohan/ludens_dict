# v0.7.1
 
import requests


class DictionaryAPI:

    def __init__(self, input_word=None, input_json=None): 
        URL_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

        self.input_word = input_word
        if input_json is None and input_word is not None:
            self.response_json = requests.get(f"{URL_API}{input_word}").json()
        elif input_word is None and input_json is not None:
            self.response_json = input_json
        elif input_word is None and input_json is None:
            raise ValueError('You must insert at least one parameter - "input_word" or "input_json"')

        self.meanings_list = []
        self._set_meanings_list()


    def _set_meanings_list(self):
        for i in range(len(self.response_json)):
            self.meanings_list.append(self.response_json[i]["meanings"])


    @property
    def meanings_dict_list(self) -> list:
        """ Ana listenin her bir dictionary elemani datalari temsil eder. Bu dictionarylerin içlerindeki 
            her bir key/value pair'i (noun0 verb1 etc.) meaningleri temsil ediyor. Bunlarin içlerindeki 
            tuplelar ise definition/example ikiliklerini sunuyor (eğer example yoksa yerine "noEx" yaziyor) """
        
        meanings_dict_list = []
        meanings_dict = {}
        for i in self.meanings_list:

            meaning_count = 0
            for n in i:
                part_of_speech = n["partOfSpeech"]

                definition_count = 0
                meaning_tuples = []
                for x in n["definitions"]:  # Every definition-ex coupe is created as a tuple
                    # At this point you can also get synonyms and antonyms (database is poor though) 
                    definition = x["definition"]
                    try:
                        example = x["example"]
                        meaning_tuples.append((f"{definition}", f"{example}".replace("\u2003", "")))
                    except KeyError:
                        meaning_tuples.append((f"{definition}", f"noEx"))

                    definition_count += 1
                meanings_dict[f"{part_of_speech}{meaning_count}"] = meaning_tuples
                meaning_tuples = []  ######
                meaning_count += 1
            meanings_dict_list.append(meanings_dict)
            meanings_dict = {}

        return meanings_dict_list

    @property
    def name(self):
        return self.response_json[0]["word"]

    @property
    def phonetic(self):
        phtcs = self.response_json[0]["phonetics"]
        for i in range(len(phtcs)):
            try:
                return phtcs[i]["text"]
            except KeyError:
                continue

    @property
    def audio(self):  # For some words (e.g. "in"): their audio url does not ends with uk.mp3. Should code smth for this!
        audio_dict = {}
        aud_phtcs = self.response_json[0]["phonetics"]  # First data contains all audio, others are duplicate
        for i in range(len(aud_phtcs)):
            try:
                match aud_phtcs[i]["audio"][-6:]:
                    case "us.mp3": audio_dict[f"us"] = (aud_phtcs[i]["audio"])
                    case "uk.mp3": audio_dict[f"uk"] = (aud_phtcs[i]["audio"])
                    case "au.mp3": audio_dict[f"au"] = (aud_phtcs[i]["audio"])
            except KeyError:
                continue
        return audio_dict

    @property
    def total_data_count(self):
        return len(self.meanings_list)  # Total data count


if __name__ == "__main__":
    test_word = DictionaryAPI(input_word="congresses")

    print(len(test_word.audio))

    for i in test_word.audio:
        print(i)

