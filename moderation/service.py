from better_profanity import profanity

class ModerationService:
    @staticmethod
    def contains_profanity(text):
        profanity.load_censor_words()
        return profanity.contains_profanity(text)

    @staticmethod
    def censor(text):
        profanity.load_censor_words()
        return profanity.censor(text)
