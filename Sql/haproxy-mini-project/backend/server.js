const express = require("express");

const app = express();

const PORT = process.env.PORT || 3000;
const SERVER_NAME = process.env.SERVER_NAME || "unknown";

app.get("/", (req, res) => {
  res.json({
    message: "Hello from backend",
    server: SERVER_NAME
  });
});

app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    server: SERVER_NAME
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`${SERVER_NAME} is running on port ${PORT}`);
});