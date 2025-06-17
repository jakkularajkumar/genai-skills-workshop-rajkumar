# ADS Chatbot Prototype

## 🧩 Challenge Overview

The Alaska Department of Snow (ADS) serves over **750,000 residents** across **650,000 square miles**. During snow forecasts, regional offices experience high call volumes related to:

- Snow plowing schedules  
- School closures  
- Service disruptions  

ADS is exploring the implementation of an **online agent (chatbot)** to offload these routine inquiries. However, there are concerns from leadership around:

- **Cloud service adoption**
- **Operational costs**
- **Data privacy and security**

## ✅ Solution Summary

This project is a **prototype chatbot** built to demonstrate a practical and scalable solution for handling common citizen inquiries. It is designed to:

- Reduce regional office call volumes  
- Improve resident access to information  
## 🔧 Implemented Features

- ✅ **Backend built with Flask**  
  - Handles agent API, prompt filtering, and response validation
  - Deployed using **Google Cloud Functions**
  - Deployed backend URL - https://testing-485101432623.europe-west1.run.app
- ✅ **BigQuery + Vertex AI Integration**  
  - Used for vector store, retrieval, and LLM interactions

- ✅ **Prompt Filtering & Response Validation**  
  - Simple logic to ensure user inputs and agent outputs are sanitized and appropriate

- ✅ **Unit Tests**  
  - Basic test coverage added for key backend functionalities

- ✅ **Frontend with React (ADS Chatbot)**  
  - Simple web interface to interact with the chatbot
  - deployed the react app directly using gcloud command line interface

## 🌐 Live Demo

**Hosted Chatbot URL**: https://ads-chatbot-485101432623.asia-east1.run.app/ 

## Screenshot of UI
<img width="947" alt="Screenshot 2025-06-18 at 1 38 24 AM" src="https://github.com/user-attachments/assets/24ecc310-ead2-4d7b-a8e6-be27fc0c0f53" />


## 🧱 Architecture Overview
<img width="467" alt="Screenshot 2025-06-18 at 1 01 19 AM" src="https://github.com/user-attachments/assets/e549df2c-94fc-4ee9-be7e-52c2ffa152b1" />


