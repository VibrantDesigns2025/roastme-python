import openai
openai.api_key = "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"  # Replace with your actual key

models = openai.Model.list()
print([m.id for m in models["data"]])
