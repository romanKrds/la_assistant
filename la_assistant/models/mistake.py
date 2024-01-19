import json


class Mistake:
    """
    This is a class for a mistake representation.

    Attributes:
    --------
    origin: str - The origin sentence based on which the mistake was created
    corrected_origin: str - The corrected version of the origin sentence 
    explanation: str - Explanation of the violated grammar rules

    Methods:
    --------
    serialize - Create a Mistake from given parameters.
    deserialize - Create a JSON string from the  Mistake.
    """

    def __init__(self, mistake):
        """
        Initialize Mistake class instance

        Parameters:
        --------
        mistake: Mistake - Mistake-like dictionary
        """
        self.origin = mistake.get('origin')
        self.corrected_origin = mistake.get('corrected_origin')
        self.explanation = mistake.get('explanation')

    @staticmethod
    def serialize(origin, raw_mistake):
        """
        Create a Mistake from given parameters

        Parameters
        ----------
        origin : str - The origin sentence
        raw_mistake : str - JSON string representing the following parameters:
            corrected_origin: str - The correct version of the origin sentence
            explanation: str - Explanation of the violated grammar rules

        Returns
        -------
        object: Mistake
        """
        mistake = {}

        try:
            mistake = json.loads(raw_mistake)
        except TypeError as e:
            print(e)

        return {
            "origin": origin,
            "corrected_origin": mistake.get('corrected_origin'),
            "explanation": mistake.get('explanation'),
        }

    def deserialize(self):
        """
        Create a JSON string from the  Mistake

        Returns
        -------
        str - JSON string representing Mistake
        """
        return json.dumps({
            "origin": self.origin,
            "corrected_origin": self.corrected_origin,
            "explanation": self.explanation
        })
