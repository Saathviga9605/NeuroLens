import { useState } from "react";
import { runAssessment } from "../services/api";

const InputPage = ({ setAnalysisResult }) => {
  const [formData, setFormData] = useState({
    typingSpeed: "",
    sleepHours: "",
    screenTime: "",
    lateNightUsage: false
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handleAnalyze = async () => {
    setError("");

    // Validation
    if (
      formData.typingSpeed === "" ||
      formData.sleepHours === "" ||
      formData.screenTime === ""
    ) {
      setError("Please fill in Typing Speed, Sleep Hours, and Screen Time.");
      return;
    }

    const ts = Number(formData.typingSpeed);
    const sh = Number(formData.sleepHours);
    const st = Number(formData.screenTime);

    if (isNaN(ts) || isNaN(sh) || isNaN(st)) {
      setError("Please enter valid numeric values.");
      return;
    }

    if (ts < 0 || sh < 0 || st < 0) {
      setError("Values cannot be negative.");
      return;
    }

    try {
      setLoading(true);

      const response = await runAssessment({
        sleep_hours: sh,
        wpm: ts,
        error_rate: 0.1,   // placeholder until typing test integrated
        rhythm_std: st     // temporary mapping from screenTime
      });

      // Send backend result to parent
      setAnalysisResult(response);

    } catch (err) {
      console.error(err);
      setError("Backend connection failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 40 }}>
      <h2>Cognitive Monitoring — Assessment</h2>

      <input
        type="number"
        name="typingSpeed"
        placeholder="Typing Speed (WPM)"
        value={formData.typingSpeed}
        onChange={handleChange}
        style={{ width: "100%", marginTop: 15, padding: 8 }}
      />

      <input
        type="number"
        name="sleepHours"
        placeholder="Sleep Hours"
        value={formData.sleepHours}
        onChange={handleChange}
        style={{ width: "100%", marginTop: 15, padding: 8 }}
      />

      <input
        type="number"
        name="screenTime"
        placeholder="Screen Time (hrs)"
        value={formData.screenTime}
        onChange={handleChange}
        style={{ width: "100%", marginTop: 15, padding: 8 }}
      />

      <label style={{ display: "block", marginTop: 15 }}>
        <input
          type="checkbox"
          name="lateNightUsage"
          checked={formData.lateNightUsage}
          onChange={handleChange}
          style={{ marginRight: 8 }}
        />
        Late Night Usage
      </label>
a
      <button
        onClick={handleAnalyze}
        style={{
          marginTop: 25,
          padding: "10px 20px",
          background: "var(--accent)",
          color: "#fff",
          border: "none",
          borderRadius: 6
        }}
      >
        {loading ? "Processing..." : "Run Cognitive Assessment"}
      </button>

      {error && (
        <div style={{ color: "#ff8b8b", marginTop: 12 }}>
          {error}
        </div>
      )}
    </div>
  );
};

export default InputPage;
