import json


class Mistake:
    def __init__(self, mistake):
        self.origin = mistake.get('origin')
        self.corrected_origin = mistake.get('corrected_origin')
        self.explanation = mistake.get('explanation')

    @staticmethod
    def serialize(origin, mistake):
        mistake = json.loads(mistake)
        return {
            "origin": origin,
            "corrected_origin": mistake.get('corrected_origin'),
            "explanation": mistake.get('explanation'),
        }

    def deserialize(self):
        return json.dumps({
            "origin": self.origin,
            "corrected_origin": self.corrected_origin,
            "explanation": self.explanation
        })
