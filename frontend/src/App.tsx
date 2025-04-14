import { useState, useEffect } from "react";
import {
  Container,
  Typography,
  CircularProgress,
  Alert,
  Box,
} from "@mui/material";
import UploadForm from "./components/UploadForm";
import SummaryCard from "./components/SummaryCard";
import { fetchResults, Summary } from "./api";

type Status = "idle" | "uploading" | "analysing" | "done" | "error";

function App() {
  const [submissionId, setSubmissionId] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [summary, setSummary] = useState<Summary | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUploadComplete = (id: string) => {
    setSubmissionId(id);
    setStatus("analysing");
  };

  useEffect(() => {
    if (status !== "analysing" || !submissionId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetchResults(submissionId);
        if (res.status === "done" && res.summary) {
          setStatus("done");
          setSummary(res.summary);
          clearInterval(interval);
        }
      } catch (err) {
        setStatus("error");
        setError("Failed to fetch analysis result.");
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [submissionId, status]);

  return (
    <Container maxWidth="sm" sx={{ mt: 6 }}>
      <Typography variant="h4" gutterBottom>
        Meet Summarizer
      </Typography>

      {status === "idle" && (
        <UploadForm
          onUploadComplete={(id) => {
            setStatus("uploading");
            handleUploadComplete(id);
          }}
        />
      )}

      {status === "analysing" && (
        <Box sx={{ textAlign: "center", mt: 4 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            Analysing your file...
          </Typography>
        </Box>
      )}

      {status === "done" && summary && <SummaryCard summary={summary} />}

      {status === "error" && error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Container>
  );
}

export default App;
