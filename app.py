from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize FastAPI app
app = FastAPI()

# Set up the Google API key environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCX8wufJmaEs6sWQoZA7lAnp1AO8mX4Zpw'
gemini_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)

# Define the request model
class BikeRecommendationRequest(BaseModel):
    user_prompt: str

@app.post("/recommend-bikes/")
async def recommend_bikes(request: BikeRecommendationRequest):
    try:
        # Create a message based on the user prompt for generating a DB query
        message = HumanMessage(
        content=f"""
        The user has asked: "{request.user_prompt}". Based on the following schema for bike models, generate a plain SQL query where table names and column names with uppercase letters are enclosed in double quotes (""). The query should be executable as-is and should recommend bikes matching the user's requirements. Ensure that all columns are included in the SELECT statement.

        Schema:
        BikeModals (
        id           String (Primary Key),
        name         String,
        description  String?,
        price        Int,
        image        String?,
        topSpeed     Int,
        range        Int,
        chargingTime Int,
        weight       Int,
        brandId      String (Foreign Key),
        brand        Brand,
        createdAt    DateTime,
        updatedAt    DateTime
        )

        Provide only the SQL query as plain text.
        """
        )



        # Invoke the model with the message
        response = model.invoke([message])

        # Return the model's response (SQL query)
        return JSONResponse(content={"sql_query": response.content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with `uvicorn`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.55.3.58", port=8000)
