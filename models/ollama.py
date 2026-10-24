class OllamaCaps:
 @staticmethod
 def context(show):return int(show.get('model_info',{}).get('context_length') or show.get('context_length'))
