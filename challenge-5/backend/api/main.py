import functions_framework
import os
import json
from google.cloud import bigquery
import pandas as pd
from google import genai
from google.genai import types
import base64
import logging
from flask import jsonify

PROJECT_ID = "qwiklabs-gcp-02-8fc93094313c"
client = bigquery.Client(project=PROJECT_ID)
init(project=PROJECT_ID, location="global")

def vector_search_data(user_query):
    return  f"""
    CREATE OR REPLACE TABLE `AuroraDS.qas` AS
    SELECT
        query.query,
        base.content
    FROM
        VECTOR_SEARCH(
            TABLE `AuroraDS.qas_embeddings`,
            'ml_generate_embedding_result',
            (
                SELECT
                    ml_generate_embedding_result,
                    content AS query
                FROM
                    ML.GENERATE_EMBEDDING(
                        MODEL `AuroraDS.Embeddings`,
                        (SELECT '{user_query}' AS content)
                    )
            ),
            top_k => 5,
            options => '{{"fraction_lists_to_search": 1.0}}'
        );
    """
    client.query(search_sql).result()

genai_client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location="global",
)

model = "gemini-2.5-pro-preview-06-05"


def generate(system_prompt, user_input):
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=user_input)
      ]
    ),
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 0.9,
    top_p = 1,
    max_output_tokens = 65535,
    system_instruction=[types.Part.from_text(text=system_prompt)],
    thinking_config=types.ThinkingConfig(
      thinking_budget=-1,
    ),
  )
  data = ''
  for chunk in genai_client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    data = data + " " +chunk.text
  return data.strip()

def gemini_self_check(user_query, response_text):
    prompt = f"""
    You are a content safety reviewer for a government chatbot.

    Evaluate the following assistant response:
    - Is it relevant to the user's question?
    - Is it fact-based and appropriate?
    - Is it free from harmful or misleading language?

    Respond ONLY with one word:
    - VALID → if the answer is acceptable
    - BLOCK → if it should not be shown to users

    Question: {user_query}
    Response: {response_text}
        """
    return generate(prompt, response_text)

def do_prompt_filtering(input):
  prompt = f"""You are a content safety reviewer for a public-facing government chatbot for the Alaska Department of Snow (ADS).
  Your job is to evaluate if a user’s question is appropriate and relevant to ADS services. Allow only safe, relevant questions

  Flag and reject questions that:
  - Include harmful, offensive, or political content
  - Ask for private or personal information
  - Are not related to ADS services

  Evaluate the following question. Respond ONLY with one of:

  - "ALLOW" (if the question is appropriate)
  - "BLOCK" (if the question should be rejected)

  Question: "{input}"
  """
  return generate(prompt, input)

def ads_chatbot(user_input):
  filter = do_prompt_filtering(user_input).strip().upper()
  if filter == "BLOCK":
    return 'Invalid prompt'
  vector_search_data(user_input)
  result_df = client.query("SELECT * FROM `AuroraDS.qas`").to_dataframe()

  system_prompt = """You are an assistant for Aurora Department of snow. Answer clearly and professionally using only the provided context. If the answer isn’t supported by the context, respond with: “Not able to answer your query. And always great him with hello or hi, and also all the time just say i am getting information, and at last reply like 'anything else i can help you with?'”'\n\n"""
  for idx, row in result_df.iterrows():
      system_prompt += f"FAQ {idx+1}:\nQ: {row['question']}\nA: {row['answer']}\n\n"

  response = generate(system_prompt, user_input)
  if gemini_self_check(user_input, response) == 'BLOCK':
    return 'Response is invalid'
  return response

#ADS ChatBot
@functions_framework.http
def faq_chatbot(request):
  try:
    if request.method == 'OPTIONS':
        # Allows POST requests from any origin with the Content-Type header
        # and caches preflight response for 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return ('', 204, headers)

    request_data = request.get_json()
    user_query = request_data['input']
    response = ads_chatbot(user_query)
    return jsonify({
            "status": "completed",
            "data": response,
        }), 200, HEADERS
    
  except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500, HEADERS