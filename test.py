import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel      



model_name = "TheBloke/Llama-2-7B-32K-Instruct-GGUF"
        
        
        
        
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define the input
input_text = "Summarize the input text: {}".format(translated_text)
print("The input text is:", input_text)
inputs = tokenizer(input_text, return_tensors="pt")



# Generate text
outputs = model.generate(inputs['input_ids'], max_length=50)
# Decode the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)