import axios from "axios";

/*
  Centralized Axios Instance
  ---------------------------
  - Base URL points to local FastAPI backend
  - Timeout prevents hanging requests
*/

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json"
  }
});


/* ============================
   🔹 Assessment Endpoints
   ============================ */

/**
 * Run full cognitive assessment
 * POST /api/assessment/run
 */
export const runAssessment = async (data) => {
  try {
    const response = await API.post("/assessment/run", data);
    return response.data;
  } catch (error) {
    console.error("Assessment error:", error);
    throw error;
  }
};


/**
 * Get session history
 * GET /api/assessment/history
 */
export const getHistory = async () => {
  try {
    const response = await API.get("/assessment/history");
    return response.data;
  } catch (error) {
    console.error("History fetch error:", error);
    throw error;
  }
};


/* ============================
   🔹 Behavioral Only (Optional)
   ============================ */

export const analyzeBehavior = async (data) => {
  try {
    const response = await API.post("/behavior/analyze", data);
    return response.data;
  } catch (error) {
    console.error("Behavior analysis error:", error);
    throw error;
  }
};


/* ============================
   🔹 Future: Voice + NLP
   (Placeholders for expansion)
   ============================ */

export const analyzeVoice = async (formData) => {
  try {
    const response = await API.post("/voice/analyze", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
    return response.data;
  } catch (error) {
    console.error("Voice analysis error:", error);
    throw error;
  }
};

export const analyzeNLP = async (data) => {
  try {
    const response = await API.post("/nlp/analyze", data);
    return response.data;
  } catch (error) {
    console.error("NLP analysis error:", error);
    throw error;
  }
};


/* ============================
   🔹 Utility
   ============================ */

export default API;