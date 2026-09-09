import cors from "cors";
import express from "express";
import { generateRoadmap, recalculateRoadmap } from "./roadmapEngine.js";

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", service: "RoadmapAI API" });
});

app.post("/api/roadmap/generate", (req, res) => {
  try {
    const profile = req.body;

    if (!profile?.area || !profile?.level || !profile?.dailyHours) {
      return res.status(400).json({
        message: "Informe área, nível e tempo disponível por dia."
      });
    }

    const roadmap = generateRoadmap(profile);
    return res.status(201).json(roadmap);
  } catch (error) {
    return res.status(500).json({
      message: "Não foi possível gerar o roadmap.",
      error: error.message
    });
  }
});

app.post("/api/roadmap/recalculate", (req, res) => {
  try {
    const { roadmap, referenceDate } = req.body;

    if (!roadmap?.weeks) {
      return res.status(400).json({
        message: "Envie um roadmap válido para recalcular."
      });
    }

    const updatedRoadmap = recalculateRoadmap(roadmap, { referenceDate });
    return res.json(updatedRoadmap);
  } catch (error) {
    return res.status(500).json({
      message: "Não foi possível recalcular o roadmap.",
      error: error.message
    });
  }
});

app.listen(PORT, () => {
  console.log(`RoadmapAI backend running on http://localhost:${PORT}`);
});
