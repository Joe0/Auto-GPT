import json
from call_ai_function import call_ai_function
from config import Config
cfg = Config()

def fix_and_parse_json(json_str: str, try_to_fix_with_gpt: bool = True):
    json_schema = """
    {
    "command": {
        "name": "command name",
        "args":{
            "arg name": "value"
        }
    },
    "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    }
    }
    """

    try:
        return json.loads(json_str)
    except Exception as e:
        # Let's do something manually - sometimes GPT responds with something BEFORE the braces:
        # "I'm sorry, I don't understand. Please try again."{"text": "I'm sorry, I don't understand. Please try again.", "confidence": 0.0}
        # So let's try to find the first brace and then parse the rest of the string
        try:
          brace_index = json_str.index("{")
          json_str = json_str[brace_index:]
          last_brace_index = json_str.rindex("}")
          json_str = json_str[:last_brace_index+1]
          return json.loads(json_str)
        except Exception as e:
          if try_to_fix_with_gpt:
            print(f"Warning: Failed to parse AI output, attempting to fix.\n If you see this warning frequently, it's likely that your prompt is confusing the AI. Try changing it up slightly.")
            # Now try to fix this up using the ai_functions
            ai_fixed_json = fix_json(json_str, json_schema)
            if ai_fixed_json != "failed":
              return json.loads(ai_fixed_json)
            else:
              print(f"Failed to fix ai output, telling the AI.") # This allows the AI to react to the error message, which usually results in it correcting its ways.
              return json_str
          else:
            raise e
        
def fix_json(json_str: str, schema: str) -> str:
    # Try to fix the JSON using gpt:
    function_string = "def fix_json(json_str: str, schema:str=None) -> str:"
    args = [json_str, schema]
    description_string = """This function takes a JSON string and ensures that it is parseable and fully compliant with the provided schema. If an object or field specified in the schema isn't contained within the correct JSON, it is omitted. The function also escapes any double quotes within JSON string values to ensure that they are valid. If the JSON string contains any None or NaN values, they are replaced with null before being parsed."""

    # If it doesn't already start with a "`", add one:
    if not json_str.startswith("`"):
      json_str = "```json\n" + json_str + "\n```"
    result_string = call_ai_function(
        function_string, args, description_string, model=cfg.fast_llm_model
    )
    if cfg.debug:
        print("------------ JSON FIX ATTEMPT ---------------")
        print(f"Original JSON: {json_str}")
        print("-----------")
        print(f"Fixed JSON: {result_string}")
        print("----------- END OF FIX ATTEMPT ----------------")
    try:
        return json.loads(result_string)
    except:
        # Get the call stack:
        # import traceback
        # call_stack = traceback.format_exc()
        # print(f"Failed to fix JSON: '{json_str}' "+call_stack)
        return "failed"